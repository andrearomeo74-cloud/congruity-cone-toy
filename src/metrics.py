from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .utils import safe_div, clamp


@dataclass
class MetricsConfig:
    eps: float = 1e-8

    # simple weights for toy breakdown
    w_E: float = 1.0
    w_I: float = 1.0
    w_S: float = 1.0

    # optional compression on denominators to avoid extreme ratios
    denom_floor: float = 0.0


def compute_congruity(
    V: float,
    E: float,
    I: float,
    S: float,
    cfg: Optional[MetricsConfig] = None
) -> Dict[str, float]:
    """
    Congruity core, divulgabile:
    C = V / (wE*E + wI*I + wS*S)

    Restituisce anche un breakdown utile per diagnostica e reply.
    """
    cfg = cfg or MetricsConfig()

    denom = cfg.w_E * E + cfg.w_I * I + cfg.w_S * S
    if cfg.denom_floor > 0.0:
        denom = max(cfg.denom_floor, denom)

    C = safe_div(V, denom, eps=cfg.eps)

    return {
        "C": C,
        "V": float(V),
        "E": float(E),
        "I": float(I),
        "S": float(S),
        "denom": float(denom),
        "E_share": safe_div(cfg.w_E * E, denom, eps=cfg.eps),
        "I_share": safe_div(cfg.w_I * I, denom, eps=cfg.eps),
        "S_share": safe_div(cfg.w_S * S, denom, eps=cfg.eps),
    }


def compute_iv(I: float, V: float, eps: float = 1e-8) -> float:
    """
    Helper per Cone, ratio informazione su valore.
    """
    return safe_div(I, V, eps=eps)


def normalize_score(x: float, lo: float, hi: float, eps: float = 1e-8) -> float:
    """
    Normalizza su [0,1] in modo robusto.
    """
    if hi <= lo:
        return 0.0
    return clamp((x - lo) / (hi - lo + eps), 0.0, 1.0)
