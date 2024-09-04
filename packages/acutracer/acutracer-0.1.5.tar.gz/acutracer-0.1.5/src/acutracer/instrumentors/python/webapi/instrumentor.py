import asyncio
from contextlib import asynccontextmanager, contextmanager
from functools import wraps

import httpx
import requests
from django.core.handlers.wsgi import WSGIRequest
from django.core.signals import request_started
from fastapi import FastAPI, Request
from flask import Flask
from flask import request as flask_request
from loguru import logger
from openinference.semconv.resource import ResourceAttributes
from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from acutracer.exporters.jaeger_exporter import CustomJaegerExporter


class WebAPIInstrumentor:
    def __init__(self, name="acutracer", tracer=None):
        self.tracer_provider = trace_sdk.TracerProvider(
            resource=Resource.create({"service.name": name}),
            span_limits=trace_sdk.SpanLimits(max_attributes=10_000),
        )
        jeager_exporter = CustomJaegerExporter()
        self.tracer_provider.add_span_processor(jeager_exporter.get_processor())

        trace.set_tracer_provider(self.tracer_provider)
        self.tracer = tracer or trace.get_tracer(__name__)

    def instrument_requests(self):
        original_send = requests.Session.send

        @wraps(original_send)
        def instrumented_send(session, request, **kwargs):
            with self.tracer.start_as_current_span(f"Requests {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                response = original_send(session, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.response_content_length", len(response.content))
                return response

        requests.Session.send = instrumented_send

    def instrument_httpx(self):
        original_send = httpx.Client.send
        original_async_send = httpx.AsyncClient.send

        @wraps(original_send)
        def instrumented_send(client, request, **kwargs):
            try:
                logger.debug(f"\n in sync httpx send {self.tracer}")
            except Exception as e:
                logger.error(f"ERROR {e}")
            with self.tracer.start_as_current_span(f"HTTP {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                response = original_send(client, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                #span.set_attribute("http.response_content_length", len(response.content))

                return response

        @wraps(original_async_send)
        async def instrumented_async_send(self, request, **kwargs):
            logger.debug("\n in A-sync httpx send")
            with self.tracer.start_as_current_span(f"HTTP {request.method} {request.url}") as span:
                headers = request.headers
                headers.update({
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                })
                response = await original_async_send(self, request, **kwargs)
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.response_content_length", len(response.content))
                return response

        httpx.Client.send = instrumented_send
        httpx.AsyncClient.send = instrumented_async_send

    def instrument(self, app: FastAPI):
        FastAPIInstrumentor.instrument_app(app)

        @app.middleware("http")
        async def add_parent_trace(request: Request, call_next):
            logger.trace(f"\n In add_parent_trace for request {request}, tracer: {self.tracer}")
            with self.tracer.start_as_current_span(f"APP http_request {request.method} {request.url}") as span:
                logger.trace(f"starting span {span.get_span_context()}")
                context = TraceContextTextMapPropagator().extract(request.headers)
                trace.set_span_in_context(span, context)

                # Add custom headers to the request state
                request.state.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }

                response = await call_next(request)
                return response
        self.instrument_httpx()
        self.instrument_requests()
        return self.tracer

    def instrument_gradio(self, app):
        original_launch = app.launch

        @wraps(original_launch)
        def instrumented_launch(*args, **kwargs):
            with self.tracer.start_as_current_span("gradio_launch") as span:
                span.set_attribute("X-acuvity-trace-id", f"{span.get_span_context().trace_id:032x}")
                span.set_attribute("X-acuvity-span-id", f"{span.get_span_context().span_id:016x}")

                self.instrument_httpx()
                self.instrument_requests()

                return original_launch(*args, **kwargs)

        app.launch = instrumented_launch
        logger.info("Gradio instrumentation applied")
        return self.tracer

    def instrument_flask(self, app: Flask):
        FlaskInstrumentor().instrument_app(app)

        @app.before_request
        def before_request():
            logger.trace(f"\n In before_request for Flask, tracer: {self.tracer}")
            with self.tracer.start_as_current_span(f"Flask http_request {flask_request.method} {flask_request.url}") as span:
                context = TraceContextTextMapPropagator().extract(flask_request.headers)
                trace.set_span_in_context(span, context)

                flask_request.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }
        self.instrument_httpx()
        self.instrument_requests()
        return self.tracer

    def instrument_django(self):
        DjangoInstrumentor().instrument()

        def start_span(sender, **kwargs):
            request = kwargs.get('request', None)
            if not isinstance(request, WSGIRequest):
                return

            with self.tracer.start_as_current_span(f"Django http_request {request.method} {request.path}") as span:
                context = TraceContextTextMapPropagator().extract(request.META)
                trace.set_span_in_context(span, context)

                request.custom_headers = {
                    "X-acuvity-trace-id": f"{span.get_span_context().trace_id:032x}",
                    "X-acuvity-span-id": f"{span.get_span_context().span_id:016x}"
                }

        request_started.connect(start_span)

        self.instrument_httpx()
        self.instrument_requests()

        return self.tracer
