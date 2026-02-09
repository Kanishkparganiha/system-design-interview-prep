"""
Chapter 2.1: Scalars, Vectors, Matrices, and Tensors
=====================================================
The building blocks of linear algebra and deep learning.

Run: python 01_vectors_matrices.py
"""

import numpy as np
import torch

print("=" * 70)
print("SCALARS, VECTORS, MATRICES, AND TENSORS")
print("=" * 70)


# =============================================================================
# SCALARS
# =============================================================================
print("\n" + "=" * 70)
print("1. SCALARS")
print("=" * 70)

print("""
A scalar is just a single number.
In ML, scalars are often used for:
  - Learning rate (α = 0.001)
  - Regularization strength (λ = 0.01)
  - Loss value (L = 0.523)
""")

# Python
scalar_python = 5.0

# NumPy (0-dimensional array)
scalar_numpy = np.array(5.0)

# PyTorch
scalar_torch = torch.tensor(5.0)

print(f"Python scalar: {scalar_python}, type: {type(scalar_python)}")
print(f"NumPy scalar:  {scalar_numpy}, shape: {scalar_numpy.shape}, ndim: {scalar_numpy.ndim}")
print(f"PyTorch scalar: {scalar_torch}, shape: {scalar_torch.shape}, ndim: {scalar_torch.ndim}")


# =============================================================================
# VECTORS
# =============================================================================
print("\n" + "=" * 70)
print("2. VECTORS")
print("=" * 70)

print("""
A vector is an array of numbers arranged in order.
Each element can be identified by its index.

In ML, vectors represent:
  - Feature vectors (input to model)
  - Weight vectors
  - Bias vectors
  - Gradient vectors
""")

# NumPy vector
v_numpy = np.array([1.0, 2.0, 3.0, 4.0])

# PyTorch vector
v_torch = torch.tensor([1.0, 2.0, 3.0, 4.0])

print(f"\nNumPy vector: {v_numpy}")
print(f"  Shape: {v_numpy.shape}")
print(f"  Dimensions: {v_numpy.ndim}")
print(f"  Accessing element v[2]: {v_numpy[2]}")

print(f"\nPyTorch vector: {v_torch}")
print(f"  Shape: {v_torch.shape}")
print(f"  Dimensions: {v_torch.ndim}")

# Row vs Column vectors
print("\n--- Row vs Column Vectors ---")
row_vector = np.array([[1, 2, 3]])      # Shape: (1, 3)
col_vector = np.array([[1], [2], [3]])  # Shape: (3, 1)

print(f"Row vector shape: {row_vector.shape}")
print(f"Column vector shape: {col_vector.shape}")

print("""
Note: In math notation:
  - Column vectors are default: x ∈ ℝⁿ means n×1
  - Row vectors: xᵀ (transpose)

In NumPy, 1D arrays don't distinguish row/column.
Use reshape or add dimensions when needed.
""")


# =============================================================================
# MATRICES
# =============================================================================
print("\n" + "=" * 70)
print("3. MATRICES")
print("=" * 70)

print("""
A matrix is a 2D array of numbers.
Element at row i, column j is denoted A[i,j] or Aᵢⱼ

In ML, matrices represent:
  - Weight matrices (layer connections)
  - Batches of data (rows = samples, cols = features)
  - Images (height × width for grayscale)
  - Covariance matrices
""")

# Creating matrices
M_numpy = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

M_torch = torch.tensor([
    [1., 2., 3.],
    [4., 5., 6.]
])

print(f"\nNumPy matrix:\n{M_numpy}")
print(f"  Shape: {M_numpy.shape} (rows, columns)")
print(f"  Accessing M[1,2]: {M_numpy[1, 2]}")

# Special matrices
print("\n--- Special Matrices ---")

# Identity matrix
I = np.eye(3)
print(f"\nIdentity matrix (3×3):\n{I}")
print("  Property: A × I = A, I × A = A")

# Zero matrix
Z = np.zeros((2, 3))
print(f"\nZero matrix (2×3):\n{Z}")

# Ones matrix
O = np.ones((2, 3))
print(f"\nOnes matrix (2×3):\n{O}")

# Random matrix
R = np.random.randn(2, 3)  # Standard normal distribution
print(f"\nRandom matrix (2×3):\n{R}")
print("  (Random values from standard normal distribution)")


# =============================================================================
# TENSORS
# =============================================================================
print("\n" + "=" * 70)
print("4. TENSORS")
print("=" * 70)

print("""
A tensor is a generalization to n dimensions.
  - 0D tensor: scalar
  - 1D tensor: vector
  - 2D tensor: matrix
  - 3D tensor: "cube" of numbers
  - nD tensor: generalization

In ML, tensors represent:
  - Color images: (height, width, channels) or (channels, height, width)
  - Batch of images: (batch, height, width, channels)
  - Video: (frames, height, width, channels)
  - NLP sequences: (batch, sequence_length, embedding_dim)
""")

# 3D Tensor (e.g., RGB image)
tensor_3d = np.random.randn(3, 4, 5)  # 3 channels, 4 height, 5 width
print(f"\n3D Tensor shape: {tensor_3d.shape}")
print(f"  Interpretation: 3 channels × 4 height × 5 width")

# 4D Tensor (e.g., batch of images)
tensor_4d = np.random.randn(32, 3, 28, 28)  # 32 images, 3 channels, 28×28
print(f"\n4D Tensor shape: {tensor_4d.shape}")
print(f"  Interpretation: 32 images × 3 channels × 28 height × 28 width")

# PyTorch tensors (with GPU support)
print("\n--- PyTorch Tensors ---")
t = torch.randn(3, 4, 5)
print(f"PyTorch tensor shape: {t.shape}")
print(f"  dtype: {t.dtype}")
print(f"  device: {t.device}")

# Move to GPU if available
if torch.cuda.is_available():
    t_gpu = t.cuda()
    print(f"  GPU tensor device: {t_gpu.device}")
else:
    print("  (CUDA not available)")


# =============================================================================
# INDEXING AND SLICING
# =============================================================================
print("\n" + "=" * 70)
print("5. INDEXING AND SLICING")
print("=" * 70)

M = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
])

print(f"\nMatrix M:\n{M}")
print(f"\nIndexing:")
print(f"  M[0, 0] = {M[0, 0]}  (first element)")
print(f"  M[2, 3] = {M[2, 3]}  (last element)")
print(f"  M[-1, -1] = {M[-1, -1]}  (last element using negative index)")

print(f"\nSlicing:")
print(f"  M[0, :] = {M[0, :]}  (first row)")
print(f"  M[:, 0] = {M[:, 0]}  (first column)")
print(f"  M[0:2, 1:3] =\n{M[0:2, 1:3]}  (submatrix)")

print(f"\nAdvanced indexing:")
print(f"  M[[0, 2], :] =\n{M[[0, 2], :]}  (rows 0 and 2)")
print(f"  M[M > 5] = {M[M > 5]}  (elements > 5)")


# =============================================================================
# RESHAPING
# =============================================================================
print("\n" + "=" * 70)
print("6. RESHAPING")
print("=" * 70)

print("""
Reshaping changes the dimensions without changing the data.
Critical for deep learning (e.g., flattening images for dense layers).
""")

# Original array
arr = np.arange(12)
print(f"\nOriginal array: {arr}")
print(f"  Shape: {arr.shape}")

# Reshape to 2D
reshaped_2d = arr.reshape(3, 4)
print(f"\nReshaped to (3, 4):\n{reshaped_2d}")

# Reshape to 3D
reshaped_3d = arr.reshape(2, 2, 3)
print(f"\nReshaped to (2, 2, 3):\n{reshaped_3d}")

# Flatten (back to 1D)
flattened = reshaped_3d.flatten()
print(f"\nFlattened: {flattened}")

# Using -1 for automatic dimension calculation
auto_reshape = arr.reshape(-1, 3)  # -1 means "figure it out"
print(f"\nReshape with -1: arr.reshape(-1, 3) gives shape {auto_reshape.shape}")

# PyTorch reshaping
print("\n--- PyTorch Reshaping ---")
t = torch.arange(12)
print(f"Original: {t}, shape: {t.shape}")
print(f"view(3, 4):\n{t.view(3, 4)}")
print(f"reshape(2, 6):\n{t.reshape(2, 6)}")


# =============================================================================
# BROADCASTING
# =============================================================================
print("\n" + "=" * 70)
print("7. BROADCASTING")
print("=" * 70)

print("""
Broadcasting allows operations on arrays of different shapes.
Rules:
  1. Dimensions are compared from right to left
  2. Dimensions must be equal, or one of them must be 1
  3. Missing dimensions are treated as 1
""")

# Scalar + matrix
M = np.array([[1, 2], [3, 4]])
scalar = 10
print(f"\nMatrix + Scalar:")
print(f"M =\n{M}")
print(f"M + 10 =\n{M + scalar}")

# Vector + matrix
v = np.array([10, 20])  # Shape (2,)
print(f"\nMatrix + Vector (row broadcast):")
print(f"v = {v}")
print(f"M + v =\n{M + v}")
print("  Each row of M gets v added to it")

# Column vector + matrix
v_col = np.array([[100], [200]])  # Shape (2, 1)
print(f"\nMatrix + Column Vector:")
print(f"v_col =\n{v_col}")
print(f"M + v_col =\n{M + v_col}")
print("  Each column of M gets v_col added to it")

# More complex broadcasting
A = np.ones((3, 4, 5))
B = np.ones((4, 5))
C = np.ones((5,))
print(f"\nComplex broadcasting:")
print(f"  A.shape = {A.shape}")
print(f"  B.shape = {B.shape}")
print(f"  (A + B).shape = {(A + B).shape}")
print(f"  (A + C).shape = {(A + C).shape}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│  Structure    │  Dimensions  │  Shape Example  │  ML Use Case       │
├─────────────────────────────────────────────────────────────────────┤
│  Scalar       │  0           │  ()             │  Loss, learning rate│
│  Vector       │  1           │  (n,)           │  Features, weights  │
│  Matrix       │  2           │  (m, n)         │  Weight matrix      │
│  3D Tensor    │  3           │  (c, h, w)      │  Single image       │
│  4D Tensor    │  4           │  (b, c, h, w)   │  Batch of images    │
└─────────────────────────────────────────────────────────────────────┘

Key Operations:
  - Indexing: M[i, j]
  - Slicing: M[start:end, :]
  - Reshaping: arr.reshape(new_shape)
  - Broadcasting: automatic shape matching
""")
