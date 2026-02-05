# Synaptic LFP: Excitation-Inhibition Balance and Signal Analysis

## Overview

This repository contains a Python framework for simulating Local Field Potentials (LFPs) using the **Filtered Point Process (FPP)** formalism. The project explores how the physiological balance between synaptic excitation and inhibition (**E/I Balance**) shapes the LFP signal in both the time and frequency domains.

The codebase provides tools to generate synthetic LFP signals, simulate varying E/I ratios, and analyze the resulting data using two complementary approaches:
1.  **Spectral Parameterization (Frequency Domain):** Analyzing the aperiodic $1/f$ slope of the Power Spectral Density (PSD).
2.  **PSI Pattern (Time Domain):** A novel metric based on the derivative of the signal's autocorrelation, designed to capture effective synaptic time constants.

## Theoretical Background

The simulations and analysis in this repository are grounded in the following theoretical concepts, detailed in the accompanying Jupyter Notebooks.

### 1. The Filtered Point Process (FPP) Model
The LFP is modeled as the summation of discrete synaptic events (Post-Synaptic Potentials, PSPs). Mathematically, this is a convolution between a spike train (modeled as a Poisson point process) and a synaptic kernel (the shape of the PSP):

$$LFP(t) = (S * K)(t) = \sum_{j} K(t - t_j)$$

Where $S$ is the spike train and $K$ is the synaptic kernel (e.g., a dual-exponential function representing AMPA or GABA currents).

### 2. The $\Psi$ Pattern 
To analyze the signal in the time domain, the $\Psi$ pattern is introduced, defined as the negative derivative of the autocorrelation function ($R_{xx}$) of the signal:

$$\Psi(\tau) = - \frac{d}{d\tau} R_{xx}(\tau)$$

Theoretical analysis shows that for FPP signals, $\Psi(\tau)$ recovers the shape of the underlying synaptic kernel $K(t)$ (specifically its autocorrelation). This allows us to estimate synaptic rise and decay times directly from the raw LFP trace.

### 3. Spectral Parameterization
In the frequency domain, the LFP is characterized by a "1/f-like" decay. We use the `specparam` (formerly FOOOF) algorithm to parameterize the aperiodic component of the PSD. The steepness of this decay (the spectral exponent $\chi$) is mathematically related to the decay time constant of the synaptic kernels.

### 4. Synaptic Balance (EIB)
The core hypothesis of this project is that the **Excitation-Inhibition Balance (EIB)** acts as a modulator of the "effective" time constant of the neural circuit.
* **High Excitation:** Dominated by fast AMPA kinetics $\rightarrow$ Faster signal decay $\rightarrow$ Flatter PSD slope.
* **High Inhibition:** Dominated by slow GABA kinetics $\rightarrow$ Slower signal decay $\rightarrow$ Steeper PSD slope.
* This relationship is observable in both the spectral exponent and the PSI pattern duration.

---

## Repository Structure

### 1. Simulation Notebooks
The `notebooks/` directory contains step-by-step tutorials and theoretical validations:

* **`01_fpps.ipynb`**: Introduction to the mathematics of Filtered Point Processes and kernel generation (Alpha, Square, Dual-Exponential).
* **`02_psi_pattern.ipynb`**: Derivation and implementation of the PSI Pattern. Demonstrates how $\Psi(\tau)$ mirrors the synaptic kernel.
* **`03_specparam.ipynb`**: Implementation of spectral parameterization to extract aperiodic exponents from simulated LFPs.
* **`04_synaptic_balance.ipynb`**: The main experiment. Simulates mixed Excitatory/Inhibitory signals and correlates the E/I ratio with the metrics defined in previous notebooks.

### 2. Python Package
The core logic is modularized in the following files:

* **`fpp_simulation.py`**:
    * Kernel generators: `alpha_function`, `dual_exponential`, `triple_square_kernel`.
    * Simulation engines: `simulate_fpp` (single population) and `simulate_fpp_balance` (dual E/I populations).
* **`signal_processing.py`**:
    * `psi_pattern`: Computes the PSI metric.
    * `averaged_multitaper_psd`: Robust PSD estimation using Multitaper methods (`nitime`).
    * `specparam`: Wrapper for the `specparam` library to fit aperiodic slopes.
* **`plotting.py`**: Utilities for visualizing traces and power spectra.

### 3. Large-Scale Simulation 
* **`synaptic_balance.py`**:
    * Contains the main pipeline for large-scale Monte Carlo simulations.
    * `eib_sim_parallel`: Runs parallelized simulations of varying E/I ratios, computing both PSI and Spectral features for each iteration.
---

## Installation & Dependencies

To run the simulations, you will need the following Python packages:

```bash
pip install numpy pandas matplotlib scipy tqdm nitime specparam
```
