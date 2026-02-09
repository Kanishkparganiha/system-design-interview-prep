# Chapter 6: Deep Feedforward Networks

> "Your first real neural network."

---

## This is Where Deep Learning Begins!

Everything before this chapter was preparation. Now we combine:
- Linear algebra (matrix operations)
- Probability (loss functions)
- Optimization (gradient descent)
- ML basics (generalization)

...to build neural networks!

---

## Scripts in This Chapter

| Script | Topic | Key Concepts |
|--------|-------|--------------|
| `01_mlp_from_scratch.py` | MLP in NumPy | Activations, layers, backprop, full training |
| `02_mlp_pytorch.py` | PyTorch MLP | nn.Module, DataLoader, training loop, inference |

---

## Key Concepts

### 1. Single Neuron (Perceptron)

```
         x₁ ──w₁──╲
                   ╲
         x₂ ──w₂────╳──▶ Σ ──▶ σ(z) ──▶ output
                   ╱
         x₃ ──w₃──╱
                  ↑
               bias b

z = w₁x₁ + w₂x₂ + w₃x₃ + b = wᵀx + b
output = σ(z)   where σ is activation function
```

### 2. Multi-Layer Perceptron (MLP)

```
Input     Hidden Layer 1    Hidden Layer 2    Output
  ○────────────○─────────────────○────────────○
  ○────────────○─────────────────○────────────○
  ○────────────○─────────────────○
  ○            ○

h₁ = σ(W₁x + b₁)
h₂ = σ(W₂h₁ + b₂)
y = softmax(W₃h₂ + b₃)
```

### 3. Universal Approximation Theorem

```
A feedforward network with:
    - At least one hidden layer
    - Sufficient neurons
    - Non-linear activation

Can approximate ANY continuous function!

(But it doesn't tell us HOW to learn it...)
```

### 4. Backpropagation

```
Forward Pass:  x → h₁ → h₂ → ŷ → Loss

Backward Pass: ∂L/∂ŷ → ∂L/∂h₂ → ∂L/∂h₁ → ∂L/∂W

Chain Rule: ∂L/∂W₁ = ∂L/∂ŷ · ∂ŷ/∂h₂ · ∂h₂/∂h₁ · ∂h₁/∂W₁
```

---

## Activation Functions Cheatsheet

| Function | Formula | Range | Use Case |
|----------|---------|-------|----------|
| ReLU | max(0, x) | [0, ∞) | Hidden layers (default) |
| Sigmoid | 1/(1+e⁻ˣ) | (0, 1) | Binary output |
| Tanh | (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | (-1, 1) | Hidden (less common) |
| Softmax | eˣⁱ/Σeˣʲ | (0, 1) | Multi-class output |
| LeakyReLU | max(0.01x, x) | (-∞, ∞) | Avoid dead ReLU |

---

## Run Order

```bash
python 01_mlp_from_scratch.py   # Start here! Understand the fundamentals
python 02_mlp_pytorch.py        # Then see how PyTorch simplifies things
```
