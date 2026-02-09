# Chapter 4: Numerical Computation

> "Making math work on real computers with finite precision."

---

## Why Numerical Computation Matters

Deep learning involves billions of floating-point operations. Understanding numerical issues helps you:
- Avoid training instabilities (NaN, Inf)
- Choose appropriate data types (float16, float32)
- Understand why certain tricks work (batch norm, gradient clipping)

---

## Scripts in This Chapter

| Script | Topic | Key Concepts |
|--------|-------|--------------|
| `01_optimization_basics.py` | Optimization | Gradient descent, SGD, momentum, Adam |
| `02_numerical_stability.py` | Stability | Overflow, underflow, softmax tricks, batch norm |
| `03_gradient_computation.py` | Gradients | Numerical vs analytical, backprop, autodiff |

---

## Key Concepts

### 1. Floating Point Representation

```
Float32: 1 sign bit + 8 exponent bits + 23 mantissa bits
Float16: 1 sign bit + 5 exponent bits + 10 mantissa bits

Range (float32): ±1.18e-38 to ±3.4e38
Precision: ~7 decimal digits

Common issues:
    - Overflow: Number too large → Inf
    - Underflow: Number too small → 0
    - Loss of precision: 1e10 + 1e-10 ≈ 1e10
```

### 2. The Softmax Trick

```python
# WRONG (overflow for large values)
softmax = exp(x) / sum(exp(x))

# RIGHT (numerically stable)
x_max = max(x)
softmax = exp(x - x_max) / sum(exp(x - x_max))
```

### 3. Log-Sum-Exp Trick

```python
# WRONG
log(sum(exp(x)))  # exp can overflow

# RIGHT
max_x = max(x)
log(sum(exp(x))) = max_x + log(sum(exp(x - max_x)))
```

---

## Run Order

```bash
python 01_optimization_basics.py
python 02_numerical_stability.py
python 03_gradient_computation.py
```
