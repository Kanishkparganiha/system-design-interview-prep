"""
Chapter 2: Solving Linear Systems
=================================
Understanding Ax = b and its applications in ML.

Run: python 06_linear_systems.py
"""

import numpy as np

print("=" * 70)
print("SOLVING LINEAR SYSTEMS")
print("=" * 70)


# =============================================================================
# 1. WHAT IS A LINEAR SYSTEM?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHAT IS A LINEAR SYSTEM?")
print("=" * 70)

print("""
A linear system is a set of linear equations:

    2x + 3y = 8
    4x + 5y = 14

In matrix form: Ax = b

    [2 3] [x]   [8]
    [4 5] [y] = [14]

    A  ·  x  =  b

Why does this matter in ML?
    - Least squares regression: (X^T X) w = X^T y
    - Normal equations for linear regression
    - Principal Component Analysis
    - Many optimization algorithms
""")


# =============================================================================
# 2. SOLVING Ax = b
# =============================================================================
print("\n" + "=" * 70)
print("2. SOLVING Ax = b")
print("=" * 70)

# Example system
A = np.array([[2, 3],
              [4, 5]])
b = np.array([8, 14])

print("System:")
print(f"A = \n{A}")
print(f"b = {b}")

# Method 1: Using inverse (NOT recommended for large systems)
print("\n--- Method 1: Using Inverse (x = A⁻¹b) ---")
A_inv = np.linalg.inv(A)
x_inv = A_inv @ b
print(f"A⁻¹ = \n{A_inv}")
print(f"x = A⁻¹b = {x_inv}")

# Method 2: Using np.linalg.solve (Recommended)
print("\n--- Method 2: np.linalg.solve (Recommended) ---")
x_solve = np.linalg.solve(A, b)
print(f"x = {x_solve}")

# Verify
print(f"\nVerification: Ax = {A @ x_solve}")
print(f"b = {b}")
print(f"Match: {np.allclose(A @ x_solve, b)}")


# =============================================================================
# 3. LINEAR INDEPENDENCE
# =============================================================================
print("\n" + "=" * 70)
print("3. LINEAR INDEPENDENCE")
print("=" * 70)

print("""
Vectors are linearly independent if no vector can be written
as a linear combination of the others.

Example of linearly DEPENDENT vectors:
    v1 = [1, 2]
    v2 = [2, 4]  (v2 = 2*v1)

Example of linearly INDEPENDENT vectors:
    v1 = [1, 0]
    v2 = [0, 1]
""")

# Check via rank
independent = np.array([[1, 0], [0, 1]])
dependent = np.array([[1, 2], [2, 4]])

print("Independent vectors:")
print(independent)
print(f"Rank: {np.linalg.matrix_rank(independent)}")
print(f"Determinant: {np.linalg.det(independent):.4f}")

print("\nDependent vectors:")
print(dependent)
print(f"Rank: {np.linalg.matrix_rank(dependent)}")
print(f"Determinant: {np.linalg.det(dependent):.4f}")

print("""
Key insight:
    - Full rank → All vectors independent → Unique solution exists
    - Rank deficient → Dependent vectors → No unique solution
    - det(A) = 0 → Singular matrix → No inverse exists
""")


# =============================================================================
# 4. OVERDETERMINED SYSTEMS (More equations than unknowns)
# =============================================================================
print("\n" + "=" * 70)
print("4. OVERDETERMINED SYSTEMS (Least Squares)")
print("=" * 70)

print("""
When we have more equations than unknowns:
    - No exact solution may exist
    - Find the best approximate solution (least squares)

This is LINEAR REGRESSION!

    X @ w ≈ y

    Find w that minimizes ||Xw - y||²
""")

# Example: Fitting a line y = mx + c to noisy data
np.random.seed(42)
x_data = np.linspace(0, 10, 20)
y_data = 2 * x_data + 1 + np.random.randn(20) * 2  # True line: y = 2x + 1

# Create design matrix [x, 1]
X = np.column_stack([x_data, np.ones_like(x_data)])

print(f"X shape: {X.shape} (20 equations, 2 unknowns)")
print(f"y shape: {y_data.shape}")

# Method 1: Normal equations: (X^T X) w = X^T y
print("\n--- Method 1: Normal Equations ---")
XtX = X.T @ X
Xty = X.T @ y_data
w_normal = np.linalg.solve(XtX, Xty)
print(f"w = [slope, intercept] = {w_normal}")
print(f"True values: [2, 1]")

# Method 2: np.linalg.lstsq
print("\n--- Method 2: np.linalg.lstsq ---")
w_lstsq, residuals, rank, s = np.linalg.lstsq(X, y_data, rcond=None)
print(f"w = {w_lstsq}")
print(f"Residuals (sum of squared errors): {residuals[0]:.4f}")


# =============================================================================
# 5. UNDERDETERMINED SYSTEMS (More unknowns than equations)
# =============================================================================
print("\n" + "=" * 70)
print("5. UNDERDETERMINED SYSTEMS")
print("=" * 70)

print("""
When we have fewer equations than unknowns:
    - Infinitely many solutions
    - Need additional constraints (e.g., minimum norm)

Used in:
    - Compressed sensing
    - Neural network training (model has more parameters than data points)
""")

# Example: 1 equation, 3 unknowns
A_under = np.array([[1, 2, 3]])
b_under = np.array([6])

print(f"A = {A_under}")
print(f"b = {b_under}")
print("Equation: x + 2y + 3z = 6")

# Get minimum norm solution using pseudo-inverse
x_min_norm = np.linalg.pinv(A_under) @ b_under
print(f"\nMinimum norm solution: {x_min_norm}")
print(f"Verification: Ax = {A_under @ x_min_norm}")
print(f"||x||² = {np.sum(x_min_norm**2):.4f}")


# =============================================================================
# 6. PSEUDO-INVERSE (Moore-Penrose)
# =============================================================================
print("\n" + "=" * 70)
print("6. PSEUDO-INVERSE (Moore-Penrose)")
print("=" * 70)

print("""
The pseudo-inverse A⁺ works for ANY matrix (not just square invertible):

    - If A is m×n:  A⁺ is n×m
    - Overdetermined (m > n): A⁺ = (AᵀA)⁻¹Aᵀ (least squares)
    - Underdetermined (m < n): A⁺ = Aᵀ(AAᵀ)⁻¹ (minimum norm)

Computed via SVD: A = UΣVᵀ  →  A⁺ = VΣ⁺Uᵀ
""")

# Example
A_rect = np.array([[1, 2], [3, 4], [5, 6]])
A_pinv = np.linalg.pinv(A_rect)

print(f"A shape: {A_rect.shape}")
print(f"A⁺ shape: {A_pinv.shape}")
print(f"\nA⁺ @ A (should be close to identity):\n{A_pinv @ A_rect}")


# =============================================================================
# 7. NUMERICAL CONSIDERATIONS
# =============================================================================
print("\n" + "=" * 70)
print("7. NUMERICAL CONSIDERATIONS")
print("=" * 70)

print("""
Condition Number:
    - Measures sensitivity of solution to input perturbations
    - High condition number → ill-conditioned → numerically unstable

    κ(A) = ||A|| · ||A⁻¹|| = σ_max / σ_min

    κ ≈ 1: Well-conditioned
    κ >> 1: Ill-conditioned
    κ = ∞: Singular
""")

# Well-conditioned matrix
A_good = np.array([[1, 0], [0, 1]])
print(f"Identity matrix condition number: {np.linalg.cond(A_good):.4f}")

# Ill-conditioned matrix (nearly singular)
A_bad = np.array([[1, 2], [1, 2.0001]])
print(f"Nearly singular matrix condition number: {np.linalg.cond(A_bad):.4f}")

print("""
Practical advice:
    1. Use np.linalg.solve() instead of computing inverse
    2. Check condition number for stability
    3. Use regularization for ill-conditioned problems
""")


# =============================================================================
# 8. APPLICATION: LINEAR REGRESSION
# =============================================================================
print("\n" + "=" * 70)
print("8. APPLICATION: LINEAR REGRESSION")
print("=" * 70)

print("""
Full linear regression example:

Given data points (x_i, y_i), find w that minimizes:

    min_w ||Xw - y||²

Solution: w = (XᵀX)⁻¹Xᵀy = X⁺y
""")

# Generate synthetic data for multiple linear regression
np.random.seed(42)
n_samples = 100
n_features = 3

# True weights
w_true = np.array([2.5, -1.0, 0.5])
bias_true = 3.0

# Generate features
X_train = np.random.randn(n_samples, n_features)
y_train = X_train @ w_true + bias_true + np.random.randn(n_samples) * 0.5

# Add bias column
X_design = np.column_stack([X_train, np.ones(n_samples)])

# Solve using normal equations
w_learned = np.linalg.lstsq(X_design, y_train, rcond=None)[0]

print(f"True weights: {w_true}, bias: {bias_true}")
print(f"Learned weights: {w_learned[:3].round(3)}, bias: {w_learned[3]:.3f}")

# Compute R² score
y_pred = X_design @ w_learned
ss_res = np.sum((y_train - y_pred) ** 2)
ss_tot = np.sum((y_train - np.mean(y_train)) ** 2)
r2 = 1 - ss_res / ss_tot
print(f"R² score: {r2:.4f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
Key Concepts:
─────────────
1. Linear systems: Ax = b
2. Solutions depend on rank of A
3. Overdetermined → least squares
4. Underdetermined → minimum norm
5. Pseudo-inverse handles all cases
6. Condition number measures stability

ML Connections:
───────────────
• Linear regression = solving overdetermined system
• Normal equations: w = (XᵀX)⁻¹Xᵀy
• Regularization helps ill-conditioned problems
• Most neural network optimization is about solving Ax = b iteratively

NumPy Functions:
───────────────
np.linalg.solve(A, b)     # Solve Ax = b (square A)
np.linalg.lstsq(A, b)     # Least squares (any A)
np.linalg.inv(A)          # Matrix inverse
np.linalg.pinv(A)         # Pseudo-inverse
np.linalg.matrix_rank(A)  # Rank
np.linalg.cond(A)         # Condition number
""")
