"""
Chapter 6: MLP in PyTorch
=========================
The modern way to build neural networks.

Compare this with 01_mlp_from_scratch.py to see how PyTorch simplifies things.

Run: python 02_mlp_pytorch.py
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import numpy as np

print("=" * 70)
print("MLP IN PYTORCH")
print("=" * 70)


# =============================================================================
# DEFINE THE MODEL
# =============================================================================
print("\n" + "=" * 70)
print("1. DEFINING THE MODEL")
print("=" * 70)

print("""
PyTorch models inherit from nn.Module.
Key methods:
    - __init__: Define layers
    - forward: Define computation
""")


class MLP(nn.Module):
    """Multi-Layer Perceptron in PyTorch"""

    def __init__(self, input_dim, hidden_dims, output_dim, dropout=0.0):
        super().__init__()

        # Build layers dynamically
        layers = []
        dims = [input_dim] + hidden_dims

        for i in range(len(dims) - 1):
            layers.append(nn.Linear(dims[i], dims[i + 1]))
            layers.append(nn.ReLU())
            if dropout > 0:
                layers.append(nn.Dropout(dropout))

        # Output layer (no ReLU, softmax is in loss function)
        layers.append(nn.Linear(dims[-1], output_dim))

        # nn.Sequential chains layers together
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


# Alternative: Explicit layer definition
class MLPExplicit(nn.Module):
    """Same MLP but with explicit layer definitions"""

    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


# Create model
model = MLP(input_dim=2, hidden_dims=[32, 16], output_dim=2)
print(f"\nModel architecture:")
print(model)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\nTotal parameters: {total_params}")
print(f"Trainable parameters: {trainable_params}")


# =============================================================================
# PREPARE DATA
# =============================================================================
print("\n" + "=" * 70)
print("2. PREPARING DATA")
print("=" * 70)

# Generate data
np.random.seed(42)
X, y = make_moons(n_samples=2000, noise=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.LongTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.LongTensor(y_test)

# Create DataLoader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f"Training samples: {len(train_dataset)}")
print(f"Test samples: {len(test_dataset)}")
print(f"Batch size: {batch_size}")
print(f"Batches per epoch: {len(train_loader)}")


# =============================================================================
# TRAINING SETUP
# =============================================================================
print("\n" + "=" * 70)
print("3. TRAINING SETUP")
print("=" * 70)

# Loss function
criterion = nn.CrossEntropyLoss()

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Learning rate scheduler (optional)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)

print(f"Loss function: CrossEntropyLoss")
print(f"Optimizer: Adam (lr=0.01)")
print(f"Scheduler: StepLR (decay by 0.1 every 30 epochs)")

# Device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")
model = model.to(device)


# =============================================================================
# TRAINING LOOP
# =============================================================================
print("\n" + "=" * 70)
print("4. TRAINING LOOP")
print("=" * 70)


def train_epoch(model, loader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()  # Set to training mode (enables dropout)
    total_loss = 0
    correct = 0
    total = 0

    for X_batch, y_batch in loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        # Forward pass
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)

        # Backward pass
        optimizer.zero_grad()  # Clear gradients
        loss.backward()        # Compute gradients
        optimizer.step()       # Update weights

        # Track metrics
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        correct += (predicted == y_batch).sum().item()
        total += y_batch.size(0)

    return total_loss / len(loader), correct / total


def evaluate(model, loader, criterion, device):
    """Evaluate model on data"""
    model.eval()  # Set to evaluation mode (disables dropout)
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():  # No gradient computation needed
        for X_batch, y_batch in loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += (predicted == y_batch).sum().item()
            total += y_batch.size(0)

    return total_loss / len(loader), correct / total


# Training
print("\nTraining...")
print("-" * 60)

epochs = 50
best_test_acc = 0

for epoch in range(epochs):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    test_loss, test_acc = evaluate(model, test_loader, criterion, device)

    scheduler.step()  # Update learning rate

    if test_acc > best_test_acc:
        best_test_acc = test_acc
        # Save best model
        torch.save(model.state_dict(), 'best_model.pth')

    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1:3d}: Train Loss={train_loss:.4f}, Train Acc={train_acc:.4f}, "
              f"Test Loss={test_loss:.4f}, Test Acc={test_acc:.4f}")

print(f"\nBest Test Accuracy: {best_test_acc:.4f}")


# =============================================================================
# MODEL INSPECTION
# =============================================================================
print("\n" + "=" * 70)
print("5. MODEL INSPECTION")
print("=" * 70)

print("\nLayer weights shapes:")
for name, param in model.named_parameters():
    print(f"  {name}: {param.shape}")

# Gradients (after training)
print("\nGradient shapes (should match weights):")
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"  {name}: {param.grad.shape}")


# =============================================================================
# INFERENCE
# =============================================================================
print("\n" + "=" * 70)
print("6. INFERENCE")
print("=" * 70)

# Load best model
model.load_state_dict(torch.load('best_model.pth'))
model.eval()

# Single prediction
sample = torch.FloatTensor([[0.5, 0.5]]).to(device)
with torch.no_grad():
    logits = model(sample)
    probs = torch.softmax(logits, dim=1)
    prediction = probs.argmax(dim=1)

print(f"\nSingle prediction:")
print(f"  Input: [0.5, 0.5]")
print(f"  Logits: {logits.cpu().numpy()}")
print(f"  Probabilities: {probs.cpu().numpy()}")
print(f"  Predicted class: {prediction.item()}")

# Batch prediction
print("\nBatch predictions:")
samples = torch.FloatTensor([
    [0.0, 0.0],
    [1.0, 1.0],
    [-1.0, 0.5],
    [0.5, -0.5]
]).to(device)

with torch.no_grad():
    logits = model(samples)
    probs = torch.softmax(logits, dim=1)
    predictions = probs.argmax(dim=1)

for i in range(len(samples)):
    print(f"  Input: {samples[i].cpu().numpy()}, "
          f"Probs: [{probs[i,0]:.3f}, {probs[i,1]:.3f}], "
          f"Pred: {predictions[i].item()}")


# =============================================================================
# COMPARISON: NUMPY vs PYTORCH
# =============================================================================
print("\n" + "=" * 70)
print("7. NUMPY vs PYTORCH COMPARISON")
print("=" * 70)

print("""
┌────────────────────────────────────────────────────────────────────────┐
│  Task              │  NumPy (Manual)          │  PyTorch              │
├────────────────────────────────────────────────────────────────────────┤
│  Forward pass      │  x @ W + b               │  model(x)             │
│  Activation        │  np.maximum(0, x)        │  nn.ReLU()            │
│  Loss              │  Manual cross-entropy    │  nn.CrossEntropyLoss()│
│  Gradients         │  Manual backprop         │  loss.backward()      │
│  Update weights    │  W -= lr * grad_W        │  optimizer.step()     │
│  GPU support       │  ❌                       │  model.to('cuda')     │
│  Save model        │  np.save()               │  torch.save()         │
│  Dropout           │  Manual random mask      │  nn.Dropout()         │
│  Batch norm        │  Complex manual code     │  nn.BatchNorm1d()     │
└────────────────────────────────────────────────────────────────────────┘

PyTorch Advantages:
    1. Automatic differentiation (autograd)
    2. GPU acceleration
    3. Pre-built layers and losses
    4. Ecosystem (torchvision, torchaudio, transformers)
    5. Easy model saving/loading
    6. Production deployment (TorchScript, ONNX)

When to Use NumPy:
    - Learning fundamentals (like 01_mlp_from_scratch.py)
    - Simple data processing
    - When you need exact control
""")


# =============================================================================
# ADVANCED: CUSTOM LAYER
# =============================================================================
print("\n" + "=" * 70)
print("8. BONUS: CUSTOM LAYER")
print("=" * 70)


class GatedLinear(nn.Module):
    """Custom gated linear layer: output = sigmoid(Wx) * tanh(Vx)"""

    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear_gate = nn.Linear(in_features, out_features)
        self.linear_transform = nn.Linear(in_features, out_features)

    def forward(self, x):
        gate = torch.sigmoid(self.linear_gate(x))
        transform = torch.tanh(self.linear_transform(x))
        return gate * transform


# Test custom layer
custom_layer = GatedLinear(10, 5)
test_input = torch.randn(3, 10)
test_output = custom_layer(test_input)

print(f"Custom GatedLinear layer:")
print(f"  Input shape: {test_input.shape}")
print(f"  Output shape: {test_output.shape}")
print(f"\nThis demonstrates how easy it is to create custom layers in PyTorch!")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("""
PyTorch Training Recipe:
────────────────────────
1. Define model (nn.Module)
2. Define loss (nn.CrossEntropyLoss, etc.)
3. Define optimizer (optim.Adam, etc.)
4. Training loop:
    a. model.train()
    b. outputs = model(inputs)
    c. loss = criterion(outputs, targets)
    d. optimizer.zero_grad()
    e. loss.backward()
    f. optimizer.step()
5. Evaluation:
    a. model.eval()
    b. with torch.no_grad(): ...
6. Save/Load:
    a. torch.save(model.state_dict(), 'model.pth')
    b. model.load_state_dict(torch.load('model.pth'))

This is the foundation for ALL deep learning in PyTorch!
""")

# Cleanup
import os
if os.path.exists('best_model.pth'):
    os.remove('best_model.pth')
