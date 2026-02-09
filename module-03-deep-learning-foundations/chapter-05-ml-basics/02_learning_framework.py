"""
Chapter 5: The Machine Learning Framework
=========================================
Understanding what it means to "learn" from data.

Run: python 02_learning_framework.py
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

print("=" * 70)
print("THE MACHINE LEARNING FRAMEWORK")
print("=" * 70)


# =============================================================================
# 1. WHAT IS MACHINE LEARNING?
# =============================================================================
print("\n" + "=" * 70)
print("1. WHAT IS MACHINE LEARNING?")
print("=" * 70)

print("""
Machine Learning: Learning from experience (data) to improve performance.

Formal definition (Tom Mitchell, 1997):
    "A computer program is said to learn from experience E
     with respect to some task T and performance measure P,
     if its performance at task T, as measured by P,
     improves with experience E."

Key components:
    T = Task (what we want to do)
    E = Experience (the data)
    P = Performance measure (how we evaluate)

Example:
    T = Classify emails as spam/not spam
    E = Historical emails with labels
    P = Accuracy on new emails
""")


# =============================================================================
# 2. TRAIN / VALIDATION / TEST SPLIT
# =============================================================================
print("\n" + "=" * 70)
print("2. DATA SPLITS")
print("=" * 70)

print("""
We split data into three parts:

    ┌────────────────────────────────────────────────────────────┐
    │                        All Data                             │
    ├──────────────────┬─────────────────┬───────────────────────┤
    │   Training Set   │ Validation Set  │      Test Set         │
    │     (60-80%)     │    (10-20%)     │      (10-20%)         │
    ├──────────────────┼─────────────────┼───────────────────────┤
    │ Learn model      │ Tune hyper-     │ Final evaluation      │
    │ parameters       │ parameters      │ (NEVER peek!)         │
    └──────────────────┴─────────────────┴───────────────────────┘

Rules:
    1. Test set is SACRED - only use once at the very end
    2. Validation set for model selection and hyperparameter tuning
    3. Training set for learning model parameters
""")

# Generate sample data
np.random.seed(42)
X, y = make_classification(n_samples=1000, n_features=20, n_informative=10,
                           n_redundant=5, n_classes=2, random_state=42)

# Split into train/val/test
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

print(f"Data split:")
print(f"  Training:   {len(X_train)} samples ({len(X_train)/len(X)*100:.0f}%)")
print(f"  Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.0f}%)")
print(f"  Test:       {len(X_test)} samples ({len(X_test)/len(X)*100:.0f}%)")


# =============================================================================
# 3. GENERALIZATION
# =============================================================================
print("\n" + "=" * 70)
print("3. GENERALIZATION: THE CORE CHALLENGE")
print("=" * 70)

print("""
Generalization = Performance on UNSEEN data

The fundamental tradeoff:
    - Too simple model: Can't capture patterns (underfitting)
    - Too complex model: Memorizes training data (overfitting)

    Training Error    ↓ as complexity ↑
    Test Error        ↓ then ↑ (U-shaped curve)
    Generalization    = Test Error - Training Error (gap)

Goal: Find the sweet spot where test error is minimized!
""")


class SimpleLinearModel:
    """Simple linear classifier for demonstration."""

    def __init__(self):
        self.W = None
        self.b = None

    def fit(self, X, y, learning_rate=0.01, epochs=100):
        n_samples, n_features = X.shape
        self.W = np.zeros(n_features)
        self.b = 0

        for _ in range(epochs):
            # Forward
            logits = X @ self.W + self.b
            probs = 1 / (1 + np.exp(-np.clip(logits, -500, 500)))

            # Gradient
            error = probs - y
            grad_W = X.T @ error / n_samples
            grad_b = error.mean()

            # Update
            self.W -= learning_rate * grad_W
            self.b -= learning_rate * grad_b

    def predict_proba(self, X):
        logits = X @ self.W + self.b
        return 1 / (1 + np.exp(-np.clip(logits, -500, 500)))

    def predict(self, X):
        return (self.predict_proba(X) > 0.5).astype(int)

    def accuracy(self, X, y):
        return (self.predict(X) == y).mean()


# Train and evaluate
model = SimpleLinearModel()
model.fit(X_train, y_train, epochs=500)

train_acc = model.accuracy(X_train, y_train)
val_acc = model.accuracy(X_val, y_val)
test_acc = model.accuracy(X_test, y_test)

print(f"\nLinear model performance:")
print(f"  Training accuracy:   {train_acc:.4f}")
print(f"  Validation accuracy: {val_acc:.4f}")
print(f"  Test accuracy:       {test_acc:.4f}")
print(f"  Generalization gap:  {train_acc - val_acc:.4f}")


# =============================================================================
# 4. CROSS-VALIDATION
# =============================================================================
print("\n" + "=" * 70)
print("4. CROSS-VALIDATION")
print("=" * 70)

print("""
Problem: Single train/val split may be unrepresentative.
Solution: K-Fold Cross-Validation

    Fold 1: [Val ] [Train] [Train] [Train] [Train]
    Fold 2: [Train] [Val ] [Train] [Train] [Train]
    Fold 3: [Train] [Train] [Val ] [Train] [Train]
    Fold 4: [Train] [Train] [Train] [Val ] [Train]
    Fold 5: [Train] [Train] [Train] [Train] [Val ]

    Final score = Average across all folds

Benefits:
    - Uses all data for both training and validation
    - More robust estimate of performance
    - Especially useful for small datasets
""")


def k_fold_cross_validation(X, y, k=5, epochs=500):
    """Perform k-fold cross-validation."""
    n_samples = len(X)
    fold_size = n_samples // k
    indices = np.random.permutation(n_samples)

    scores = []
    for i in range(k):
        # Split into fold
        val_idx = indices[i * fold_size:(i + 1) * fold_size]
        train_idx = np.concatenate([indices[:i * fold_size],
                                    indices[(i + 1) * fold_size:]])

        X_train_fold = X[train_idx]
        y_train_fold = y[train_idx]
        X_val_fold = X[val_idx]
        y_val_fold = y[val_idx]

        # Train and evaluate
        model = SimpleLinearModel()
        model.fit(X_train_fold, y_train_fold, epochs=epochs)
        scores.append(model.accuracy(X_val_fold, y_val_fold))

    return scores


# Perform cross-validation
cv_scores = k_fold_cross_validation(X_temp, y_temp, k=5)

print(f"5-Fold Cross-Validation:")
for i, score in enumerate(cv_scores):
    print(f"  Fold {i+1}: {score:.4f}")
print(f"  Mean: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")


# =============================================================================
# 5. HYPERPARAMETER TUNING
# =============================================================================
print("\n" + "=" * 70)
print("5. HYPERPARAMETER TUNING")
print("=" * 70)

print("""
Two types of parameters:
    - Model parameters: Learned from data (weights, biases)
    - Hyperparameters: Set before training (learning rate, layers, etc.)

Tuning strategies:
    1. Grid Search: Try all combinations
    2. Random Search: Random sampling (often better!)
    3. Bayesian Optimization: Smart sampling based on results

Use validation set (or cross-validation) for tuning!
NEVER tune on test set!
""")


def hyperparameter_search(X_train, y_train, X_val, y_val, learning_rates, epochs_list):
    """Simple grid search for hyperparameters."""
    best_score = 0
    best_params = {}
    results = []

    for lr in learning_rates:
        for epochs in epochs_list:
            model = SimpleLinearModel()
            model.fit(X_train, y_train, learning_rate=lr, epochs=epochs)
            val_acc = model.accuracy(X_val, y_val)
            results.append((lr, epochs, val_acc))

            if val_acc > best_score:
                best_score = val_acc
                best_params = {'learning_rate': lr, 'epochs': epochs}

    return best_params, best_score, results


# Grid search
learning_rates = [0.001, 0.01, 0.1]
epochs_list = [100, 500, 1000]

best_params, best_score, results = hyperparameter_search(
    X_train, y_train, X_val, y_val, learning_rates, epochs_list
)

print(f"Grid Search Results:")
print(f"  Best validation accuracy: {best_score:.4f}")
print(f"  Best hyperparameters: {best_params}")


# =============================================================================
# 6. MODEL SELECTION
# =============================================================================
print("\n" + "=" * 70)
print("6. MODEL SELECTION")
print("=" * 70)

print("""
Model selection workflow:

    1. Split data: train / val / test
    2. For each model candidate:
        a. For each hyperparameter setting:
            - Train on training set
            - Evaluate on validation set
        b. Select best hyperparameters
    3. Select model with best validation performance
    4. Train final model on train + val
    5. Report final performance on test set

IMPORTANT: Test set used ONLY ONCE at the very end!
""")


# =============================================================================
# 7. ESTIMATOR TYPES
# =============================================================================
print("\n" + "=" * 70)
print("7. TYPES OF LEARNING")
print("=" * 70)

print("""
Supervised Learning:
    - Input: Data + Labels
    - Goal: Learn mapping X → Y
    - Examples: Classification, Regression

Unsupervised Learning:
    - Input: Data only (no labels)
    - Goal: Find structure in data
    - Examples: Clustering, Dimensionality reduction

Semi-supervised Learning:
    - Input: Some labeled + lots of unlabeled data
    - Goal: Use unlabeled data to improve
    - Examples: Self-training, pseudo-labeling

Self-supervised Learning:
    - Input: Data (create own labels from data)
    - Goal: Learn useful representations
    - Examples: Language models, contrastive learning

Reinforcement Learning:
    - Input: Environment + Rewards
    - Goal: Learn optimal actions
    - Examples: Game playing, robotics
""")


# =============================================================================
# 8. LEARNING CURVES
# =============================================================================
print("\n" + "=" * 70)
print("8. LEARNING CURVES")
print("=" * 70)

print("""
Learning curves show how performance changes with training data size:

    Samples     Train Error     Test Error
    ───────     ───────────     ──────────
      100          0.05           0.30
      500          0.08           0.20
     1000          0.10           0.15
     5000          0.11           0.13

Interpretations:
    - High bias (underfitting):
        Both curves plateau at high error
        → Need more complex model

    - High variance (overfitting):
        Large gap between curves
        → Need more data or regularization
""")


def compute_learning_curve(X, y, train_sizes):
    """Compute learning curve."""
    n_samples = len(X)

    # Split off test set
    split_idx = int(0.2 * n_samples)
    X_test = X[:split_idx]
    y_test = y[:split_idx]
    X_train_full = X[split_idx:]
    y_train_full = y[split_idx:]

    train_scores = []
    test_scores = []

    for train_size in train_sizes:
        if train_size > len(X_train_full):
            continue

        X_train = X_train_full[:train_size]
        y_train = y_train_full[:train_size]

        model = SimpleLinearModel()
        model.fit(X_train, y_train, epochs=500)

        train_scores.append(model.accuracy(X_train, y_train))
        test_scores.append(model.accuracy(X_test, y_test))

    return train_sizes[:len(train_scores)], train_scores, test_scores


train_sizes = [50, 100, 200, 400, 600]
sizes, train_scores, test_scores = compute_learning_curve(X, y, train_sizes)

print(f"Learning Curve:")
print(f"{'Samples':<10} {'Train Acc':<12} {'Test Acc':<12} {'Gap':<10}")
print("-" * 44)
for size, train, test in zip(sizes, train_scores, test_scores):
    print(f"{size:<10} {train:<12.4f} {test:<12.4f} {train-test:<10.4f}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: ML FRAMEWORK")
print("=" * 70)

print("""
Key Concepts:
─────────────
1. Task (T), Experience (E), Performance (P)
2. Train/Validation/Test split
3. Generalization: perform well on unseen data
4. Cross-validation for robust evaluation
5. Hyperparameter tuning on validation set
6. Model selection workflow

Best Practices:
───────────────
• NEVER use test set for training or tuning
• Use cross-validation for small datasets
• Random search often beats grid search
• Track both training and validation metrics
• Plot learning curves for diagnosis

Common Mistakes:
───────────────
• Peeking at test set during development
• Not shuffling data before splitting
• Data leakage (info from test leaks to train)
• Tuning on training set
• Reporting validation accuracy as final result
""")
