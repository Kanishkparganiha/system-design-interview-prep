"""
Chapter 5: Overfitting and Regularization
=========================================
The central challenge of machine learning: generalization.

Run: python 01_overfitting_regularization.py
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso

print("=" * 70)
print("OVERFITTING AND REGULARIZATION")
print("=" * 70)


# =============================================================================
# THE GENERALIZATION PROBLEM
# =============================================================================
print("\n" + "=" * 70)
print("1. THE GENERALIZATION PROBLEM")
print("=" * 70)

print("""
The Goal of Machine Learning:
─────────────────────────────
NOT to fit the training data perfectly!
BUT to generalize well to NEW, unseen data.

Training Error: How well we fit training data
Test Error:     How well we do on new data (what we care about!)

The Gap:
    Generalization Gap = Test Error - Training Error

If gap is large → OVERFITTING (memorized, didn't learn)
""")


# =============================================================================
# DEMONSTRATING OVERFITTING
# =============================================================================
print("\n" + "=" * 70)
print("2. DEMONSTRATING OVERFITTING")
print("=" * 70)

# Generate simple data
np.random.seed(42)
n_samples = 20

# True function: y = sin(x) + noise
X = np.sort(np.random.uniform(0, 2*np.pi, n_samples))
y_true = np.sin(X)
y = y_true + 0.3 * np.random.randn(n_samples)

# Fit polynomial models of different degrees
degrees = [1, 3, 15]
X_plot = np.linspace(0, 2*np.pi, 100)

print(f"Data: {n_samples} points from y = sin(x) + noise")
print(f"\nFitting polynomials of degree {degrees}:")
print("-" * 50)

for degree in degrees:
    # Transform features
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X.reshape(-1, 1))
    X_plot_poly = poly.transform(X_plot.reshape(-1, 1))

    # Fit model
    model = LinearRegression()
    model.fit(X_poly, y)

    # Predictions
    y_train_pred = model.predict(X_poly)
    y_plot_pred = model.predict(X_plot_poly)

    # Errors
    train_mse = np.mean((y - y_train_pred) ** 2)

    # "Test" on true function
    test_mse = np.mean((np.sin(X_plot) - y_plot_pred) ** 2)

    status = "UNDERFITTING" if degree == 1 else ("OVERFITTING" if degree == 15 else "GOOD FIT")
    print(f"  Degree {degree:2d}: Train MSE = {train_mse:.4f}, 'Test' MSE = {test_mse:.4f}  [{status}]")

print("""
Observation:
    - Degree 1: High train AND test error (underfitting)
    - Degree 3: Reasonable train and test error (good fit)
    - Degree 15: Very low train error, HIGH test error (overfitting!)
""")


# =============================================================================
# BIAS-VARIANCE TRADEOFF
# =============================================================================
print("\n" + "=" * 70)
print("3. BIAS-VARIANCE TRADEOFF")
print("=" * 70)

print("""
Expected Test Error can be decomposed:

    E[(y - ŷ)²] = Bias²(ŷ) + Var(ŷ) + σ²
                   ↓         ↓        ↓
               Underfitting  Overfitting  Irreducible noise

┌────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   Error                                                             │
│     │    ╲                                                          │
│     │     ╲  Bias²                                                  │
│     │      ╲                                                        │
│     │       ╲___                                                    │
│     │           ╲___                          ___/                  │
│     │               ╲______        __________╱                      │
│     │                     ╲______╱                                  │
│     │                      Total Error                              │
│     │                                  ___/                         │
│     │                           Variance                            │
│     │                                                               │
│     └────────────────────────────────────────────────────▶         │
│           Simple                             Complex                │
│                        Model Complexity                             │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

The Sweet Spot: Minimum total error (balance bias and variance)
""")


# =============================================================================
# TRAIN/VALIDATION/TEST SPLIT
# =============================================================================
print("\n" + "=" * 70)
print("4. TRAIN/VALIDATION/TEST SPLIT")
print("=" * 70)

print("""
Why THREE sets?

1. TRAINING SET (60-80%):
   - Used to train the model
   - Fit parameters (weights, biases)

2. VALIDATION SET (10-20%):
   - Used to tune hyperparameters
   - Select model complexity
   - Early stopping decisions
   - Can look at many times during development

3. TEST SET (10-20%):
   - Final evaluation ONLY
   - Estimates real-world performance
   - NEVER use for any decisions!
   - Look at ONCE at the very end
""")

# Demonstration
np.random.seed(42)
X_all = np.random.randn(1000, 10)
y_all = np.random.randn(1000)

X_temp, X_test, y_temp, y_test = train_test_split(X_all, y_all, test_size=0.15)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.176)  # 0.176 of 0.85 ≈ 0.15

print(f"\nSplitting 1000 samples:")
print(f"  Training:   {len(X_train)} samples ({len(X_train)/10:.0f}%)")
print(f"  Validation: {len(X_val)} samples ({len(X_val)/10:.0f}%)")
print(f"  Test:       {len(X_test)} samples ({len(X_test)/10:.0f}%)")


# =============================================================================
# L2 REGULARIZATION (RIDGE / WEIGHT DECAY)
# =============================================================================
print("\n" + "=" * 70)
print("5. L2 REGULARIZATION (RIDGE / WEIGHT DECAY)")
print("=" * 70)

print("""
L2 Regularization adds penalty on weight magnitudes:

    Loss = Original_Loss + λ Σ wᵢ²

Effect:
    - Shrinks all weights toward 0
    - Weights don't become exactly 0
    - Smoother, simpler models
    - Prevents any single feature from dominating

In neural networks, this is called "Weight Decay":
    w = w - lr * (grad + weight_decay * w)
""")

# Demonstrate on polynomial regression
np.random.seed(42)
X = np.sort(np.random.uniform(0, 2*np.pi, 20))
y = np.sin(X) + 0.3 * np.random.randn(20)

poly = PolynomialFeatures(15)
X_poly = poly.fit_transform(X.reshape(-1, 1))

# Fit with different regularization strengths
alphas = [0, 0.001, 0.1, 10]

print(f"\nPolynomial Regression (degree=15) with L2 regularization:")
print("-" * 60)

for alpha in alphas:
    if alpha == 0:
        model = LinearRegression()
    else:
        model = Ridge(alpha=alpha)

    model.fit(X_poly, y)
    y_pred = model.predict(X_poly)
    train_mse = np.mean((y - y_pred) ** 2)

    # Sum of squared weights
    weight_norm = np.sum(model.coef_ ** 2)

    print(f"  λ = {alpha:6.3f}: Train MSE = {train_mse:.4f}, ||w||² = {weight_norm:.4f}")

print("""
Observation:
    - λ = 0: Low train error, HUGE weights (overfitting)
    - λ = 0.1: Slightly higher train error, reasonable weights
    - λ = 10: Higher train error, small weights (underfitting)
""")


# =============================================================================
# L1 REGULARIZATION (LASSO / SPARSITY)
# =============================================================================
print("\n" + "=" * 70)
print("6. L1 REGULARIZATION (LASSO / SPARSITY)")
print("=" * 70)

print("""
L1 Regularization adds penalty on absolute weights:

    Loss = Original_Loss + λ Σ |wᵢ|

Effect:
    - Shrinks weights toward 0
    - Some weights become EXACTLY 0 (sparsity!)
    - Automatic feature selection
    - Good when many features are irrelevant

L1 vs L2:
    L1: Sparse weights (some exactly 0)
    L2: Small but non-zero weights
""")

# Demonstrate sparsity
print(f"\nComparing L1 vs L2 on polynomial features:")
print("-" * 60)

# L2 (Ridge)
ridge = Ridge(alpha=0.1)
ridge.fit(X_poly, y)
ridge_nonzero = np.sum(np.abs(ridge.coef_) > 1e-4)

# L1 (Lasso)
lasso = Lasso(alpha=0.01)
lasso.fit(X_poly, y)
lasso_nonzero = np.sum(np.abs(lasso.coef_) > 1e-4)

print(f"  L2 (Ridge): {ridge_nonzero}/{len(ridge.coef_)} non-zero coefficients")
print(f"  L1 (Lasso): {lasso_nonzero}/{len(lasso.coef_)} non-zero coefficients")

print("\n  Lasso coefficients:", lasso.coef_.round(3))
print("\n→ L1 produces SPARSE solutions (feature selection)!")


# =============================================================================
# DROPOUT (FOR NEURAL NETWORKS)
# =============================================================================
print("\n" + "=" * 70)
print("7. DROPOUT (FOR NEURAL NETWORKS)")
print("=" * 70)

print("""
Dropout randomly "drops" neurons during training:

During Training:
    - Each neuron has probability p of being set to 0
    - Forces network to not rely on any single neuron
    - Like training an ensemble of networks

During Inference:
    - All neurons active
    - Scale outputs by (1-p) to maintain expected values
    - Or use "inverted dropout" (scale during training instead)

Typical dropout rates:
    - Input layer: 0.2
    - Hidden layers: 0.5
""")

import torch
import torch.nn as nn

# Demonstrate dropout
class ModelWithDropout(nn.Module):
    def __init__(self, dropout_rate=0.5):
        super().__init__()
        self.fc1 = nn.Linear(10, 50)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(50, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)  # Apply dropout
        x = self.fc2(x)
        return x

model = ModelWithDropout(dropout_rate=0.5)

# Same input, different outputs during training (dropout is random)
x = torch.randn(1, 10)

model.train()  # Enable dropout
print("\nDropout during training (different each time):")
for i in range(3):
    out = model(x)
    print(f"  Forward pass {i+1}: {out.item():.4f}")

model.eval()  # Disable dropout
print("\nDropout during inference (deterministic):")
for i in range(3):
    with torch.no_grad():
        out = model(x)
    print(f"  Forward pass {i+1}: {out.item():.4f}")


# =============================================================================
# EARLY STOPPING
# =============================================================================
print("\n" + "=" * 70)
print("8. EARLY STOPPING")
print("=" * 70)

print("""
Early Stopping: Stop training when validation error stops improving.

    Training Loss
         │    ╲
         │     ╲____
         │          ╲___
         │              ╲___
         │                  ╲_______________
    ─────┼─────────────────────────────────────▶ Epochs
         │
    Validation Loss
         │    ╲
         │     ╲____
         │          ╲___
         │              ╲___
         │                  ╱‾‾‾‾‾‾‾   ← STOP HERE!
    ─────┼─────────────────────────────────────▶ Epochs
                           │
                    Best model saved

Why it works:
    - Limits effective model capacity
    - Free regularization (no extra hyperparameter to tune)
    - Just need patience parameter (how many epochs to wait)
""")

# Simulate training with early stopping
np.random.seed(42)

# Fake training and validation loss curves
epochs = np.arange(1, 51)
train_loss = 1.0 * np.exp(-epochs / 15) + 0.1
val_loss = 1.0 * np.exp(-epochs / 15) + 0.15 + 0.005 * (epochs - 20) * (epochs > 20)

best_epoch = np.argmin(val_loss) + 1
patience = 5
stop_epoch = best_epoch + patience

print(f"\nSimulated training:")
print(f"  Best validation loss at epoch {best_epoch}")
print(f"  With patience={patience}, stop at epoch {stop_epoch}")
print(f"  (Instead of continuing to epoch 50)")


# =============================================================================
# DATA AUGMENTATION
# =============================================================================
print("\n" + "=" * 70)
print("9. DATA AUGMENTATION")
print("=" * 70)

print("""
Data Augmentation: Create more training data through transformations.

For Images:
    - Random crops
    - Horizontal/vertical flips
    - Rotation
    - Color jitter
    - Cutout / Random erasing
    - Mixup (blend two images)

For Text:
    - Synonym replacement
    - Random insertion/deletion
    - Back-translation

For Audio:
    - Time stretching
    - Pitch shifting
    - Adding noise

Effect: Regularization by increasing data diversity!
""")

# PyTorch example
from torchvision import transforms

augmentation = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
])

print("\nPyTorch augmentation pipeline:")
print("  1. RandomHorizontalFlip (50%)")
print("  2. RandomRotation (±10°)")
print("  3. ColorJitter")
print("  4. RandomResizedCrop")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: REGULARIZATION TECHNIQUES")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────────┐
│  Technique          │  How it Works                │  When to Use      │
├─────────────────────────────────────────────────────────────────────────┤
│  L2 / Weight Decay  │  Penalize large weights      │  Default choice   │
│  L1 / Lasso         │  Sparse weights              │  Feature selection│
│  Dropout            │  Random neuron dropping      │  Neural networks  │
│  Early Stopping     │  Stop when val loss ↑        │  Always use!      │
│  Data Augmentation  │  Increase data diversity     │  Limited data     │
│  Batch Normalization│  Normalize activations       │  Deep networks    │
│  Label Smoothing    │  Soften one-hot labels       │  Classification   │
└─────────────────────────────────────────────────────────────────────────┘

Rules of Thumb:
───────────────
1. Always use train/val/test split
2. Start simple, add complexity if underfitting
3. If overfitting: more data > more regularization > simpler model
4. Combine multiple techniques (they're complementary)
5. Monitor both train AND validation loss
""")
