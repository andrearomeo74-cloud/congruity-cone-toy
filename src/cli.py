from __future__ import annotations

import argparse
from dataclasses import asdict

from .cones import ConeConfig, compute_ci, compute_cone_state
from .gates import GateConfig, gate_from_inputs


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="congruity-cone",
        description="Compute CI, Congruity Cone state, and ex ante gate decision."
    )

    p.add_argument("--V", type=float, required=True, help="Value")
    p.add_argument("--E", type=float, required=True, help="Energy/Entropy cost")
    p.add_argument("--I", type=float, required=True, help="Information/Interventions")
    p.add_argument("--S", type=float, required=True, help="Scaling/Structure overhead")

    p.add_argument("--epsilon", type=float, default=1e-9, help="Numerical stabilizer")
    p.add_argument("--tau", type=float, default=0.25, help="Cone sharpness")
    p.add_argument("--dt", type=float, default=1.0, help="Time step proxy")

    p.add_argument("--allow_max_distance", type=float, default=0.35)
    p.add_argument("--allow_max_volatility", type=float, default=0.35)
    p.add_argument("--review_max_distance", type=float, default=0.65)
    p.add_argument("--review_max_volatility", type=float, default=0.65)
    p.add_argument("--block_distance", type=float, default=0.85)

    p.add_argument("--json", action="store_true", help="Print as JSON like dict")
    return p


def main() -> None:
    args = build_parser().parse_args()

    cone_cfg = ConeConfig(
        epsilon=args.epsilon,
        tau=args.tau,
        dt=args.dt,
    )

    gate_cfg = GateConfig(
        cone=cone_cfg,
        allow_max_distance=args.allow_max_distance,
        allow_max_volatility=args.allow_max_volatility,
        review_max_distance=args.review_max_distance,
        review_max_volatility=args.review_max_volatility,
        block_distance=args.block_distance,
    )

    ci = compute_ci(V=args.V, E=args.E, I=args.I, S=args.S, epsilon=cone_cfg.epsilon)
    decision, state, details = gate_from_inputs(
        V=args.V, E=args.E, I=args.I, S=args.S, cfg=gate_cfg
    )

    if args.json:
        payload = {
            "inputs": {"V": args.V, "E": args.E, "I": args.I, "S": args.S},
            "ci": ci,
            "cone_state": asdict(state),
            "decision": decision.value,
            "details": details,
        }
        print(payload)
        return

    print(f"CI: {ci:.6g}")
    print(f"Cone, distance_risk: {state.distance_risk:.6g}, volatility_risk: {state.volatility_risk:.6g}")
    print(f"Decision: {decision.value}")
    print(f"Details: {details}")


if __name__ == "__main__":
    main()
