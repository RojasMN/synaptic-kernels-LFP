# Packages 
import numpy as np

############################## KERNEL GENERATORS ##############################

def alpha_function(t_sec, fs, tau_s, max_amplitude, effective_duration = 0.1):
    
    N = int(fs * t_sec)
    time = np.arange(N) / fs 
    kernel = time * np.exp(-time / tau_s)
    kernel[time > effective_duration] = 0
    
    if np.max(kernel) > 0:
        kernel = kernel / np.max(kernel) * max_amplitude
        
    return kernel, time 


def triple_square_kernel(t_sec, fs, t1_s, t2_s, t3_s, amplitude1 = 1.0, amplitude2 = 1.0, amplitude3 = 1.0):
 
    # Generates a square pulse kernel with three possible amplitude levels 

    N = int(fs * t_sec)
    time = np.arange(N) / fs
    kernel = np.zeros_like(time)
    
    kernel[(time >= 0) & (time < t1_s)] = amplitude1
    kernel[(time >= t1_s) & (time < t2_s)] = amplitude2
    kernel[(time >= t2_s) & (time < t3_s)] = amplitude3
    kernel[time >= t3_s] = 0
    
    return kernel, time

    
def dual_exponential(t_sec, fs, tau_rise_s, tau_decay_s, max_amplitude, effective_duration = 0.1):
    
    if tau_rise_s >= tau_decay_s:
        print(f'tau_rise_s ({tau_rise_s}) must be greater than tau_decay_s ({tau_decay_s}).')
        return 0
    
    N = int(fs * t_sec)
    time = np.arange(N) / fs
    kernel = np.exp(-time / tau_decay_s) - np.exp(-time / tau_rise_s)
    kernel[time > effective_duration] = 0
    
    if np.max(kernel) > 0:
        kernel = kernel / np.max(kernel) * max_amplitude
    
    return kernel, time


############################## LFP GENERATORS ##############################

# One kernel LFP
def simulate_fpp(kernel, fs, t_sec, num_neurons, rate):
    
    N = int(fs * t_sec)
    time = np.arange(N) / fs
    n_bins = len(time)
    dt = 1 / fs 
    
    # Spike train
    prob_spike = rate * dt 
    spikes_pop = np.random.binomial(n = num_neurons, p = prob_spike, size = n_bins) 
    
    # Match number of points between the kernel and the signal
    if len(kernel) != N:
        print(f'Kernel must have the same number of points of the signal.')
        return 0
    
    F_spike = np.fft.fft(spikes_pop)
    F_kernel = np.fft.fft(kernel)
    signal = np.fft.ifft(F_spike * F_kernel).real
    signal = signal - np.mean(signal)
    
    event_rate = np.sum(spikes_pop) / t_sec
    
    return signal, time, event_rate


# Two kernel LFP (usually excitatory AMPA and inhibitory GABAa synaptic events are used)
def simulate_fpp_balance(kernel_ex, kernel_in, fs, t_sec, n_ex, n_in, rate_ex, rate_in, w_ex = -1, w_in = 1):
    
    N = int(fs * t_sec)
    time = np.arange(N) / fs
    n_bins = len(time)
    dt = 1 / fs 
    
    # Excitatory and inhibitory spike trains 
    prob_spike_ex = rate_ex * dt 
    spikes_pop_ex = np.random.binomial(n = n_ex, p = prob_spike_ex, size = n_bins)
    prob_spike_in = rate_in * dt 
    spikes_pop_in = np.random.binomial(n = n_in, p = prob_spike_in, size = n_bins) 
    
    # Match number of points between the kernel and the signal
    if len(kernel_ex) != N or len(kernel_in) != N:
        print('Kernels must have the same number of points of the signal.')
        return 0
    
    # FFT
    F_spike_ex = np.fft.fft(spikes_pop_ex)
    F_spike_in = np.fft.fft(spikes_pop_in)
    F_kernel_ex = np.fft.fft(kernel_ex)
    F_kernel_in = np.fft.fft(kernel_in)
    
    # Excitatory and inhibitory signals 
    signal_ex = np.fft.ifft(F_spike_ex * F_kernel_ex).real
    signal_in = np.fft.ifft(F_spike_in * F_kernel_in).real
    signal_ex = signal_ex - np.mean(signal_ex)
    signal_in = signal_in - np.mean(signal_in)
    
    # Total signal
    total_signal = (signal_ex * w_ex) + (signal_in * w_in)
    
    return total_signal, (signal_ex * w_ex), (signal_in * w_in), time