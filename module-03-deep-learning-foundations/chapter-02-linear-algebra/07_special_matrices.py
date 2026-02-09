"""
Chapter 2: Special Matrices
===========================
Matrices with special properties that appear frequently in ML.

Run: python 07_special_matrices.py
"""

import numpy as np

print("=" * 70)
print("SPECIAL MATRICES IN MACHINE LEARNING")
print("=" * 70)


# =============================================================================
# 1. DIAGONAL MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("1. DIAGONAL MATRICES")
print("=" * 70)

print("""
Diagonal matrix: Only diagonal elements are non-zero.

    D = [d₁  0   0 ]
        [0   d₂  0 ]
        [0   0   d₃]

Properties:
    - D @ x scales each element: [d₁x₁, d₂x₂, d₃x₃]
    - Easy inverse: D⁻¹ has 1/dᵢ on diagonal
    - Eigenvalues ARE the diagonal elements

ML uses:
    - Scaling features (StandardScaler)
    - Attention weights (in diagonal form)
    - Learning rate per parameter
""")

# Create diagonal matrix
d = np.array([2, 3, 4])
D = np.diag(d)

print(f"Diagonal values: {d}")
print(f"Diagonal matrix D:\n{D}")

# Multiplication is scaling
x = np.array([1, 1, 1])
print(f"\nx = {x}")
print(f"D @ x = {D @ x}")

# Inverse
D_inv = np.diag(1/d)
print(f"\nD⁻¹:\n{D_inv}")
print(f"D @ D⁻¹:\n{D @ D_inv}")

# Eigenvalues
eigenvalues = np.linalg.eigvals(D)
print(f"\nEigenvalues: {eigenvalues}")
print(f"Diagonal elements: {d}")


# =============================================================================
# 2. SYMMETRIC MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("2. SYMMETRIC MATRICES")
print("=" * 70)

print("""
Symmetric matrix: A = Aᵀ

Properties:
    - All eigenvalues are REAL
    - Eigenvectors are ORTHOGONAL
    - Can be diagonalized: A = QΛQᵀ (spectral theorem)

ML uses:
    - Covariance matrices (always symmetric!)
    - Gram matrices (XᵀX)
    - Hessian matrices (second derivatives)
    - Kernel matrices
""")

# Create symmetric matrix
A = np.array([[4, 2, 1],
              [2, 5, 3],
              [1, 3, 6]])

print(f"A:\n{A}")
print(f"\nAᵀ:\n{A.T}")
print(f"\nA == Aᵀ: {np.allclose(A, A.T)}")

# Eigendecomposition
eigenvalues, eigenvectors = np.linalg.eigh(A)  # eigh for symmetric
print(f"\nEigenvalues (all real): {eigenvalues}")

# Eigenvectors are orthogonal
print(f"\nEigenvectors orthogonal? QᵀQ:\n{(eigenvectors.T @ eigenvectors).round(6)}")

# Covariance matrix example
print("\n--- Covariance Matrix Example ---")
np.random.seed(42)
data = np.random.randn(100, 3)
cov_matrix = np.cov(data.T)
print(f"Covariance matrix:\n{cov_matrix.round(3)}")
print(f"Is symmetric: {np.allclose(cov_matrix, cov_matrix.T)}")


# =============================================================================
# 3. ORTHOGONAL MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("3. ORTHOGONAL MATRICES")
print("=" * 70)

print("""
Orthogonal matrix: QᵀQ = QQᵀ = I (inverse is transpose!)

Properties:
    - Columns are orthonormal vectors
    - Preserves lengths: ||Qx|| = ||x||
    - Preserves angles
    - det(Q) = ±1

ML uses:
    - Rotations (data augmentation)
    - Orthogonal weight initialization
    - PCA (eigenvectors form orthogonal matrix)
    - Gram-Schmidt orthogonalization
""")

# Create orthogonal matrix (rotation)
theta = np.pi / 4  # 45 degrees
Q = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

print(f"Rotation matrix (45°):\n{Q.round(4)}")
print(f"\nQᵀQ:\n{(Q.T @ Q).round(6)}")
print(f"\ndet(Q): {np.linalg.det(Q):.4f}")

# Preserves length
x = np.array([3, 4])
Qx = Q @ x
print(f"\nx = {x}, ||x|| = {np.linalg.norm(x)}")
print(f"Qx = {Qx.round(4)}, ||Qx|| = {np.linalg.norm(Qx):.4f}")


# =============================================================================
# 4. POSITIVE DEFINITE MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("4. POSITIVE DEFINITE (PD) MATRICES")
print("=" * 70)

print("""
Positive definite: xᵀAx > 0 for all x ≠ 0

Properties:
    - All eigenvalues are POSITIVE
    - Symmetric and PD → has unique Cholesky decomposition
    - A = LLᵀ where L is lower triangular

ML uses:
    - Covariance matrices (must be positive semi-definite)
    - Hessian at minimum (positive definite)
    - Kernel matrices (Gram matrices)
    - Mahalanobis distance
""")

# Create positive definite matrix
A_pd = np.array([[4, 2],
                 [2, 3]])

print(f"A:\n{A_pd}")

# Check eigenvalues
eigenvalues = np.linalg.eigvals(A_pd)
print(f"\nEigenvalues: {eigenvalues}")
print(f"All positive: {all(eigenvalues > 0)}")

# xᵀAx test
x = np.array([1, 2])
xAx = x.T @ A_pd @ x
print(f"\nx = {x}")
print(f"xᵀAx = {xAx} > 0: {xAx > 0}")

# Cholesky decomposition
L = np.linalg.cholesky(A_pd)
print(f"\nCholesky decomposition L:\n{L}")
print(f"LLᵀ:\n{L @ L.T}")


# =============================================================================
# 5. SPARSE MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("5. SPARSE MATRICES")
print("=" * 70)

print("""
Sparse matrix: Most elements are zero.

Properties:
    - Efficient storage (only store non-zeros)
    - Fast operations (skip zeros)

ML uses:
    - One-hot encodings
    - Bag of words / TF-IDF
    - Graph adjacency matrices
    - Convolution kernels
""")

from scipy import sparse

# Create sparse matrix
dense = np.array([[1, 0, 0, 2],
                  [0, 0, 3, 0],
                  [0, 0, 0, 0],
                  [4, 0, 0, 5]])

sp = sparse.csr_matrix(dense)

print(f"Dense matrix:\n{dense}")
print(f"\nSparse representation (CSR):")
print(f"Data: {sp.data}")
print(f"Indices: {sp.indices}")
print(f"Indptr: {sp.indptr}")

print(f"\nMemory comparison:")
print(f"Dense: {dense.nbytes} bytes")
print(f"Sparse: {sp.data.nbytes + sp.indices.nbytes + sp.indptr.nbytes} bytes")

# One-hot encoding example
print("\n--- One-Hot Encoding (Sparse) ---")
labels = [0, 2, 1, 0, 2]
n_classes = 3
one_hot = sparse.eye(n_classes, format='csr')[labels]
print(f"Labels: {labels}")
print(f"One-hot (dense):\n{one_hot.toarray()}")


# =============================================================================
# 6. IDENTITY MATRIX
# =============================================================================
print("\n" + "=" * 70)
print("6. IDENTITY MATRIX")
print("=" * 70)

print("""
Identity matrix: 1s on diagonal, 0s elsewhere.

    I = [1 0 0]
        [0 1 0]
        [0 0 1]

Properties:
    - AI = IA = A (multiplicative identity)
    - I⁻¹ = I
    - All eigenvalues = 1

ML uses:
    - Regularization: (XᵀX + λI)⁻¹Xᵀy
    - Skip connections: y = F(x) + Ix
    - Weight initialization
""")

I = np.eye(3)
print(f"Identity matrix I:\n{I}")

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"\nA @ I == A: {np.allclose(A @ I, A)}")
print(f"I @ A == A: {np.allclose(I @ A, A)}")

# Regularization example
print("\n--- Ridge Regression (L2 Regularization) ---")
print("(XᵀX + λI)⁻¹Xᵀy prevents overfitting by adding λI")


# =============================================================================
# 7. TRIANGULAR MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("7. TRIANGULAR MATRICES")
print("=" * 70)

print("""
Lower triangular: All elements above diagonal are 0
Upper triangular: All elements below diagonal are 0

Properties:
    - Determinant = product of diagonal elements
    - Easy to solve linear systems (back/forward substitution)
    - LU decomposition: A = LU

ML uses:
    - Cholesky decomposition (for sampling)
    - Attention masks (causal/autoregressive)
    - QR decomposition
""")

L = np.array([[1, 0, 0],
              [2, 3, 0],
              [4, 5, 6]])

U = np.array([[1, 2, 3],
              [0, 4, 5],
              [0, 0, 6]])

print(f"Lower triangular L:\n{L}")
print(f"\nUpper triangular U:\n{U}")
print(f"\ndet(L) = {np.linalg.det(L):.1f} = {1*3*6}")
print(f"det(U) = {np.linalg.det(U):.1f} = {1*4*6}")

# Attention mask example
print("\n--- Causal Attention Mask (Transformer) ---")
seq_len = 5
causal_mask = np.tril(np.ones((seq_len, seq_len)))
print(f"Causal mask (lower triangular):\n{causal_mask}")
print("Position i can only attend to positions 0..i")


# =============================================================================
# 8. LOW-RANK MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("8. LOW-RANK MATRICES")
print("=" * 70)

print("""
Low-rank matrix: rank(A) << min(m, n)

Can be written as: A = UVᵀ where U (m×k), V (n×k), k = rank

Properties:
    - Efficient storage: O(k(m+n)) instead of O(mn)
    - Fast multiplication

ML uses:
    - Matrix factorization (recommender systems)
    - LoRA (Low-Rank Adaptation for LLMs)
    - Dimensionality reduction
""")

# Full matrix
m, n = 100, 80
k = 5  # Low rank

# Create low-rank matrix as UV^T
np.random.seed(42)
U = np.random.randn(m, k)
V = np.random.randn(n, k)
A_low_rank = U @ V.T

print(f"Full matrix shape: {A_low_rank.shape}")
print(f"Rank: {np.linalg.matrix_rank(A_low_rank)}")
print(f"\nStorage comparison:")
print(f"Full matrix: {m * n} values")
print(f"Low-rank (U, V): {m * k + n * k} values")
print(f"Compression ratio: {(m * n) / (m * k + n * k):.1f}x")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: SPECIAL MATRICES")
print("=" * 70)

print("""
┌─────────────────┬────────────────────────────────────────────────────┐
│ Matrix Type     │ Key Property & ML Use                              │
├─────────────────┼────────────────────────────────────────────────────┤
│ Diagonal        │ Dᵢⱼ = 0 if i≠j | Scaling, per-param learning rates │
│ Symmetric       │ A = Aᵀ | Covariance, Hessian, kernel matrices     │
│ Orthogonal      │ QᵀQ = I | Rotations, preserves geometry           │
│ Positive Def.   │ xᵀAx > 0 | Covariance, convex optimization        │
│ Sparse          │ Mostly zeros | One-hot, text, graphs              │
│ Identity        │ AI = A | Regularization, skip connections         │
│ Triangular      │ Zeros above/below | Cholesky, attention masks     │
│ Low-Rank        │ A = UVᵀ | Compression, LoRA, factorization        │
└─────────────────┴────────────────────────────────────────────────────┘

NumPy Creation Functions:
─────────────────────────
np.diag(v)           # Diagonal matrix from vector
np.eye(n)            # Identity matrix
np.tril(A)           # Lower triangular
np.triu(A)           # Upper triangular
sparse.csr_matrix(A) # Sparse matrix
np.linalg.cholesky(A)# Cholesky decomposition (returns L)
""")
