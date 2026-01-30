# Packages 
import numpy as np
from nitime.algorithms.spectral import multi_taper_psd
from numpy.lib.stride_tricks import sliding_window_view
from specparam import SpectralModel


def circular_autocorrelation(signal, fs):
    
    N = signal.shape[-1]
    time_lags = np.arange(N) / fs
    
    F_signal = np.fft.fft(signal)
    psd = F_signal * np.conj(F_signal)
    autocorr = np.fft.ifft(psd).real

    return autocorr / N, time_lags
    

def circular_crosscorrelation(signal1, signal2, fs):
    
    N = signal1.shape[-1]
    assert signal2.shape[-1] == N
    time_lags = np.arange(N) / fs
    
    F1 = np.fft.fft(signal1)
    F2 = np.fft.fft(signal2)
    cross_psd = F1 * np.conj(F2)
    cross_corr = np.fft.ifft(cross_psd).real
    
    return cross_corr / N, time_lags


def psi_pattern(signal, fs):
    
    # The frequency rate needs to be defined to compute a good estimate 
    # of the derivative of the autocorrelation
    
    N = signal.shape[-1]
    time_lags = np.arange(N) / fs
    
    autocorr, _ = circular_autocorrelation(signal, fs)
    psi = -np.gradient(autocorr, 1 / fs, axis = -1)
    
    return psi, time_lags 


def averaged_multitaper_psd(signal, fs, window_sec, overlap_sec, NW = 3):
    
    """
    Parameters:
    - signal: 1D array of the time-series data 
    - fs: Sampling frequency
    - window_sec: Length of each segment in seconds
    - overlap_sec: Overlap between segments in seconds
    - NW: Time-bandwidth product. 
    
    NW controls the smoothing of the PSD. A higher value implies a smoother trace but less frequency resolution. 
    
    """
    
    n_window = int(window_sec * fs)
    n_overlap = int(overlap_sec * fs)
    step = n_window - n_overlap
    
    # This creates a virtual view without copying data (memory efficient)
    # Shape: (number of windows, samples per window)
    windows = sliding_window_view(signal, window_shape = n_window)[::step].copy()
    
    # Compute multitaper PSD using nitime package
    freqs, psd_all, _ = multi_taper_psd(windows, Fs = fs, NW = NW, adaptive = True, jackknife = False)
    avg_psd = np.mean(psd_all, axis = 0)
    
    return avg_psd, freqs


def averaged_psi_pattern(signal, fs, window_sec, overlap_sec):
    
    # This function uses the same logic as the multitaper function to compute the 
    # averaged PSI pattern across all segments of a given signal
    
    n_window = int(window_sec * fs)
    n_overlap = int(overlap_sec * fs)
    step = n_window - n_overlap
    
    segments = sliding_window_view(signal, window_shape = n_window)[::step].copy()
    psi_segments, time_lags = psi_pattern(segments, fs)
    avg_psi = np.mean(psi_segments, axis = 0)
    
    return avg_psi, time_lags


def psi_params(psi, time_lags, decay_threshold = 0.15):
    
    idx_max = np.argmax(psi)
    max_val = psi[idx_max]
    t_max = time_lags[idx_max]
    rise_time = t_max - time_lags[0]
    
    psi_decay_seg = psi[idx_max: ]
    target_val = max_val * decay_threshold
    
    # The decay time index is relative to the segment (we have to add the initial part)
    below_target_indices = np.where(psi_decay_seg <= target_val)[0]
    idx_decay_relative = below_target_indices[0]
    idx_decay_end = idx_max + idx_decay_relative
    
    t_decay_end = time_lags[idx_decay_end]
    decay_time = t_decay_end - t_max
    
    return t_max, rise_time, decay_time, max_val


def specparam(psd, freqs, freq_range = [40, 85], aperiodic_mode = 'fixed', verbose = False):
    
    fm = SpectralModel(peak_width_limits=[1, 8], max_n_peaks=6, min_peak_height=0.15, aperiodic_mode = aperiodic_mode)
    fm.add_data(freqs, psd, freq_range)
    fm.fit()
    
    aperiodic_params = fm.results.params.aperiodic.params
    error = fm.results.metrics.results['error_mae']
    r2 = fm.results.metrics.results['gof_rsquared']
    
    if verbose == True:
        print(f'Aperiodic Params: {aperiodic_params}')
        print(f'Error: {error}')
        print(f'R2: {r2}')
    
    return fm