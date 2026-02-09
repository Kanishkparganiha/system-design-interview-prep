# Chapter 2: Linear Algebra

> "Linear algebra is the branch of mathematics concerning linear equations, linear maps, and their representations in vector spaces and through matrices."

---

## Why Linear Algebra for Deep Learning?

```
Neural Network = Lots of Matrix Multiplications + Nonlinearities

Input [784] ──▶ Weight [784×256] ──▶ Hidden [256] ──▶ Weight [256×10] ──▶ Output [10]
              (matrix multiply)                   (matrix multiply)
```

Every forward pass, every backpropagation, every optimization step — it's all linear algebra.

---

## Scripts in This Chapter

| Script | Topic | Key Concepts |
|--------|-------|--------------|
| `01_vectors_matrices.py` | Basics | Scalars, vectors, matrices, tensors, broadcasting |
| `02_matrix_operations.py` | Operations | Multiplication, transpose, inverse, neural net example |
| `03_norms.py` | Norms | L1, L2, Frobenius, regularization connection |
| `04_eigendecomposition.py` | Eigen | Eigenvalues, eigenvectors, PCA preview |
| `05_svd.py` | SVD | Singular Value Decomposition, compression |
| `06_linear_systems.py` | Systems | Solving Ax = b, least squares, pseudo-inverse |
| `07_special_matrices.py` | Special Types | Diagonal, symmetric, orthogonal, positive definite |
| `08_pca_from_scratch.py` | Application | Complete PCA implementation and comparison

---

## Key Concepts

### 1. Scalars, Vectors, Matrices, Tensors

```
Scalar:  x = 5                    (0-dimensional)
Vector:  x = [1, 2, 3]            (1-dimensional)
Matrix:  X = [[1,2], [3,4]]       (2-dimensional)
Tensor:  X = [[[1,2],[3,4]],      (n-dimensional)
              [[5,6],[7,8]]]
```

### 2. Matrix Multiplication

```
A (m×n) × B (n×p) = C (m×p)

[a₁₁ a₁₂]   [b₁₁ b₁₂]   [a₁₁b₁₁+a₁₂b₂₁  a₁₁b₁₂+a₁₂b₂₂]
[a₂₁ a₂₂] × [b₂₁ b₂₂] = [a₂₁b₁₁+a₂₂b₂₁  a₂₁b₁₂+a₂₂b₂₂]

Deep Learning: Input × Weights = Output
```

### 3. Eigendecomposition

```
Av = λv

A = matrix
v = eigenvector (direction unchanged by A)
λ = eigenvalue (how much v is scaled)

A = VΛV⁻¹  (decomposition)
```

### 4. Singular Value Decomposition (SVD)

```
A = UΣVᵀ

U = left singular vectors (m×m)
Σ = singular values (diagonal, m×n)
V = right singular vectors (n×n)

Used for: PCA, compression, recommender systems
```

---

## Quick Reference

### NumPy Cheat Sheet

```python
import numpy as np

# Creating arrays
v = np.array([1, 2, 3])           # Vector
M = np.array([[1, 2], [3, 4]])    # Matrix
I = np.eye(3)                      # Identity matrix
Z = np.zeros((3, 3))               # Zero matrix

# Operations
M.T                                # Transpose
M @ v                              # Matrix-vector product
np.dot(M, v)                       # Same as above
np.linalg.inv(M)                   # Inverse
np.linalg.det(M)                   # Determinant

# Eigendecomposition
eigenvalues, eigenvectors = np.linalg.eig(M)

# SVD
U, S, Vt = np.linalg.svd(M)

# Norms
np.linalg.norm(v, ord=1)           # L1 norm
np.linalg.norm(v, ord=2)           # L2 norm (default)
np.linalg.norm(M, ord='fro')       # Frobenius norm
```

### PyTorch Cheat Sheet

```python
import torch

# Creating tensors
v = torch.tensor([1., 2., 3.])
M = torch.tensor([[1., 2.], [3., 4.]])
I = torch.eye(3)
Z = torch.zeros(3, 3)

# Operations
M.T                                # Transpose
M @ v                              # Matrix-vector product
torch.inverse(M)                   # Inverse
torch.det(M)                       # Determinant

# Eigendecomposition
eigenvalues, eigenvectors = torch.linalg.eig(M)

# SVD
U, S, Vt = torch.linalg.svd(M)

# Norms
torch.norm(v, p=1)                 # L1 norm
torch.norm(v, p=2)                 # L2 norm
torch.norm(M, p='fro')             # Frobenius norm
```

---

## Exercises

After completing the scripts, try these:

1. **Implement matrix multiplication** without using `@` or `np.dot`
2. **Verify** that eigendecomposition satisfies `Av = λv`
3. **Compress an image** using SVD (keep top k singular values)
4. **Implement PCA** and visualize on MNIST digits

---

## Interview Questions

**Q: Why is matrix multiplication used in neural networks?**
> A: It efficiently computes the weighted sum of inputs. Each neuron's output is a dot product of inputs and weights, which can be computed as matrix multiplication for all neurons simultaneously.

**Q: What's the computational complexity of matrix multiplication?**
> A: O(n³) for naive algorithm, but optimized algorithms exist (Strassen: O(n^2.807))

**Q: What are eigenvalues/eigenvectors used for in ML?**
> A: PCA (dimensionality reduction), understanding linear transformations, spectral clustering, analyzing convergence of iterative algorithms.

---

## Run Order

```bash
python 01_vectors_matrices.py
python 02_matrix_operations.py
python 03_norms.py
python 04_eigendecomposition.py
python 05_svd.py
python 06_linear_systems.py
python 07_special_matrices.py
python 08_pca_from_scratch.py
```
