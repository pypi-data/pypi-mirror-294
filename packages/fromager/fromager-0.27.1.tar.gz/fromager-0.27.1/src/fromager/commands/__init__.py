from . import (
    bootstrap,
    build,
    build_order,
    canonicalize,
    download_sequence,
    graph,
    list_overrides,
    server,
    step,
)

commands = [
    bootstrap.bootstrap,
    build.build,
    build.build_sequence,
    build_order.build_order,
    graph.graph,
    list_overrides.list_overrides,
    step.step,
    canonicalize.canonicalize,
    download_sequence.download_sequence,
    server.wheel_server,
]
