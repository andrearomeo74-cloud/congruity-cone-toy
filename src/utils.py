from __future__ import annotations

from typing import Optional


def clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def safe_div(n: float, d: float, eps: float = 1e-12) -> float:
    return n / (d if abs(d) > eps else (eps if d >= 0 else -eps))


def ema(prev: Optional[float], x: float, alpha: float) -> float:
    """
    Exponential moving average.
    alpha in (0,1], higher means faster tracking.
    If prev is None, initialize with x.
    """
    if prev is None:
        return x
    return alpha * x + (1.0 - alpha) * prev


def diff1(x_t: float, x_prev: Optional[float]) -> float:
    if x_prev is None:
        return 0.0
    return x_t - x_prev


def diff2(d1_t: float, d1_prev: Optional[float]) -> float:
    if d1_prev is None:
        return 0.0
    return d1_t - d1_prev


def rolling_abs_sum_update(prev_sum: float, new_abs: float, old_abs: float) -> float:
    """
    Update a rolling sum of absolute values when using a fixed size window.
    drift_sum = drift_sum + |new| - |old|
    """
    return prev_sum + new_abs - old_abs
