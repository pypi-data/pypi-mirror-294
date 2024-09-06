import functools
import os
import time
from contextlib import contextmanager
from enum import StrEnum
from typing import Generator, assert_never, cast

from opentelemetry import _logs, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import Logger as OTELLogger
from opentelemetry.sdk._logs import LoggerProvider, LogRecord
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Attributes, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
)
from opentelemetry.trace import Tracer

from uncountable.core.version import get_version
from uncountable.types import base_t, job_definition_t


def _cast_attributes(attributes: dict[str, base_t.JsonValue]) -> Attributes:
    return cast(Attributes, attributes)


@functools.cache
def get_otel_resource() -> Resource:
    attributes: dict[str, base_t.JsonValue] = {
        "service.name": "integration-server",
        "sdk.version": get_version(),
    }
    unc_version = os.environ.get("UNC_VERSION")
    if unc_version is not None:
        attributes["service.version"] = unc_version
    unc_env = os.environ.get("UNC_INTEGRATION_ENV")
    if unc_env is not None:
        attributes["deployment.environment"] = unc_env
    resource = Resource.create(attributes=_cast_attributes(attributes))
    return resource


@functools.cache
def get_otel_tracer() -> Tracer:
    provider = TracerProvider(resource=get_otel_resource())
    provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)
    return provider.get_tracer("integration.telemetry")


@functools.cache
def get_otel_logger() -> OTELLogger:
    provider = LoggerProvider(resource=get_otel_resource())
    provider.add_log_record_processor(BatchLogRecordProcessor(ConsoleLogExporter()))
    provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    _logs.set_logger_provider(provider)
    return provider.get_logger("integration.telemetry")


class LogSeverity(StrEnum):
    INFO = "Info"
    WARN = "Warn"
    ERROR = "Error"


class Logger:
    current_span_id: int | None = None
    current_trace_id: int | None = None

    def _patch_attributes(self, attributes: Attributes | None) -> Attributes:
        return attributes or {}

    def _emit_log(
        self, message: str, *, severity: LogSeverity, attributes: Attributes | None
    ) -> None:
        otel_logger = get_otel_logger()
        log_record = LogRecord(
            body=message,
            severity_text=severity,
            timestamp=time.time_ns(),
            attributes=self._patch_attributes(attributes),
            span_id=self.current_span_id,
            trace_id=self.current_trace_id,
        )
        otel_logger.emit(log_record)

    def log_info(self, message: str, *, attributes: Attributes | None = None) -> None:
        self._emit_log(
            message=message, severity=LogSeverity.INFO, attributes=attributes
        )

    def log_warning(
        self, message: str, *, attributes: Attributes | None = None
    ) -> None:
        self._emit_log(
            message=message, severity=LogSeverity.WARN, attributes=attributes
        )

    def log_error(self, message: str, *, attributes: Attributes | None = None) -> None:
        self._emit_log(
            message=message, severity=LogSeverity.ERROR, attributes=attributes
        )


class JobLogger(Logger):
    def __init__(
        self,
        *,
        profile_metadata: job_definition_t.ProfileMetadata,
        job_definition: job_definition_t.JobDefinition,
    ) -> None:
        self.profile_metadata = profile_metadata
        self.job_definition = job_definition

    def _patch_attributes(self, attributes: Attributes | None) -> Attributes:
        patched_attributes: dict[str, base_t.JsonValue] = {
            **(attributes if attributes is not None else {})
        }
        patched_attributes["profile.name"] = self.profile_metadata.name
        patched_attributes["profile.base_url"] = self.profile_metadata.base_url
        patched_attributes["job.name"] = self.job_definition.name
        patched_attributes["job.id"] = self.job_definition.id
        patched_attributes["job.definition_type"] = self.job_definition.type
        match self.job_definition:
            case job_definition_t.CronJobDefinition():
                patched_attributes["job.definition.cron_spec"] = (
                    self.job_definition.cron_spec
                )
            case _:
                assert_never(self.job_definition)
        patched_attributes["job.definition.executor.type"] = (
            self.job_definition.executor.type
        )
        match self.job_definition.executor:
            case job_definition_t.JobExecutorScript():
                patched_attributes["job.definition.executor.import_path"] = (
                    self.job_definition.executor.import_path
                )
            case job_definition_t.JobExecutorGenericUpload():
                patched_attributes["job.definition.executor.data_source.type"] = (
                    self.job_definition.executor.data_source.type
                )
            case _:
                assert_never(self.job_definition.executor)
        return _cast_attributes(patched_attributes)

    @contextmanager
    def push_scope(
        self, scope_name: str, *, attributes: Attributes | None = None
    ) -> Generator["JobLogger", None, None]:
        with get_otel_tracer().start_as_current_span(
            scope_name, attributes=self._patch_attributes(attributes)
        ) as span:
            self.current_span_id = span.get_span_context().span_id
            self.current_trace_id = span.get_span_context().trace_id
            yield self
