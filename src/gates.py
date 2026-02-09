from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

from .cones import ConeConfig, ConeState, compute_cone_state


class GateDecision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


@dataclass
class GateConfig:
    cone: ConeConfig = ConeConfig()

    # decision thresholds, divulgabili e semplici
    allow_max_distance: float = 0.35
    allow_max_volatility: float = 0.35

    review_max_distance: float = 0.65
    review_max_volatility: float = 0.65

    # if below this, the system is too close to irreversibility
    block_distance: float = 0.85


def decide_gate(
    state: ConeState,
    cfg: Optional[GateConfig] = None
) -> Tuple[GateDecision, Dict[str, float]]:
    """
    Gate ex ante su base ConeState.
    Logic:
    1) se distance_risk è altissima, block
    2) se distance e volatility sono basse, allow
    3) altrimenti review
    """
    cfg = cfg or GateConfig()

    d = state.distance_risk
    v = state.volatility_risk

    if d >= cfg.block_distance:
        return GateDecision.BLOCK, {
            "distance_risk": d,
            "volatility_risk": v,
            "reason_code": 3.0,  # 3 = boundary breach proximity
        }

    if d <= cfg.allow_max_distance and v <= cfg.allow_max_volatility:
        return GateDecision.ALLOW, {
            "distance_risk": d,
            "volatility_risk": v,
            "reason_code": 1.0,  # 1 = stable, admissible
        }

    if d <= cfg.review_max_distance and v <= cfg.review_max_volatility:
        return GateDecision.REVIEW, {
            "distance_risk": d,
            "volatility_risk": v,
            "reason_code": 2.0,  # 2 = needs refinement
        }

    return GateDecision.BLOCK, {
        "distance_risk": d,
        "volatility_risk": v,
        "reason_code": 4.0,  # 4 = risk too high
    }


def gate_from_inputs(
    V: float,
    E: float,
    I: float,
    S: float,
    cfg: Optional[GateConfig] = None
) -> Tuple[GateDecision, ConeState, Dict[str, float]]:
    """
    Convenience wrapper: calcola cone state e poi decision.
    """
    cfg = cfg or GateConfig()
    state = compute_cone_state(V=V, E=E, I=I, S=S, cfg=cfg.cone)
    decision, details = decide_gate(state, cfg=cfg)
    return decision, state, details
