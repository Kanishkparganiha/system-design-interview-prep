"""
Chapter 4: Gradient Computation
===============================
Numerical vs analytical gradients and gradient checking.

Run: python 03_gradient_computation.py
"""

import numpy as np

print("=" * 70)
print("GRADIENT COMPUTATION")
print("=" * 70)


# =============================================================================
# 1. WHY GRADIENTS MATTER
# =============================================================================
print("\n" + "=" * 70)
print("1. WHY GRADIENTS MATTER")
print("=" * 70)

print("""
Gradient descent updates parameters using gradients:

    θ_{t+1} = θ_t - η × ∇L(θ_t)

The gradient ∇L(θ) tells us:
    - Direction of steepest increase (we go opposite)
    - How sensitive the loss is to each parameter

Computing gradients correctly is CRITICAL!
    - Wrong gradients → model doesn't learn
    - Numerical issues → NaN/Inf values
""")


# =============================================================================
# 2. NUMERICAL GRADIENTS
# =============================================================================
print("\n" + "=" * 70)
print("2. NUMERICAL GRADIENTS (Finite Differences)")
print("=" * 70)

print("""
Numerical gradient uses the definition of derivative:

    Forward difference:  ∂f/∂x ≈ (f(x+h) - f(x)) / h

    Central difference:  ∂f/∂x ≈ (f(x+h) - f(x-h)) / (2h)

Central difference is more accurate (O(h²) vs O(h) error).
""")


def numerical_gradient_1d(f, x, h=1e-5):
    """Compute numerical gradient for a scalar function."""
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_gradient(f, x, h=1e-5):
    """Compute numerical gradient for a function of array x."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad


# Example: f(x) = x²
f = lambda x: x ** 2
x = 3.0

numerical_grad = numerical_gradient_1d(f, x)
analytical_grad = 2 * x  # f'(x) = 2x

print(f"f(x) = x², at x = {x}")
print(f"  Numerical gradient:  {numerical_grad:.6f}")
print(f"  Analytical gradient: {analytical_grad:.6f}")
print(f"  Difference: {abs(numerical_grad - analytical_grad):.2e}")


# =============================================================================
# 3. ANALYTICAL GRADIENTS (CALCULUS)
# =============================================================================
print("\n" + "=" * 70)
print("3. ANALYTICAL GRADIENTS")
print("=" * 70)

print("""
Analytical gradients are derived using calculus rules:

Common derivatives:
    d/dx (x^n) = n × x^(n-1)
    d/dx (e^x) = e^x
    d/dx (log x) = 1/x
    d/dx (sin x) = cos x

Chain rule (crucial for neural networks!):
    d/dx f(g(x)) = f'(g(x)) × g'(x)
""")


# Example: Complex function
def complex_function(x):
    """f(x) = sin(x²) + exp(-x)"""
    return np.sin(x ** 2) + np.exp(-x)


def complex_gradient_analytical(x):
    """Analytical gradient of f(x) = sin(x²) + exp(-x)"""
    # d/dx sin(x²) = cos(x²) × 2x (chain rule)
    # d/dx exp(-x) = -exp(-x)
    return np.cos(x ** 2) * 2 * x - np.exp(-x)


x = 1.5
print(f"\nf(x) = sin(x²) + exp(-x), at x = {x}")
print(f"  Numerical:  {numerical_gradient_1d(complex_function, x):.6f}")
print(f"  Analytical: {complex_gradient_analytical(x):.6f}")


# =============================================================================
# 4. GRADIENT CHECKING
# =============================================================================
print("\n" + "=" * 70)
print("4. GRADIENT CHECKING")
print("=" * 70)

print("""
ALWAYS verify your analytical gradients with numerical gradients!

Relative error check:
    error = |numerical - analytical| / max(|numerical|, |analytical|, ε)

Thresholds:
    error < 1e-7: Excellent
    error < 1e-5: Good
    error < 1e-3: Probably OK (might be numerical precision)
    error > 1e-3: Something is wrong!
""")


def gradient_check(f, analytical_grad_fn, x, h=1e-5, threshold=1e-5):
    """
    Check if analytical gradients match numerical gradients.

    Args:
        f: Function to differentiate
        analytical_grad_fn: Function that returns analytical gradients
        x: Point at which to check
        h: Step size for numerical gradient
        threshold: Error threshold

    Returns:
        (passed, errors) tuple
    """
    numerical_grad = numerical_gradient(f, x, h)
    analytical_grad = analytical_grad_fn(x)

    # Compute relative error
    errors = []
    for i in range(len(x)):
        num = numerical_grad[i]
        ana = analytical_grad[i]

        # Relative error with epsilon for stability
        rel_error = abs(num - ana) / max(abs(num), abs(ana), 1e-8)
        errors.append(rel_error)

    max_error = max(errors)
    passed = max_error < threshold

    return passed, errors, numerical_grad, analytical_grad


# Example: Gradient check for linear layer
def linear_forward(W, x, b):
    """y = Wx + b"""
    return W @ x + b


def linear_loss(params, x, y_true):
    """MSE loss for linear layer."""
    W = params[:6].reshape(2, 3)
    b = params[6:]
    y_pred = W @ x + b
    return np.mean((y_pred - y_true) ** 2)


def linear_grad_analytical(params, x, y_true):
    """Analytical gradients for linear layer with MSE loss."""
    W = params[:6].reshape(2, 3)
    b = params[6:]
    y_pred = W @ x + b
    error = y_pred - y_true

    # dL/dW = 2/n × error × xᵀ
    grad_W = (2 / len(y_pred)) * np.outer(error, x)
    # dL/db = 2/n × error
    grad_b = (2 / len(y_pred)) * error

    return np.concatenate([grad_W.flatten(), grad_b])


# Test
np.random.seed(42)
W = np.random.randn(2, 3)
b = np.random.randn(2)
x = np.random.randn(3)
y_true = np.random.randn(2)

params = np.concatenate([W.flatten(), b])
f = lambda p: linear_loss(p, x, y_true)
grad_fn = lambda p: linear_grad_analytical(p, x, y_true)

passed, errors, num_grad, ana_grad = gradient_check(f, grad_fn, params)

print(f"Gradient check for linear layer:")
print(f"  Passed: {passed}")
print(f"  Max relative error: {max(errors):.2e}")
print(f"\n  Numerical:  {num_grad.round(6)}")
print(f"  Analytical: {ana_grad.round(6)}")


# =============================================================================
# 5. BACKPROPAGATION
# =============================================================================
print("\n" + "=" * 70)
print("5. BACKPROPAGATION (Chain Rule Applied)")
print("=" * 70)

print("""
Backpropagation efficiently computes all gradients using the chain rule.

Forward pass: Compute output layer by layer, save intermediate values
Backward pass: Compute gradients layer by layer, from output to input

Example: y = sigmoid(W₂ × ReLU(W₁ × x))

Forward:
    z₁ = W₁ × x
    a₁ = ReLU(z₁)
    z₂ = W₂ × a₁
    y = sigmoid(z₂)

Backward:
    ∂L/∂y = (computed from loss)
    ∂L/∂z₂ = ∂L/∂y × sigmoid'(z₂)
    ∂L/∂W₂ = ∂L/∂z₂ × a₁ᵀ
    ∂L/∂a₁ = W₂ᵀ × ∂L/∂z₂
    ∂L/∂z₁ = ∂L/∂a₁ × ReLU'(z₁)
    ∂L/∂W₁ = ∂L/∂z₁ × xᵀ
""")


class ComputationalGraph:
    """Simple computational graph demonstrating backprop."""

    def __init__(self):
        self.cache = {}

    def forward(self, x, W1, W2):
        """Forward pass through 2-layer network."""
        # Layer 1
        self.cache['x'] = x
        z1 = W1 @ x
        self.cache['z1'] = z1
        a1 = np.maximum(0, z1)  # ReLU
        self.cache['a1'] = a1
        self.cache['W1'] = W1

        # Layer 2
        z2 = W2 @ a1
        self.cache['z2'] = z2
        y = 1 / (1 + np.exp(-z2))  # Sigmoid
        self.cache['y'] = y
        self.cache['W2'] = W2

        return y

    def backward(self, dL_dy):
        """Backward pass (backpropagation)."""
        grads = {}

        # Get cached values
        y = self.cache['y']
        z2 = self.cache['z2']
        a1 = self.cache['a1']
        z1 = self.cache['z1']
        x = self.cache['x']
        W2 = self.cache['W2']
        W1 = self.cache['W1']

        # Backward through sigmoid
        dL_dz2 = dL_dy * y * (1 - y)

        # Gradients for W2
        grads['W2'] = np.outer(dL_dz2, a1)

        # Backward through W2
        dL_da1 = W2.T @ dL_dz2

        # Backward through ReLU
        dL_dz1 = dL_da1 * (z1 > 0)

        # Gradients for W1
        grads['W1'] = np.outer(dL_dz1, x)

        return grads


# Demo
np.random.seed(42)
x = np.random.randn(3)
W1 = np.random.randn(4, 3)
W2 = np.random.randn(2, 4)
y_true = np.array([0.7, 0.3])

graph = ComputationalGraph()
y = graph.forward(x, W1, W2)

# MSE loss gradient
dL_dy = 2 * (y - y_true) / len(y)

grads = graph.backward(dL_dy)

print("Two-layer network backpropagation:")
print(f"  Input shape:  {x.shape}")
print(f"  W1 shape:     {W1.shape}")
print(f"  W2 shape:     {W2.shape}")
print(f"  Output:       {y.round(4)}")
print(f"  dL/dW2 shape: {grads['W2'].shape}")
print(f"  dL/dW1 shape: {grads['W1'].shape}")


# =============================================================================
# 6. AUTOMATIC DIFFERENTIATION
# =============================================================================
print("\n" + "=" * 70)
print("6. AUTOMATIC DIFFERENTIATION (How PyTorch Works)")
print("=" * 70)

print("""
Automatic differentiation (autodiff) computes exact gradients automatically.

Two modes:
    - Forward mode: Compute ∂y/∂x along with y
    - Reverse mode: Compute all ∂L/∂xᵢ efficiently (backprop)

Reverse mode is efficient when we have many inputs, few outputs.
Perfect for neural networks: many parameters, one loss!

How it works:
    1. Build computational graph during forward pass
    2. Store gradient functions for each operation
    3. Traverse graph backward, applying chain rule
""")

# Simple autodiff implementation
class Var:
    """Variable with automatic gradient tracking."""

    def __init__(self, value, _children=(), _op=''):
        self.value = value
        self.grad = 0.0
        self._backward = lambda: None
        self._children = set(_children)
        self._op = _op

    def __add__(self, other):
        other = other if isinstance(other, Var) else Var(other)
        out = Var(self.value + other.value, (self, other), '+')

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Var) else Var(other)
        out = Var(self.value * other.value, (self, other), '*')

        def _backward():
            self.grad += other.value * out.grad
            other.grad += self.value * out.grad
        out._backward = _backward
        return out

    def __pow__(self, power):
        out = Var(self.value ** power, (self,), f'**{power}')

        def _backward():
            self.grad += power * (self.value ** (power - 1)) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        """Compute gradients via reverse-mode autodiff."""
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward()


# Demo autodiff
x = Var(2.0)
y = Var(3.0)

# f = x² + xy + y²
f = x ** 2 + x * y + y ** 2
f.backward()

print(f"f = x² + xy + y² at x={x.value}, y={y.value}")
print(f"  f = {f.value}")
print(f"  ∂f/∂x = {x.grad} (should be 2x + y = 7)")
print(f"  ∂f/∂y = {y.grad} (should be x + 2y = 8)")


# =============================================================================
# 7. COMMON GRADIENT PATTERNS
# =============================================================================
print("\n" + "=" * 70)
print("7. COMMON GRADIENT PATTERNS")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│ Operation              │ Forward         │ Backward (∂L/∂x)        │
├─────────────────────────────────────────────────────────────────────┤
│ Addition: y = x + c    │ y = x + c       │ ∂L/∂y                   │
│ Multiply: y = x × c    │ y = x × c       │ c × ∂L/∂y               │
│ MatMul: y = Wx         │ y = W @ x       │ Wᵀ @ ∂L/∂y              │
│ ReLU: y = max(0, x)    │ y = max(0,x)    │ ∂L/∂y × (x > 0)         │
│ Sigmoid: y = σ(x)      │ y = σ(x)        │ ∂L/∂y × y × (1-y)       │
│ Softmax + CE           │ y = softmax(x)  │ y - y_true              │
│ Sum: y = Σxᵢ           │ y = sum(x)      │ ones × ∂L/∂y            │
│ Mean: y = mean(x)      │ y = mean(x)     │ ones/n × ∂L/∂y          │
└─────────────────────────────────────────────────────────────────────┘
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: GRADIENT COMPUTATION")
print("=" * 70)

print("""
Key Concepts:
─────────────
1. Numerical gradients: Finite differences (for checking)
2. Analytical gradients: Calculus rules (for efficiency)
3. Backpropagation: Chain rule applied layer by layer
4. Autodiff: Automatic exact gradient computation

Gradient Checking:
──────────────────
• Always verify new gradient implementations
• Use central difference for accuracy
• Check relative error, not absolute
• Typical threshold: 1e-5

Best Practices:
───────────────
• Use frameworks (PyTorch/TensorFlow) for autodiff
• Gradient check custom layers manually
• Watch for numerical issues (vanishing/exploding)
• Understand how gradients flow for debugging

Common Issues:
──────────────
• Vanishing gradients → use ReLU, skip connections
• Exploding gradients → gradient clipping
• NaN gradients → numerical stability issues
• Zero gradients → dead ReLU, wrong architecture
""")
