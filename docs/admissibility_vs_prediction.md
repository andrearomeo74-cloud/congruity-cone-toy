# Admissibility vs Prediction

This document clarifies a critical distinction underlying this repository:

**Congruity is not a predictive framework.  
Congruity Cones do not forecast outcomes.**

They constrain what futures are *structurally admissible*.

---

## 1. Prediction answers a different question

Prediction asks:

> “What is the most likely outcome?”

This requires:
- probabilistic modeling
- calibration against historical labels
- accuracy, recall, confidence intervals
- post-hoc error correction

Prediction operates *inside* an assumed state space.

---

## 2. Admissibility answers a prior question

Congruity and Congruity Cones ask:

> “Which future trajectories are still structurally viable from here?”

This operates **before** prediction.

It does not rank outcomes by likelihood.
It restricts the space in which outcomes are allowed to exist.

---

## 3. Why Congruity cannot (and should not) predict

Congruity-based systems deliberately avoid:
- probabilistic forecasts
- numerical confidence claims
- point predictions
- accuracy metrics

Because once a trajectory becomes structurally inadmissible,
its probability is irrelevant.

It should not be optimized.
It should be excluded.

---

## 4. The role of Congruity Cones

Congruity evaluates a state.

Congruity Cones constrain the **set of future states**
by enforcing:

- curvature limits (how fast conditions can worsen)
- drift accumulation (latent debt on plateaus)
- synchrony constraints (mismatch between agents or subsystems)
- history-aware thresholds

The result is a shrinking or expanding cone of admissible futures.

This cone is **not a probability distribution**.

---

## 5. Error is the wrong metric

Asking “with what error does this predict?” is a category mistake.

Admissibility systems are evaluated by:
- false allowance (letting an impossible path survive)
- premature exclusion (blocking a still-viable path)
- stability under perturbation
- consistency across scales and regimes

Not by forecast accuracy.

---

## 6. Relation to downstream models

Admissibility acts as an *ex-ante gate*.

Prediction, optimization, or control may occur **only inside**
the admissible region.

This sequencing is intentional:

> Admissibility first.  
> Optimization later.  
> Correction never.

---

## 7. Summary

Prediction chooses among futures.  
Admissibility decides which futures are allowed to exist.

Congruity Cones do not say *what will happen*.

They say:

> “From here, only these futures remain possible.”
