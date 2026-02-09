"""
Chapter 4: Optimization Basics
==============================
Gradient descent and optimization - how neural networks learn.

Run: python 01_optimization_basics.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("OPTIMIZATION BASICS")
print("=" * 70)


# =============================================================================
# GRADIENT DESCENT INTUITION
# =============================================================================
print("\n" + "=" * 70)
print("1. GRADIENT DESCENT INTUITION")
print("=" * 70)

print("""
Goal: Find parameters θ that minimize a loss function L(θ)

Gradient Descent Algorithm:
    1. Start at some θ₀
    2. Compute gradient ∇L(θ)
    3. Update: θ = θ - α · ∇L(θ)
    4. Repeat until convergence

Where α is the learning rate.

Intuition: The gradient points "uphill" (direction of steepest increase).
           We go in the OPPOSITE direction to descend.
""")


# =============================================================================
# SIMPLE 1D EXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("2. SIMPLE 1D EXAMPLE: f(x) = x²")
print("=" * 70)

def f(x):
    """Loss function: f(x) = x²"""
    return x ** 2

def df(x):
    """Gradient: df/dx = 2x"""
    return 2 * x

# Gradient descent
x = 5.0  # Start far from minimum
learning_rate = 0.1
history = [x]

print(f"Starting at x = {x}")
print(f"Learning rate α = {learning_rate}")
print(f"\nGradient Descent Steps:")
print("-" * 40)

for i in range(10):
    grad = df(x)
    x_new = x - learning_rate * grad
    print(f"  Step {i+1}: x = {x:.4f}, grad = {grad:.4f}, new_x = {x_new:.4f}")
    x = x_new
    history.append(x)

print(f"\nFinal x = {x:.6f} (should be close to 0)")
print(f"Final f(x) = {f(x):.6f}")


# =============================================================================
# LEARNING RATE IMPORTANCE
# =============================================================================
print("\n" + "=" * 70)
print("3. LEARNING RATE IMPORTANCE")
print("=" * 70)

print("""
Learning rate α is crucial:
    - Too small: Slow convergence
    - Too large: Overshooting, divergence
    - Just right: Fast, stable convergence
""")

def gradient_descent_1d(x0, lr, n_steps, f, df):
    x = x0
    history = [x]
    for _ in range(n_steps):
        x = x - lr * df(x)
        history.append(x)
    return history

# Compare different learning rates
learning_rates = [0.01, 0.1, 0.5, 0.99, 1.01]
x0 = 5.0

print(f"Starting at x = {x0}")
print("-" * 50)

for lr in learning_rates:
    history = gradient_descent_1d(x0, lr, 20, f, df)
    final = history[-1]
    if np.isnan(final) or np.abs(final) > 1e10:
        status = "DIVERGED"
    elif np.abs(final) < 0.01:
        status = "CONVERGED"
    else:
        status = "SLOW"
    print(f"  lr = {lr:5.2f}: final x = {final:12.4f}  [{status}]")


# =============================================================================
# 2D OPTIMIZATION
# =============================================================================
print("\n" + "=" * 70)
print("4. 2D OPTIMIZATION")
print("=" * 70)

print("""
Real neural networks have millions of parameters.
Let's see gradient descent in 2D: f(x, y) = x² + 2y²
""")

def f_2d(x, y):
    return x**2 + 2*y**2

def grad_2d(x, y):
    return np.array([2*x, 4*y])

# Gradient descent in 2D
point = np.array([4.0, 3.0])
lr = 0.1
history_2d = [point.copy()]

print(f"Starting at ({point[0]}, {point[1]})")
print(f"f(x,y) = x² + 2y²")
print("-" * 40)

for i in range(10):
    grad = grad_2d(point[0], point[1])
    point = point - lr * grad
    history_2d.append(point.copy())
    loss = f_2d(point[0], point[1])
    print(f"  Step {i+1}: ({point[0]:6.3f}, {point[1]:6.3f}), loss = {loss:.4f}")

print(f"\nMinimum found at ({point[0]:.4f}, {point[1]:.4f})")
print(f"True minimum at (0, 0)")


# =============================================================================
# STOCHASTIC GRADIENT DESCENT (SGD)
# =============================================================================
print("\n" + "=" * 70)
print("5. STOCHASTIC GRADIENT DESCENT (SGD)")
print("=" * 70)

print("""
In deep learning, we can't compute gradient on ALL data (too expensive).

Instead, we use MINI-BATCHES:

Batch Gradient Descent:
    θ = θ - α · (1/N) Σ ∇L(xᵢ, yᵢ, θ)   [all N samples]

Stochastic Gradient Descent (SGD):
    θ = θ - α · ∇L(x_random, y_random, θ)   [one sample]

Mini-batch SGD (most common):
    θ = θ - α · (1/B) Σ ∇L(xᵢ, yᵢ, θ)   [B samples]

Typical batch sizes: 32, 64, 128, 256
""")

# Simulate linear regression with SGD
np.random.seed(42)
N = 100
X = np.random.randn(N, 1)
y_true = 3 * X.squeeze() + 2 + 0.1 * np.random.randn(N)  # y = 3x + 2 + noise

def mse_loss(w, b, X, y):
    pred = X @ w + b
    return np.mean((pred - y) ** 2)

def grad_mse(w, b, X, y):
    pred = X @ w + b
    error = pred - y
    dw = 2 * np.mean(error * X.T, axis=1)
    db = 2 * np.mean(error)
    return dw, db

# Full batch gradient descent
w_full = np.array([0.0])
b_full = 0.0
lr = 0.1
losses_full = []

for epoch in range(100):
    dw, db = grad_mse(w_full, b_full, X, y_true)
    w_full = w_full - lr * dw
    b_full = b_full - lr * db
    losses_full.append(mse_loss(w_full, b_full, X, y_true))

print(f"\nFull Batch GD (100 epochs):")
print(f"  True: w=3, b=2")
print(f"  Found: w={w_full[0]:.4f}, b={b_full:.4f}")

# Mini-batch SGD
w_sgd = np.array([0.0])
b_sgd = 0.0
batch_size = 10
losses_sgd = []

for epoch in range(100):
    # Shuffle data
    indices = np.random.permutation(N)
    for i in range(0, N, batch_size):
        batch_idx = indices[i:i+batch_size]
        X_batch = X[batch_idx]
        y_batch = y_true[batch_idx]

        dw, db = grad_mse(w_sgd, b_sgd, X_batch, y_batch)
        w_sgd = w_sgd - lr * dw
        b_sgd = b_sgd - lr * db

    losses_sgd.append(mse_loss(w_sgd, b_sgd, X, y_true))

print(f"\nMini-batch SGD (batch_size={batch_size}, 100 epochs):")
print(f"  True: w=3, b=2")
print(f"  Found: w={w_sgd[0]:.4f}, b={b_sgd:.4f}")


# =============================================================================
# MOMENTUM
# =============================================================================
print("\n" + "=" * 70)
print("6. MOMENTUM")
print("=" * 70)

print("""
Momentum helps accelerate SGD and dampen oscillations.

Standard SGD:
    θ = θ - α · ∇L

SGD with Momentum:
    v = β · v + ∇L          (velocity accumulation)
    θ = θ - α · v

Where β is the momentum coefficient (typically 0.9).

Intuition: Like a ball rolling downhill, it accumulates velocity.
""")

def sgd_with_momentum(x0, lr, momentum, n_steps, f, df):
    x = x0
    v = 0
    history = [x]
    for _ in range(n_steps):
        grad = df(x)
        v = momentum * v + grad
        x = x - lr * v
        history.append(x)
    return history

# Compare with and without momentum
print("\nComparing on f(x) = x² starting from x=5:")
history_no_mom = gradient_descent_1d(5.0, 0.05, 20, f, df)
history_mom = sgd_with_momentum(5.0, 0.05, 0.9, 20, f, df)

print(f"  Without momentum: final x = {history_no_mom[-1]:.6f}")
print(f"  With momentum:    final x = {history_mom[-1]:.6f}")


# =============================================================================
# ADAPTIVE LEARNING RATES
# =============================================================================
print("\n" + "=" * 70)
print("7. ADAPTIVE LEARNING RATES")
print("=" * 70)

print("""
Problem: Different parameters may need different learning rates.

Solution: Adaptive optimizers adjust lr per-parameter.

RMSprop:
    v = β · v + (1-β) · g²     (accumulate squared gradients)
    θ = θ - α · g / √(v + ε)   (scale by inverse of RMS)

Adam (most popular):
    m = β₁ · m + (1-β₁) · g    (first moment - momentum)
    v = β₂ · v + (1-β₂) · g²   (second moment - RMSprop)
    m̂ = m / (1 - β₁ᵗ)          (bias correction)
    v̂ = v / (1 - β₂ᵗ)
    θ = θ - α · m̂ / √(v̂ + ε)

Default Adam: β₁=0.9, β₂=0.999, ε=1e-8
""")

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = 0
        self.v = 0
        self.t = 0

    def step(self, x, grad):
        self.t += 1
        self.m = self.beta1 * self.m + (1 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * grad**2

        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)

        return x - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

# Adam optimization
x = 5.0
adam = Adam(lr=0.5)
history_adam = [x]

for i in range(30):
    grad = df(x)
    x = adam.step(x, grad)
    history_adam.append(x)

print(f"\nAdam optimization on f(x) = x²:")
print(f"  Starting at x = 5.0")
print(f"  After 30 steps: x = {x:.6f}")


# =============================================================================
# PYTORCH OPTIMIZERS
# =============================================================================
print("\n" + "=" * 70)
print("8. PYTORCH OPTIMIZERS")
print("=" * 70)

import torch
import torch.optim as optim

# Simple optimization in PyTorch
x_torch = torch.tensor([5.0], requires_grad=True)

# Different optimizers
optimizers = {
    'SGD': optim.SGD([x_torch], lr=0.1),
    'SGD+Momentum': optim.SGD([x_torch], lr=0.1, momentum=0.9),
    'Adam': optim.Adam([x_torch], lr=0.5),
}

for name, optimizer in optimizers.items():
    x_torch = torch.tensor([5.0], requires_grad=True)
    if 'Momentum' in name:
        optimizer = optim.SGD([x_torch], lr=0.1, momentum=0.9)
    elif name == 'Adam':
        optimizer = optim.Adam([x_torch], lr=0.5)
    else:
        optimizer = optim.SGD([x_torch], lr=0.1)

    for _ in range(20):
        optimizer.zero_grad()
        loss = x_torch ** 2
        loss.backward()
        optimizer.step()

    print(f"  {name:15}: x = {x_torch.item():.6f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌──────────────────────────────────────────────────────────────────────────┐
│  Optimizer      │  Update Rule                    │  When to Use        │
├──────────────────────────────────────────────────────────────────────────┤
│  SGD            │  θ -= α·∇L                      │  Simple, stable      │
│  SGD+Momentum   │  v = βv + ∇L; θ -= α·v          │  Faster convergence  │
│  RMSprop        │  Adaptive lr per parameter      │  Non-stationary      │
│  Adam           │  Momentum + RMSprop             │  Default choice      │
│  AdamW          │  Adam + weight decay            │  With regularization │
└──────────────────────────────────────────────────────────────────────────┘

Key Hyperparameters:
─────────────────────
• Learning rate (α): Most important! Start with 1e-3 for Adam
• Batch size: Larger = more stable gradients, slower updates
• Momentum (β): 0.9 is standard
• Weight decay: 1e-4 to 1e-2

Tips:
─────
• Start with Adam (usually works)
• If overfitting, try AdamW with weight decay
• For vision, SGD+Momentum often works better
• Use learning rate schedulers for better convergence
""")
