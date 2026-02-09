"""
Chapter 2.4: Eigendecomposition
===============================
Understanding eigenvectors and eigenvalues - the heart of PCA and beyond.

Run: python 04_eigendecomposition.py
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("EIGENDECOMPOSITION")
print("=" * 70)


# =============================================================================
# WHAT ARE EIGENVECTORS AND EIGENVALUES?
# =============================================================================
print("\n" + "=" * 70)
print("1. EIGENVECTORS AND EIGENVALUES")
print("=" * 70)

print("""
For a square matrix A, an eigenvector v and eigenvalue λ satisfy:

    Av = λv

Meaning: When A transforms v, the result is just v scaled by λ.
         The DIRECTION doesn't change, only the MAGNITUDE.

Think of it as:
    - Eigenvectors: The "natural directions" of a transformation
    - Eigenvalues: How much each direction is stretched/compressed
""")

# Example
A = np.array([
    [4, 1],
    [2, 3]
])

eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"\nMatrix A:\n{A}")
print(f"\nEigenvalues: {eigenvalues}")
print(f"\nEigenvectors (columns):\n{eigenvectors}")

# Verify Av = λv
print("\n--- Verification: Av = λv ---")
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lam = eigenvalues[i]

    Av = A @ v
    lambda_v = lam * v

    print(f"\nEigenvector {i+1}: v = {v}")
    print(f"Eigenvalue {i+1}: λ = {lam:.4f}")
    print(f"A @ v     = {Av}")
    print(f"λ * v     = {lambda_v}")
    print(f"Equal? {np.allclose(Av, lambda_v)}")


# =============================================================================
# GEOMETRIC INTERPRETATION
# =============================================================================
print("\n" + "=" * 70)
print("2. GEOMETRIC INTERPRETATION")
print("=" * 70)

print("""
Imagine a linear transformation (like stretching or rotating).

- Most vectors change BOTH direction AND length
- Eigenvectors only change LENGTH (scaled by eigenvalue)

Eigenvalue meanings:
    λ > 1:  Stretched
    λ = 1:  Unchanged
    0 < λ < 1: Compressed
    λ = 0:  Collapsed to zero
    λ < 0:  Flipped AND scaled
""")

# Visualization
print("\nSaving visualization to 'eigen_visualization.png'...")

try:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Original vectors
    v1 = eigenvectors[:, 0]
    v2 = eigenvectors[:, 1]

    # Random non-eigenvector
    v_random = np.array([1, 0.5])
    v_random = v_random / np.linalg.norm(v_random)

    # Before transformation
    ax = axes[0]
    ax.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1,
              color='blue', label=f'Eigenvector 1 (λ={eigenvalues[0]:.2f})')
    ax.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1,
              color='red', label=f'Eigenvector 2 (λ={eigenvalues[1]:.2f})')
    ax.quiver(0, 0, v_random[0], v_random[1], angles='xy', scale_units='xy', scale=1,
              color='green', label='Random vector')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('Before Transformation', fontsize=12)
    ax.legend(loc='upper left')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

    # After transformation
    ax = axes[1]
    Av1 = A @ v1
    Av2 = A @ v2
    Av_random = A @ v_random

    ax.quiver(0, 0, Av1[0], Av1[1], angles='xy', scale_units='xy', scale=1,
              color='blue', label=f'A @ eigenvector 1')
    ax.quiver(0, 0, Av2[0], Av2[1], angles='xy', scale_units='xy', scale=1,
              color='red', label=f'A @ eigenvector 2')
    ax.quiver(0, 0, Av_random[0], Av_random[1], angles='xy', scale_units='xy', scale=1,
              color='green', label='A @ random vector')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title('After Transformation A@v', fontsize=12)
    ax.legend(loc='upper left')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig('eigen_visualization.png', dpi=150)
    plt.close()
    print("✓ Saved!")
except Exception as e:
    print(f"Could not save plot: {e}")

print("""
Observation:
- Eigenvectors keep their direction (just scaled)
- Random vectors change BOTH direction and length
""")


# =============================================================================
# EIGENDECOMPOSITION (DIAGONALIZATION)
# =============================================================================
print("\n" + "=" * 70)
print("3. EIGENDECOMPOSITION (DIAGONALIZATION)")
print("=" * 70)

print("""
A square matrix A can be decomposed as:

    A = VΛV⁻¹

Where:
    V = matrix of eigenvectors (columns)
    Λ = diagonal matrix of eigenvalues
    V⁻¹ = inverse of V

This works when A has n linearly independent eigenvectors.
""")

# Decomposition
V = eigenvectors
Lambda = np.diag(eigenvalues)
V_inv = np.linalg.inv(V)

print(f"\nA:\n{A}")
print(f"\nV (eigenvectors):\n{V}")
print(f"\nΛ (eigenvalues on diagonal):\n{Lambda}")
print(f"\nV⁻¹:\n{V_inv}")

# Reconstruct A
A_reconstructed = V @ Lambda @ V_inv
print(f"\nV @ Λ @ V⁻¹:\n{A_reconstructed.real}")
print(f"\nMatches A? {np.allclose(A, A_reconstructed)}")


# =============================================================================
# COMPUTING MATRIX POWERS
# =============================================================================
print("\n" + "=" * 70)
print("4. APPLICATION: MATRIX POWERS")
print("=" * 70)

print("""
Eigendecomposition makes computing Aⁿ efficient!

    A = VΛV⁻¹
    A² = VΛV⁻¹ · VΛV⁻¹ = VΛ²V⁻¹
    Aⁿ = VΛⁿV⁻¹

And Λⁿ is easy: just raise each diagonal element to power n!
""")

n = 10
A_power_naive = np.linalg.matrix_power(A, n)

# Using eigendecomposition
Lambda_n = np.diag(eigenvalues ** n)
A_power_eigen = V @ Lambda_n @ V_inv

print(f"\nA^{n} (naive):\n{A_power_naive}")
print(f"\nA^{n} (via eigendecomposition):\n{A_power_eigen.real}")
print(f"\nMatch? {np.allclose(A_power_naive, A_power_eigen)}")

print("""
This is useful for:
    - Solving recurrence relations
    - Analyzing dynamical systems
    - Understanding convergence of iterative algorithms
""")


# =============================================================================
# SYMMETRIC MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("5. SYMMETRIC MATRICES (SPECIAL CASE)")
print("=" * 70)

print("""
For symmetric matrices (A = Aᵀ), eigendecomposition is nicer:

    A = QΛQᵀ    (not Q⁻¹, but Qᵀ!)

Properties:
    - All eigenvalues are REAL (not complex)
    - Eigenvectors are ORTHOGONAL
    - Q is an orthogonal matrix (QᵀQ = I)

Symmetric matrices are common in ML:
    - Covariance matrices
    - Hessian matrices
    - Gram matrices (XᵀX)
""")

# Create symmetric matrix
S = np.array([
    [4, 2, 1],
    [2, 5, 3],
    [1, 3, 6]
])

print(f"\nSymmetric matrix S:\n{S}")
print(f"Is symmetric? {np.allclose(S, S.T)}")

eigenvalues_s, eigenvectors_s = np.linalg.eig(S)

print(f"\nEigenvalues (all real): {eigenvalues_s}")
print(f"\nEigenvectors (orthogonal):\n{eigenvectors_s}")

# Check orthogonality
Q = eigenvectors_s
print(f"\nQᵀQ (should be identity):\n{(Q.T @ Q).round(6)}")


# =============================================================================
# POSITIVE DEFINITE MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("6. POSITIVE DEFINITE MATRICES")
print("=" * 70)

print("""
A symmetric matrix is POSITIVE DEFINITE if all eigenvalues > 0.
Equivalently: xᵀAx > 0 for all non-zero x.

Why it matters:
    - Covariance matrices are positive semi-definite
    - Hessian being positive definite → local minimum
    - Ensures certain optimization problems have solutions
""")

# Check positive definiteness via eigenvalues
eigenvalues_s, _ = np.linalg.eig(S)
print(f"\nEigenvalues of S: {eigenvalues_s}")
print(f"All positive? {np.all(eigenvalues_s > 0)}")
print(f"→ S is positive definite")

# Create indefinite matrix
Indef = np.array([[1, 2], [2, 1]])
eig_indef, _ = np.linalg.eig(Indef)
print(f"\nMatrix [[1,2],[2,1]] eigenvalues: {eig_indef}")
print(f"All positive? {np.all(eig_indef > 0)}")
print(f"→ This matrix is NOT positive definite")


# =============================================================================
# PCA PREVIEW
# =============================================================================
print("\n" + "=" * 70)
print("7. APPLICATION: PCA PREVIEW")
print("=" * 70)

print("""
Principal Component Analysis uses eigendecomposition!

Given data X (n_samples × n_features):
    1. Compute covariance matrix: C = (1/n) XᵀX
    2. Find eigenvectors of C
    3. Top eigenvectors = principal components
    4. Project data onto principal components

The eigenvalue = variance explained in that direction.
""")

# Generate 2D data with correlation
np.random.seed(42)
n_samples = 200
X = np.random.randn(n_samples, 2)
X = X @ np.array([[2, 1], [1, 2]])  # Add correlation

# Center the data
X_centered = X - X.mean(axis=0)

# Compute covariance matrix
cov_matrix = (X_centered.T @ X_centered) / n_samples

print(f"\nCovariance matrix:\n{cov_matrix}")

# Eigendecomposition
eigenvalues_pca, eigenvectors_pca = np.linalg.eig(cov_matrix)

# Sort by eigenvalue (descending)
idx = np.argsort(eigenvalues_pca)[::-1]
eigenvalues_pca = eigenvalues_pca[idx]
eigenvectors_pca = eigenvectors_pca[:, idx]

print(f"\nEigenvalues (variance in each PC): {eigenvalues_pca}")
print(f"Variance explained: {eigenvalues_pca / eigenvalues_pca.sum() * 100}%")
print(f"\nPrincipal components:\n{eigenvectors_pca}")

print("""
The first PC captures most variance!
See chapter 07_svd.py and 08_pca_from_scratch.py for full implementation.
""")


# =============================================================================
# NUMPY vs PYTORCH
# =============================================================================
print("\n" + "=" * 70)
print("8. NUMPY vs PYTORCH")
print("=" * 70)

import torch

A_torch = torch.tensor(A, dtype=torch.float32)

# PyTorch eigendecomposition
eigenvalues_torch, eigenvectors_torch = torch.linalg.eig(A_torch)

print("NumPy:")
print(f"  Eigenvalues: {eigenvalues}")
print(f"\nPyTorch:")
print(f"  Eigenvalues: {eigenvalues_torch}")

# For symmetric matrices, use eigh (faster, always real)
S_torch = torch.tensor(S, dtype=torch.float32)
eigenvalues_sym, eigenvectors_sym = torch.linalg.eigh(S_torch)
print(f"\nPyTorch eigh (for symmetric): {eigenvalues_sym}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  Concept            │  Formula          │  Use in Deep Learning        │
├─────────────────────────────────────────────────────────────────────────┤
│  Eigenvalue eq.     │  Av = λv          │  Understanding transformations│
│  Eigendecomposition │  A = VΛV⁻¹        │  Matrix powers, analysis      │
│  Symmetric matrices │  A = QΛQᵀ         │  Covariance, Hessian          │
│  Positive definite  │  all λ > 0        │  Convex optimization          │
│  PCA                │  eigen of cov     │  Dimensionality reduction     │
└─────────────────────────────────────────────────────────────────────────┘

Key Insights:
  • Eigenvectors = natural directions of a transformation
  • Eigenvalues = how much each direction is scaled
  • Symmetric matrices have real eigenvalues, orthogonal eigenvectors
  • PCA finds directions of maximum variance using eigendecomposition
""")
