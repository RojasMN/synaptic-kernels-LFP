# Synaptic LFP: Excitation-Inhibition Balance and Signal Analysis

## Overview

This repository contains a Python framework for simulating Local Field Potentials (LFPs) using the **Filtered Point Process (FPP)** formalism. The project explores how the physiological balance between synaptic excitation and inhibition (**E/I Balance**) shapes the LFP signal in both the time and frequency domains.

The codebase provides tools to generate synthetic LFP signals, simulate varying E/I ratios, and analyze the resulting data using two complementary approaches:
1.  **Spectral Parameterization (Frequency Domain):** Analyzing the aperiodic $1/f$ slope of the Power Spectral Density (PSD).
2.  **PSI Pattern (Time Domain):** A novel metric based on the derivative of the signal's autocorrelation, designed to capture effective synaptic time constants.

## Background

The simulations and analysis in this repository are grounded in the following theoretical concepts, detailed briefly in the `background.pdf` file.

## Repository Structure

### 1. Simulation Notebooks
The `notebooks/` directory contains step-by-step tutorials and theoretical validations:

* **`01_fpps.ipynb`**: Introduction to the mathematics of Filtered Point Processes and kernel generation (Alpha, Square, Dual-Exponential).
* **`02_psi_pattern.ipynb`**: Derivation and implementation of the PSI Pattern. Demonstrates how $\Psi(\tau)$ mirrors the synaptic kernel.
* **`03_specparam.ipynb`**: Implementation of spectral parameterization to extract aperiodic exponents from simulated LFPs.
* **`04_synaptic_balance.ipynb`**: The main experiment. Simulates mixed Excitatory/Inhibitory signals and correlates the E/I ratio with the metrics defined in previous notebooks.

### 2. Python Files
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

## Installation and Dependencies
To run the simulations, you will need the following Python packages:

```bash
pip install numpy pandas matplotlib scipy tqdm nitime specparam

```
---

## References

For further reading, please consult the following literature. The **$\Psi$ pattern** and its application as a signal analysis tool for recovering transients are detailed in **Díaz et al. (2023)**. The methodology for the **parameterization of power spectra** (separating periodic and aperiodic components) is established in **Donoghue et al. (2020)**. For physiological background on the **spectral exponent** and scale-free brain activity, refer to **He (2014)**. Additionally, the **Filtered Point Process (FPP)** model has been extensively used to simulate neural signals such as EEGs and LFPs in works by **Gao et al. (2017)**, **Halgren et al. (2021)**, and **Miller et al. (2009)**.

1. Díaz, J., Ando, H., Han, G., Malyshevskaya, O., Hayashi, X., Letelier, J.-C., Yanagisawa, M., & Vogt, K. E. (2023). Recovering Arrhythmic EEG Transients from Their Stochastic Interference. *arXiv*. [DOI: 10.48550/arXiv.2303.07683](https://doi.org/10.48550/arXiv.2303.07683)
2. Donoghue, T., Haller, M., Peterson, E. J., Varma, P., Sebastian, P., Gao, R., Noto, T., Lara, A. H., Wallis, J. D., Knight, R. T., Shestyuk, A., & Voytek, B. (2020). Parameterizing neural power spectra into periodic and aperiodic components. *Nature Neuroscience*, *23*(12), 1655–1665. [DOI: 10.1038/s41593-020-00744-x](https://doi.org/10.1038/s41593-020-00744-x)
3. Gao, R., Peterson, E. J., & Voytek, B. (2017). Inferring synaptic excitation/inhibition balance from field potentials. *NeuroImage*, *158*, 70–78. [DOI: 10.1016/j.neuroimage.2017.06.078](https://doi.org/10.1016/j.neuroimage.2017.06.078)
4. He, B. J. (2014). Scale-free brain activity: past, present, and future. *Trends in Cognitive Sciences*, *18*(9), 480–487. [DOI: 10.1016/j.tics.2014.04.003](https://doi.org/10.1016/j.tics.2014.04.003)
5. Halgren, M., Kang, R., Voytek, B., Ulbert, I., Fabo, D., Eross, L., ... & Halgren, E. (2021). The timescale and magnitude of aperiodic activity decreases with cortical depth in humans, macaques and mice. *bioRxiv*. [DOI: 10.1101/2021.07.28.454235](https://doi.org/10.1101/2021.07.28.454235)
6. Miller, K. J., Sorensen, L. B., Ojemann, J. G., & den Nijs, M. (2009). Power-law scaling in the brain surface electric potential. *PLOS Computational Biology*, *5*(12), e1000609. [DOI: 10.1371/journal.pcbi.1000609](https://doi.org/10.1371/journal.pcbi.1000609)





