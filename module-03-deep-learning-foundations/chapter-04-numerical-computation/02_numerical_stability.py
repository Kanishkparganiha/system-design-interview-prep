"""
Chapter 4: Numerical Stability
==============================
Understanding and avoiding numerical issues in deep learning.

Run: python 02_numerical_stability.py
"""

import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("NUMERICAL STABILITY IN DEEP LEARNING")
print("=" * 70)


# =============================================================================
# 1. FLOATING POINT REPRESENTATION
# =============================================================================
print("\n" + "=" * 70)
print("1. FLOATING POINT BASICS")
print("=" * 70)

print("""
Computers represent real numbers in floating point:

    x = (-1)^s × m × 2^e

    s = sign bit (0 or 1)
    m = mantissa (significand)
    e = exponent

Common formats:
    float32: 1 sign + 8 exp + 23 mantissa bits
    float16: 1 sign + 5 exp + 10 mantissa bits
    bfloat16: 1 sign + 8 exp + 7 mantissa bits (good range, less precision)

Key limitations:
    - Finite precision (can't represent all real numbers)
    - Limited range (overflow/underflow possible)
""")

# Demonstrate precision limits
print("Precision limits:")
print(f"  float64 epsilon: {np.finfo(np.float64).eps}")
print(f"  float32 epsilon: {np.finfo(np.float32).eps}")
print(f"  float16 epsilon: {np.finfo(np.float16).eps}")

print("\nRange limits (float32):")
print(f"  Max: {np.finfo(np.float32).max}")
print(f"  Min positive: {np.finfo(np.float32).tiny}")


# =============================================================================
# 2. OVERFLOW AND UNDERFLOW
# =============================================================================
print("\n" + "=" * 70)
print("2. OVERFLOW AND UNDERFLOW")
print("=" * 70)

print("""
OVERFLOW: Number too large to represent → Inf
UNDERFLOW: Number too small (close to 0) → 0

Both can cause problems in computations!
""")

# Overflow example
x = np.float32(1e38)
print(f"Overflow example:")
print(f"  x = 1e38")
print(f"  x * 10 = {x * 10}")  # Inf

# Underflow example
y = np.float32(1e-45)
print(f"\nUnderflow example:")
print(f"  y = 1e-45")
print(f"  y / 10 = {y / 10}")  # 0


# Common problematic operations
print("\n--- Problematic Operations ---")

# exp() overflow
print("\nexp() overflow:")
for val in [10, 100, 1000]:
    result = np.exp(np.float32(val))
    print(f"  exp({val}) = {result}")

# log() of small numbers
print("\nlog() underflow issues:")
small_probs = [1e-5, 1e-30, 1e-45, 0]
for p in small_probs:
    with np.errstate(divide='ignore'):
        result = np.log(np.float32(p))
    print(f"  log({p}) = {result}")


# =============================================================================
# 3. SOFTMAX STABILITY
# =============================================================================
print("\n" + "=" * 70)
print("3. SOFTMAX: THE CLASSIC STABILITY PROBLEM")
print("=" * 70)

print("""
Softmax: p_i = exp(x_i) / Σ exp(x_j)

Problem: exp(x) can overflow for large x!
""")


def softmax_unstable(x):
    """Naive softmax - prone to overflow."""
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()


def softmax_stable(x):
    """Stable softmax using the max subtraction trick."""
    # Subtract max to prevent overflow
    # Mathematically equivalent: exp(x-c)/sum(exp(x-c)) = exp(x)/sum(exp(x))
    x_shifted = x - np.max(x)
    exp_x = np.exp(x_shifted)
    return exp_x / exp_x.sum()


# Compare
x_small = np.array([1.0, 2.0, 3.0])
x_large = np.array([1000.0, 1001.0, 1002.0])

print("Small values (both work):")
print(f"  Unstable: {softmax_unstable(x_small).round(4)}")
print(f"  Stable:   {softmax_stable(x_small).round(4)}")

print("\nLarge values (unstable fails!):")
print(f"  Unstable: {softmax_unstable(x_large)}")
print(f"  Stable:   {softmax_stable(x_large).round(4)}")


# =============================================================================
# 4. LOG-SUM-EXP TRICK
# =============================================================================
print("\n" + "=" * 70)
print("4. LOG-SUM-EXP TRICK")
print("=" * 70)

print("""
Often need: log(Σ exp(x_i))

Naive approach overflows. Solution:

    log(Σ exp(x_i)) = max(x) + log(Σ exp(x_i - max(x)))

Now exp() only sees values ≤ 0, so no overflow!
""")


def logsumexp_unstable(x):
    """Naive log-sum-exp."""
    return np.log(np.sum(np.exp(x)))


def logsumexp_stable(x):
    """Stable log-sum-exp."""
    x_max = np.max(x)
    return x_max + np.log(np.sum(np.exp(x - x_max)))


x_test = np.array([1000, 1001, 1002])

print(f"x = {x_test}")
print(f"  Unstable logsumexp: {logsumexp_unstable(x_test)}")
print(f"  Stable logsumexp:   {logsumexp_stable(x_test):.4f}")
print(f"  NumPy scipy:        {np.logaddexp.reduce(x_test):.4f}")


# =============================================================================
# 5. CROSS-ENTROPY STABILITY
# =============================================================================
print("\n" + "=" * 70)
print("5. CROSS-ENTROPY LOSS STABILITY")
print("=" * 70)

print("""
Cross-entropy: L = -Σ y_true × log(y_pred)

Problems:
    1. log(0) = -inf
    2. log(very small) = very negative

Solutions:
    1. Clip probabilities: clip(y_pred, epsilon, 1-epsilon)
    2. Better: Compute from logits directly
""")


def cross_entropy_unstable(y_true, y_pred):
    """Naive cross-entropy."""
    return -np.sum(y_true * np.log(y_pred))


def cross_entropy_stable(y_true, y_pred, eps=1e-15):
    """Stable cross-entropy with clipping."""
    y_pred_clipped = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true * np.log(y_pred_clipped))


def cross_entropy_from_logits(y_true, logits):
    """
    Most stable: compute from logits using log-sum-exp.

    CE = -y·logits + log(sum(exp(logits)))
    """
    return -np.sum(y_true * logits) + logsumexp_stable(logits)


# Demo
y_true = np.array([1, 0, 0])

# Good predictions
y_pred_good = np.array([0.9, 0.05, 0.05])
print(f"Good prediction {y_pred_good}:")
print(f"  CE = {cross_entropy_stable(y_true, y_pred_good):.4f}")

# Almost certain prediction
y_pred_certain = np.array([0.9999999, 1e-8, 1e-8])
print(f"\nAlmost certain {y_pred_certain}:")
print(f"  CE (stable) = {cross_entropy_stable(y_true, y_pred_certain):.8f}")

# From logits
logits = np.array([10, -10, -10])
print(f"\nFrom logits {logits}:")
print(f"  CE = {cross_entropy_from_logits(y_true, logits):.8f}")


# =============================================================================
# 6. GRADIENT ISSUES
# =============================================================================
print("\n" + "=" * 70)
print("6. GRADIENT STABILITY ISSUES")
print("=" * 70)

print("""
VANISHING GRADIENTS:
    - Gradients become very small (→ 0)
    - Deep networks stop learning
    - Causes: sigmoid/tanh saturation, deep networks

EXPLODING GRADIENTS:
    - Gradients become very large (→ ∞)
    - Weights blow up, NaN losses
    - Causes: large weights, poor initialization

Solutions:
    - Use ReLU (doesn't saturate for positive values)
    - Proper initialization (Xavier, He)
    - Batch normalization
    - Gradient clipping
    - Skip connections (ResNet)
""")

# Sigmoid saturation
def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)


print("Sigmoid gradient (derivative):")
for x in [0, 1, 5, 10, 20]:
    grad = sigmoid_derivative(x)
    print(f"  x={x:2d}: sigmoid'(x) = {grad:.6f}")

print("\nVanishing gradient example:")
print("After 10 layers with sigmoid, gradient ≈ (0.25)^10 =", 0.25**10)


# Gradient clipping
def clip_gradients(gradients, max_norm):
    """Clip gradients by global norm."""
    total_norm = np.sqrt(sum(np.sum(g**2) for g in gradients))
    clip_coef = max_norm / (total_norm + 1e-6)
    if clip_coef < 1:
        gradients = [g * clip_coef for g in gradients]
    return gradients, total_norm


# Demo gradient clipping
grads = [np.array([100, 200]), np.array([300])]
clipped, norm = clip_gradients(grads, max_norm=10)
print(f"\nGradient clipping:")
print(f"  Original norm: {norm:.2f}")
print(f"  After clipping (max_norm=10): {[g.round(2) for g in clipped]}")


# =============================================================================
# 7. BATCH NORMALIZATION
# =============================================================================
print("\n" + "=" * 70)
print("7. BATCH NORMALIZATION")
print("=" * 70)

print("""
BatchNorm normalizes activations to have mean=0, variance=1:

    x_norm = (x - μ_batch) / √(σ²_batch + ε)
    y = γ × x_norm + β  (learnable scale and shift)

Benefits:
    - Reduces internal covariate shift
    - Allows higher learning rates
    - Acts as regularization
    - Helps with vanishing/exploding gradients

The ε (epsilon) term prevents division by zero!
""")


class BatchNorm1D:
    """Simple batch normalization."""

    def __init__(self, num_features, eps=1e-5, momentum=0.1):
        self.eps = eps
        self.momentum = momentum
        self.gamma = np.ones(num_features)
        self.beta = np.zeros(num_features)
        self.running_mean = np.zeros(num_features)
        self.running_var = np.ones(num_features)

    def forward(self, x, training=True):
        if training:
            mean = x.mean(axis=0)
            var = x.var(axis=0)

            # Update running stats
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * var
        else:
            mean = self.running_mean
            var = self.running_var

        # Normalize
        x_norm = (x - mean) / np.sqrt(var + self.eps)

        # Scale and shift
        return self.gamma * x_norm + self.beta


# Demo
np.random.seed(42)
x = np.random.randn(32, 64) * 10 + 5  # Mean ~5, std ~10

bn = BatchNorm1D(64)
x_normed = bn.forward(x)

print(f"Before BatchNorm:")
print(f"  Mean: {x.mean():.2f}, Std: {x.std():.2f}")
print(f"\nAfter BatchNorm:")
print(f"  Mean: {x_normed.mean():.4f}, Std: {x_normed.std():.4f}")


# =============================================================================
# 8. MIXED PRECISION TRAINING
# =============================================================================
print("\n" + "=" * 70)
print("8. MIXED PRECISION TRAINING")
print("=" * 70)

print("""
Use lower precision (float16) for speed, higher precision for stability:

    Forward pass:  float16 (fast)
    Loss:          float32 (stable)
    Gradients:     float16 (fast)
    Weight update: float32 (precise)

Loss Scaling:
    - Multiply loss by large constant before backward
    - Gradients scale up (prevent underflow)
    - Divide gradients before update

Benefits:
    - 2x memory savings
    - Faster computation (especially on GPUs)
    - Same accuracy (if done right)
""")

# Demonstrate loss scaling
loss_fp32 = 0.0001
loss_fp16 = np.float16(loss_fp32)
print(f"Small loss comparison:")
print(f"  float32: {loss_fp32}")
print(f"  float16: {loss_fp16}")

# With loss scaling
scale_factor = 1024
scaled_loss = loss_fp32 * scale_factor
scaled_loss_fp16 = np.float16(scaled_loss)
print(f"\nWith loss scaling (factor={scale_factor}):")
print(f"  Scaled loss (float16): {scaled_loss_fp16}")
print(f"  Unscaled: {scaled_loss_fp16 / scale_factor}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: NUMERICAL STABILITY")
print("=" * 70)

print("""
Common Issues and Solutions:
────────────────────────────

┌──────────────────┬────────────────────────────────────────────────────┐
│ Problem          │ Solution                                           │
├──────────────────┼────────────────────────────────────────────────────┤
│ exp() overflow   │ Subtract max (softmax trick)                       │
│ log(0)           │ Clip values, use from-logits formulation           │
│ log-sum-exp      │ Max subtraction trick                              │
│ Vanishing grad   │ ReLU, skip connections, proper init                │
│ Exploding grad   │ Gradient clipping, normalization                   │
│ Division by 0    │ Add epsilon (ε) to denominator                     │
│ float16 underflow│ Loss scaling                                       │
└──────────────────┴────────────────────────────────────────────────────┘

Best Practices:
───────────────
1. Use stable implementations (PyTorch/TensorFlow handle this)
2. Monitor for NaN/Inf during training
3. Use gradient clipping as safety net
4. Apply batch/layer normalization
5. Initialize weights properly
6. Start with float32, then try mixed precision
""")
