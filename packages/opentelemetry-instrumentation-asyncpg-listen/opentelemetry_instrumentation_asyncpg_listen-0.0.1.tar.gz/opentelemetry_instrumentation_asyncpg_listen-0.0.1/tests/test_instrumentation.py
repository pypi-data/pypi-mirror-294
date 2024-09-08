import asyncio
import contextlib
import dataclasses

import asyncpg
import asyncpg_listen
import pytest_pg
from opentelemetry.sdk.trace import SynchronousMultiSpanProcessor, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, set_tracer_provider

from opentelemetry.instrumentation.asyncpg_listen import AsyncpgListenInstrumentor


class Handler:
    def __init__(self, delay: float = 0) -> None:
        self.delay = delay
        self.notifications: list[asyncpg_listen.NotificationOrTimeout] = []

    async def handle(self, notification: asyncpg_listen.NotificationOrTimeout) -> None:
        await asyncio.sleep(self.delay)
        self.notifications.append(notification)


async def test_instrumentation(pg_14: pytest_pg.PG) -> None:
    AsyncpgListenInstrumentor().instrument()
    in_memory_span_exporter = InMemorySpanExporter()

    span_processor = SynchronousMultiSpanProcessor()
    span_processor.add_span_processor(SimpleSpanProcessor(in_memory_span_exporter))
    set_tracer_provider(TracerProvider(active_span_processor=span_processor))

    handler = Handler()
    listener = asyncpg_listen.NotificationListener(asyncpg_listen.connect_func(**dataclasses.asdict(pg_14)))
    listener_task = asyncio.create_task(listener.run({"active": handler.handle}, notification_timeout=1))
    await asyncio.sleep(0.1)

    connection = await asyncpg.connect(**dataclasses.asdict(pg_14))
    try:
        await connection.execute("NOTIFY active, '1'")
        await connection.execute("NOTIFY active, '2'")
        await asyncio.sleep(0.75)
    finally:
        await asyncio.shield(connection.close())

    await cancel_and_wait(listener_task)

    assert handler.notifications == [
        asyncpg_listen.Notification("active", "1"),
        asyncpg_listen.Notification("active", "2"),
    ]

    spans = in_memory_span_exporter.get_finished_spans()

    assert len(spans) == 2

    for span in spans:
        assert span.name == "Notification #active"
        assert span.kind == SpanKind.INTERNAL
        assert span.attributes == {"channel": "active"}

    AsyncpgListenInstrumentor().uninstrument()


async def cancel_and_wait(future: "asyncio.Future[None]") -> None:
    future.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await future
