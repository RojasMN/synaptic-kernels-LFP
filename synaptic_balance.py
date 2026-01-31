import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# Packages 
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import random
import time
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

from utils.signal_processing import *
from utils.fpp_simulation import *
from utils.plotting import *


# Worker function
def run_single_sim(args):
    
    # Unpack arguments 
    sim_id, kernel_ampa, kernel_gaba, fs, t_sec, rate_ex, rate_in, w_ex, w_in = args
    
    # EIB
    min_eib = 0.01
    max_eib = 100
    n_total = 10000
    
    log_eib = random.uniform(np.log10(min_eib), np.log10(max_eib))
    target_eib = 10 ** log_eib
    
    n_ex = int(n_total * (target_eib / (1 + target_eib)))
    n_in = n_total - n_ex
    n_ex = max(1, n_ex)
    n_in = max(1, n_in)
    
    eib = n_ex / n_in
    
    # LFP
    lfp, _, _, _ = simulate_fpp_balance(kernel_ex = kernel_ampa, 
                                        kernel_in = kernel_gaba, 
                                        fs = fs, 
                                        t_sec = t_sec,
                                        n_ex = n_ex, 
                                        n_in = n_in, 
                                        rate_ex = rate_ex, 
                                        rate_in = rate_in,
                                        w_ex = w_ex, 
                                        w_in = w_in)
    
    psi, psi_lags = averaged_psi_pattern(signal = lfp, fs = fs, window_sec = 2, overlap_sec = 1)
    psd, freqs = averaged_multitaper_psd(signal = lfp, fs = fs, window_sec = 2, overlap_sec = 1, NW = 3)
    
    # Pattern parameterization 
    psi_duration, psi_rise, psi_decay, psi_maxval = psi_params(psi = psi,
                                                               time_lags = psi_lags)

    # Spectral parameterization: linear regression between 40 and 85 Hz
    model_linear = specparam(psd = psd,
                             freqs = freqs,
                             freq_range = [40, 85],
                             aperiodic_mode = 'fixed')
        
    offset_linear, exp_linear = model_linear.results.params.aperiodic.params
        
        
    # Spectral parameterization: double exponent fit between 1 and 300 Hz a
    model_dexp = specparam(psd = psd,
                           freqs = freqs, 
                           freq_range = [1, 300],
                           aperiodic_mode = 'doublexp')
        
    offset_dexp, exp_0, knee, exp_1 = model_dexp.results.params.aperiodic.params    
    
    return {
        'sim_id': sim_id,
        'n_ex': n_ex,
        'n_in': n_in,
        'eib': eib,
        'psi_duration': psi_duration,
        'psi_rise': psi_rise,
        'psi_decay': psi_decay,
        'psi_maxval': psi_maxval,
        'offset_linear': offset_linear,
        'exp_linear': exp_linear,
        'offset_dexp': offset_dexp,
        'exp_0': exp_0,
        'knee': knee,
        'exp_1': exp_1
    }


# Parallelized simulation 
def eib_sim_parallel(num_sims, fs = 10000, t_sec = 150, n_jobs = -1):
    
    kernel_ampa, _ = dual_exponential(t_sec = t_sec, 
                                      fs = fs, 
                                      tau_rise_s = 0.2 / 1000,
                                      tau_decay_s = 2 / 1000, 
                                      max_amplitude = 1)

    kernel_gaba, _ = dual_exponential(t_sec = t_sec, 
                                      fs = fs, 
                                      tau_rise_s = 0.5 / 1000,
                                      tau_decay_s = 10 / 1000, 
                                      max_amplitude = 1)
    
    # Fixed parameters
    rate_ex, rate_in = 50, 50       # Firing rates
    w_ex, w_in = -1, 1              # Weights
    
    tasks = []
    for i in range(num_sims):
        task_args = (i, kernel_ampa, kernel_gaba, fs, t_sec, rate_ex, rate_in, w_ex, w_in)
        tasks.append(task_args)
        
    # CPU cores
    if n_jobs == -1:
        n_jobs = cpu_count()
        
    print(f'Starting {num_sims} simulations on {n_jobs} cores.')

    results = []
    with Pool(processes = n_jobs) as pool:
        for result in tqdm(pool.imap_unordered(run_single_sim, tasks), total = num_sims, desc = 'Running simulations'):
            results.append(result)
    
    final_data = pd.DataFrame(results)
    final_data = final_data.sort_values('sim_id').reset_index(drop = True)
        
    return final_data


# Run the simulation
if __name__ == '__main__':
    
    SIM_COUNT = 2000
    
    OUTPUT_FOLDER = 'simulation_results'
    FILENAME = 'eib_simulation_results.csv'
    
    os.makedirs(OUTPUT_FOLDER, exist_ok = True)
    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, FILENAME)
    OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, FILENAME)
    
    start_time = time.time()
    final_results = eib_sim_parallel(num_sims = SIM_COUNT, n_jobs = -1)
    final_results.to_csv(OUTPUT_FILE, index = False)
    elapsed = time.time() - start_time
    
    print(f'Simulation took {elapsed:.2f} seconds.')
    print(f'Results saved to {OUTPUT_FILE}')