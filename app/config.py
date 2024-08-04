import os

# Application settings
APP_NAME = "comsci"
APP_VERSION = "1.0.0"

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# OpenTelemetry settings
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317")

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Prometheus settings
PROMETHEUS_PUSH_GATEWAY = os.getenv("PROMETHEUS_PUSH_GATEWAY", "http://prometheus-pushgateway:9091")