"""
Chapter 2.5: Singular Value Decomposition (SVD)
===============================================
The most important matrix decomposition in machine learning.

Run: python 05_svd.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("SINGULAR VALUE DECOMPOSITION (SVD)")
print("=" * 70)


# =============================================================================
# WHAT IS SVD?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHAT IS SVD?")
print("=" * 70)

print("""
SVD decomposes ANY matrix (even non-square) into three matrices:

    A = UΣVᵀ

Where:
    A = original matrix (m × n)
    U = left singular vectors (m × m), orthogonal
    Σ = singular values on diagonal (m × n)
    V = right singular vectors (n × n), orthogonal

Singular values σ₁ ≥ σ₂ ≥ ... ≥ σₘᵢₙ ≥ 0 (always non-negative!)

Unlike eigendecomposition:
    - Works for ANY matrix (not just square)
    - Always exists
    - Singular values are always real and non-negative
""")

# Example
A = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
])  # 4×3 matrix

U, S, Vt = np.linalg.svd(A)

print(f"\nOriginal A ({A.shape[0]}×{A.shape[1]}):\n{A}")
print(f"\nU ({U.shape[0]}×{U.shape[1]}):\n{U.round(3)}")
print(f"\nSingular values: {S.round(3)}")
print(f"\nVᵀ ({Vt.shape[0]}×{Vt.shape[1]}):\n{Vt.round(3)}")


# =============================================================================
# RECONSTRUCTING THE MATRIX
# =============================================================================
print("\n" + "=" * 70)
print("2. RECONSTRUCTING THE MATRIX")
print("=" * 70)

# Reconstruct A from SVD
# Need to create full Σ matrix
Sigma = np.zeros((A.shape[0], A.shape[1]))
Sigma[:len(S), :len(S)] = np.diag(S)

A_reconstructed = U @ Sigma @ Vt

print(f"Σ matrix ({Sigma.shape[0]}×{Sigma.shape[1]}):\n{Sigma.round(3)}")
print(f"\nReconstructed A = UΣVᵀ:\n{A_reconstructed.round(3)}")
print(f"\nMatches original? {np.allclose(A, A_reconstructed)}")


# =============================================================================
# LOW-RANK APPROXIMATION
# =============================================================================
print("\n" + "=" * 70)
print("3. LOW-RANK APPROXIMATION (KEY APPLICATION!)")
print("=" * 70)

print("""
The magic of SVD: We can approximate A using only top k singular values!

    A ≈ Aₖ = Σᵢ₌₁ᵏ σᵢ uᵢ vᵢᵀ

This is the BEST rank-k approximation (minimizes ||A - Aₖ||).

Why it matters:
    - Compression (images, data)
    - Noise reduction
    - Dimensionality reduction (PCA is SVD in disguise!)
    - Recommender systems (matrix completion)
""")

# Create a 10×10 matrix
np.random.seed(42)
A_large = np.random.randn(10, 10)

U, S, Vt = np.linalg.svd(A_large)

print(f"Original matrix: 10×10 = 100 values")
print(f"Singular values: {S.round(2)}")

# Approximate with different ranks
for k in [1, 3, 5, 10]:
    # Truncated SVD
    U_k = U[:, :k]
    S_k = S[:k]
    Vt_k = Vt[:k, :]

    A_approx = U_k @ np.diag(S_k) @ Vt_k

    # Reconstruction error
    error = np.linalg.norm(A_large - A_approx, 'fro') / np.linalg.norm(A_large, 'fro')
    storage = k * (10 + 1 + 10)  # U columns + singular values + V rows

    print(f"\nRank-{k} approximation:")
    print(f"  Storage: {storage} values (vs 100)")
    print(f"  Compression: {100 * (1 - storage/100):.1f}%")
    print(f"  Relative error: {error:.4f}")


# =============================================================================
# IMAGE COMPRESSION EXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("4. IMAGE COMPRESSION EXAMPLE")
print("=" * 70)

print("""
Images can be compressed using SVD:
    1. Treat image as a matrix (grayscale)
    2. Compute SVD
    3. Keep only top k singular values
    4. Reconstruct image

The fewer singular values, the more compression (but lower quality).
""")

# Create a simple "image" (gradient pattern)
image = np.outer(np.linspace(0, 1, 50), np.linspace(0, 1, 50))
image += 0.1 * np.random.randn(50, 50)  # Add noise

U, S, Vt = np.linalg.svd(image)

print(f"Original image: 50×50 = 2500 values")
print(f"Top 10 singular values: {S[:10].round(2)}")

# Save compression visualization
try:
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    axes = axes.flatten()

    ranks = [1, 5, 10, 20, 50]

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title(f'Original (2500 values)')
    axes[0].axis('off')

    for i, k in enumerate(ranks):
        img_approx = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
        storage = k * (50 + 1 + 50)
        compression = 100 * (1 - storage / 2500)

        axes[i+1].imshow(img_approx, cmap='gray')
        axes[i+1].set_title(f'Rank {k}: {storage} values ({compression:.0f}% compressed)')
        axes[i+1].axis('off')

    plt.tight_layout()
    plt.savefig('svd_compression.png', dpi=150)
    plt.close()
    print("\n✓ Saved visualization to 'svd_compression.png'")
except Exception as e:
    print(f"Could not save plot: {e}")


# =============================================================================
# SVD AND EIGENDECOMPOSITION
# =============================================================================
print("\n" + "=" * 70)
print("5. SVD vs EIGENDECOMPOSITION")
print("=" * 70)

print("""
The connection between SVD and eigendecomposition:

For A = UΣVᵀ:
    - Columns of U are eigenvectors of AAᵀ
    - Columns of V are eigenvectors of AᵀA
    - σᵢ² are the eigenvalues of both AAᵀ and AᵀA

This is why PCA can be done via either:
    1. Eigendecomposition of covariance matrix XᵀX
    2. SVD of data matrix X (more numerically stable!)
""")

A = np.array([[1, 2], [3, 4], [5, 6]])

# SVD
U, S, Vt = np.linalg.svd(A)

# Eigendecomposition of AᵀA
ATA = A.T @ A
eigenvalues_ATA, eigenvectors_ATA = np.linalg.eig(ATA)

print(f"\nA:\n{A}")
print(f"\nSVD singular values: {S}")
print(f"Singular values squared: {S**2}")
print(f"\nEigenvalues of AᵀA: {sorted(eigenvalues_ATA, reverse=True)}")
print(f"\n→ σᵢ² = eigenvalues of AᵀA ✓")


# =============================================================================
# TRUNCATED SVD IN PRACTICE
# =============================================================================
print("\n" + "=" * 70)
print("6. TRUNCATED SVD IN PRACTICE")
print("=" * 70)

print("""
For large matrices, computing full SVD is expensive.
Use TRUNCATED SVD to get only top k components.

scikit-learn provides TruncatedSVD:
    - More memory efficient
    - Faster for sparse matrices
    - Used in LSA (Latent Semantic Analysis)
""")

from sklearn.decomposition import TruncatedSVD

# Create a larger matrix
np.random.seed(42)
X = np.random.randn(1000, 100)

# Full SVD (for comparison)
import time

start = time.time()
U_full, S_full, Vt_full = np.linalg.svd(X, full_matrices=False)
time_full = time.time() - start

# Truncated SVD (only top 10)
start = time.time()
svd = TruncatedSVD(n_components=10)
X_reduced = svd.fit_transform(X)
time_truncated = time.time() - start

print(f"Matrix shape: {X.shape}")
print(f"\nFull SVD:")
print(f"  Time: {time_full:.4f}s")
print(f"  Components: {len(S_full)}")

print(f"\nTruncated SVD (k=10):")
print(f"  Time: {time_truncated:.4f}s")
print(f"  Components: {svd.n_components}")
print(f"  Variance explained: {svd.explained_variance_ratio_.sum():.2%}")


# =============================================================================
# RECOMMENDER SYSTEMS (MATRIX FACTORIZATION)
# =============================================================================
print("\n" + "=" * 70)
print("7. APPLICATION: RECOMMENDER SYSTEMS")
print("=" * 70)

print("""
SVD is used in recommender systems (e.g., Netflix Prize).

User-Item matrix R ≈ UΣVᵀ

Where:
    - Rows = users
    - Columns = items (movies)
    - Values = ratings (with many missing)

The low-rank approximation fills in missing values!
""")

# Simulated ratings matrix (0 = not rated)
ratings = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [1, 0, 0, 4],
    [0, 1, 5, 4]
])

print(f"Ratings matrix (0 = not rated):\n{ratings}")

# Fill missing with mean
ratings_filled = ratings.astype(float)
ratings_filled[ratings_filled == 0] = np.mean(ratings[ratings > 0])

# Low-rank approximation
U, S, Vt = np.linalg.svd(ratings_filled)

# Use rank 2 approximation
k = 2
predicted = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

print(f"\nPredicted ratings (rank-{k} approximation):\n{predicted.round(2)}")

# Show predictions for originally missing values
print("\nPredictions for missing ratings:")
for i in range(ratings.shape[0]):
    for j in range(ratings.shape[1]):
        if ratings[i, j] == 0:
            print(f"  User {i+1}, Item {j+1}: {predicted[i,j]:.2f}")


# =============================================================================
# PYTORCH SVD
# =============================================================================
print("\n" + "=" * 70)
print("8. PYTORCH SVD")
print("=" * 70)

import torch

A_torch = torch.tensor(A, dtype=torch.float32)

# PyTorch SVD
U_torch, S_torch, Vh_torch = torch.linalg.svd(A_torch)

print("PyTorch SVD:")
print(f"  U shape: {U_torch.shape}")
print(f"  S: {S_torch}")
print(f"  Vᵀ shape: {Vh_torch.shape}")

# Low-rank with PyTorch
k = 1
A_approx_torch = U_torch[:, :k] @ torch.diag(S_torch[:k]) @ Vh_torch[:k, :]
print(f"\nRank-{k} approximation:\n{A_approx_torch}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌──────────────────────────────────────────────────────────────────────────┐
│  Concept              │  Formula            │  Application               │
├──────────────────────────────────────────────────────────────────────────┤
│  Full SVD             │  A = UΣVᵀ           │  Complete decomposition    │
│  Truncated SVD        │  A ≈ UₖΣₖVₖᵀ        │  Compression, PCA          │
│  Low-rank approx      │  Best rank-k        │  Noise reduction           │
│  Matrix completion    │  Fill missing       │  Recommender systems       │
│  Numerical stability  │  Better than eig    │  Preferred for PCA         │
└──────────────────────────────────────────────────────────────────────────┘

Key Properties:
  • Works for ANY matrix (m×n)
  • Singular values are always non-negative
  • U and V are orthogonal
  • σᵢ² = eigenvalues of AᵀA
  • Optimal low-rank approximation (Eckart-Young theorem)

Applications in ML:
  • PCA / Dimensionality reduction
  • Image compression
  • Recommender systems
  • Latent Semantic Analysis (NLP)
  • Pseudoinverse computation
""")
