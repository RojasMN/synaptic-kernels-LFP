# Synaptic LFP: Excitation-Inhibition Balance and Signal Analysis

## Overview

This repository contains a Python framework for simulating Local Field Potentials (LFPs) using the **Filtered Point Process (FPP)** formalism. The project explores how the physiological balance between synaptic excitation and inhibition (**E/I Balance**) shapes the LFP signal in both the time and frequency domains.

The codebase provides tools to generate synthetic LFP signals, simulate varying E/I ratios, and analyze the resulting data using two complementary approaches:
1.  **Spectral Parameterization (Frequency Domain):** Analyzing the aperiodic $1/f$ slope of the Power Spectral Density (PSD).
2.  **PSI Pattern (Time Domain):** A novel metric based on the derivative of the signal's autocorrelation, designed to capture effective synaptic time constants.

## Background

The simulations and analysis in this repository are grounded in the following theoretical concepts, detailed briefly in the `background.pdf` file.

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
    * `psi_pattern`: Computes the $\Psi$ pattern.
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
