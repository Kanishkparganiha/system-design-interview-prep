"""
Chapter 6: Multi-Layer Perceptron from Scratch
==============================================
Building a neural network using only NumPy.

This is THE most important script in the entire module.
Understanding this = understanding deep learning fundamentals.

Run: python 01_mlp_from_scratch.py
"""

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

print("=" * 70)
print("MULTI-LAYER PERCEPTRON FROM SCRATCH")
print("=" * 70)


# =============================================================================
# ACTIVATION FUNCTIONS
# =============================================================================
print("\n" + "=" * 70)
print("1. ACTIVATION FUNCTIONS")
print("=" * 70)

print("""
Activation functions introduce non-linearity.
Without them, stacking layers is useless (just matrix multiplication).

Each activation needs:
    - Forward: output = f(input)
    - Backward: gradient = f'(input) for backprop
""")


class ReLU:
    """Rectified Linear Unit: f(x) = max(0, x)"""

    def forward(self, x):
        self.x = x
        return np.maximum(0, x)

    def backward(self, grad_output):
        # d(ReLU)/dx = 1 if x > 0, else 0
        return grad_output * (self.x > 0)


class Sigmoid:
    """Sigmoid: f(x) = 1 / (1 + exp(-x))"""

    def forward(self, x):
        self.out = 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        return self.out

    def backward(self, grad_output):
        # d(sigmoid)/dx = sigmoid * (1 - sigmoid)
        return grad_output * self.out * (1 - self.out)


class Softmax:
    """Softmax for multi-class output"""

    def forward(self, x):
        # Subtract max for numerical stability
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.out = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self.out

    def backward(self, grad_output):
        # Combined with cross-entropy, gradient is simple: softmax - y_true
        return grad_output


# Demo activation functions
x = np.array([-2, -1, 0, 1, 2])
print(f"\nInput: {x}")
print(f"ReLU:    {ReLU().forward(x)}")
print(f"Sigmoid: {Sigmoid().forward(x).round(3)}")


# =============================================================================
# LOSS FUNCTIONS
# =============================================================================
print("\n" + "=" * 70)
print("2. LOSS FUNCTIONS")
print("=" * 70)


class CrossEntropyLoss:
    """Cross-entropy loss for classification"""

    def forward(self, y_pred, y_true):
        """
        y_pred: softmax probabilities (batch_size, num_classes)
        y_true: one-hot encoded labels (batch_size, num_classes)
        """
        self.y_pred = y_pred
        self.y_true = y_true

        # Clip to avoid log(0)
        y_pred_clipped = np.clip(y_pred, 1e-15, 1 - 1e-15)

        # Cross-entropy: -sum(y_true * log(y_pred))
        loss = -np.sum(y_true * np.log(y_pred_clipped)) / y_pred.shape[0]
        return loss

    def backward(self):
        """Gradient of CE + Softmax combined"""
        # This is the beautiful simplification!
        return (self.y_pred - self.y_true) / self.y_pred.shape[0]


class MSELoss:
    """Mean Squared Error for regression"""

    def forward(self, y_pred, y_true):
        self.y_pred = y_pred
        self.y_true = y_true
        return np.mean((y_pred - y_true) ** 2)

    def backward(self):
        return 2 * (self.y_pred - self.y_true) / self.y_pred.shape[0]


# =============================================================================
# LINEAR LAYER
# =============================================================================
print("\n" + "=" * 70)
print("3. LINEAR (DENSE) LAYER")
print("=" * 70)

print("""
A linear layer computes: output = input @ W + b

Forward:  y = xW + b
Backward:
    ∂L/∂W = xᵀ @ ∂L/∂y    (gradient w.r.t. weights)
    ∂L/∂b = sum(∂L/∂y)    (gradient w.r.t. bias)
    ∂L/∂x = ∂L/∂y @ Wᵀ    (gradient to pass back)
""")


class Linear:
    """Fully connected (dense) layer"""

    def __init__(self, in_features, out_features):
        # Xavier/Glorot initialization
        scale = np.sqrt(2.0 / (in_features + out_features))
        self.W = np.random.randn(in_features, out_features) * scale
        self.b = np.zeros((1, out_features))

        # Gradients
        self.grad_W = None
        self.grad_b = None

    def forward(self, x):
        self.x = x
        return x @ self.W + self.b

    def backward(self, grad_output):
        # Gradient w.r.t. weights
        self.grad_W = self.x.T @ grad_output

        # Gradient w.r.t. bias
        self.grad_b = np.sum(grad_output, axis=0, keepdims=True)

        # Gradient to pass back to previous layer
        return grad_output @ self.W.T


# =============================================================================
# COMPLETE MLP CLASS
# =============================================================================
print("\n" + "=" * 70)
print("4. COMPLETE MLP CLASS")
print("=" * 70)


class MLP:
    """
    Multi-Layer Perceptron from scratch.

    Architecture: Input → Linear → ReLU → Linear → ReLU → Linear → Softmax
    """

    def __init__(self, input_dim, hidden_dims, output_dim):
        """
        Args:
            input_dim: Number of input features
            hidden_dims: List of hidden layer sizes, e.g., [64, 32]
            output_dim: Number of output classes
        """
        self.layers = []
        self.activations = []

        # Build network
        dims = [input_dim] + hidden_dims + [output_dim]

        for i in range(len(dims) - 1):
            self.layers.append(Linear(dims[i], dims[i + 1]))

            # Add ReLU for hidden layers, Softmax for output
            if i < len(dims) - 2:
                self.activations.append(ReLU())
            else:
                self.activations.append(Softmax())

        print(f"Created MLP: {' → '.join(map(str, dims))}")

    def forward(self, x):
        """Forward pass through the network"""
        for layer, activation in zip(self.layers, self.activations):
            x = layer.forward(x)
            x = activation.forward(x)
        return x

    def backward(self, grad):
        """Backward pass (backpropagation)"""
        # Go through layers in reverse
        for layer, activation in zip(reversed(self.layers), reversed(self.activations)):
            grad = activation.backward(grad)
            grad = layer.backward(grad)

    def get_params(self):
        """Get all parameters and gradients"""
        params = []
        grads = []
        for layer in self.layers:
            params.extend([layer.W, layer.b])
            grads.extend([layer.grad_W, layer.grad_b])
        return params, grads


# =============================================================================
# OPTIMIZER (SGD)
# =============================================================================
print("\n" + "=" * 70)
print("5. OPTIMIZER")
print("=" * 70)


class SGD:
    """Stochastic Gradient Descent with optional momentum"""

    def __init__(self, params, lr=0.01, momentum=0.0):
        self.params = params
        self.lr = lr
        self.momentum = momentum
        self.velocities = [np.zeros_like(p) for p in params]

    def step(self, grads):
        """Update parameters using gradients"""
        for i, (param, grad) in enumerate(zip(self.params, grads)):
            self.velocities[i] = self.momentum * self.velocities[i] + grad
            param -= self.lr * self.velocities[i]


# =============================================================================
# TRAINING LOOP
# =============================================================================
print("\n" + "=" * 70)
print("6. TRAINING ON MOON DATASET")
print("=" * 70)

# Generate dataset
np.random.seed(42)
X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# One-hot encode labels
def one_hot(y, num_classes):
    return np.eye(num_classes)[y]

y_train_oh = one_hot(y_train, 2)
y_test_oh = one_hot(y_test, 2)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")
print(f"Input dimension: {X_train.shape[1]}")
print(f"Number of classes: 2")

# Create model
model = MLP(input_dim=2, hidden_dims=[16, 8], output_dim=2)
loss_fn = CrossEntropyLoss()

# Get parameters for optimizer
params, _ = model.get_params()
optimizer = SGD(params, lr=0.5, momentum=0.9)

# Training
print("\nTraining...")
print("-" * 50)

epochs = 100
batch_size = 32

for epoch in range(epochs):
    # Shuffle training data
    indices = np.random.permutation(len(X_train))
    X_shuffled = X_train[indices]
    y_shuffled = y_train_oh[indices]

    epoch_loss = 0
    num_batches = 0

    # Mini-batch training
    for i in range(0, len(X_train), batch_size):
        X_batch = X_shuffled[i:i + batch_size]
        y_batch = y_shuffled[i:i + batch_size]

        # Forward pass
        y_pred = model.forward(X_batch)

        # Compute loss
        loss = loss_fn.forward(y_pred, y_batch)
        epoch_loss += loss
        num_batches += 1

        # Backward pass
        grad = loss_fn.backward()
        model.backward(grad)

        # Update parameters
        _, grads = model.get_params()
        optimizer.step(grads)

    # Print progress
    if (epoch + 1) % 20 == 0:
        avg_loss = epoch_loss / num_batches

        # Compute accuracy
        y_pred_train = model.forward(X_train)
        train_acc = np.mean(np.argmax(y_pred_train, axis=1) == y_train)

        y_pred_test = model.forward(X_test)
        test_acc = np.mean(np.argmax(y_pred_test, axis=1) == y_test)

        print(f"Epoch {epoch+1:3d}: Loss = {avg_loss:.4f}, Train Acc = {train_acc:.4f}, Test Acc = {test_acc:.4f}")


# =============================================================================
# FINAL EVALUATION
# =============================================================================
print("\n" + "=" * 70)
print("7. FINAL EVALUATION")
print("=" * 70)

y_pred_test = model.forward(X_test)
test_predictions = np.argmax(y_pred_test, axis=1)
test_accuracy = np.mean(test_predictions == y_test)

print(f"\nFinal Test Accuracy: {test_accuracy:.4f}")

# Show some predictions
print("\nSample predictions:")
print("-" * 40)
for i in range(5):
    pred_probs = y_pred_test[i]
    pred_class = test_predictions[i]
    true_class = y_test[i]
    correct = "✓" if pred_class == true_class else "✗"
    print(f"  Probs: [{pred_probs[0]:.3f}, {pred_probs[1]:.3f}] → Pred: {pred_class}, True: {true_class} {correct}")


# =============================================================================
# UNDERSTANDING BACKPROPAGATION
# =============================================================================
print("\n" + "=" * 70)
print("8. UNDERSTANDING BACKPROPAGATION")
print("=" * 70)

print("""
The Chain Rule in Action:

Given: Input x → Layer1 → h₁ → Layer2 → h₂ → Output → Loss

Forward Pass:
    h₁ = ReLU(W₁x + b₁)
    h₂ = ReLU(W₂h₁ + b₂)
    ŷ = Softmax(W₃h₂ + b₃)
    L = CrossEntropy(ŷ, y)

Backward Pass (computing gradients):

    ∂L/∂W₃ = ∂L/∂ŷ × ∂ŷ/∂(W₃h₂) × ∂(W₃h₂)/∂W₃
                ↑            ↑              ↑
           from loss   from softmax   h₂ (saved)

    ∂L/∂W₂ = ∂L/∂ŷ × ∂ŷ/∂h₂ × ∂h₂/∂(W₂h₁) × ∂(W₂h₁)/∂W₂
                         ↑            ↑              ↑
                      chain        ReLU grad     h₁ (saved)

Key Insight: We need to save intermediate values during forward pass
             to use them during backward pass!

This is why PyTorch has:
    with torch.no_grad():   # Don't save for backprop
    .detach()               # Stop gradient flow
""")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: WHAT WE BUILT")
print("=" * 70)

print("""
Components Built:
─────────────────
1. Activation Functions (ReLU, Sigmoid, Softmax)
2. Loss Functions (Cross-Entropy, MSE)
3. Linear Layer (with forward & backward)
4. Complete MLP (stacking layers)
5. Optimizer (SGD with momentum)
6. Training Loop (batching, epochs)

Key Equations:
──────────────
Forward:  y = σ(Wx + b)
Loss:     L = -Σ y_true × log(y_pred)
Backward: ∂L/∂W = xᵀ × ∂L/∂y
Update:   W = W - lr × ∂L/∂W

What PyTorch Does For You:
──────────────────────────
1. Automatic differentiation (no manual backward())
2. GPU acceleration
3. Many optimizers (Adam, AdamW, etc.)
4. Batching utilities (DataLoader)
5. Pre-built layers (Conv2D, LSTM, Transformer)

But understanding this from scratch is invaluable!
""")
