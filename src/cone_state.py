from __future__ import annotations

from dataclasses import dataclass, field
from typing import Deque, Optional
from collections import deque

from .utils import ema, diff1, diff2, clamp, safe_div, rolling_abs_sum_update


@dataclass
class ConeConfig:
    """
    Config minimale per Congruity Cone toy.
    Tutto rule based, niente meta learner.
    """
    ema_alpha_d1: float = 0.35
    ema_alpha_d2: float = 0.25
    ema_alpha_ref: float = 0.15

    drift_window: int = 10

    eps: float = 1e-8

    tolerance_k: float = 3.0
    tolerance_min: int = 1
    tolerance_max: int = 6

    drift_k: float = 1.5
    drift_min_ref: float = 1e-3

    regime_var_mult: float = 3.0
    rebaseline_decay: float = 0.7


@dataclass
class ConeState:
    """
    Stato per un singolo agente.
    Traccia I_over_V, derivate discrete, EMA, drift, tolleranza dinamica e soglie endogene.
    """
    cfg: ConeConfig = field(default_factory=ConeConfig)

    # raw scalar
    iv: Optional[float] = None

    # first and second differences (raw)
    d1: Optional[float] = None
    d2: Optional[float] = None

    # EMA of derivatives
    ema_d1: Optional[float] = None
    ema_d2: Optional[float] = None

    # rolling drift sum of |d1| over window
    _d1_abs_window: Deque[float] = field(default_factory=deque)
    drift_sum: float = 0.0

    # endogenous drift reference from admissible history
    drift_ref: Optional[float] = None

    # simple online variance proxy for ema_d2 (Welford-like on ema_d2)
    var_count: int = 0
    var_mean: float = 0.0
    var_m2: float = 0.0
    hist_var: Optional[float] = None

    # flag
    last_prune: bool = False

    def update_iv(self, I: float, V: float) -> None:
        iv_new = safe_div(I, V, eps=self.cfg.eps)
        if self.iv is None:
            self.iv = iv_new
            self.d1 = 0.0
            self.d2 = 0.0
            self.ema_d1 = iv_new * 0.0
            self.ema_d2 = iv_new * 0.0
            self._push_d1_abs(0.0)
            self._update_var(0.0)
            return

        d1_new = diff1(iv_new, self.iv)
        d2_new = diff2(d1_new, self.d1)

        self.iv = iv_new
        self.d1 = d1_new
        self.d2 = d2_new

        self.ema_d1 = ema(self.ema_d1, d1_new, self.cfg.ema_alpha_d1)
        self.ema_d2 = ema(self.ema_d2, d2_new, self.cfg.ema_alpha_d2)

        self._push_d1_abs(abs(d1_new))
        self._update_var(self.ema_d2 if self.ema_d2 is not None else 0.0)

    def _push_d1_abs(self, abs_d1: float) -> None:
        w = self.cfg.drift_window
        if w <= 0:
            return

        if len(self._d1_abs_window) < w:
            self._d1_abs_window.append(abs_d1)
            self.drift_sum += abs_d1
        else:
            old = self._d1_abs_window.popleft()
            self._d1_abs_window.append(abs_d1)
            self.drift_sum = rolling_abs_sum_update(self.drift_sum, abs_d1, old)

    def _update_var(self, x: float) -> None:
        self.var_count += 1
        delta = x - self.var_mean
        self.var_mean += delta / self.var_count
        delta2 = x - self.var_mean
        self.var_m2 += delta * delta2

        if self.var_count > 1:
            current_var = self.var_m2 / (self.var_count - 1)
            if self.hist_var is None:
                self.hist_var = current_var
            else:
                # slowly track long term variance
                self.hist_var = ema(self.hist_var, current_var, self.cfg.ema_alpha_ref)

    def current_var(self) -> float:
        if self.var_count <= 1:
            return 0.0
        return self.var_m2 / (self.var_count - 1)

    def tolerance_window(self) -> int:
        """
        Endogenous tolerance: inverse curvature.
        tol = k / (eps + |ema_d2|), clamped to integer [min,max]
        """
        d2 = abs(self.ema_d2) if self.ema_d2 is not None else 0.0
        raw = self.cfg.tolerance_k / (self.cfg.eps + d2)
        raw = clamp(raw, float(self.cfg.tolerance_min), float(self.cfg.tolerance_max))
        return int(round(raw))

    def drift_threshold(self) -> float:
        """
        Endogenous drift threshold from admissible history.
        """
        ref = self.drift_ref if self.drift_ref is not None else self.cfg.drift_min_ref
        return max(self.cfg.drift_min_ref, self.cfg.drift_k * ref)

    def update_drift_ref_if_stable(self, C: Optional[float], stability: float = 0.8) -> None:
        """
        Update drift_ref only when system is stable:
        low curvature and high C and no prune on this step.
        """
        if self.last_prune:
            return

        d2 = abs(self.ema_d2) if self.ema_d2 is not None else 0.0
        if d2 < self.cfg.eps and C is not None and C >= stability:
            if self.drift_ref is None:
                self.drift_ref = max(self.cfg.drift_min_ref, self.drift_sum)
            else:
                self.drift_ref = ema(self.drift_ref, self.drift_sum, self.cfg.ema_alpha_ref)

    def detect_regime_shift(self) -> bool:
        """
        Regime shift: variance of curvature spikes vs historical variance.
        """
        if self.hist_var is None:
            return False
        return self.current_var() > self.cfg.regime_var_mult * self.hist_var

    def apply_rebaseline_on_shift(self) -> None:
        """
        Discrete reset, but keep continuity via decay on drift_ref.
        """
        if self.drift_ref is not None:
            self.drift_ref *= self.cfg.rebaseline_decay
