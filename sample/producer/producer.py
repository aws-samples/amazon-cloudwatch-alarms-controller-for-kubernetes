# Basic packages for your application
import boto3
import json
import random
import time
import os
import logging
from statsd import StatsClient

# Add imports for OTel components into the application
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
# Import the AWS X-Ray for OTel Python IDs Generator into the application.
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.sdk.extension.aws.trace.propagation.aws_xray_format import AwsXRayFormat

from prometheus_client import start_http_server, Summary

start_http_server(8000)

OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')
OTEL_METRICS_EXPORTER_OTLP_ENDPOINT = os.environ.get('OTEL_METRICS_EXPORTER_OTLP_ENDPOINT')
logging.basicConfig(level=logging.INFO)

# Sends generated traces in the OTLP format to an ADOT Collector running on port 55678
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
# Processes traces in batches as opposed to immediately one after the other
span_processor = BatchSpanProcessor(otlp_exporter)
# Configures the Global Tracer Provider
trace.set_tracer_provider(TracerProvider(active_span_processor=span_processor, id_generator=AwsXRayIdGenerator()))
BotocoreInstrumentor().instrument()
tracer = trace.get_tracer(__name__)

random.seed(time.time())
statsd = StatsClient(host = OTEL_METRICS_EXPORTER_OTLP_ENDPOINT, port = 8125)

REQUEST_TIME = Summary('message_producing_seconds', 'Time spent producing mesasge')

@REQUEST_TIME.time()
def main_function():
  return f"Sending message: {random.random()}"

if __name__ == "__main__":
  sqs_client = boto3.client("sqs")
  sqs_queue = os.environ.get('QUEUE_NAME')
  queue_url = sqs_client.get_queue_url(
        QueueName=sqs_queue
    )

  queue_url = queue_url['QueueUrl']
  while True:
    with tracer.start_as_current_span("put message to queue"):
      message = main_function()
      sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
      )
      logging.info("sent message %s", message)
      statsd.incr('messages')
    time.sleep(1)
