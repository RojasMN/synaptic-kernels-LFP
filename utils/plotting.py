# Packages 
import numpy as np
import matplotlib.pyplot as plt


def plot_trace(trace, time, size = (5, 2), xlim = (0, 0.05), title = 'Signal', trace_color = 'tab:blue', linewidth = 2):
    
    plt.figure(figsize = size)
    plt.plot(time, trace, color = trace_color, linewidth = linewidth)
    
    t_arr = np.asarray(time)
    y_arr = np.asarray(trace)
    mask = (t_arr >= xlim[0]) & (t_arr <= xlim[1])
    
    if np.any(mask):
        visible_y = y_arr[mask]
        y_min = visible_y.min()
        y_max = visible_y.max()
        
        y_range = y_max - y_min
        if y_range == 0: y_range = 1.0  # Prevent crash if flat line
        margin = y_range * 0.1
        plt.ylim(y_min - margin, y_max + margin)
    
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (AU)")
    plt.xlim(xlim)
    plt.grid(True, which = 'both', linestyle = '--', alpha = 0.7)
    plt.axhline(0, color = 'black', linewidth = 0.2) 
    plt.show()

    
def plot_psd_log(psd, freqs, size = (5, 4), xlim = None, title = 'PSD', color = 'black', linewidth = 1.5):
    
    plt.figure(figsize = size)
    plt.loglog(freqs, psd, color = color, linewidth = linewidth)
    
    if xlim is not None:
        plt.xlim(xlim)
        f_arr = np.asarray(freqs)
        p_arr = np.asarray(psd)
        mask = (f_arr >= xlim[0]) & (f_arr <= xlim[1]) & (f_arr > 0)

        if np.any(mask):
            visible_power = p_arr[mask]
            p_min = visible_power.min()
            p_max = visible_power.max()
            plt.ylim(p_min * 0.8, p_max * 1.5)
    
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power ($AU^2/Hz$)")
    
    plt.grid(True, which = 'both', linestyle = '--', alpha = 0.6)
    plt.show()