"""
Chapter 5: Capacity, Bias, and Variance
=======================================
Understanding the fundamental tradeoffs in machine learning.

Run: python 03_capacity_bias_variance.py
"""

import numpy as np

print("=" * 70)
print("CAPACITY, BIAS, AND VARIANCE")
print("=" * 70)


# =============================================================================
# 1. MODEL CAPACITY
# =============================================================================
print("\n" + "=" * 70)
print("1. MODEL CAPACITY")
print("=" * 70)

print("""
Capacity = Model's ability to fit a variety of functions.

High capacity models can:
    ✓ Learn complex patterns
    ✗ Memorize noise (overfit)

Low capacity models can:
    ✓ Generalize well
    ✗ Miss complex patterns (underfit)

Capacity factors:
    - Number of parameters
    - Architecture (layers, connections)
    - Expressiveness of functions

Example: Polynomial regression
    - Degree 1: y = ax + b (low capacity)
    - Degree 5: y = ax⁵ + bx⁴ + cx³ + dx² + ex + f (higher capacity)
""")


def fit_polynomial(X, y, degree):
    """Fit polynomial of given degree."""
    # Create polynomial features
    X_poly = np.column_stack([X ** d for d in range(degree + 1)])
    # Solve normal equations
    coeffs = np.linalg.lstsq(X_poly, y, rcond=None)[0]
    return coeffs


def predict_polynomial(X, coeffs):
    """Predict using polynomial coefficients."""
    degree = len(coeffs) - 1
    X_poly = np.column_stack([X ** d for d in range(degree + 1)])
    return X_poly @ coeffs


# Generate noisy data from simple function
np.random.seed(42)
n_samples = 30
X_train = np.random.uniform(-3, 3, n_samples)
y_true = np.sin(X_train)  # True function
y_train = y_true + np.random.randn(n_samples) * 0.3  # Noisy observations

X_test = np.linspace(-3, 3, 100)
y_test_true = np.sin(X_test)

print("\nPolynomial fits of different capacities:")
print(f"{'Degree':<8} {'Train MSE':<12} {'Test MSE':<12} {'Status':<15}")
print("-" * 47)

for degree in [1, 3, 5, 10, 20]:
    coeffs = fit_polynomial(X_train, y_train, degree)
    train_pred = predict_polynomial(X_train, coeffs)
    test_pred = predict_polynomial(X_test, coeffs)

    train_mse = np.mean((train_pred - y_train) ** 2)
    test_mse = np.mean((test_pred - y_test_true) ** 2)

    if train_mse > 0.1:
        status = "Underfitting"
    elif test_mse > train_mse * 3:
        status = "Overfitting"
    else:
        status = "Good fit"

    print(f"{degree:<8} {train_mse:<12.4f} {test_mse:<12.4f} {status:<15}")


# =============================================================================
# 2. BIAS-VARIANCE DECOMPOSITION
# =============================================================================
print("\n" + "=" * 70)
print("2. BIAS-VARIANCE DECOMPOSITION")
print("=" * 70)

print("""
Expected Error = Bias² + Variance + Irreducible Noise

    E[(y - ŷ)²] = E[(ŷ - E[ŷ])²] + (E[ŷ] - f(x))² + σ²
                  ─────────────   ─────────────────   ──
                    Variance           Bias²         Noise

Where:
    y = true value = f(x) + ε
    ŷ = model prediction
    E[ŷ] = expected prediction (over different training sets)

Intuition:
    Bias = How far is average prediction from truth?
           (systematic error)

    Variance = How much do predictions vary across training sets?
               (sensitivity to training data)
""")


def estimate_bias_variance(model_class, X_train_all, y_train_all, X_test, y_test_true,
                          n_experiments=50, train_size=20):
    """
    Estimate bias and variance through bootstrap experiments.
    """
    predictions = []

    for _ in range(n_experiments):
        # Bootstrap sample
        idx = np.random.choice(len(X_train_all), train_size, replace=True)
        X_train = X_train_all[idx]
        y_train = y_train_all[idx]

        # Train model and predict
        model = model_class()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        predictions.append(pred)

    predictions = np.array(predictions)

    # Compute statistics
    mean_pred = predictions.mean(axis=0)
    variance = predictions.var(axis=0).mean()
    bias_squared = ((mean_pred - y_test_true) ** 2).mean()

    return bias_squared, variance


# Simple model class for experiments
class PolynomialModel:
    def __init__(self, degree=1):
        self.degree = degree
        self.coeffs = None

    def fit(self, X, y):
        self.coeffs = fit_polynomial(X, y, self.degree)

    def predict(self, X):
        return predict_polynomial(X, self.coeffs)


# Generate more training data for experiments
np.random.seed(42)
X_train_all = np.random.uniform(-3, 3, 200)
y_train_all = np.sin(X_train_all) + np.random.randn(200) * 0.3

X_test = np.linspace(-3, 3, 50)
y_test_true = np.sin(X_test)

print("\nBias-Variance Tradeoff:")
print(f"{'Degree':<8} {'Bias²':<12} {'Variance':<12} {'Total':<12}")
print("-" * 44)

for degree in [1, 2, 3, 5, 10, 15]:
    class Model:
        def fit(self, X, y):
            self.coeffs = fit_polynomial(X, y, degree)
        def predict(self, X):
            return predict_polynomial(X, self.coeffs)

    bias_sq, var = estimate_bias_variance(
        Model, X_train_all, y_train_all, X_test, y_test_true
    )
    total = bias_sq + var
    print(f"{degree:<8} {bias_sq:<12.4f} {var:<12.4f} {total:<12.4f}")


# =============================================================================
# 3. UNDERFITTING VS OVERFITTING
# =============================================================================
print("\n" + "=" * 70)
print("3. UNDERFITTING VS OVERFITTING")
print("=" * 70)

print("""
UNDERFITTING (High Bias):
    Symptoms:
        - High training error
        - High test error
        - Both errors similar

    Causes:
        - Model too simple
        - Not enough features
        - Too much regularization

    Solutions:
        - More complex model
        - More/better features
        - Less regularization
        - Train longer

OVERFITTING (High Variance):
    Symptoms:
        - Low training error
        - High test error
        - Large gap between errors

    Causes:
        - Model too complex
        - Not enough data
        - Too little regularization

    Solutions:
        - More training data
        - Simpler model
        - Regularization (L1, L2, dropout)
        - Early stopping
        - Data augmentation

Visualization:
                    │
       Training ────┼─────────────────────────────
          Error     │                           ╱
                    │                       ╱
                    │                   ╱
                    │              ╱ ←── Test Error
                    │          ╱
                    │     ╱
                    │ ╱
        Underfitting│        OPTIMAL      Overfitting
                    └──────────────────────────────→
                              Model Complexity
""")


# =============================================================================
# 4. NO FREE LUNCH THEOREM
# =============================================================================
print("\n" + "=" * 70)
print("4. NO FREE LUNCH THEOREM")
print("=" * 70)

print("""
No Free Lunch Theorem (Wolpert & Macready, 1997):

    "Averaged over ALL possible problems, every learning algorithm
     performs equally well."

Implication:
    - No universally best algorithm
    - Must match algorithm to problem
    - Domain knowledge matters!

In practice:
    - Some assumptions are always made
    - Algorithms that work well on "natural" problems
    - Neural networks have good inductive biases for many tasks
""")


# =============================================================================
# 5. VC DIMENSION
# =============================================================================
print("\n" + "=" * 70)
print("5. VC DIMENSION (Formal Capacity Measure)")
print("=" * 70)

print("""
VC Dimension = Maximum number of points a model can shatter.

"Shatter" = correctly classify all 2^n possible labelings of n points.

Examples:
    - Linear classifier in 2D: VC = 3 (can shatter 3 points, not 4)
    - Linear classifier in d-D: VC = d + 1
    - k-NN with k=1: VC = infinity
    - Neural network: Roughly O(# parameters)

Why it matters:
    - Gives theoretical bound on generalization error
    - Higher VC → more capacity → needs more data

Generalization bound (simplified):
    Test error ≤ Train error + O(√(VC/n))

    Where n = number of training samples
""")

# Demonstrate shattering with linear classifier
print("\n--- Linear Classifier Shattering Demo ---")

def can_shatter_2d(points, labels):
    """Check if points with labels can be linearly separated."""
    # Simple perceptron test
    X = np.array(points)
    y = np.array(labels) * 2 - 1  # Convert to {-1, +1}

    # Try to find separating hyperplane
    w = np.zeros(2)
    b = 0

    for _ in range(1000):
        for xi, yi in zip(X, y):
            if yi * (w @ xi + b) <= 0:
                w += 0.1 * yi * xi
                b += 0.1 * yi

    # Check if all points correctly classified
    correct = all(yi * (w @ xi + b) > 0 for xi, yi in zip(X, y))
    return correct


# 3 points: can shatter
points_3 = [[0, 0], [1, 0], [0, 1]]
print(f"\n3 points in 2D (should shatter all 8 labelings):")
can_shatter_all = True
for i in range(8):
    labels = [(i >> j) & 1 for j in range(3)]
    if not can_shatter_2d(points_3, labels):
        can_shatter_all = False
        break
print(f"  Result: {'Can shatter' if can_shatter_all else 'Cannot shatter'}")


# =============================================================================
# 6. REGULARIZATION EFFECT ON CAPACITY
# =============================================================================
print("\n" + "=" * 70)
print("6. REGULARIZATION EFFECT ON CAPACITY")
print("=" * 70)

print("""
Regularization constrains the model, reducing effective capacity.

    Loss = Data Loss + λ × Regularization Term

    λ = 0:   No regularization (full capacity)
    λ → ∞:  Heavy regularization (reduced capacity)

Effect on bias-variance:
    - Increases bias (simpler models)
    - Decreases variance (more stable)

Sweet spot: λ that minimizes validation error
""")


def fit_ridge(X, y, degree, alpha):
    """Fit polynomial with L2 regularization."""
    X_poly = np.column_stack([X ** d for d in range(degree + 1)])
    # Ridge regression: (X^T X + αI)^{-1} X^T y
    n_features = X_poly.shape[1]
    I = np.eye(n_features)
    I[0, 0] = 0  # Don't regularize bias
    coeffs = np.linalg.solve(X_poly.T @ X_poly + alpha * I, X_poly.T @ y)
    return coeffs


print("\nEffect of regularization on high-degree polynomial:")
print(f"{'Alpha':<12} {'Train MSE':<12} {'Test MSE':<12}")
print("-" * 36)

degree = 15
for alpha in [0, 0.001, 0.01, 0.1, 1, 10]:
    coeffs = fit_ridge(X_train_all[:30], y_train_all[:30], degree, alpha)
    train_pred = predict_polynomial(X_train_all[:30], coeffs)
    test_pred = predict_polynomial(X_test, coeffs)

    train_mse = np.mean((train_pred - y_train_all[:30]) ** 2)
    test_mse = np.mean((test_pred - y_test_true) ** 2)

    print(f"{alpha:<12} {train_mse:<12.4f} {test_mse:<12.4f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
Key Equations:
──────────────
    Expected Error = Bias² + Variance + Noise

    Test Error ≤ Train Error + O(√(VC/n))

Key Insights:
─────────────
1. Capacity = model's ability to fit functions
2. High capacity → low bias, high variance
3. Low capacity → high bias, low variance
4. Optimal: minimize test error, not training error
5. Regularization reduces effective capacity

Practical Guidelines:
────────────────────
• Start simple, increase complexity as needed
• Watch for gap between train and test error
• Use validation set to tune capacity/regularization
• More data → can use higher capacity models
• Regularization is your friend for complex models

Diagnosis Checklist:
───────────────────
┌────────────────────────────────────────────────────────────────────┐
│ Train Error │ Test Error │ Gap   │ Diagnosis       │ Action       │
├────────────────────────────────────────────────────────────────────┤
│ High        │ High       │ Small │ Underfitting    │ ↑ Capacity   │
│ Low         │ High       │ Large │ Overfitting     │ ↑ Regularize │
│ Low         │ Low        │ Small │ Good fit        │ Keep it!     │
└────────────────────────────────────────────────────────────────────┘
""")
