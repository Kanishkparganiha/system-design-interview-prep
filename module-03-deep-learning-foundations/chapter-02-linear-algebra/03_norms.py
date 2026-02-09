"""
Chapter 2.3: Norms
==================
Measuring the size of vectors and matrices.
Critical for regularization and optimization in deep learning.

Run: python 03_norms.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("NORMS: MEASURING SIZE")
print("=" * 70)


# =============================================================================
# VECTOR NORMS
# =============================================================================
print("\n" + "=" * 70)
print("1. VECTOR NORMS (Lp NORMS)")
print("=" * 70)

print("""
A norm measures the "size" or "length" of a vector.
The general Lp norm is:

    ||x||_p = (Σᵢ |xᵢ|^p)^(1/p)

Common norms:
    L1 norm (p=1): Manhattan distance
    L2 norm (p=2): Euclidean distance (most common)
    L∞ norm (p=∞): Maximum absolute value
""")

x = np.array([3, -4, 0, 5, -2])
print(f"\nVector x = {x}")

# L1 Norm (Manhattan)
l1 = np.linalg.norm(x, ord=1)
l1_manual = np.sum(np.abs(x))
print(f"\nL1 Norm (Manhattan): ||x||₁ = Σ|xᵢ| = {l1}")
print(f"  = |3| + |-4| + |0| + |5| + |-2| = {l1_manual}")

# L2 Norm (Euclidean)
l2 = np.linalg.norm(x, ord=2)
l2_manual = np.sqrt(np.sum(x**2))
print(f"\nL2 Norm (Euclidean): ||x||₂ = √(Σxᵢ²) = {l2:.4f}")
print(f"  = √(9 + 16 + 0 + 25 + 4) = √54 = {l2_manual:.4f}")

# L∞ Norm (Max)
linf = np.linalg.norm(x, ord=np.inf)
print(f"\nL∞ Norm (Max): ||x||_∞ = max|xᵢ| = {linf}")


# =============================================================================
# NORM PROPERTIES
# =============================================================================
print("\n" + "=" * 70)
print("2. NORM PROPERTIES")
print("=" * 70)

print("""
A valid norm must satisfy:

1. Non-negativity: ||x|| ≥ 0, and ||x|| = 0 iff x = 0
2. Scalar multiplication: ||αx|| = |α| · ||x||
3. Triangle inequality: ||x + y|| ≤ ||x|| + ||y||
""")

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
alpha = -2

print(f"x = {x}")
print(f"y = {y}")
print(f"α = {alpha}")

# Property 2: Scalar multiplication
print(f"\nScalar multiplication: ||αx|| = |α| · ||x||")
print(f"  ||{alpha}x||₂ = {np.linalg.norm(alpha * x):.4f}")
print(f"  |{alpha}| · ||x||₂ = {abs(alpha) * np.linalg.norm(x):.4f}")

# Property 3: Triangle inequality
print(f"\nTriangle inequality: ||x + y|| ≤ ||x|| + ||y||")
print(f"  ||x + y||₂ = {np.linalg.norm(x + y):.4f}")
print(f"  ||x||₂ + ||y||₂ = {np.linalg.norm(x) + np.linalg.norm(y):.4f}")


# =============================================================================
# UNIT VECTORS
# =============================================================================
print("\n" + "=" * 70)
print("3. UNIT VECTORS (NORMALIZATION)")
print("=" * 70)

print("""
A unit vector has norm = 1.
To normalize a vector: x̂ = x / ||x||

Used everywhere in ML:
  - Word embeddings normalization
  - Batch normalization (kind of)
  - Cosine similarity computation
""")

x = np.array([3.0, 4.0])
print(f"\nOriginal vector: x = {x}")
print(f"||x||₂ = {np.linalg.norm(x)}")

x_normalized = x / np.linalg.norm(x)
print(f"\nNormalized: x̂ = {x_normalized}")
print(f"||x̂||₂ = {np.linalg.norm(x_normalized):.6f}")


# =============================================================================
# L1 vs L2 REGULARIZATION
# =============================================================================
print("\n" + "=" * 70)
print("4. L1 vs L2 IN REGULARIZATION")
print("=" * 70)

print("""
In deep learning, norms are used for regularization:

L2 Regularization (Ridge / Weight Decay):
    Loss = Original_Loss + λ||w||₂²
    - Penalizes large weights
    - Weights shrink toward 0 but rarely become exactly 0
    - Smooth penalty

L1 Regularization (Lasso):
    Loss = Original_Loss + λ||w||₁
    - Also penalizes large weights
    - Produces SPARSE weights (many exactly 0)
    - Good for feature selection
""")

# Demonstrate sparsity
print("\n--- Sparsity Demonstration ---")
# Simulating gradient descent with L1 vs L2

w = np.array([0.5, 0.3, 0.1, -0.05, 0.02])
lambda_reg = 0.1
learning_rate = 0.1

print(f"Original weights: {w}")

# L2 gradient: ∂(||w||₂²)/∂w = 2w
w_l2 = w.copy()
for _ in range(20):
    grad_l2 = 2 * w_l2  # L2 gradient
    w_l2 = w_l2 - learning_rate * lambda_reg * grad_l2

print(f"After L2 regularization: {w_l2}")
print(f"  Number of zeros: {np.sum(np.abs(w_l2) < 1e-6)}")

# L1 gradient: ∂(||w||₁)/∂w = sign(w)
w_l1 = w.copy()
for _ in range(20):
    grad_l1 = np.sign(w_l1)  # L1 gradient
    w_l1 = w_l1 - learning_rate * lambda_reg * grad_l1
    w_l1 = np.where(np.abs(w_l1) < 0.01, 0, w_l1)  # Threshold small values

print(f"After L1 regularization: {w_l1}")
print(f"  Number of zeros: {np.sum(np.abs(w_l1) < 1e-6)}")

print("\n→ L1 produces sparser weights (more zeros)!")


# =============================================================================
# MATRIX NORMS
# =============================================================================
print("\n" + "=" * 70)
print("5. MATRIX NORMS")
print("=" * 70)

print("""
Extending norms to matrices:

Frobenius Norm (most common for matrices):
    ||A||_F = √(Σᵢⱼ Aᵢⱼ²) = √(Tr(AᵀA))
    - Treats matrix as a long vector

Spectral Norm (L2 norm for matrices):
    ||A||₂ = largest singular value of A
    - Maximum "stretching" factor

Nuclear Norm (sum of singular values):
    ||A||_* = Σᵢ σᵢ
    - Used for matrix completion, low-rank approximation
""")

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(f"\nMatrix A:\n{A}")

# Frobenius norm
frob = np.linalg.norm(A, ord='fro')
frob_manual = np.sqrt(np.sum(A**2))
print(f"\nFrobenius norm: ||A||_F = {frob:.4f}")
print(f"  = √(1² + 2² + 3² + 4² + 5² + 6²) = {frob_manual:.4f}")

# Spectral norm
spectral = np.linalg.norm(A, ord=2)
U, S, Vt = np.linalg.svd(A)
print(f"\nSpectral norm: ||A||₂ = {spectral:.4f}")
print(f"  = largest singular value = {S[0]:.4f}")

# Nuclear norm
nuclear = np.sum(S)
print(f"\nNuclear norm: ||A||_* = {nuclear:.4f}")
print(f"  = sum of singular values = {S[0]:.4f} + {S[1]:.4f}")


# =============================================================================
# COSINE SIMILARITY
# =============================================================================
print("\n" + "=" * 70)
print("6. COSINE SIMILARITY")
print("=" * 70)

print("""
Cosine similarity measures the angle between vectors:

    cos(θ) = (a · b) / (||a||₂ · ||b||₂)

Range: [-1, 1]
    1:  Same direction
    0:  Perpendicular
   -1:  Opposite direction

Used heavily in:
    - Word embeddings (Word2Vec, GloVe)
    - Recommendation systems
    - Document similarity
""")

# Example: Word embeddings
king = np.array([0.8, 0.6, 0.2, 0.1])
queen = np.array([0.75, 0.65, 0.25, 0.15])
apple = np.array([0.1, 0.2, 0.8, 0.7])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"\n'king' embedding:  {king}")
print(f"'queen' embedding: {queen}")
print(f"'apple' embedding: {apple}")

print(f"\nCosine similarity:")
print(f"  king ↔ queen: {cosine_similarity(king, queen):.4f} (similar)")
print(f"  king ↔ apple: {cosine_similarity(king, apple):.4f} (different)")
print(f"  queen ↔ apple: {cosine_similarity(queen, apple):.4f} (different)")


# =============================================================================
# DISTANCE METRICS
# =============================================================================
print("\n" + "=" * 70)
print("7. DISTANCE METRICS")
print("=" * 70)

print("""
Distance between two vectors:
    Euclidean: ||a - b||₂ = √(Σ(aᵢ - bᵢ)²)
    Manhattan: ||a - b||₁ = Σ|aᵢ - bᵢ|
    Cosine distance: 1 - cosine_similarity(a, b)
""")

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"\na = {a}")
print(f"b = {b}")

euclidean = np.linalg.norm(a - b, ord=2)
manhattan = np.linalg.norm(a - b, ord=1)
cosine_dist = 1 - cosine_similarity(a, b)

print(f"\nEuclidean distance: {euclidean:.4f}")
print(f"Manhattan distance: {manhattan:.4f}")
print(f"Cosine distance: {cosine_dist:.4f}")


# =============================================================================
# VISUALIZATION (Optional)
# =============================================================================
print("\n" + "=" * 70)
print("8. VISUALIZATION: UNIT CIRCLES IN DIFFERENT NORMS")
print("=" * 70)

print("""
The "unit circle" looks different for each norm!
    L1: Diamond shape
    L2: Circle (Euclidean)
    L∞: Square
""")

# Create unit "circles" for different norms
theta = np.linspace(0, 2*np.pi, 100)

# L2 unit circle
x_l2 = np.cos(theta)
y_l2 = np.sin(theta)

# L1 unit "circle" (diamond)
t = np.linspace(0, 1, 25)
x_l1 = np.concatenate([t, 1-t, -t, t-1])
y_l1 = np.concatenate([1-t, -t, t-1, t])

# L∞ unit "circle" (square)
x_linf = np.array([1, 1, -1, -1, 1])
y_linf = np.array([1, -1, -1, 1, 1])

print("\nSaving visualization to 'norm_unit_circles.png'...")

try:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    axes[0].plot(x_l1, y_l1, 'b-', linewidth=2)
    axes[0].set_title('L1 Norm (Diamond)', fontsize=12)
    axes[0].set_xlim(-1.5, 1.5)
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].set_aspect('equal')
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=0, color='k', linewidth=0.5)
    axes[0].axvline(x=0, color='k', linewidth=0.5)

    axes[1].plot(x_l2, y_l2, 'g-', linewidth=2)
    axes[1].set_title('L2 Norm (Circle)', fontsize=12)
    axes[1].set_xlim(-1.5, 1.5)
    axes[1].set_ylim(-1.5, 1.5)
    axes[1].set_aspect('equal')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='k', linewidth=0.5)
    axes[1].axvline(x=0, color='k', linewidth=0.5)

    axes[2].plot(x_linf, y_linf, 'r-', linewidth=2)
    axes[2].set_title('L∞ Norm (Square)', fontsize=12)
    axes[2].set_xlim(-1.5, 1.5)
    axes[2].set_ylim(-1.5, 1.5)
    axes[2].set_aspect('equal')
    axes[2].grid(True, alpha=0.3)
    axes[2].axhline(y=0, color='k', linewidth=0.5)
    axes[2].axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('norm_unit_circles.png', dpi=150)
    plt.close()
    print("✓ Saved!")
except Exception as e:
    print(f"Could not save plot: {e}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌────────────────────────────────────────────────────────────────────────┐
│  Norm              │  Formula              │  Deep Learning Use        │
├────────────────────────────────────────────────────────────────────────┤
│  L1 (Manhattan)    │  Σ|xᵢ|                │  Sparse regularization    │
│  L2 (Euclidean)    │  √(Σxᵢ²)             │  Weight decay, distances  │
│  L∞ (Max)          │  max|xᵢ|             │  Robust optimization      │
│  Frobenius         │  √(ΣΣAᵢⱼ²)           │  Matrix regularization    │
│  Spectral          │  max singular value   │  Lipschitz constraints    │
└────────────────────────────────────────────────────────────────────────┘

Key Applications:
  • Regularization: Prevent overfitting (L1 → sparsity, L2 → small weights)
  • Normalization: Create unit vectors
  • Similarity: Cosine similarity for embeddings
  • Distance: Measuring how far apart vectors are
""")
