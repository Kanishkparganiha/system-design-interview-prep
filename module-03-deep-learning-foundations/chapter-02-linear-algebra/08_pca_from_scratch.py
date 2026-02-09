"""
Chapter 2: PCA from Scratch
===========================
Implementing Principal Component Analysis using what we learned.

This script brings together:
    - Covariance matrices (symmetric)
    - Eigendecomposition
    - SVD
    - Linear transformations

Run: python 08_pca_from_scratch.py
"""

import numpy as np
from sklearn.datasets import load_iris, load_digits

print("=" * 70)
print("PRINCIPAL COMPONENT ANALYSIS (PCA) FROM SCRATCH")
print("=" * 70)


# =============================================================================
# 1. WHAT IS PCA?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHAT IS PCA?")
print("=" * 70)

print("""
PCA finds directions of maximum variance in data.

Why use PCA?
    1. Dimensionality reduction (compress data)
    2. Noise reduction (keep only important directions)
    3. Visualization (project to 2D/3D)
    4. Decorrelation (make features independent)

The Math:
    1. Center the data: X_centered = X - mean(X)
    2. Compute covariance: C = (1/n) X_centeredᵀ X_centered
    3. Eigendecompose: C = VΛVᵀ
    4. Principal components = eigenvectors sorted by eigenvalues
    5. Project: X_pca = X_centered @ V
""")


# =============================================================================
# 2. PCA IMPLEMENTATION
# =============================================================================
print("\n" + "=" * 70)
print("2. PCA IMPLEMENTATION")
print("=" * 70)


class PCA:
    """Principal Component Analysis from scratch."""

    def __init__(self, n_components=None):
        self.n_components = n_components
        self.mean_ = None
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None

    def fit(self, X):
        """Fit PCA on data X."""
        n_samples, n_features = X.shape

        # Step 1: Center the data
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # Step 2: Compute covariance matrix
        # Using n-1 for unbiased estimate (Bessel's correction)
        cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)

        # Step 3: Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Step 4: Sort by eigenvalue (descending)
        sorted_idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_idx]
        eigenvectors = eigenvectors[:, sorted_idx]

        # Store results
        if self.n_components is None:
            self.n_components = n_features

        self.components_ = eigenvectors[:, :self.n_components].T
        self.explained_variance_ = eigenvalues[:self.n_components]
        self.explained_variance_ratio_ = (
            self.explained_variance_ / eigenvalues.sum()
        )

        return self

    def transform(self, X):
        """Project data onto principal components."""
        X_centered = X - self.mean_
        return X_centered @ self.components_.T

    def fit_transform(self, X):
        """Fit and transform in one step."""
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X_pca):
        """Reconstruct original data from PCA representation."""
        return X_pca @ self.components_ + self.mean_


# Test on simple data
np.random.seed(42)
# Create correlated 2D data
X_simple = np.random.randn(100, 2) @ np.array([[2, 1], [1, 2]])

pca = PCA(n_components=2)
X_transformed = pca.fit_transform(X_simple)

print("Simple 2D example:")
print(f"Original data shape: {X_simple.shape}")
print(f"Transformed shape: {X_transformed.shape}")
print(f"\nPrincipal components (directions):\n{pca.components_}")
print(f"\nExplained variance: {pca.explained_variance_}")
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")


# =============================================================================
# 3. PCA USING SVD (More Numerically Stable)
# =============================================================================
print("\n" + "=" * 70)
print("3. PCA USING SVD (Preferred Method)")
print("=" * 70)

print("""
Instead of computing the covariance matrix, we can use SVD directly:

    X_centered = UΣVᵀ

Then:
    - Principal components = rows of Vᵀ
    - Variance = σ²/(n-1) where σ are singular values

Advantages:
    - More numerically stable
    - Works for n_samples < n_features
    - No need to compute covariance matrix
""")


class PCA_SVD:
    """PCA using SVD (more stable)."""

    def __init__(self, n_components=None):
        self.n_components = n_components
        self.mean_ = None
        self.components_ = None
        self.explained_variance_ = None
        self.singular_values_ = None

    def fit(self, X):
        n_samples, n_features = X.shape

        # Center
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # SVD
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)

        # Get components
        if self.n_components is None:
            self.n_components = min(n_samples, n_features)

        self.components_ = Vt[:self.n_components]
        self.singular_values_ = S[:self.n_components]
        self.explained_variance_ = (S[:self.n_components] ** 2) / (n_samples - 1)
        self.explained_variance_ratio_ = (
            self.explained_variance_ / (S ** 2).sum() * (n_samples - 1)
        )

        return self

    def transform(self, X):
        X_centered = X - self.mean_
        return X_centered @ self.components_.T

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)


# Compare eigendecomposition vs SVD
print("\nComparing Eigendecomposition vs SVD on same data:")
pca_eig = PCA(n_components=2)
pca_svd = PCA_SVD(n_components=2)

X_eig = pca_eig.fit_transform(X_simple)
X_svd = pca_svd.fit_transform(X_simple)

print(f"Eigendecomposition variance: {pca_eig.explained_variance_.round(4)}")
print(f"SVD variance: {pca_svd.explained_variance_.round(4)}")
print(f"Results match: {np.allclose(np.abs(X_eig), np.abs(X_svd))}")


# =============================================================================
# 4. DIMENSIONALITY REDUCTION EXAMPLE
# =============================================================================
print("\n" + "=" * 70)
print("4. DIMENSIONALITY REDUCTION: IRIS DATASET")
print("=" * 70)

# Load Iris dataset
iris = load_iris()
X_iris = iris.data
y_iris = iris.target

print(f"Original shape: {X_iris.shape} (150 samples, 4 features)")

# Apply PCA
pca_iris = PCA(n_components=2)
X_iris_pca = pca_iris.fit_transform(X_iris)

print(f"Reduced shape: {X_iris_pca.shape} (150 samples, 2 components)")
print(f"\nVariance explained:")
for i, (var, ratio) in enumerate(zip(pca_iris.explained_variance_,
                                      pca_iris.explained_variance_ratio_)):
    print(f"  PC{i+1}: {var:.4f} ({ratio*100:.1f}%)")

print(f"\nTotal variance retained: {sum(pca_iris.explained_variance_ratio_)*100:.1f}%")


# =============================================================================
# 5. CHOOSING NUMBER OF COMPONENTS
# =============================================================================
print("\n" + "=" * 70)
print("5. CHOOSING NUMBER OF COMPONENTS")
print("=" * 70)

print("""
Common strategies:
    1. Keep components explaining X% variance (e.g., 95%)
    2. Look for "elbow" in scree plot
    3. Kaiser criterion: keep eigenvalues > 1
    4. Cross-validation on downstream task
""")

# Full PCA on Iris
pca_full = PCA(n_components=4)
pca_full.fit(X_iris)

print("Iris dataset - all components:")
cumulative = np.cumsum(pca_full.explained_variance_ratio_)
for i in range(4):
    print(f"  PC{i+1}: {pca_full.explained_variance_ratio_[i]*100:.1f}% "
          f"(cumulative: {cumulative[i]*100:.1f}%)")

# Find minimum components for 95% variance
n_for_95 = np.argmax(cumulative >= 0.95) + 1
print(f"\nComponents needed for 95% variance: {n_for_95}")


# =============================================================================
# 6. RECONSTRUCTION ERROR
# =============================================================================
print("\n" + "=" * 70)
print("6. RECONSTRUCTION ERROR")
print("=" * 70)

print("""
After reducing dimensions, we can reconstruct approximate original data.
Reconstruction error measures information loss.

    Error = ||X - X_reconstructed||²
""")

# Reduce to 2D and reconstruct
pca_2d = PCA(n_components=2)
X_iris_2d = pca_2d.fit_transform(X_iris)
X_reconstructed = pca_2d.inverse_transform(X_iris_2d)

# Compute error
reconstruction_error = np.mean((X_iris - X_reconstructed) ** 2)
total_variance = np.var(X_iris)

print(f"Original variance: {total_variance:.4f}")
print(f"Reconstruction MSE: {reconstruction_error:.4f}")
print(f"Relative error: {reconstruction_error/total_variance*100:.1f}%")


# =============================================================================
# 7. WHITENING (DECORRELATION + UNIT VARIANCE)
# =============================================================================
print("\n" + "=" * 70)
print("7. WHITENING (ZCA/PCA)")
print("=" * 70)

print("""
Whitening transforms data to have:
    1. Zero mean
    2. Unit variance in each direction
    3. No correlation between features

PCA whitening: X_white = X_pca / sqrt(eigenvalues)
ZCA whitening: Project back to original space

Used in:
    - Data preprocessing for neural networks
    - Batch normalization (approximate whitening)
""")


def pca_whiten(X, n_components=None):
    """Apply PCA whitening."""
    pca = PCA(n_components)
    X_pca = pca.fit_transform(X)

    # Divide by sqrt of variance to get unit variance
    X_white = X_pca / np.sqrt(pca.explained_variance_ + 1e-8)

    return X_white, pca


X_white, _ = pca_whiten(X_iris, n_components=4)

print("Before whitening:")
print(f"  Mean: {X_iris.mean(axis=0).round(2)}")
print(f"  Std: {X_iris.std(axis=0).round(2)}")

print("\nAfter whitening:")
print(f"  Mean: {X_white.mean(axis=0).round(2)}")
print(f"  Std: {X_white.std(axis=0).round(2)}")


# =============================================================================
# 8. COMPARISON WITH SKLEARN
# =============================================================================
print("\n" + "=" * 70)
print("8. COMPARISON WITH SKLEARN")
print("=" * 70)

from sklearn.decomposition import PCA as SklearnPCA

# Our implementation
pca_ours = PCA(n_components=2)
X_ours = pca_ours.fit_transform(X_iris)

# Sklearn
pca_sklearn = SklearnPCA(n_components=2)
X_sklearn = pca_sklearn.fit_transform(X_iris)

print("Comparing our PCA with sklearn:")
print(f"\nExplained variance ratio:")
print(f"  Ours:    {pca_ours.explained_variance_ratio_.round(4)}")
print(f"  Sklearn: {pca_sklearn.explained_variance_ratio_.round(4)}")

# Note: Signs might differ (eigenvectors can point in opposite directions)
print(f"\nTransformed data (first 3 samples):")
print(f"  Ours:    \n{np.abs(X_ours[:3]).round(4)}")
print(f"  Sklearn: \n{np.abs(X_sklearn[:3]).round(4)}")

print(f"\nResults match: {np.allclose(np.abs(X_ours), np.abs(X_sklearn))}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: PCA")
print("=" * 70)

print("""
PCA Algorithm:
──────────────
1. Center data: X = X - mean(X)
2. Compute covariance: C = XᵀX / (n-1)
3. Eigendecompose: C = VΛVᵀ  (or use SVD: X = UΣVᵀ)
4. Sort by eigenvalues (descending)
5. Project: X_pca = X @ V[:, :k]

Key Properties:
───────────────
• Principal components are orthogonal
• First PC captures maximum variance
• Each subsequent PC captures remaining variance
• Total variance = sum of all eigenvalues

Use Cases in Deep Learning:
───────────────────────────
• Data visualization (reduce to 2D/3D)
• Feature extraction (preprocessing)
• Noise reduction (keep top components)
• Initialization (PCA whitening before training)
• Compression (store less data)

Mathematical Connection:
───────────────────────
• Covariance matrix → symmetric → real eigenvalues
• SVD of X gives same components as eigendecomposition of XᵀX
• Singular values σ relate to eigenvalues: λ = σ²/(n-1)
""")
