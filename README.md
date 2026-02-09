# Congruity Cone — Toy Sandbox

This repository is a minimal, exploratory sandbox to test **Congruity Cones**:
a geometry-inspired extension of Congruity that constrains system evolution
via admissible trajectories, history-aware thresholds, and regime-aware pruning.

The goal is not optimization, but **ex-ante exclusion of structurally unsustainable paths**.

---

## What this repo is

A toy environment to experiment with:

- Congruity vs Congruity Cones
- History-aware admissibility gates
- Collective and individual drift
- Regime shifts and endogenous re-baselining
- Async agents and synchronization tolerance
- Plateau detection and latent debt buildup

All simulations are intentionally simple and interpretable.

---

## What this repo is NOT

- Not a production framework
- Not a training system
- Not MARL
- Not optimization-by-reward

This is about **structural constraint**, not performance chasing.

---

## Core idea (informal)

Classic Congruity evaluates a state.

**Congruity Cones** constrain the *set of future states*  
by enforcing curvature, drift, and synchrony limits derived from history.

If Congruity asks:
> “Is this state admissible?”

Congruity Cones ask:
> “Which futures remain admissible from here?”

---

## Planned components

- Scalar Congruity baseline
- Cone curvature (1st & 2nd order)
- Drift accumulation on plateaus
- Endogenous thresholds via EMA history
- Regime shift detection
- Controlled re-baselining
- Minimal toy simulations (no black boxes)

---

## License

MIT — experimental, educational, and collaborative.

## Quickstart

### Install

```bash
pip install -e .

Run CLI

Compute Congruity Index (CI), Congruity Cone state, and the ex-ante gate decision.

python -m src.cli --V 100 --E 20 --I 10 --S 5

JSON output (machine-readable):

python -m src.cli --V 100 --E 20 --I 10 --S 5 --json

Tune Congruity Cone thresholds

Adjust cone boundaries directly from the command line:

python -m src.cli --V 100 --E 20 --I 10 --S 5 \
  --allow_max_distance 0.35 --allow_max_volatility 0.35 \
  --review_max_distance 0.65 --review_max_volatility 0.65 \
  --block_distance 0.85

Interpretation

CI is a scalar compression of system efficiency.
The Congruity Cone adds trajectory awareness via distance and volatility.
The gate returns one of three states:

ALLOW → admissible trajectory

REVIEW → marginal / unstable region

BLOCK → structurally inadmissible path
