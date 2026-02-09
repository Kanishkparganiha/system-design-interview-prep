# Chapter 3: Probability and Information Theory

> "Probability theory is the mathematical framework for reasoning about uncertainty."

---

## Why Probability for Deep Learning?

- **Uncertainty quantification**: Neural networks output probabilities
- **Loss functions**: Cross-entropy is derived from information theory
- **Generative models**: VAEs, GANs, diffusion models
- **Bayesian deep learning**: Uncertainty estimation
- **Regularization**: Dropout is probabilistic

---

## Scripts in This Chapter

| Script | Topic | Key Concepts |
|--------|-------|--------------|
| `01_probability_basics.py` | Foundations | Random variables, PMF, PDF, expectations, variance |
| `02_information_theory.py` | Information | Entropy, cross-entropy, KL divergence, loss functions |
| `03_common_distributions.py` | Distributions | Bernoulli, Gaussian, Categorical, softmax |
| `04_bayes_theorem.py` | Bayes | Prior, likelihood, posterior, Naive Bayes |
| `05_sampling.py` | Sampling | Monte Carlo, reparameterization, MCMC, Gumbel-softmax |

---

## Key Concepts

### 1. Random Variables

```
Discrete: X ∈ {0, 1, 2, ...}  →  PMF: P(X = x)
Continuous: X ∈ ℝ            →  PDF: p(x), P(a ≤ X ≤ b) = ∫p(x)dx
```

### 2. Expectation and Variance

```
E[X] = Σ x·P(x)         (discrete)
E[X] = ∫ x·p(x)dx       (continuous)

Var[X] = E[(X - E[X])²] = E[X²] - E[X]²
```

### 3. Common Distributions

| Distribution | Support | Use in DL |
|--------------|---------|-----------|
| Bernoulli | {0, 1} | Binary classification output |
| Categorical | {1, ..., K} | Multi-class classification |
| Gaussian | ℝ | VAE latent space, noise |
| Uniform | [a, b] | Initialization, sampling |

### 4. Information Theory

```
Entropy:        H(X) = -Σ P(x) log P(x)
Cross-entropy:  H(P, Q) = -Σ P(x) log Q(x)
KL Divergence:  D_KL(P || Q) = Σ P(x) log(P(x)/Q(x))

Cross-entropy loss = -Σ y·log(ŷ)  ← This is cross-entropy!
```

---

## Run Order

```bash
python 01_probability_basics.py
python 02_information_theory.py
python 03_common_distributions.py
python 04_bayes_theorem.py
python 05_sampling.py
```
