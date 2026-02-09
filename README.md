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
