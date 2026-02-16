from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "tm_service_request_total",
    "Total requests handled by service",
    ["service", "endpoint", "method"],
)

REQUEST_LATENCY = Histogram(
    "tm_service_request_latency_seconds",
    "Request latency in seconds",
    ["service", "endpoint", "method"],
)
