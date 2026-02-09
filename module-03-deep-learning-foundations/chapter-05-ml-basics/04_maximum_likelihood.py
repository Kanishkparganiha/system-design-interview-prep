"""
Chapter 5: Maximum Likelihood Estimation
========================================
The probabilistic foundation of learning.

Run: python 04_maximum_likelihood.py
"""

import numpy as np

print("=" * 70)
print("MAXIMUM LIKELIHOOD ESTIMATION (MLE)")
print("=" * 70)


# =============================================================================
# 1. WHAT IS MAXIMUM LIKELIHOOD?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHAT IS MAXIMUM LIKELIHOOD?")
print("=" * 70)

print("""
Maximum Likelihood Estimation (MLE):
    Find parameters that maximize the probability of observed data.

    θ_MLE = argmax_θ P(D|θ)
          = argmax_θ L(θ)      (L = likelihood function)
          = argmax_θ log L(θ)  (log-likelihood, more stable)

Intuition:
    "What parameters make our data most probable?"

Why it matters for Deep Learning:
    - Training = maximizing likelihood
    - Loss functions derived from likelihood
    - Foundation for understanding loss functions
""")


# =============================================================================
# 2. MLE FOR GAUSSIAN
# =============================================================================
print("\n" + "=" * 70)
print("2. MLE FOR GAUSSIAN DISTRIBUTION")
print("=" * 70)

print("""
Given data x₁, x₂, ..., xₙ from N(μ, σ²):

    L(μ, σ²) = ∏ᵢ (1/√(2πσ²)) exp(-(xᵢ-μ)²/(2σ²))

    log L = -n/2 log(2π) - n/2 log(σ²) - Σ(xᵢ-μ)²/(2σ²)

Setting derivatives to zero:
    ∂log L/∂μ = 0  →  μ_MLE = (1/n) Σxᵢ = sample mean
    ∂log L/∂σ² = 0  →  σ²_MLE = (1/n) Σ(xᵢ-μ)² = sample variance
""")

# Generate data from Gaussian
np.random.seed(42)
true_mu = 5.0
true_sigma = 2.0
data = np.random.normal(true_mu, true_sigma, 100)

# MLE estimates
mu_mle = np.mean(data)
sigma_mle = np.std(data)  # Note: numpy uses 1/n, which is MLE

print(f"True parameters: μ = {true_mu}, σ = {true_sigma}")
print(f"MLE estimates:   μ = {mu_mle:.3f}, σ = {sigma_mle:.3f}")


def gaussian_log_likelihood(data, mu, sigma):
    """Compute log-likelihood for Gaussian."""
    n = len(data)
    log_lik = -n/2 * np.log(2 * np.pi)
    log_lik -= n * np.log(sigma)
    log_lik -= np.sum((data - mu)**2) / (2 * sigma**2)
    return log_lik


print(f"\nLog-likelihood at MLE: {gaussian_log_likelihood(data, mu_mle, sigma_mle):.2f}")
print(f"Log-likelihood at true: {gaussian_log_likelihood(data, true_mu, true_sigma):.2f}")


# =============================================================================
# 3. MLE FOR BERNOULLI (BINARY CLASSIFICATION)
# =============================================================================
print("\n" + "=" * 70)
print("3. MLE FOR BERNOULLI → BINARY CROSS-ENTROPY")
print("=" * 70)

print("""
Given binary data y₁, y₂, ..., yₙ from Bernoulli(p):

    L(p) = ∏ᵢ p^(yᵢ) × (1-p)^(1-yᵢ)

    log L = Σᵢ [yᵢ log(p) + (1-yᵢ) log(1-p)]

MLE: p_MLE = (1/n) Σyᵢ = sample proportion

NEGATIVE log-likelihood:
    -log L = -Σᵢ [yᵢ log(p) + (1-yᵢ) log(1-p)]
           = Binary Cross-Entropy!

This is why we use BCE loss for binary classification!
""")


def binary_cross_entropy(y_true, y_pred, eps=1e-15):
    """Binary cross-entropy = negative log-likelihood for Bernoulli."""
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


# Example: Binary classification
y_true = np.array([1, 1, 0, 1, 0, 0, 1, 0, 1, 1])
y_pred_good = np.array([0.9, 0.8, 0.2, 0.7, 0.3, 0.1, 0.9, 0.2, 0.8, 0.7])
y_pred_bad = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

print(f"True labels:        {y_true}")
print(f"Good predictions:   {y_pred_good}")
print(f"Random predictions: {y_pred_bad}")
print(f"\nBCE (good):   {binary_cross_entropy(y_true, y_pred_good):.4f}")
print(f"BCE (random): {binary_cross_entropy(y_true, y_pred_bad):.4f}")


# =============================================================================
# 4. MLE FOR CATEGORICAL → CROSS-ENTROPY
# =============================================================================
print("\n" + "=" * 70)
print("4. MLE FOR CATEGORICAL → CROSS-ENTROPY")
print("=" * 70)

print("""
Given one-hot encoded labels and softmax predictions:

    y_true = [0, 1, 0]  (one-hot, class 1)
    y_pred = [0.1, 0.7, 0.2]  (softmax output)

Negative log-likelihood:
    -log L = -Σ y_true_k × log(y_pred_k)
           = -log(y_pred for correct class)
           = Categorical Cross-Entropy!
""")


def categorical_cross_entropy(y_true, y_pred, eps=1e-15):
    """Categorical cross-entropy = negative log-likelihood for Categorical."""
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true * np.log(y_pred), axis=-1).mean()


# Example: Multi-class classification
y_true_onehot = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
y_pred_good = np.array([[0.9, 0.05, 0.05], [0.1, 0.8, 0.1], [0.05, 0.1, 0.85]])
y_pred_uniform = np.array([[0.33, 0.33, 0.34], [0.33, 0.33, 0.34], [0.33, 0.33, 0.34]])

print(f"CCE (good predictions):   {categorical_cross_entropy(y_true_onehot, y_pred_good):.4f}")
print(f"CCE (uniform predictions): {categorical_cross_entropy(y_true_onehot, y_pred_uniform):.4f}")
print(f"\nMinimum possible CCE (perfect): 0.0")


# =============================================================================
# 5. MLE FOR REGRESSION → MSE
# =============================================================================
print("\n" + "=" * 70)
print("5. MLE FOR REGRESSION → MSE LOSS")
print("=" * 70)

print("""
Assume: y = f(x) + ε, where ε ~ N(0, σ²)

Given predictions ŷ and true values y:

    P(y|x) = N(y; ŷ, σ²)

    log L = -n/2 log(2π) - n log(σ) - Σ(yᵢ-ŷᵢ)²/(2σ²)

Maximizing log L w.r.t. ŷ:
    argmax_ŷ log L = argmax_ŷ -Σ(yᵢ-ŷᵢ)²
                   = argmin_ŷ Σ(yᵢ-ŷᵢ)²
                   = argmin_ŷ MSE!

So minimizing MSE = MLE under Gaussian noise assumption!
""")


def mse_loss(y_true, y_pred):
    """Mean Squared Error = derived from Gaussian MLE."""
    return np.mean((y_true - y_pred) ** 2)


# Example: Regression
y_true_reg = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y_pred_good = np.array([1.1, 1.9, 3.1, 4.0, 5.2])
y_pred_bad = np.array([2.0, 2.5, 2.5, 3.0, 3.5])

print(f"MSE (good predictions): {mse_loss(y_true_reg, y_pred_good):.4f}")
print(f"MSE (poor predictions): {mse_loss(y_true_reg, y_pred_bad):.4f}")


# =============================================================================
# 6. MAP VS MLE (REGULARIZATION CONNECTION)
# =============================================================================
print("\n" + "=" * 70)
print("6. MAP VS MLE → REGULARIZATION")
print("=" * 70)

print("""
Maximum A Posteriori (MAP) includes a prior:

    θ_MAP = argmax_θ P(θ|D) = argmax_θ P(D|θ) × P(θ)

Log form:
    θ_MAP = argmax_θ [log P(D|θ) + log P(θ)]

With Gaussian prior P(θ) = N(0, τ²):
    log P(θ) = -||θ||²/(2τ²) + const

    θ_MAP = argmax_θ [log P(D|θ) - λ||θ||²]
          = argmin_θ [-log P(D|θ) + λ||θ||²]
          = argmin_θ [Loss + L2 Regularization]

Connection:
    - MLE: No prior (just likelihood)
    - MAP with Gaussian prior = L2 regularization
    - MAP with Laplace prior = L1 regularization
""")


def ridge_mle_map(X, y, lambda_reg):
    """
    Compare MLE (OLS) vs MAP (Ridge) regression.
    """
    n, d = X.shape

    # MLE: (X^T X)^{-1} X^T y
    w_mle = np.linalg.solve(X.T @ X, X.T @ y)

    # MAP/Ridge: (X^T X + λI)^{-1} X^T y
    w_map = np.linalg.solve(X.T @ X + lambda_reg * np.eye(d), X.T @ y)

    return w_mle, w_map


# Example with collinear features (where regularization helps)
np.random.seed(42)
n_samples = 50
X = np.random.randn(n_samples, 10)
# Add collinearity
X[:, 5] = X[:, 0] + np.random.randn(n_samples) * 0.1
X[:, 6] = X[:, 1] + np.random.randn(n_samples) * 0.1

true_w = np.random.randn(10) * 0.5
y = X @ true_w + np.random.randn(n_samples) * 0.5

w_mle, w_map = ridge_mle_map(X, y, lambda_reg=1.0)

print(f"Weight norms:")
print(f"  True weights:  ||w|| = {np.linalg.norm(true_w):.4f}")
print(f"  MLE weights:   ||w|| = {np.linalg.norm(w_mle):.4f}")
print(f"  MAP weights:   ||w|| = {np.linalg.norm(w_map):.4f}")

# Test error
X_test = np.random.randn(100, 10)
X_test[:, 5] = X_test[:, 0] + np.random.randn(100) * 0.1
X_test[:, 6] = X_test[:, 1] + np.random.randn(100) * 0.1
y_test = X_test @ true_w + np.random.randn(100) * 0.5

print(f"\nTest MSE:")
print(f"  MLE: {np.mean((X_test @ w_mle - y_test)**2):.4f}")
print(f"  MAP: {np.mean((X_test @ w_map - y_test)**2):.4f}")


# =============================================================================
# 7. LOSS FUNCTIONS SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("7. LOSS FUNCTIONS FROM LIKELIHOOD")
print("=" * 70)

print("""
┌──────────────────────────────────────────────────────────────────────┐
│ Assumption                    │ Negative Log-Likelihood = Loss      │
├──────────────────────────────────────────────────────────────────────┤
│ y|x ~ Bernoulli(σ(f(x)))     │ Binary Cross-Entropy               │
│ y|x ~ Categorical(softmax)   │ Categorical Cross-Entropy          │
│ y|x ~ N(f(x), σ²)            │ Mean Squared Error                  │
│ y|x ~ Laplace(f(x), b)       │ Mean Absolute Error (L1)            │
│ + Gaussian prior on θ         │ + L2 Regularization                 │
│ + Laplace prior on θ          │ + L1 Regularization                 │
└──────────────────────────────────────────────────────────────────────┘

The choice of loss function = assumption about data distribution!
""")


# =============================================================================
# 8. MLE IN NEURAL NETWORKS
# =============================================================================
print("\n" + "=" * 70)
print("8. MLE IN NEURAL NETWORKS")
print("=" * 70)

print("""
Neural network training = MLE (or MAP with regularization)

Classification:
    - Softmax output = P(y|x; θ)
    - Cross-entropy loss = -log P(y|x; θ)
    - Minimize loss = Maximize likelihood

Regression:
    - Network output = μ = f(x; θ)
    - Assume y ~ N(μ, σ²)
    - MSE loss = -log P(y|x; θ) (up to constants)

With regularization:
    Loss = -log P(D|θ) + λR(θ)
         = NLL + regularization
         = Negative log posterior (up to constant)
         = MAP estimation!

SGD minimizing this loss = finding θ that maximizes P(θ|D)
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: MAXIMUM LIKELIHOOD")
print("=" * 70)

print("""
Key Concepts:
─────────────
1. MLE finds parameters that maximize P(data|parameters)
2. Minimizing negative log-likelihood = MLE
3. Common loss functions are negative log-likelihoods
4. Adding priors → MAP → regularization

Loss Function Derivations:
─────────────────────────
• Binary CE ← Bernoulli assumption
• Categorical CE ← Categorical assumption
• MSE ← Gaussian noise assumption
• MAE ← Laplace noise assumption
• L2 reg ← Gaussian prior on weights
• L1 reg ← Laplace prior on weights

Practical Implications:
──────────────────────
• Understand what your loss function assumes
• Match loss to your problem's characteristics
• Heavy-tailed noise → robust losses (MAE, Huber)
• Outliers → consider different distributions
• Class imbalance → weighted likelihood

Formula Summary:
───────────────
θ_MLE = argmax_θ P(D|θ) = argmin_θ Loss(D, θ)
θ_MAP = argmax_θ P(D|θ)P(θ) = argmin_θ [Loss(D, θ) + λ·Reg(θ)]
""")
