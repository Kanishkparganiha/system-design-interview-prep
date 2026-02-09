"""
Chapter 3: Common Probability Distributions
===========================================
Distributions you'll encounter in deep learning.

Run: python 03_common_distributions.py
"""

import numpy as np

print("=" * 70)
print("COMMON PROBABILITY DISTRIBUTIONS")
print("=" * 70)


# =============================================================================
# 1. BERNOULLI DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("1. BERNOULLI DISTRIBUTION")
print("=" * 70)

print("""
Single binary outcome (coin flip).

    X ∈ {0, 1}
    P(X=1) = p
    P(X=0) = 1-p

    E[X] = p
    Var[X] = p(1-p)

ML Uses:
    - Binary classification output
    - Dropout (each neuron on/off)
    - Binary cross-entropy loss
""")


class Bernoulli:
    def __init__(self, p):
        self.p = p

    def pmf(self, x):
        """Probability mass function."""
        return self.p if x == 1 else (1 - self.p)

    def sample(self, n=1):
        """Generate samples."""
        return (np.random.random(n) < self.p).astype(int)

    @property
    def mean(self):
        return self.p

    @property
    def variance(self):
        return self.p * (1 - self.p)


# Demo
bern = Bernoulli(p=0.7)
samples = bern.sample(1000)

print(f"Bernoulli(p=0.7)")
print(f"  P(X=1) = {bern.pmf(1)}")
print(f"  P(X=0) = {bern.pmf(0)}")
print(f"  E[X] = {bern.mean}")
print(f"  Var[X] = {bern.variance}")
print(f"\n  Sample mean: {samples.mean():.3f}")
print(f"  Sample variance: {samples.var():.3f}")


# =============================================================================
# 2. CATEGORICAL DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("2. CATEGORICAL (MULTINOMIAL) DISTRIBUTION")
print("=" * 70)

print("""
Multiple discrete outcomes (dice roll).

    X ∈ {1, 2, ..., K}
    P(X=k) = p_k where Σp_k = 1

ML Uses:
    - Multi-class classification
    - Softmax output
    - Categorical cross-entropy loss
    - Word embeddings / vocabulary
""")


class Categorical:
    def __init__(self, probs):
        self.probs = np.array(probs)
        assert np.isclose(self.probs.sum(), 1.0), "Probs must sum to 1"

    def pmf(self, x):
        """P(X=x)"""
        return self.probs[x]

    def sample(self, n=1):
        """Generate samples."""
        return np.random.choice(len(self.probs), size=n, p=self.probs)

    @property
    def mode(self):
        return np.argmax(self.probs)


# Demo
cat = Categorical([0.1, 0.2, 0.4, 0.3])  # 4-class
samples = cat.sample(1000)

print(f"Categorical with probs = [0.1, 0.2, 0.4, 0.3]")
print(f"  P(X=0) = {cat.pmf(0)}")
print(f"  P(X=2) = {cat.pmf(2)}")
print(f"  Mode = {cat.mode}")
print(f"\n  Sample distribution:")
for i in range(4):
    print(f"    Class {i}: {(samples == i).mean():.3f}")


# =============================================================================
# 3. GAUSSIAN (NORMAL) DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("3. GAUSSIAN (NORMAL) DISTRIBUTION")
print("=" * 70)

print("""
The most important continuous distribution.

    X ~ N(μ, σ²)

    PDF: p(x) = (1/√(2πσ²)) exp(-(x-μ)²/(2σ²))

    E[X] = μ
    Var[X] = σ²

ML Uses:
    - Weight initialization
    - VAE latent space (reparameterization trick)
    - Gaussian noise (data augmentation)
    - Regression output distribution
    - Maximum likelihood → MSE loss
""")


class Gaussian:
    def __init__(self, mu=0, sigma=1):
        self.mu = mu
        self.sigma = sigma

    def pdf(self, x):
        """Probability density function."""
        coef = 1 / (self.sigma * np.sqrt(2 * np.pi))
        exponent = -((x - self.mu) ** 2) / (2 * self.sigma ** 2)
        return coef * np.exp(exponent)

    def log_pdf(self, x):
        """Log PDF (more stable)."""
        return -0.5 * np.log(2 * np.pi) - np.log(self.sigma) - \
               ((x - self.mu) ** 2) / (2 * self.sigma ** 2)

    def sample(self, n=1):
        """Generate samples using reparameterization trick."""
        # x = μ + σ * ε where ε ~ N(0,1)
        epsilon = np.random.randn(n)
        return self.mu + self.sigma * epsilon

    @property
    def mean(self):
        return self.mu

    @property
    def variance(self):
        return self.sigma ** 2


# Demo
gauss = Gaussian(mu=5, sigma=2)
samples = gauss.sample(1000)

print(f"Gaussian(μ=5, σ=2)")
print(f"  PDF at x=5: {gauss.pdf(5):.4f}")
print(f"  PDF at x=0: {gauss.pdf(0):.4f}")
print(f"  E[X] = {gauss.mean}")
print(f"  Var[X] = {gauss.variance}")
print(f"\n  Sample mean: {samples.mean():.3f}")
print(f"  Sample std: {samples.std():.3f}")

# Reparameterization trick for VAE
print("\n--- Reparameterization Trick (VAE) ---")
print("""
Instead of sampling z ~ N(μ, σ²):
    z = μ + σ * ε, where ε ~ N(0,1)

This allows gradients to flow through μ and σ!
""")


# =============================================================================
# 4. MULTIVARIATE GAUSSIAN
# =============================================================================
print("\n" + "=" * 70)
print("4. MULTIVARIATE GAUSSIAN")
print("=" * 70)

print("""
Generalization to multiple dimensions.

    X ~ N(μ, Σ)

    μ = mean vector (d,)
    Σ = covariance matrix (d, d), must be positive semi-definite

    PDF: p(x) = (1/√((2π)^d |Σ|)) exp(-0.5(x-μ)ᵀΣ⁻¹(x-μ))

ML Uses:
    - Multivariate regression
    - Gaussian Mixture Models (GMM)
    - VAE latent space (multi-dimensional)
    - Batch normalization statistics
""")


class MultivariateGaussian:
    def __init__(self, mu, cov):
        self.mu = np.array(mu)
        self.cov = np.array(cov)
        self.d = len(mu)

        # Precompute for sampling
        self.L = np.linalg.cholesky(cov)

    def sample(self, n=1):
        """Sample using Cholesky decomposition."""
        # x = μ + L @ ε where ε ~ N(0, I)
        epsilon = np.random.randn(n, self.d)
        return self.mu + epsilon @ self.L.T

    def log_pdf(self, x):
        """Log probability density."""
        diff = x - self.mu
        inv_cov = np.linalg.inv(self.cov)
        det_cov = np.linalg.det(self.cov)

        log_norm = -0.5 * (self.d * np.log(2 * np.pi) + np.log(det_cov))
        log_exp = -0.5 * diff @ inv_cov @ diff

        return log_norm + log_exp


# Demo
mu_2d = [1, 2]
cov_2d = [[1, 0.5], [0.5, 1]]  # Correlated

mvg = MultivariateGaussian(mu_2d, cov_2d)
samples_2d = mvg.sample(1000)

print(f"Multivariate Gaussian:")
print(f"  μ = {mu_2d}")
print(f"  Σ = {cov_2d}")
print(f"\n  Sample mean: {samples_2d.mean(axis=0).round(3)}")
print(f"  Sample cov:\n{np.cov(samples_2d.T).round(3)}")


# =============================================================================
# 5. UNIFORM DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("5. UNIFORM DISTRIBUTION")
print("=" * 70)

print("""
Equal probability for all values in a range.

    X ~ Uniform(a, b)

    PDF: p(x) = 1/(b-a) for a ≤ x ≤ b, else 0
    E[X] = (a+b)/2
    Var[X] = (b-a)²/12

ML Uses:
    - Weight initialization (e.g., Xavier uniform)
    - Random sampling
    - Dropout masks
    - Data shuffling
""")


class Uniform:
    def __init__(self, a=0, b=1):
        self.a = a
        self.b = b

    def pdf(self, x):
        if self.a <= x <= self.b:
            return 1 / (self.b - self.a)
        return 0

    def sample(self, n=1):
        return np.random.uniform(self.a, self.b, n)

    @property
    def mean(self):
        return (self.a + self.b) / 2

    @property
    def variance(self):
        return (self.b - self.a) ** 2 / 12


# Demo
unif = Uniform(-1, 1)
samples = unif.sample(1000)

print(f"Uniform(-1, 1)")
print(f"  E[X] = {unif.mean}")
print(f"  Var[X] = {unif.variance:.4f}")
print(f"\n  Sample mean: {samples.mean():.3f}")
print(f"  Sample variance: {samples.var():.3f}")


# =============================================================================
# 6. EXPONENTIAL DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("6. EXPONENTIAL DISTRIBUTION")
print("=" * 70)

print("""
Time until an event occurs.

    X ~ Exp(λ)  (λ = rate parameter)

    PDF: p(x) = λ exp(-λx) for x ≥ 0
    E[X] = 1/λ
    Var[X] = 1/λ²

ML Uses:
    - Learning rate schedules (exponential decay)
    - Attention weights (softmax is exponential)
    - Modeling wait times
""")


class Exponential:
    def __init__(self, rate):
        self.rate = rate

    def pdf(self, x):
        if x >= 0:
            return self.rate * np.exp(-self.rate * x)
        return 0

    def sample(self, n=1):
        # Inverse transform sampling
        u = np.random.uniform(0, 1, n)
        return -np.log(u) / self.rate

    @property
    def mean(self):
        return 1 / self.rate


# Demo
exp = Exponential(rate=2)
samples = exp.sample(1000)

print(f"Exponential(λ=2)")
print(f"  E[X] = {exp.mean}")
print(f"  Sample mean: {samples.mean():.3f}")


# =============================================================================
# 7. SOFTMAX AS A DISTRIBUTION
# =============================================================================
print("\n" + "=" * 70)
print("7. SOFTMAX: TURNING LOGITS INTO PROBABILITIES")
print("=" * 70)

print("""
Softmax converts real numbers (logits) into a probability distribution.

    softmax(z)_i = exp(z_i) / Σ exp(z_j)

Properties:
    - Output in (0, 1)
    - Sum to 1
    - Temperature scaling: softmax(z/T)
        - T → 0: one-hot (argmax)
        - T → ∞: uniform

ML Uses:
    - Classification output layer
    - Attention weights
    - Gumbel-softmax (differentiable sampling)
""")


def softmax(z, temperature=1.0):
    """Numerically stable softmax with temperature."""
    z_scaled = z / temperature
    z_shifted = z_scaled - np.max(z_scaled)  # Stability trick
    exp_z = np.exp(z_shifted)
    return exp_z / exp_z.sum()


# Demo
logits = np.array([2.0, 1.0, 0.1])

print(f"Logits: {logits}")
print(f"\nSoftmax with different temperatures:")
for T in [0.5, 1.0, 2.0, 10.0]:
    probs = softmax(logits, T)
    print(f"  T={T:4.1f}: {probs.round(3)}")


# =============================================================================
# 8. SUMMARY TABLE
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: DISTRIBUTIONS IN DEEP LEARNING")
print("=" * 70)

print("""
┌─────────────────┬────────────────┬───────────────────────────────────────┐
│ Distribution    │ Support        │ ML Application                        │
├─────────────────┼────────────────┼───────────────────────────────────────┤
│ Bernoulli       │ {0, 1}         │ Binary classification, dropout        │
│ Categorical     │ {1,...,K}      │ Multi-class classification            │
│ Gaussian        │ ℝ              │ VAE latent, noise, regression         │
│ Multivariate G. │ ℝⁿ             │ GMM, multivariate modeling            │
│ Uniform         │ [a, b]         │ Initialization, sampling              │
│ Exponential     │ [0, ∞)         │ Learning rate decay, attention        │
└─────────────────┴────────────────┴───────────────────────────────────────┘

Key Connections:
────────────────
• Binary cross-entropy ← Bernoulli negative log likelihood
• Categorical cross-entropy ← Categorical negative log likelihood
• MSE loss ← Gaussian negative log likelihood
• Softmax output = Categorical distribution parameters

Sampling Tricks:
───────────────
• Reparameterization: z = μ + σε (enables backprop through sampling)
• Gumbel-softmax: differentiable categorical sampling
• Inverse transform: F⁻¹(U) where U ~ Uniform(0,1)
""")
