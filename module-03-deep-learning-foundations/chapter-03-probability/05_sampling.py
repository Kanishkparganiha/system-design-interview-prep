"""
Chapter 3: Sampling Methods
===========================
Generating samples from probability distributions.

Run: python 05_sampling.py
"""

import numpy as np

print("=" * 70)
print("SAMPLING METHODS")
print("=" * 70)


# =============================================================================
# 1. WHY SAMPLING?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHY DO WE NEED SAMPLING?")
print("=" * 70)

print("""
Many computations in ML require expectations:

    E[f(x)] = ∫ f(x) p(x) dx

This integral is often intractable. Solution: Monte Carlo approximation!

    E[f(x)] ≈ (1/N) Σ f(xᵢ)  where xᵢ ~ p(x)

Applications in Deep Learning:
    - Training VAEs (sampling from latent space)
    - Dropout (random sampling of neurons)
    - Data augmentation
    - Stochastic gradient descent (sampling batches)
    - Generative models (GANs, diffusion)
""")


# =============================================================================
# 2. INVERSE TRANSFORM SAMPLING
# =============================================================================
print("\n" + "=" * 70)
print("2. INVERSE TRANSFORM SAMPLING")
print("=" * 70)

print("""
If we can compute the inverse CDF (F⁻¹), we can sample:

    X = F⁻¹(U) where U ~ Uniform(0, 1)

Example: Exponential distribution
    CDF: F(x) = 1 - exp(-λx)
    Inverse: F⁻¹(u) = -ln(1-u)/λ
""")


def sample_exponential(rate, n):
    """Sample from Exponential(rate) using inverse transform."""
    u = np.random.uniform(0, 1, n)
    return -np.log(1 - u) / rate


# Demo
samples_exp = sample_exponential(rate=2, n=10000)
print(f"Exponential(λ=2) samples:")
print(f"  Theoretical mean: {1/2}")
print(f"  Sample mean: {samples_exp.mean():.4f}")


# Sampling from any discrete distribution
def sample_discrete(probs, n):
    """Sample from discrete distribution using inverse CDF."""
    cdf = np.cumsum(probs)
    u = np.random.uniform(0, 1, n)
    samples = np.searchsorted(cdf, u)
    return samples


probs = [0.1, 0.2, 0.4, 0.3]
samples_disc = sample_discrete(probs, 10000)

print(f"\nDiscrete distribution {probs}:")
print(f"  Sample frequencies: {[np.mean(samples_disc == i) for i in range(4)]}")


# =============================================================================
# 3. BOX-MULLER TRANSFORM
# =============================================================================
print("\n" + "=" * 70)
print("3. BOX-MULLER TRANSFORM (Sampling Gaussians)")
print("=" * 70)

print("""
Generate Gaussian samples from uniform samples:

    Given U₁, U₂ ~ Uniform(0, 1):
    Z₁ = √(-2 ln U₁) cos(2π U₂)
    Z₂ = √(-2 ln U₁) sin(2π U₂)

    Then Z₁, Z₂ ~ N(0, 1) and are independent!
""")


def box_muller(n):
    """Generate n standard normal samples using Box-Muller."""
    # Generate pairs
    n_pairs = (n + 1) // 2
    u1 = np.random.uniform(0, 1, n_pairs)
    u2 = np.random.uniform(0, 1, n_pairs)

    r = np.sqrt(-2 * np.log(u1))
    theta = 2 * np.pi * u2

    z1 = r * np.cos(theta)
    z2 = r * np.sin(theta)

    samples = np.concatenate([z1, z2])[:n]
    return samples


samples_bm = box_muller(10000)
print(f"Box-Muller N(0,1) samples:")
print(f"  Mean: {samples_bm.mean():.4f} (expected: 0)")
print(f"  Std:  {samples_bm.std():.4f} (expected: 1)")


# =============================================================================
# 4. REPARAMETERIZATION TRICK
# =============================================================================
print("\n" + "=" * 70)
print("4. REPARAMETERIZATION TRICK (Key for VAEs!)")
print("=" * 70)

print("""
Problem: We want to backpropagate through sampling!

    z ~ N(μ, σ²)  → How to compute ∂z/∂μ?

Solution: Reparameterize!

    ε ~ N(0, 1)           (sample from fixed distribution)
    z = μ + σ × ε         (deterministic transformation)

Now gradients flow through μ and σ!

    ∂z/∂μ = 1
    ∂z/∂σ = ε

This enables training VAEs with gradient descent.
""")


def reparameterize(mu, log_var, n_samples=1):
    """
    Sample z = μ + σ × ε using reparameterization.

    Args:
        mu: Mean (can be a vector)
        log_var: Log variance (for numerical stability)
        n_samples: Number of samples

    Returns:
        Samples from N(μ, σ²)
    """
    std = np.exp(0.5 * log_var)  # σ = exp(log_var/2)
    epsilon = np.random.randn(n_samples, *mu.shape)
    z = mu + std * epsilon
    return z


# Demo
mu = np.array([1.0, 2.0, 3.0])
log_var = np.array([0.0, 0.5, -0.5])  # Different variances

print(f"μ = {mu}")
print(f"σ = {np.exp(0.5 * log_var).round(3)}")

samples_reparam = reparameterize(mu, log_var, n_samples=5000)
print(f"\nSample statistics (5000 samples):")
print(f"  Mean:  {samples_reparam.mean(axis=0).round(3)}")
print(f"  Std:   {samples_reparam.std(axis=0).round(3)}")


# =============================================================================
# 5. REJECTION SAMPLING
# =============================================================================
print("\n" + "=" * 70)
print("5. REJECTION SAMPLING")
print("=" * 70)

print("""
Sample from complex distribution p(x) using simpler proposal q(x):

    1. Find M such that M × q(x) ≥ p(x) for all x
    2. Sample x ~ q(x)
    3. Sample u ~ Uniform(0, M × q(x))
    4. Accept if u ≤ p(x), otherwise reject

Works for any distribution where we can evaluate p(x) (up to constant).
""")


def rejection_sample(target_pdf, proposal_sample, proposal_pdf, M, n):
    """
    Rejection sampling.

    Args:
        target_pdf: Function p(x) to sample from
        proposal_sample: Function to sample from q
        proposal_pdf: Function q(x)
        M: Constant such that M*q(x) >= p(x)
        n: Number of samples needed
    """
    samples = []
    total_proposed = 0

    while len(samples) < n:
        x = proposal_sample()
        u = np.random.uniform(0, M * proposal_pdf(x))
        total_proposed += 1

        if u <= target_pdf(x):
            samples.append(x)

    acceptance_rate = n / total_proposed
    return np.array(samples), acceptance_rate


# Example: Sample from truncated Gaussian using uniform proposal
def truncated_gaussian_pdf(x):
    """Unnormalized truncated Gaussian on [0, 2]."""
    if 0 <= x <= 2:
        return np.exp(-0.5 * (x - 1) ** 2)
    return 0


samples_rej, acc_rate = rejection_sample(
    target_pdf=truncated_gaussian_pdf,
    proposal_sample=lambda: np.random.uniform(0, 2),
    proposal_pdf=lambda x: 0.5,  # Uniform[0,2] has density 1/2
    M=2.5,  # M must satisfy M*0.5 >= exp(-0.5*(x-1)^2)
    n=5000
)

print(f"Rejection sampling from truncated Gaussian:")
print(f"  Acceptance rate: {acc_rate:.3f}")
print(f"  Sample mean: {samples_rej.mean():.3f}")
print(f"  Sample std:  {samples_rej.std():.3f}")


# =============================================================================
# 6. IMPORTANCE SAMPLING
# =============================================================================
print("\n" + "=" * 70)
print("6. IMPORTANCE SAMPLING")
print("=" * 70)

print("""
Estimate E_p[f(x)] using samples from a different distribution q(x):

    E_p[f(x)] = E_q[f(x) × p(x)/q(x)]
              ≈ (1/N) Σ f(xᵢ) × w(xᵢ)

where w(x) = p(x)/q(x) are importance weights.

Key insight: We don't need to sample from p, just evaluate it!

Applications:
    - Off-policy reinforcement learning
    - Rare event simulation
    - Approximate inference
""")


def importance_sampling_estimate(f, target_pdf, proposal_sample, proposal_pdf, n):
    """
    Estimate E_p[f(x)] using importance sampling.

    Returns: estimate, variance, effective sample size
    """
    samples = np.array([proposal_sample() for _ in range(n)])
    target_vals = np.array([target_pdf(x) for x in samples])
    proposal_vals = np.array([proposal_pdf(x) for x in samples])

    # Importance weights
    weights = target_vals / proposal_vals
    weights_normalized = weights / weights.sum()

    # Weighted estimate
    f_vals = np.array([f(x) for x in samples])
    estimate = np.sum(weights_normalized * f_vals)

    # Effective sample size
    ess = 1 / np.sum(weights_normalized ** 2)

    return estimate, ess


# Example: Estimate E[x] for a distribution
def target(x):
    """Target: mixture of Gaussians (unnormalized)."""
    return 0.3 * np.exp(-0.5 * (x - 2) ** 2) + 0.7 * np.exp(-0.5 * (x + 1) ** 2)


def proposal_sample():
    return np.random.uniform(-5, 5)


def proposal_pdf(x):
    return 0.1 if -5 <= x <= 5 else 0


estimate, ess = importance_sampling_estimate(
    f=lambda x: x,
    target_pdf=target,
    proposal_sample=proposal_sample,
    proposal_pdf=proposal_pdf,
    n=10000
)

print(f"Importance sampling estimate of E[x]:")
print(f"  Estimate: {estimate:.4f}")
print(f"  Effective sample size: {ess:.0f} / 10000")


# =============================================================================
# 7. MARKOV CHAIN MONTE CARLO (MCMC)
# =============================================================================
print("\n" + "=" * 70)
print("7. MARKOV CHAIN MONTE CARLO (MCMC)")
print("=" * 70)

print("""
When we can't sample directly, use a Markov chain that converges to p(x).

Metropolis-Hastings Algorithm:
    1. Start at x₀
    2. Propose x' ~ q(x'|x)
    3. Accept with probability min(1, p(x')q(x|x') / p(x)q(x'|x))
    4. If accepted, x_{t+1} = x', else x_{t+1} = x_t
    5. Repeat

For symmetric proposals (q(x'|x) = q(x|x')):
    Accept prob = min(1, p(x')/p(x))
""")


def metropolis_hastings(target_pdf, x0, proposal_std, n_samples, burn_in=1000):
    """
    Metropolis-Hastings with Gaussian proposal.

    Args:
        target_pdf: Unnormalized target density
        x0: Starting point
        proposal_std: Standard deviation of Gaussian proposal
        n_samples: Number of samples to return
        burn_in: Number of initial samples to discard
    """
    x = x0
    samples = []
    accepted = 0

    for i in range(n_samples + burn_in):
        # Propose
        x_proposed = x + np.random.randn() * proposal_std

        # Accept/reject
        acceptance_ratio = target_pdf(x_proposed) / (target_pdf(x) + 1e-10)

        if np.random.random() < acceptance_ratio:
            x = x_proposed
            if i >= burn_in:
                accepted += 1

        if i >= burn_in:
            samples.append(x)

    acceptance_rate = accepted / n_samples
    return np.array(samples), acceptance_rate


# Sample from bimodal distribution
def bimodal(x):
    """Bimodal distribution (unnormalized)."""
    return np.exp(-0.5 * (x - 3) ** 2) + np.exp(-0.5 * (x + 3) ** 2)


samples_mh, acc_rate = metropolis_hastings(
    target_pdf=bimodal,
    x0=0,
    proposal_std=2.0,
    n_samples=10000,
    burn_in=1000
)

print(f"MCMC sampling from bimodal distribution:")
print(f"  Acceptance rate: {acc_rate:.3f}")
print(f"  Sample mean: {samples_mh.mean():.3f}")
print(f"  Sample std:  {samples_mh.std():.3f}")


# =============================================================================
# 8. GUMBEL-SOFTMAX (Differentiable Categorical Sampling)
# =============================================================================
print("\n" + "=" * 70)
print("8. GUMBEL-SOFTMAX TRICK")
print("=" * 70)

print("""
Problem: How to backprop through categorical sampling?

Solution: Gumbel-Softmax!

    1. Add Gumbel noise: g_i = -log(-log(u_i)), u_i ~ Uniform(0,1)
    2. Soft sample: y_i = softmax((log(π_i) + g_i) / τ)

As temperature τ → 0, approaches one-hot (true sample).
As temperature τ → ∞, approaches uniform.

Used in: VAEs with discrete latents, differentiable NAS.
""")


def gumbel_softmax(logits, temperature=1.0, hard=False):
    """
    Sample from categorical using Gumbel-Softmax.

    Args:
        logits: Log probabilities (unnormalized)
        temperature: Temperature parameter
        hard: If True, return one-hot but gradients go through soft

    Returns:
        Soft (or hard) sample
    """
    # Sample Gumbel noise
    u = np.random.uniform(0, 1, logits.shape)
    gumbel = -np.log(-np.log(u + 1e-10) + 1e-10)

    # Add noise and apply temperature-scaled softmax
    y = (logits + gumbel) / temperature
    y_soft = np.exp(y - y.max()) / np.exp(y - y.max()).sum()

    if hard:
        # Straight-through: hard in forward, soft gradient in backward
        y_hard = np.zeros_like(y_soft)
        y_hard[np.argmax(y_soft)] = 1
        return y_hard  # In practice, use y_hard - y_soft.detach() + y_soft
    return y_soft


logits = np.array([1.0, 2.0, 0.5])
print(f"Logits: {logits}")
print(f"True probs: {np.exp(logits) / np.exp(logits).sum()}")

print(f"\nGumbel-Softmax samples at different temperatures:")
for temp in [0.1, 0.5, 1.0, 5.0]:
    sample = gumbel_softmax(logits, temperature=temp)
    print(f"  τ={temp}: {sample.round(3)}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: SAMPLING METHODS")
print("=" * 70)

print("""
┌──────────────────────────┬──────────────────────────────────────────────┐
│ Method                   │ Use Case                                     │
├──────────────────────────┼──────────────────────────────────────────────┤
│ Inverse Transform        │ When CDF⁻¹ is available                      │
│ Box-Muller               │ Gaussian sampling from uniforms              │
│ Reparameterization       │ VAEs, backprop through sampling              │
│ Rejection Sampling       │ Any distribution (can be slow)               │
│ Importance Sampling      │ Estimating expectations, off-policy RL       │
│ MCMC                     │ Complex posteriors, Bayesian inference       │
│ Gumbel-Softmax           │ Differentiable categorical sampling          │
└──────────────────────────┴──────────────────────────────────────────────┘

Key Insights for Deep Learning:
───────────────────────────────
1. Reparameterization trick enables backprop through Gaussian sampling
2. Gumbel-softmax enables backprop through categorical sampling
3. MCMC approximates intractable posteriors (Bayesian deep learning)
4. Monte Carlo estimation replaces intractable integrals

Practical Tips:
───────────────
• Always use reparameterization for continuous latents
• Gumbel-softmax for discrete latents (anneal temperature)
• Check effective sample size for importance sampling
• MCMC needs burn-in and convergence diagnostics
""")
