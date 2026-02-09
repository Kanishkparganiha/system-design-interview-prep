"""
Chapter 3.1: Probability Basics
===============================
The mathematical language of uncertainty.

Run: python 01_probability_basics.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("PROBABILITY BASICS")
print("=" * 70)


# =============================================================================
# RANDOM VARIABLES
# =============================================================================
print("\n" + "=" * 70)
print("1. RANDOM VARIABLES")
print("=" * 70)

print("""
A random variable is a variable whose value is determined by chance.

Discrete: Takes countable values (e.g., dice roll: 1,2,3,4,5,6)
Continuous: Takes any value in a range (e.g., temperature: 20.5°C)

In Deep Learning:
    - Input X: random sample from data distribution
    - Output Y: predicted class (discrete) or value (continuous)
    - Weights W: can be treated as random in Bayesian DL
""")

# Simulating a discrete random variable (dice roll)
np.random.seed(42)
dice_rolls = np.random.randint(1, 7, size=10000)

print("\nSimulating 10,000 dice rolls:")
for i in range(1, 7):
    count = np.sum(dice_rolls == i)
    print(f"  P(X = {i}) ≈ {count/10000:.4f}  (theory: 0.1667)")


# =============================================================================
# PROBABILITY MASS FUNCTION (PMF) - DISCRETE
# =============================================================================
print("\n" + "=" * 70)
print("2. PROBABILITY MASS FUNCTION (PMF)")
print("=" * 70)

print("""
For discrete random variables, PMF gives P(X = x).

Properties:
    1. P(X = x) ≥ 0 for all x
    2. Σ P(X = x) = 1

Example: Biased coin (70% heads)
""")

# Biased coin
p_heads = 0.7
p_tails = 0.3

print(f"\nBiased coin PMF:")
print(f"  P(X = Heads) = {p_heads}")
print(f"  P(X = Tails) = {p_tails}")
print(f"  Sum = {p_heads + p_tails}")

# Simulate
flips = np.random.choice(['H', 'T'], size=10000, p=[p_heads, p_tails])
print(f"\nSimulation (10,000 flips):")
print(f"  Heads: {np.sum(flips == 'H') / 10000:.4f}")
print(f"  Tails: {np.sum(flips == 'T') / 10000:.4f}")


# =============================================================================
# PROBABILITY DENSITY FUNCTION (PDF) - CONTINUOUS
# =============================================================================
print("\n" + "=" * 70)
print("3. PROBABILITY DENSITY FUNCTION (PDF)")
print("=" * 70)

print("""
For continuous random variables, PDF gives density p(x).

Note: P(X = x) = 0 for continuous variables!
Instead: P(a ≤ X ≤ b) = ∫ₐᵇ p(x) dx

Properties:
    1. p(x) ≥ 0 for all x
    2. ∫ p(x) dx = 1

Example: Gaussian (Normal) Distribution
""")

# Gaussian PDF
def gaussian_pdf(x, mu=0, sigma=1):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

x = np.linspace(-4, 4, 1000)
pdf_values = gaussian_pdf(x, mu=0, sigma=1)

print(f"\nGaussian(μ=0, σ=1):")
print(f"  p(0) = {gaussian_pdf(0):.4f}")
print(f"  p(1) = {gaussian_pdf(1):.4f}")
print(f"  p(2) = {gaussian_pdf(2):.4f}")
print(f"  ∫ p(x) dx ≈ {np.trapz(pdf_values, x):.6f} (should be 1)")


# =============================================================================
# EXPECTATION (MEAN)
# =============================================================================
print("\n" + "=" * 70)
print("4. EXPECTATION (MEAN)")
print("=" * 70)

print("""
Expected value = "average" outcome weighted by probability.

Discrete:   E[X] = Σ x · P(X = x)
Continuous: E[X] = ∫ x · p(x) dx

Properties:
    E[aX + b] = a·E[X] + b
    E[X + Y] = E[X] + E[Y]  (always true!)
    E[XY] = E[X]·E[Y]       (only if independent)
""")

# Discrete example: Expected value of dice roll
outcomes = np.array([1, 2, 3, 4, 5, 6])
probabilities = np.array([1/6] * 6)
expected_value = np.sum(outcomes * probabilities)

print(f"\nFair dice:")
print(f"  E[X] = (1+2+3+4+5+6)/6 = {expected_value:.2f}")
print(f"  Simulation mean: {np.mean(dice_rolls):.4f}")

# Continuous example: Gaussian
samples = np.random.normal(loc=5, scale=2, size=10000)
print(f"\nGaussian(μ=5, σ=2):")
print(f"  Theory E[X] = 5")
print(f"  Sample mean: {np.mean(samples):.4f}")


# =============================================================================
# VARIANCE AND STANDARD DEVIATION
# =============================================================================
print("\n" + "=" * 70)
print("5. VARIANCE AND STANDARD DEVIATION")
print("=" * 70)

print("""
Variance measures spread around the mean.

Var[X] = E[(X - E[X])²] = E[X²] - E[X]²

Standard deviation: σ = √Var[X]

Properties:
    Var[aX + b] = a²·Var[X]
    Var[X + Y] = Var[X] + Var[Y]  (if independent)
""")

# Dice variance
E_X = expected_value
E_X2 = np.sum(outcomes**2 * probabilities)
variance = E_X2 - E_X**2

print(f"\nFair dice:")
print(f"  E[X²] = {E_X2:.4f}")
print(f"  Var[X] = E[X²] - E[X]² = {E_X2:.4f} - {E_X**2:.4f} = {variance:.4f}")
print(f"  σ = √Var[X] = {np.sqrt(variance):.4f}")
print(f"  Sample variance: {np.var(dice_rolls):.4f}")

# Gaussian
print(f"\nGaussian(μ=5, σ=2):")
print(f"  Theory Var[X] = σ² = 4")
print(f"  Sample variance: {np.var(samples):.4f}")


# =============================================================================
# JOINT AND CONDITIONAL PROBABILITY
# =============================================================================
print("\n" + "=" * 70)
print("6. JOINT AND CONDITIONAL PROBABILITY")
print("=" * 70)

print("""
Joint probability: P(X=x, Y=y) = probability of both events

Conditional probability: P(Y=y | X=x) = probability of Y given X
    P(Y|X) = P(X,Y) / P(X)

Marginalization: P(X) = Σᵧ P(X, Y=y)

Chain rule: P(X,Y) = P(Y|X) · P(X)
""")

# Example: Weather and umbrella
# P(Rain) = 0.3, P(Umbrella | Rain) = 0.9, P(Umbrella | No Rain) = 0.2

p_rain = 0.3
p_no_rain = 0.7
p_umbrella_given_rain = 0.9
p_umbrella_given_no_rain = 0.2

# Joint probabilities
p_rain_and_umbrella = p_umbrella_given_rain * p_rain
p_rain_and_no_umbrella = (1 - p_umbrella_given_rain) * p_rain
p_no_rain_and_umbrella = p_umbrella_given_no_rain * p_no_rain
p_no_rain_and_no_umbrella = (1 - p_umbrella_given_no_rain) * p_no_rain

print("\nJoint probability table:")
print("                    Umbrella    No Umbrella")
print(f"  Rain              {p_rain_and_umbrella:.3f}       {p_rain_and_no_umbrella:.3f}")
print(f"  No Rain           {p_no_rain_and_umbrella:.3f}       {p_no_rain_and_no_umbrella:.3f}")

# Marginal: P(Umbrella)
p_umbrella = p_rain_and_umbrella + p_no_rain_and_umbrella
print(f"\nMarginal P(Umbrella) = {p_umbrella:.3f}")


# =============================================================================
# INDEPENDENCE
# =============================================================================
print("\n" + "=" * 70)
print("7. INDEPENDENCE")
print("=" * 70)

print("""
X and Y are independent if:
    P(X, Y) = P(X) · P(Y)

Equivalently:
    P(Y | X) = P(Y)  (knowing X doesn't change Y)

Conditional independence: X ⊥ Y | Z
    P(X, Y | Z) = P(X | Z) · P(Y | Z)

In neural networks:
    - IID assumption: samples are independent & identically distributed
    - Dropout: randomly independent zeroing of neurons
""")

# Simulation: Are two dice independent?
np.random.seed(42)
n = 10000
die1 = np.random.randint(1, 7, n)
die2 = np.random.randint(1, 7, n)

# Check: P(die1=1, die2=1) ≈ P(die1=1) × P(die2=1)
p_1_1 = np.mean((die1 == 1) & (die2 == 1))
p_1 = np.mean(die1 == 1)
p_1_b = np.mean(die2 == 1)

print(f"\nTwo dice (should be independent):")
print(f"  P(die1=1, die2=1) = {p_1_1:.4f}")
print(f"  P(die1=1) × P(die2=1) = {p_1 * p_1_b:.4f}")
print(f"  Independent? {np.isclose(p_1_1, p_1 * p_1_b, atol=0.01)}")


# =============================================================================
# COVARIANCE AND CORRELATION
# =============================================================================
print("\n" + "=" * 70)
print("8. COVARIANCE AND CORRELATION")
print("=" * 70)

print("""
Covariance measures how two variables vary together:
    Cov(X, Y) = E[(X - E[X])(Y - E[Y])] = E[XY] - E[X]E[Y]

Correlation (normalized covariance):
    ρ(X, Y) = Cov(X, Y) / (σ_X · σ_Y)

Range: ρ ∈ [-1, 1]
    ρ = 1:  Perfect positive correlation
    ρ = 0:  Uncorrelated (but not necessarily independent!)
    ρ = -1: Perfect negative correlation
""")

# Generate correlated data
np.random.seed(42)
n = 1000

# Uncorrelated
X_uncorr = np.random.randn(n)
Y_uncorr = np.random.randn(n)

# Correlated
X_corr = np.random.randn(n)
Y_corr = 0.8 * X_corr + 0.6 * np.random.randn(n)

print(f"\nUncorrelated variables:")
print(f"  Covariance: {np.cov(X_uncorr, Y_uncorr)[0,1]:.4f}")
print(f"  Correlation: {np.corrcoef(X_uncorr, Y_uncorr)[0,1]:.4f}")

print(f"\nCorrelated variables:")
print(f"  Covariance: {np.cov(X_corr, Y_corr)[0,1]:.4f}")
print(f"  Correlation: {np.corrcoef(X_corr, Y_corr)[0,1]:.4f}")


# =============================================================================
# DEEP LEARNING CONNECTION
# =============================================================================
print("\n" + "=" * 70)
print("9. CONNECTION TO DEEP LEARNING")
print("=" * 70)

print("""
┌────────────────────────────────────────────────────────────────────────┐
│  Probability Concept    │  Deep Learning Application                  │
├────────────────────────────────────────────────────────────────────────┤
│  P(Y|X)                 │  What neural networks model!                │
│  Softmax output         │  Categorical distribution over classes      │
│  Sigmoid output         │  Bernoulli parameter for binary class       │
│  MSE Loss               │  Assumes Gaussian noise                     │
│  Cross-entropy Loss     │  -log P(correct class)                      │
│  Dropout                │  Bernoulli mask on neurons                  │
│  Batch mean/var         │  Sample statistics for normalization        │
│  VAE                    │  Models P(X|Z) and Q(Z|X)                   │
└────────────────────────────────────────────────────────────────────────┘
""")

# Example: Softmax as probability distribution
def softmax(logits):
    exp_logits = np.exp(logits - np.max(logits))  # Subtract max for stability
    return exp_logits / np.sum(exp_logits)

logits = np.array([2.0, 1.0, 0.1])
probs = softmax(logits)

print("\nSoftmax example:")
print(f"  Logits: {logits}")
print(f"  Probabilities: {probs}")
print(f"  Sum: {np.sum(probs):.6f} (should be 1)")
print(f"  All ≥ 0: {np.all(probs >= 0)}")
print("\n→ Softmax outputs a valid probability distribution!")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
Key Formulas:
─────────────
E[X] = Σ x·P(x)                    Expectation
Var[X] = E[X²] - E[X]²              Variance
P(Y|X) = P(X,Y) / P(X)              Conditional probability
P(X,Y) = P(X) · P(Y)                Independence condition
Cov(X,Y) = E[XY] - E[X]E[Y]         Covariance
ρ(X,Y) = Cov(X,Y) / (σ_X · σ_Y)    Correlation

Why It Matters for DL:
──────────────────────
• Neural networks learn P(Y|X)
• Loss functions are probabilistic (-log likelihood)
• Regularization has Bayesian interpretation
• Generative models explicitly model P(X)
""")
