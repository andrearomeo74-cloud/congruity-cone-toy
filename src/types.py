from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Metrics:
    """
    Minimal metrics computed from a 1D signal x_t, typically x_t = I_t / V_t.

    d1, first difference (proxy for first derivative)
    d2, second difference (proxy for curvature)
    ema_d1, EMA of d1
    ema_d2, EMA of d2
    drift, accumulated magnitude of d1 over a window (plateau drift detector)
    """
    t: int
    x: float
    d1: float
    d2: float
    ema_d1: float
    ema_d2: float
    drift: float


@dataclass(frozen=True)
class GateDecision:
    """
    Decision emitted by an admissibility gate.

    admissible, if True the trajectory continues
    reason, short tag for debugging and plots
    threshold, the active threshold used for the decision, if any
    """
    admissible: bool
    reason: str
    threshold: Optional[float] = None


@dataclass(frozen=True)
class RegimeEvent:
    """
    Regime shift event.

    kind, a short label, for example "curvature_spike" or "variance_burst"
    t, time index where detected
    score, detection score, higher means stronger evidence
    details, optional diagnostic tuple, keeps it lightweight
    """
    kind: str
    t: int
    score: float
    details: Optional[Tuple[float, float]] = None
