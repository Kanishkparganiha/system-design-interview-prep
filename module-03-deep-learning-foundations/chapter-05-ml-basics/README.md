# Chapter 5: Machine Learning Basics

> "The foundation before we go deep."

---

## Why This Chapter?

Before understanding DEEP learning, you need to understand MACHINE learning:
- What is learning?
- How do we measure success?
- What can go wrong (overfitting, underfitting)?
- How to prevent failures (regularization)?

---

## Scripts in This Chapter

| Script | Topic | Key Concepts |
|--------|-------|--------------|
| `01_overfitting_regularization.py` | Regularization | L1, L2, dropout, early stopping, weight decay |
| `02_learning_framework.py` | Framework | Training/val/test, cross-validation, hyperparameter tuning |
| `03_capacity_bias_variance.py` | Capacity | Bias-variance tradeoff, VC dimension, model selection |
| `04_maximum_likelihood.py` | MLE | Maximum likelihood, loss function derivations, MAP |

---

## Key Concepts

### 1. The Learning Problem

```
Given: Training data {(x₁,y₁), (x₂,y₂), ..., (xₙ,yₙ)}
Find:  A function f(x) that predicts y for NEW data

Challenge: We want to generalize, not memorize!
```

### 2. Train/Validation/Test Split

```
┌──────────────────────────────────────────────────────────┐
│                     All Data                              │
├────────────────┬───────────────┬─────────────────────────┤
│    Training    │  Validation   │         Test            │
│     (70%)      │    (15%)      │        (15%)            │
├────────────────┼───────────────┼─────────────────────────┤
│ Learn params   │ Tune hyper-   │ Final evaluation        │
│                │ parameters    │ (never peek!)           │
└────────────────┴───────────────┴─────────────────────────┘
```

### 3. Bias-Variance Tradeoff

```
Error = Bias² + Variance + Irreducible Noise

High Bias (Underfitting):
    - Model too simple
    - High training error
    - High test error

High Variance (Overfitting):
    - Model too complex
    - Low training error
    - HIGH test error
```

### 4. Regularization

```
Original loss:    L(θ) = Σ loss(f(xᵢ), yᵢ)
Regularized:      L(θ) = Σ loss(f(xᵢ), yᵢ) + λ·R(θ)

R(θ) = ||θ||₂²   (L2 / Ridge / Weight Decay)
R(θ) = ||θ||₁    (L1 / Lasso / Sparsity)
```

---

## Run Order

```bash
python 01_overfitting_regularization.py
python 02_learning_framework.py
python 03_capacity_bias_variance.py
python 04_maximum_likelihood.py
```
