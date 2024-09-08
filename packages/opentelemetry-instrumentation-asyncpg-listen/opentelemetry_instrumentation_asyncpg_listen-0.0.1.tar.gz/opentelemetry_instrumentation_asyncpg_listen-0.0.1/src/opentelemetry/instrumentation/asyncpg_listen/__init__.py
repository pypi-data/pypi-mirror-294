import timeit
from typing import Collection, Tuple

import asyncpg_listen
import wrapt
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.utils import is_instrumentation_enabled, unwrap
from opentelemetry.metrics import Meter, get_meter
from opentelemetry.trace import SpanKind, Tracer, get_tracer

from .package import _instruments
from .version import __version__

__all__: Tuple[str, ...] = ("AsyncpgListenInstrumentor",)


class AsyncpgListenInstrumentor(BaseInstrumentor):
    """An instrumentor for asyncpg_listen

    See `BaseInstrumentor`
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        tracer_provider = kwargs.get("tracer_provider", None)
        tracer = get_tracer(__package__, __version__, tracer_provider)  # type: ignore
        meter_provider = kwargs.get("meter_provider", None)
        meter = get_meter(__package__, meter_provider=meter_provider)  # type: ignore

        async def wrapper(wrapped, instance, args, kwargs):
            if not is_instrumentation_enabled():
                return wrapped(*args, **kwargs)

            handler_per_channel = args[0]
            instrumented_handler_per_channel = {}

            for channel, handler in handler_per_channel.items():
                instrumented_handler_per_channel[channel] = self.__instrument_handle(handler, tracer, meter)

            return await wrapped(instrumented_handler_per_channel, **kwargs)

        wrapt.wrap_function_wrapper(asyncpg_listen.NotificationListener, "run", wrapper)

    def _uninstrument(self, **kwargs):
        unwrap(asyncpg_listen.NotificationListener, "run")

    @staticmethod
    def __instrument_handle(
        handler: asyncpg_listen.NotificationHandler, tracer: Tracer, meter: Meter
    ) -> asyncpg_listen.NotificationHandler:
        handler_duration_meter = meter.create_histogram("asyncpg_listen.handler.duration", unit="s")

        async def __instrumented_handler(notification: asyncpg_listen.NotificationOrTimeout) -> None:
            if not is_instrumentation_enabled():
                return await handler(notification)

            start_time = timeit.default_timer()

            if isinstance(notification, asyncpg_listen.Timeout):
                span_name = f"Notification timeout #{notification.channel}"
            else:
                span_name = f"Notification #{notification.channel}"

            with tracer.start_as_current_span(
                name=span_name,
                kind=SpanKind.INTERNAL,
                attributes={"channel": notification.channel},
            ):
                try:
                    await handler(notification)
                finally:
                    elapsed = max(0, timeit.default_timer() - start_time)
                    handler_duration_meter.record(elapsed, {"channel": notification.channel})

        return __instrumented_handler
