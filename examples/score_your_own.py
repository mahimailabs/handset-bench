"""Score any TTS through a phone line. No GPU, no cloud account, no corpus download.

Run with:  uv run python examples/score_your_own.py
"""

import time

import numpy as np

from handset_bench.adapters.base import SynthResult, Timings
from handset_bench.conditions import resolve
from handset_bench.runner import run_quality
from handset_bench.textset import loader


class MyTTS:
    """Replace synthesize with a call into your own system."""

    def version_string(self) -> str:
        return "example-tone-0.1"

    def synthesize(self, text: str, *, voice: str | None = None) -> SynthResult:
        submitted = time.perf_counter_ns()
        samples = int(16000 * max(0.4, len(text) * 0.05))
        pcm = (0.2 * np.sin(2 * np.pi * 220 * np.arange(samples) / 16000)).astype(
            np.float32
        )
        done = time.perf_counter_ns()
        return SynthResult(
            pcm=pcm,
            sample_rate=16000,
            timings=Timings(submitted, done, done),
            status="ok",
        )


class PerfectASR:
    """Stands in for a real recogniser, so the harness is what gets exercised."""

    def __init__(self, truth: list[str]):
        self.truth = list(truth)

    def transcribe(self, pcm, sample_rate: int) -> str:
        return self.truth.pop(0)

    def name(self) -> str:
        return "oracle"

    def revision(self) -> str:
        return "1"


def main() -> None:
    utterances = loader.sample(loader.load(), 12)
    categories = sorted({u.category for u in utterances})
    print(f"{len(utterances)} utterances across {len(categories)} categories\n")

    for name in ("wideband", "clean", "loss_1pct", "loss_3pct"):
        record = run_quality(
            MyTTS(),
            system="example",
            asr=PerfectASR([u.text for u in utterances]),
            utterances=utterances,
            condition=resolve(name),
        )
        print(f"  {name:10s} WER {100 * record.aggregate['wer']:6.2f}%")


if __name__ == "__main__":
    main()
