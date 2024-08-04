from fastapi import FastAPI, Request, HTTPException
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import make_asgi_app

from logging_package.logging_config import get_logger, configure_logging
from calculator_package.calculator import perform_calculation
from monitoring_metrics.metrics import (
    REQUEST_COUNT, CALCULATION_COUNT, timing_decorator, error_tracker, hit_counter
)

configure_logging()
logger = get_logger(__name__)

app = FastAPI()

# OpenTelemetry setup
resource = Resource(attributes={
    SERVICE_NAME: "comsci"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

# Set up Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("Received request", path=request.url.path, method=request.method)
    response = await call_next(request)
    logger.info("Sent response", path=request.url.path, method=request.method, status_code=response.status_code)
    return response

@app.get("/")
@timing_decorator
@error_tracker
@hit_counter("/")
async def root():
    REQUEST_COUNT.inc()
    logger.info("Root endpoint called")
    return {"message": "Hello, World"}

@app.get("/health")
@timing_decorator
@error_tracker
@hit_counter("/health")
async def health():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

@app.get("/calculate")
@timing_decorator
@error_tracker
@hit_counter("/calculate")
async def calculate(a: float, b: float, operation: str):
    REQUEST_COUNT.inc()
    CALCULATION_COUNT.inc()
    logger.info("Calculate endpoint called", a=a, b=b, operation=operation)
    try:
        result = perform_calculation(a, b, operation)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting application")
    uvicorn.run(app, host="0.0.0.0", port=8000)