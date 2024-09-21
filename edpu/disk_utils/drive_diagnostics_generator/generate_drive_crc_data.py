from __future__ import annotations


class GenerateDriveCrcData:
    def __init__(self: GenerateDriveCrcData, batch_blocks: str, max_cached_batches: str, echo_rate: str) -> None:
        self.batch_blocks = batch_blocks
        self.max_cached_batches = max_cached_batches
        self.echo_rate = echo_rate
