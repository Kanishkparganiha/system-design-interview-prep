"""
Chapter 3.2: Information Theory
===============================
Entropy, cross-entropy, and KL divergence - the foundation of loss functions.

Run: python 02_information_theory.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("INFORMATION THEORY")
print("=" * 70)


# =============================================================================
# ENTROPY
# =============================================================================
print("\n" + "=" * 70)
print("1. ENTROPY - MEASURING UNCERTAINTY")
print("=" * 70)

print("""
Shannon Entropy measures the "uncertainty" or "information content" of a distribution.

    H(X) = -Σ P(x) log₂ P(x)    (in bits)
    H(X) = -Σ P(x) ln P(x)      (in nats, used in ML)

Intuition:
    - Low entropy: Distribution is concentrated (predictable)
    - High entropy: Distribution is spread out (unpredictable)

Maximum entropy for K classes: log(K) (uniform distribution)
""")

def entropy(probs):
    """Calculate entropy in nats (natural log)."""
    probs = np.array(probs)
    # Avoid log(0) by filtering zeros
    probs = probs[probs > 0]
    return -np.sum(probs * np.log(probs))

# Examples
print("\nExamples:")

# Certain outcome
p_certain = [1.0, 0.0, 0.0]
print(f"  Certain [1, 0, 0]: H = {entropy(p_certain):.4f} nats")

# Maximum uncertainty (uniform)
p_uniform = [1/3, 1/3, 1/3]
print(f"  Uniform [⅓, ⅓, ⅓]: H = {entropy(p_uniform):.4f} nats")
print(f"    (Maximum possible: ln(3) = {np.log(3):.4f})")

# Biased
p_biased = [0.7, 0.2, 0.1]
print(f"  Biased [0.7, 0.2, 0.1]: H = {entropy(p_biased):.4f} nats")

# Binary entropy (special case)
print("\n--- Binary Entropy ---")
print("For binary outcome with P(X=1) = p:")
print("H(p) = -p·log(p) - (1-p)·log(1-p)")

for p in [0.0, 0.1, 0.5, 0.9, 1.0]:
    if p == 0 or p == 1:
        h = 0
    else:
        h = -p * np.log(p) - (1-p) * np.log(1-p)
    print(f"  p = {p}: H = {h:.4f}")

print("\n→ Maximum uncertainty at p = 0.5!")


# =============================================================================
# CROSS-ENTROPY
# =============================================================================
print("\n" + "=" * 70)
print("2. CROSS-ENTROPY - THE LOSS FUNCTION")
print("=" * 70)

print("""
Cross-entropy between TRUE distribution P and PREDICTED distribution Q:

    H(P, Q) = -Σ P(x) log Q(x)

In classification:
    P = one-hot true label (e.g., [0, 1, 0])
    Q = softmax predictions (e.g., [0.1, 0.7, 0.2])

Cross-entropy loss = -Σ yᵢ log(ŷᵢ) = -log(ŷ_correct_class)

This is THE standard loss function for classification!
""")

def cross_entropy(p_true, q_pred):
    """Cross-entropy H(P, Q)."""
    p_true = np.array(p_true)
    q_pred = np.array(q_pred)
    # Clip to avoid log(0)
    q_pred = np.clip(q_pred, 1e-15, 1 - 1e-15)
    return -np.sum(p_true * np.log(q_pred))

# Example: Classification
print("\nClassification Example:")
y_true = [0, 1, 0]  # True label is class 1
print(f"True label (one-hot): {y_true}")

# Good prediction
y_pred_good = [0.1, 0.8, 0.1]
print(f"\nGood prediction: {y_pred_good}")
print(f"  Cross-entropy loss: {cross_entropy(y_true, y_pred_good):.4f}")
print(f"  = -log(0.8) = {-np.log(0.8):.4f}")

# Bad prediction
y_pred_bad = [0.1, 0.2, 0.7]
print(f"\nBad prediction: {y_pred_bad}")
print(f"  Cross-entropy loss: {cross_entropy(y_true, y_pred_bad):.4f}")
print(f"  = -log(0.2) = {-np.log(0.2):.4f}")

# Very bad prediction
y_pred_terrible = [0.01, 0.01, 0.98]
print(f"\nTerrible prediction: {y_pred_terrible}")
print(f"  Cross-entropy loss: {cross_entropy(y_true, y_pred_terrible):.4f}")
print(f"  = -log(0.01) = {-np.log(0.01):.4f}")

print("\n→ Lower prediction for true class = Higher loss!")


# =============================================================================
# BINARY CROSS-ENTROPY
# =============================================================================
print("\n" + "=" * 70)
print("3. BINARY CROSS-ENTROPY")
print("=" * 70)

print("""
For binary classification (two classes):

    BCE = -[y·log(ŷ) + (1-y)·log(1-ŷ)]

Where:
    y = true label (0 or 1)
    ŷ = predicted probability of class 1 (sigmoid output)

This is equivalent to cross-entropy for 2 classes.
""")

def binary_cross_entropy(y_true, y_pred):
    """Binary cross-entropy loss."""
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    return -(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

print("\nBinary Classification Examples:")
print("True label y = 1:")
for y_pred in [0.9, 0.7, 0.5, 0.3, 0.1]:
    loss = binary_cross_entropy(1, y_pred)
    print(f"  ŷ = {y_pred}: BCE = {loss:.4f}")

print("\nTrue label y = 0:")
for y_pred in [0.1, 0.3, 0.5, 0.7, 0.9]:
    loss = binary_cross_entropy(0, y_pred)
    print(f"  ŷ = {y_pred}: BCE = {loss:.4f}")


# =============================================================================
# KL DIVERGENCE
# =============================================================================
print("\n" + "=" * 70)
print("4. KL DIVERGENCE - MEASURING DISTRIBUTION DIFFERENCE")
print("=" * 70)

print("""
Kullback-Leibler Divergence measures how different Q is from P:

    D_KL(P || Q) = Σ P(x) log(P(x) / Q(x))
                 = H(P, Q) - H(P)
                 = Cross-entropy - Entropy

Properties:
    - D_KL ≥ 0 always
    - D_KL = 0 iff P = Q
    - NOT symmetric: D_KL(P || Q) ≠ D_KL(Q || P)

Used in:
    - VAE loss (KL between prior and posterior)
    - Knowledge distillation
    - Reinforcement learning (policy updates)
""")

def kl_divergence(p, q):
    """KL divergence D_KL(P || Q)."""
    p = np.array(p)
    q = np.array(q)
    # Avoid division by zero and log(0)
    mask = p > 0
    return np.sum(p[mask] * np.log(p[mask] / q[mask]))

# Examples
p = [0.4, 0.3, 0.3]
q1 = [0.4, 0.3, 0.3]  # Same as p
q2 = [0.35, 0.35, 0.3]  # Slightly different
q3 = [0.1, 0.1, 0.8]  # Very different

print(f"\nP = {p}")
print(f"\nQ1 = {q1} (same as P)")
print(f"  D_KL(P || Q1) = {kl_divergence(p, q1):.6f}")

print(f"\nQ2 = {q2} (slightly different)")
print(f"  D_KL(P || Q2) = {kl_divergence(p, q2):.6f}")

print(f"\nQ3 = {q3} (very different)")
print(f"  D_KL(P || Q3) = {kl_divergence(p, q3):.6f}")

# Asymmetry
print("\n--- Asymmetry of KL Divergence ---")
print(f"D_KL(P || Q3) = {kl_divergence(p, q3):.4f}")
print(f"D_KL(Q3 || P) = {kl_divergence(q3, p):.4f}")
print("→ Not the same! KL divergence is asymmetric.")


# =============================================================================
# RELATIONSHIP BETWEEN H, H(P,Q), AND KL
# =============================================================================
print("\n" + "=" * 70)
print("5. RELATIONSHIP: H, H(P,Q), KL")
print("=" * 70)

print("""
Key relationship:

    H(P, Q) = H(P) + D_KL(P || Q)

    Cross-entropy = Entropy + KL Divergence

Since entropy H(P) is constant for fixed true distribution P:
    Minimizing cross-entropy = Minimizing KL divergence

That's why cross-entropy is a good loss function!
It pushes Q (predictions) toward P (true distribution).
""")

p = [0.7, 0.2, 0.1]
q = [0.5, 0.3, 0.2]

h_p = entropy(p)
h_pq = cross_entropy(p, q)
kl_pq = kl_divergence(p, q)

print(f"\nP = {p}")
print(f"Q = {q}")
print(f"\nH(P) = {h_p:.4f}")
print(f"D_KL(P || Q) = {kl_pq:.4f}")
print(f"H(P) + D_KL = {h_p + kl_pq:.4f}")
print(f"H(P, Q) = {h_pq:.4f}")
print(f"\n✓ H(P, Q) = H(P) + D_KL(P || Q)")


# =============================================================================
# VAE LOSS FUNCTION
# =============================================================================
print("\n" + "=" * 70)
print("6. APPLICATION: VAE LOSS")
print("=" * 70)

print("""
Variational Autoencoder (VAE) loss has two terms:

    L = Reconstruction Loss + β · KL Divergence
    L = E[log p(x|z)] - β · D_KL(q(z|x) || p(z))

Where:
    - Reconstruction: How well can we reconstruct x from z?
    - KL term: How close is the encoder q(z|x) to prior p(z)?
    - p(z) is usually N(0, I)

The KL term for Gaussians has a closed form:
    D_KL(N(μ, σ²) || N(0, 1)) = ½ Σ (μ² + σ² - log(σ²) - 1)
""")

def kl_gaussian(mu, log_var):
    """KL divergence between N(mu, exp(log_var)) and N(0, 1)."""
    # D_KL = 0.5 * sum(mu^2 + sigma^2 - log(sigma^2) - 1)
    return -0.5 * np.sum(1 + log_var - mu**2 - np.exp(log_var))

# Example
mu = np.array([0.5, -0.3, 0.1])
log_var = np.array([-0.5, -0.2, -0.8])  # log(variance)

kl = kl_gaussian(mu, log_var)
print(f"\nEncoder outputs:")
print(f"  μ = {mu}")
print(f"  log(σ²) = {log_var}")
print(f"\nD_KL(q(z|x) || p(z)) = {kl:.4f}")

# If mu=0 and log_var=0 (meaning sigma=1), KL should be 0
print(f"\nWith μ=0, σ=1: D_KL = {kl_gaussian(np.zeros(3), np.zeros(3)):.4f}")


# =============================================================================
# PYTORCH IMPLEMENTATION
# =============================================================================
print("\n" + "=" * 70)
print("7. PYTORCH IMPLEMENTATION")
print("=" * 70)

import torch
import torch.nn.functional as F

# Cross-entropy in PyTorch
logits = torch.tensor([[2.0, 1.0, 0.1]])  # Raw scores (before softmax)
target = torch.tensor([0])  # True class index

# PyTorch cross-entropy applies softmax internally!
loss = F.cross_entropy(logits, target)
print(f"PyTorch cross-entropy:")
print(f"  Logits: {logits.numpy()}")
print(f"  Target class: {target.item()}")
print(f"  Loss: {loss.item():.4f}")

# Manual calculation
probs = F.softmax(logits, dim=1)
print(f"  Softmax probs: {probs.detach().numpy()}")
manual_loss = -torch.log(probs[0, target]).item()
print(f"  Manual: -log({probs[0, target].item():.4f}) = {manual_loss:.4f}")

# Binary cross-entropy
y_true_bin = torch.tensor([1.0])
y_pred_bin = torch.tensor([0.8])
bce = F.binary_cross_entropy(y_pred_bin, y_true_bin)
print(f"\nPyTorch BCE:")
print(f"  y={y_true_bin.item()}, ŷ={y_pred_bin.item()}")
print(f"  Loss: {bce.item():.4f}")

# KL Divergence
p_tensor = torch.tensor([0.4, 0.3, 0.3])
q_tensor = torch.tensor([0.1, 0.1, 0.8])
kl_torch = F.kl_div(q_tensor.log(), p_tensor, reduction='sum')
print(f"\nPyTorch KL Divergence:")
print(f"  D_KL(P || Q) = {kl_torch.item():.4f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  Measure          │  Formula                  │  Use in DL              │
├─────────────────────────────────────────────────────────────────────────┤
│  Entropy          │  -Σ P log P               │  Uncertainty measure    │
│  Cross-entropy    │  -Σ P log Q               │  Classification loss    │
│  KL Divergence    │  Σ P log(P/Q)             │  VAE, distillation      │
│  Binary CE        │  -y log ŷ - (1-y) log(1-ŷ)│  Binary classification  │
└─────────────────────────────────────────────────────────────────────────┘

Key Insights:
─────────────
• Cross-entropy loss = entropy + KL divergence
• Minimizing CE pushes predictions toward true distribution
• KL divergence is asymmetric (order matters!)
• VAE uses KL to regularize latent space
• PyTorch's cross_entropy expects logits, not probabilities
""")
