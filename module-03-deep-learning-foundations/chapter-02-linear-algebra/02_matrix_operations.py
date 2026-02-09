"""
Chapter 2.2: Matrix Operations
==============================
The fundamental operations used in every neural network.

Run: python 02_matrix_operations.py
"""

import numpy as np
import torch

print("=" * 70)
print("MATRIX OPERATIONS")
print("=" * 70)


# =============================================================================
# TRANSPOSE
# =============================================================================
print("\n" + "=" * 70)
print("1. TRANSPOSE")
print("=" * 70)

print("""
Transpose flips a matrix over its diagonal.
(Aᵀ)ᵢⱼ = Aⱼᵢ

Rows become columns, columns become rows.
Shape (m, n) → (n, m)
""")

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(f"A (2×3):\n{A}")
print(f"\nAᵀ (3×2):\n{A.T}")

# Properties
print("\nProperties of Transpose:")
B = np.array([[1, 2], [3, 4]])
print(f"  (Aᵀ)ᵀ = A: {np.allclose((A.T).T, A)}")
print(f"  (AB)ᵀ = BᵀAᵀ: {np.allclose((A @ B).T, B.T @ A.T)}")
print(f"  (A + B)ᵀ = Aᵀ + Bᵀ: (for same-shaped matrices)")


# =============================================================================
# MATRIX ADDITION
# =============================================================================
print("\n" + "=" * 70)
print("2. MATRIX ADDITION")
print("=" * 70)

print("""
Element-wise addition. Matrices must have the same shape.
(A + B)ᵢⱼ = Aᵢⱼ + Bᵢⱼ
""")

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"A:\n{A}")
print(f"\nB:\n{B}")
print(f"\nA + B:\n{A + B}")

# Properties
print("\nProperties:")
print(f"  Commutative: A + B = B + A: {np.allclose(A + B, B + A)}")
print(f"  Associative: (A + B) + C = A + (B + C)")


# =============================================================================
# SCALAR MULTIPLICATION
# =============================================================================
print("\n" + "=" * 70)
print("3. SCALAR MULTIPLICATION")
print("=" * 70)

print("""
Multiply every element by a scalar.
(cA)ᵢⱼ = c × Aᵢⱼ
""")

A = np.array([[1, 2], [3, 4]])
c = 3

print(f"A:\n{A}")
print(f"\n3 × A:\n{c * A}")


# =============================================================================
# MATRIX MULTIPLICATION
# =============================================================================
print("\n" + "=" * 70)
print("4. MATRIX MULTIPLICATION")
print("=" * 70)

print("""
The most important operation in deep learning!

For A (m×n) and B (n×p), the product C = AB has shape (m×p).
Cᵢⱼ = Σₖ Aᵢₖ × Bₖⱼ

Rule: Inner dimensions must match!
      (m×n) @ (n×p) = (m×p)
           ↑   ↑
         must match
""")

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])  # 2×3

B = np.array([
    [7, 8],
    [9, 10],
    [11, 12]
])  # 3×2

print(f"A (2×3):\n{A}")
print(f"\nB (3×2):\n{B}")
print(f"\nA @ B (2×2):\n{A @ B}")

# Step by step computation
print("\n--- How it's computed ---")
C = A @ B
print(f"C[0,0] = 1×7 + 2×9 + 3×11 = {1*7 + 2*9 + 3*11} ✓ {C[0,0]}")
print(f"C[0,1] = 1×8 + 2×10 + 3×12 = {1*8 + 2*10 + 3*12} ✓ {C[0,1]}")
print(f"C[1,0] = 4×7 + 5×9 + 6×11 = {4*7 + 5*9 + 6*11} ✓ {C[1,0]}")
print(f"C[1,1] = 4×8 + 5×10 + 6×12 = {4*8 + 5*10 + 6*12} ✓ {C[1,1]}")

# Properties
print("\nProperties of Matrix Multiplication:")
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = np.array([[1, 0], [0, 1]])

print(f"  Associative: (AB)C = A(BC): {np.allclose((A @ B) @ C, A @ (B @ C))}")
print(f"  Distributive: A(B + C) = AB + AC: {np.allclose(A @ (B + C), A @ B + A @ C)}")
print(f"  NOT Commutative: AB ≠ BA generally: {not np.allclose(A @ B, B @ A)}")

# Matrix-vector multiplication
print("\n--- Matrix-Vector Multiplication ---")
W = np.array([[1, 2, 3], [4, 5, 6]])  # 2×3
x = np.array([1, 0, 1])  # 3×1 (column vector)

print(f"W (2×3):\n{W}")
print(f"x (3,): {x}")
print(f"W @ x (2,): {W @ x}")
print("\nThis is how neural networks compute: output = W @ input")


# =============================================================================
# ELEMENT-WISE (HADAMARD) PRODUCT
# =============================================================================
print("\n" + "=" * 70)
print("5. ELEMENT-WISE (HADAMARD) PRODUCT")
print("=" * 70)

print("""
Element-wise multiplication (NOT matrix multiplication).
(A ⊙ B)ᵢⱼ = Aᵢⱼ × Bᵢⱼ

Used in: Attention mechanisms, gating in LSTMs
""")

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print(f"A:\n{A}")
print(f"\nB:\n{B}")
print(f"\nA * B (element-wise):\n{A * B}")
print(f"\nA @ B (matrix multiply):\n{A @ B}")
print("\n⚠️  These are DIFFERENT operations!")


# =============================================================================
# DOT PRODUCT
# =============================================================================
print("\n" + "=" * 70)
print("6. DOT PRODUCT (INNER PRODUCT)")
print("=" * 70)

print("""
For vectors a and b, dot product is:
a · b = Σᵢ aᵢ × bᵢ = aᵀb

Result is a scalar.
Measures similarity between vectors.
""")

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(f"a = {a}")
print(f"b = {b}")
print(f"a · b = 1×4 + 2×5 + 3×6 = {np.dot(a, b)}")

# Geometric interpretation
print("\n--- Geometric Interpretation ---")
print("a · b = |a| × |b| × cos(θ)")
print(f"|a| = {np.linalg.norm(a):.3f}")
print(f"|b| = {np.linalg.norm(b):.3f}")
cos_theta = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(f"cos(θ) = {cos_theta:.3f}")
print(f"θ = {np.degrees(np.arccos(cos_theta)):.1f}°")

# Perpendicular vectors
print("\n--- Perpendicular Vectors ---")
a = np.array([1, 0])
b = np.array([0, 1])
print(f"a = {a}, b = {b}")
print(f"a · b = {np.dot(a, b)} (perpendicular if dot product = 0)")


# =============================================================================
# MATRIX INVERSE
# =============================================================================
print("\n" + "=" * 70)
print("7. MATRIX INVERSE")
print("=" * 70)

print("""
For square matrix A, its inverse A⁻¹ satisfies:
A × A⁻¹ = A⁻¹ × A = I (identity matrix)

Used to solve systems: Ax = b → x = A⁻¹b
""")

A = np.array([[4, 7], [2, 6]])

print(f"A:\n{A}")
A_inv = np.linalg.inv(A)
print(f"\nA⁻¹:\n{A_inv}")
print(f"\nVerification - A @ A⁻¹:\n{A @ A_inv}")
print("(Should be identity matrix)")

# When inverse doesn't exist
print("\n--- Singular Matrices ---")
print("""
A matrix is SINGULAR (non-invertible) if:
  - Determinant = 0
  - Rows/columns are linearly dependent
  - Cannot solve Ax = b uniquely
""")

singular = np.array([[1, 2], [2, 4]])  # Row 2 = 2 × Row 1
print(f"Singular matrix:\n{singular}")
print(f"Determinant: {np.linalg.det(singular):.6f}")

# Pseudo-inverse
print("\n--- Pseudo-Inverse (Moore-Penrose) ---")
print("For non-square or singular matrices, use pseudo-inverse A⁺")
A_rect = np.array([[1, 2], [3, 4], [5, 6]])  # 3×2
A_pinv = np.linalg.pinv(A_rect)
print(f"A (3×2):\n{A_rect}")
print(f"\nA⁺ (2×3):\n{A_pinv}")


# =============================================================================
# DETERMINANT
# =============================================================================
print("\n" + "=" * 70)
print("8. DETERMINANT")
print("=" * 70)

print("""
The determinant measures how a matrix scales area/volume.
  det(A) > 0: preserves orientation
  det(A) < 0: flips orientation
  det(A) = 0: collapses dimension (singular)
""")

A = np.array([[3, 1], [2, 4]])
print(f"A:\n{A}")
print(f"det(A) = 3×4 - 1×2 = {np.linalg.det(A):.0f}")

# 2×2 formula
print("\n--- 2×2 Determinant Formula ---")
print("""
det([[a, b], [c, d]]) = ad - bc
""")

# 3×3 determinant
B = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"\nB:\n{B}")
print(f"det(B) = {np.linalg.det(B):.6f}")
print("(Close to 0 → nearly singular)")


# =============================================================================
# TRACE
# =============================================================================
print("\n" + "=" * 70)
print("9. TRACE")
print("=" * 70)

print("""
Trace is the sum of diagonal elements.
Tr(A) = Σᵢ Aᵢᵢ

Properties:
  Tr(A) = Tr(Aᵀ)
  Tr(ABC) = Tr(CAB) = Tr(BCA)  (cyclic property)
  Tr(A) = sum of eigenvalues
""")

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"A:\n{A}")
print(f"Tr(A) = 1 + 5 + 9 = {np.trace(A)}")


# =============================================================================
# NEURAL NETWORK EXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("10. NEURAL NETWORK: PUTTING IT TOGETHER")
print("=" * 70)

print("""
A single dense layer: y = Wx + b

Where:
  x = input vector (features)
  W = weight matrix
  b = bias vector
  y = output vector
""")

# Simulating a layer
input_dim = 4
output_dim = 3
batch_size = 2

# Random weights and bias
np.random.seed(42)
W = np.random.randn(output_dim, input_dim)  # 3×4
b = np.random.randn(output_dim)             # 3

# Input batch (2 samples, 4 features each)
X = np.random.randn(batch_size, input_dim)  # 2×4

print(f"Input X (batch_size×input_dim = {batch_size}×{input_dim}):\n{X}")
print(f"\nWeights W (output_dim×input_dim = {output_dim}×{input_dim}):\n{W}")
print(f"\nBias b (output_dim = {output_dim}): {b}")

# Forward pass
# For batch: Y = XWᵀ + b (each row of X gets transformed)
Y = X @ W.T + b

print(f"\nOutput Y = XWᵀ + b (batch_size×output_dim = {batch_size}×{output_dim}):\n{Y}")

print("""
This is the core computation of neural networks!
  - Matrix multiplication: X @ W.T
  - Broadcasting: + b (added to each sample)
  - Activation function would be applied next (e.g., ReLU)
""")


# =============================================================================
# PYTORCH COMPARISON
# =============================================================================
print("\n" + "=" * 70)
print("11. PYTORCH EQUIVALENT")
print("=" * 70)

# Convert to PyTorch
X_torch = torch.tensor(X, dtype=torch.float32)
W_torch = torch.tensor(W, dtype=torch.float32)
b_torch = torch.tensor(b, dtype=torch.float32)

# Using nn.Linear
import torch.nn as nn

linear_layer = nn.Linear(input_dim, output_dim, bias=True)

# Set weights manually to match
with torch.no_grad():
    linear_layer.weight.copy_(W_torch)
    linear_layer.bias.copy_(b_torch)

Y_torch = linear_layer(X_torch)

print(f"PyTorch nn.Linear output:\n{Y_torch.detach().numpy()}")
print(f"\nMatches NumPy: {np.allclose(Y, Y_torch.detach().numpy())}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│  Operation           │  Symbol  │  NumPy          │  Use in DL      │
├─────────────────────────────────────────────────────────────────────┤
│  Transpose           │  Aᵀ      │  A.T            │  Backprop       │
│  Matrix Multiply     │  AB      │  A @ B          │  Forward pass   │
│  Element-wise Mult   │  A ⊙ B   │  A * B          │  Attention      │
│  Dot Product         │  a·b     │  np.dot(a,b)    │  Similarity     │
│  Inverse             │  A⁻¹     │  np.linalg.inv  │  Solving systems│
│  Determinant         │  det(A)  │  np.linalg.det  │  Volume scaling │
│  Trace               │  Tr(A)   │  np.trace(A)    │  Sum of eigenval│
└─────────────────────────────────────────────────────────────────────┘
""")
