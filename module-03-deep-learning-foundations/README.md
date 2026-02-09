# Module 03: Deep Learning Foundations

> Based on "Deep Learning" by Goodfellow, Bengio, and Courville (Chapters 2-6)
> Learn by coding — every concept implemented from scratch in NumPy and PyTorch.

---

## Book Reference

📚 **Deep Learning** by Ian Goodfellow, Yoshua Bengio, and Aaron Courville
- Free online: [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/)

---

## Module Structure

| Chapter | Topic | Key Concepts |
|---------|-------|--------------|
| [Chapter 2](./chapter-02-linear-algebra/) | **Linear Algebra** | Vectors, matrices, eigendecomposition, SVD |
| [Chapter 3](./chapter-03-probability/) | **Probability & Information Theory** | Distributions, Bayes, entropy, KL divergence |
| [Chapter 4](./chapter-04-numerical-computation/) | **Numerical Computation** | Overflow, gradients, optimization |
| [Chapter 5](./chapter-05-ml-basics/) | **Machine Learning Basics** | Capacity, bias-variance, MLE, regularization |
| [Chapter 6](./chapter-06-feedforward-networks/) | **Deep Feedforward Networks** | MLPs, activation functions, backpropagation |

---

## Learning Path

```
Chapter 2: Linear Algebra
         │
         │  "The language of deep learning"
         ▼
Chapter 3: Probability
         │
         │  "Reasoning under uncertainty"
         ▼
Chapter 4: Numerical Computation
         │
         │  "Making it work on computers"
         ▼
Chapter 5: ML Basics
         │
         │  "The foundations before depth"
         ▼
Chapter 6: Feedforward Networks
         │
         │  "Your first neural network"
         ▼
    Ready for CNNs, RNNs, Transformers!
```

---

## Prerequisites

```bash
# Create virtual environment (recommended)
python -m venv deep-learning-env
source deep-learning-env/bin/activate  # Linux/Mac
# or: deep-learning-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## How to Use This Module

### For Each Chapter:

1. **Read** the README for conceptual understanding
2. **Run** the Python scripts to see concepts in action
3. **Modify** the code and experiment
4. **Complete** the exercises at the end

### Suggested Daily Practice:

```
Day 1-3:   Chapter 2 - Linear Algebra
Day 4-6:   Chapter 3 - Probability
Day 7-8:   Chapter 4 - Numerical Computation
Day 9-12:  Chapter 5 - ML Basics
Day 13-18: Chapter 6 - Feedforward Networks
Day 19-21: Review & Build a project
```

---

## What You'll Build

By the end of this module, you'll have implemented:

- ✅ Matrix operations from scratch
- ✅ PCA using eigendecomposition
- ✅ Probability distributions and sampling
- ✅ Gradient descent optimizer
- ✅ Linear and logistic regression
- ✅ Multi-layer perceptron (MLP) from scratch
- ✅ Backpropagation algorithm
- ✅ Complete neural network in NumPy AND PyTorch

---

## Quick Start

```bash
cd module-03-deep-learning-foundations

# Start with linear algebra basics
cd chapter-02-linear-algebra
python 01_vectors_matrices.py

# Each script is self-contained and runnable
python 02_matrix_operations.py
python 03_eigendecomposition.py
```

---

*"If you can't implement it, you don't understand it."*
