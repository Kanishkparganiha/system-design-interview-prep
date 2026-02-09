"""
Chapter 3: Bayes' Theorem
=========================
The foundation of probabilistic reasoning.

Run: python 04_bayes_theorem.py
"""

import numpy as np

print("=" * 70)
print("BAYES' THEOREM")
print("=" * 70)


# =============================================================================
# 1. BAYES' THEOREM BASICS
# =============================================================================
print("\n" + "=" * 70)
print("1. BAYES' THEOREM")
print("=" * 70)

print("""
Bayes' Theorem relates conditional probabilities:

    P(A|B) = P(B|A) × P(A) / P(B)

In ML notation:

    P(θ|D) = P(D|θ) × P(θ) / P(D)

Where:
    θ = parameters (what we want to learn)
    D = data (what we observe)

    P(θ)      = Prior (what we believe before seeing data)
    P(D|θ)    = Likelihood (probability of data given parameters)
    P(θ|D)    = Posterior (updated belief after seeing data)
    P(D)      = Evidence (normalizing constant)
""")


# =============================================================================
# 2. CLASSIC EXAMPLE: MEDICAL DIAGNOSIS
# =============================================================================
print("\n" + "=" * 70)
print("2. CLASSIC EXAMPLE: MEDICAL DIAGNOSIS")
print("=" * 70)

print("""
A disease affects 1% of the population.
A test detects the disease with 99% accuracy (true positive rate).
The test has 5% false positive rate.

Question: If you test positive, what's the probability you have the disease?
""")

# Given probabilities
P_disease = 0.01          # Prior: P(D)
P_no_disease = 0.99       # P(not D)
P_pos_given_disease = 0.99     # Sensitivity: P(+|D)
P_pos_given_no_disease = 0.05  # False positive: P(+|not D)

# Calculate P(+) using law of total probability
P_positive = (P_pos_given_disease * P_disease +
              P_pos_given_no_disease * P_no_disease)

# Apply Bayes' theorem
P_disease_given_pos = (P_pos_given_disease * P_disease) / P_positive

print(f"Given:")
print(f"  P(Disease) = {P_disease}")
print(f"  P(+|Disease) = {P_pos_given_disease}")
print(f"  P(+|No Disease) = {P_pos_given_no_disease}")
print(f"\nCalculations:")
print(f"  P(+) = {P_positive:.4f}")
print(f"\nResult:")
print(f"  P(Disease|+) = {P_disease_given_pos:.4f} ({P_disease_given_pos*100:.1f}%)")

print("""
Surprising! Despite 99% test accuracy, a positive test only gives ~17%
probability of having the disease.

Why? The prior P(Disease) = 1% is very low, so false positives dominate.
This is why we need to update beliefs using Bayes' theorem!
""")


# =============================================================================
# 3. BAYESIAN INFERENCE FOR COIN FLIP
# =============================================================================
print("\n" + "=" * 70)
print("3. BAYESIAN INFERENCE: LEARNING COIN BIAS")
print("=" * 70)

print("""
We flip a coin and want to estimate its bias θ (probability of heads).

Prior: θ ~ Beta(α, β)
Likelihood: X ~ Bernoulli(θ)
Posterior: θ|X ~ Beta(α + heads, β + tails)

The Beta distribution is "conjugate" to Bernoulli:
    - Posterior is same family as prior
    - Easy to update!
""")


class BetaDistribution:
    """Beta distribution for Bayesian inference."""

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def pdf(self, theta):
        """Probability density (unnormalized for simplicity)."""
        return (theta ** (self.alpha - 1)) * ((1 - theta) ** (self.beta - 1))

    @property
    def mean(self):
        return self.alpha / (self.alpha + self.beta)

    @property
    def mode(self):
        if self.alpha > 1 and self.beta > 1:
            return (self.alpha - 1) / (self.alpha + self.beta - 2)
        return None

    def update(self, heads, tails):
        """Update posterior after observing data."""
        return BetaDistribution(self.alpha + heads, self.beta + tails)


# Start with uniform prior (no prior belief)
prior = BetaDistribution(alpha=1, beta=1)
print(f"Prior: Beta(1, 1) - uniform, no prior belief")
print(f"  Mean: {prior.mean:.3f}")

# Simulate flipping a biased coin (true bias = 0.7)
np.random.seed(42)
true_bias = 0.7
n_flips = 100
flips = np.random.random(n_flips) < true_bias

# Update belief sequentially
posterior = prior
update_points = [0, 1, 5, 10, 25, 50, 100]
print(f"\nUpdating beliefs as we see more data (true bias = {true_bias}):")

current_heads = 0
current_tails = 0
for i, flip in enumerate(flips):
    if flip:
        current_heads += 1
    else:
        current_tails += 1

    if i + 1 in update_points:
        posterior = prior.update(current_heads, current_tails)
        print(f"  After {i+1:3d} flips: {current_heads} heads, "
              f"posterior mean = {posterior.mean:.3f}")


# =============================================================================
# 4. MAXIMUM A POSTERIORI (MAP) ESTIMATION
# =============================================================================
print("\n" + "=" * 70)
print("4. MAXIMUM A POSTERIORI (MAP)")
print("=" * 70)

print("""
MAP finds the most probable parameters given the data:

    θ_MAP = argmax_θ P(θ|D)
          = argmax_θ P(D|θ) × P(θ)
          = argmax_θ [log P(D|θ) + log P(θ)]

Compare to Maximum Likelihood Estimation (MLE):
    θ_MLE = argmax_θ P(D|θ)

The difference:
    - MLE ignores prior (only looks at data)
    - MAP includes prior (regularization!)

Connection to regularization:
    - Gaussian prior N(0, σ²) → L2 regularization
    - Laplace prior → L1 regularization
""")

# Example: Linear regression with Gaussian prior = Ridge regression
print("\n--- MAP = Regularized MLE ---")
print("""
Linear regression:
    y = Xw + ε, where ε ~ N(0, σ²)

MLE: minimize ||y - Xw||²
     → Ordinary least squares

MAP with w ~ N(0, τ²I):
    minimize ||y - Xw||² + (σ²/τ²)||w||²
    → Ridge regression!

The prior strength (1/τ²) becomes the regularization parameter λ.
""")


# =============================================================================
# 5. BAYESIAN VS FREQUENTIST
# =============================================================================
print("\n" + "=" * 70)
print("5. BAYESIAN VS FREQUENTIST")
print("=" * 70)

print("""
Two philosophical approaches to probability:

FREQUENTIST:
    - Probability = long-run frequency
    - Parameters are fixed (unknown) constants
    - Data is random
    - Point estimates (MLE)
    - Confidence intervals

BAYESIAN:
    - Probability = degree of belief
    - Parameters have probability distributions
    - Data is fixed (once observed)
    - Full posterior distribution
    - Credible intervals

In Deep Learning:
    - Most training is frequentist (SGD on likelihood)
    - Bayesian methods: uncertainty estimation, regularization
    - Dropout ≈ approximate Bayesian inference
""")


# =============================================================================
# 6. NAIVE BAYES CLASSIFIER
# =============================================================================
print("\n" + "=" * 70)
print("6. NAIVE BAYES CLASSIFIER")
print("=" * 70)

print("""
Applies Bayes' theorem with "naive" independence assumption:

    P(y|x₁,...,xₙ) ∝ P(y) × ∏ᵢ P(xᵢ|y)

Despite the strong assumption, works surprisingly well for:
    - Text classification (spam detection)
    - Sentiment analysis
    - When features are actually somewhat independent
""")


class NaiveBayes:
    """Simple Gaussian Naive Bayes classifier."""

    def fit(self, X, y):
        self.classes = np.unique(y)
        self.n_features = X.shape[1]

        # Compute class priors
        self.priors = {}
        self.means = {}
        self.vars = {}

        for c in self.classes:
            X_c = X[y == c]
            self.priors[c] = len(X_c) / len(X)
            self.means[c] = X_c.mean(axis=0)
            self.vars[c] = X_c.var(axis=0) + 1e-9  # Add small value for stability

        return self

    def _log_likelihood(self, x, c):
        """Log P(x|c) assuming Gaussian."""
        mean = self.means[c]
        var = self.vars[c]
        log_prob = -0.5 * np.sum(np.log(2 * np.pi * var))
        log_prob -= 0.5 * np.sum(((x - mean) ** 2) / var)
        return log_prob

    def predict_proba(self, X):
        """Compute posterior probabilities."""
        log_probs = np.zeros((len(X), len(self.classes)))

        for i, c in enumerate(self.classes):
            log_prior = np.log(self.priors[c])
            for j, x in enumerate(X):
                log_probs[j, i] = log_prior + self._log_likelihood(x, c)

        # Convert to probabilities (softmax)
        log_probs -= log_probs.max(axis=1, keepdims=True)
        probs = np.exp(log_probs)
        return probs / probs.sum(axis=1, keepdims=True)

    def predict(self, X):
        probs = self.predict_proba(X)
        return self.classes[probs.argmax(axis=1)]


# Demo on synthetic data
np.random.seed(42)
# Class 0: centered at (0, 0)
X0 = np.random.randn(50, 2) + [0, 0]
# Class 1: centered at (3, 3)
X1 = np.random.randn(50, 2) + [3, 3]

X_train = np.vstack([X0, X1])
y_train = np.array([0] * 50 + [1] * 50)

nb = NaiveBayes()
nb.fit(X_train, y_train)

# Test predictions
X_test = np.array([[0, 0], [3, 3], [1.5, 1.5]])
probs = nb.predict_proba(X_test)
preds = nb.predict(X_test)

print("Naive Bayes Classification:")
print(f"\nTest points and predictions:")
for i, (x, p, pred) in enumerate(zip(X_test, probs, preds)):
    print(f"  x={x} → P(class)={p.round(3)} → predicted class {pred}")


# =============================================================================
# 7. BAYESIAN NEURAL NETWORKS (CONCEPT)
# =============================================================================
print("\n" + "=" * 70)
print("7. BAYESIAN NEURAL NETWORKS (CONCEPT)")
print("=" * 70)

print("""
Instead of point estimates for weights, maintain distributions:

    w ~ P(w|D)  (posterior distribution over weights)

Benefits:
    1. Uncertainty quantification ("I don't know")
    2. Better generalization (implicit regularization)
    3. Automatic Occam's razor

Challenges:
    - Intractable posterior (high-dimensional)
    - Approximations needed (variational inference, MCMC)

Practical approximations:
    - Dropout at test time ≈ Monte Carlo sampling
    - Ensemble of networks
    - Variational inference (learn approximate posterior)
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: BAYES' THEOREM")
print("=" * 70)

print("""
Core Formula:
─────────────
    P(θ|D) = P(D|θ) × P(θ) / P(D)

    Posterior ∝ Likelihood × Prior

Key Concepts:
─────────────
1. Prior: Initial belief before data
2. Likelihood: How well parameters explain data
3. Posterior: Updated belief after data
4. Evidence: Normalizing constant (often intractable)

ML Connections:
───────────────
• MLE = MAP with uniform prior
• L2 regularization = Gaussian prior
• L1 regularization = Laplace prior
• Dropout ≈ Bayesian approximation

When to Use Bayesian Methods:
────────────────────────────
• Small datasets (prior helps)
• Need uncertainty estimates
• Want to incorporate domain knowledge
• Avoiding overfitting

When to Use Frequentist/MLE:
───────────────────────────
• Large datasets (prior washes out)
• Computational efficiency important
• Simple point estimates sufficient
""")
