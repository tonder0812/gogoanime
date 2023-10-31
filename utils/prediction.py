import threading
import time

from printer import AbstractPrinter
from utils.format import format_time


class EMA:
    """
    Exponential moving average: smoothing to give progressively lower
    weights to older values.

    Parameters
    ----------
    smoothing  : float, optional
        Smoothing factor in range [0, 1], [default: 0.3].
        Increase to give more weight to recent values.
        Ranges from 0 (yields old value) to 1 (yields new value).
    """

    def __init__(self, smoothing: float = 0.3):
        self.alpha: float = smoothing
        self.last: float = 0
        self.calls: float = 0

    def __call__(self, x: float | None = None) -> float:
        """
        Parameters
        ----------
        x  : float
            New value to include in EMA.
        """
        beta = 1 - self.alpha
        if x is not None:
            self.last = self.alpha * x + beta * self.last
            self.calls += 1
        return self.last / (1 - beta**self.calls) if self.calls else self.last


class Prediction:
    def __init__(self, p: AbstractPrinter, file_var: str, total: int):
        self._running: bool = True
        self.p = p
        self.download_id: str = file_var
        self.total: int = total
        self.lock: threading.Lock = threading.Lock()
        self.segments_processed: int = 0
        self.segments_processed_since_last_update: int = 0
        self.prediction: EMA = EMA()

    def stop(self):
        with self.lock:
            self._running = False
            self.p.set(self.download_id + "_estimated", format_time(0))

    def add(self, amt: int = 1):
        with self.lock:
            self.segments_processed += amt
            self.segments_processed_since_last_update += amt

    def run(self):
        last = time.perf_counter()
        time.sleep(1)
        while self._running:
            with self.lock:
                cur = time.perf_counter()
                delta = cur - last
                if self.segments_processed_since_last_update > 0:
                    prediction = self.prediction(
                        delta / self.segments_processed_since_last_update
                    )
                    last = cur
                    self.segments_processed_since_last_update = 0
                    self.p.set(
                        self.download_id + "_estimated",
                        format_time(
                            prediction * (self.total - self.segments_processed)
                        ),
                    )
                    self.p.set(self.download_id + "_updated", time.asctime())
            time.sleep(1)
