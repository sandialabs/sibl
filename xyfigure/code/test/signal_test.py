import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# references
# https://dsp.stackexchange.com/questions/49460/apply-low-pass-butterworth-filter-in-python

# client filter input begin
fs = 100  # Hz, sampling frequency in t_v_sines.csv
fc = 10  # cutoff frequency of the filter
filter_order = 4  
filter_type = 'low'
# client filter input end

# client signal data begin
t = np.arange(fs) / fs  # seconds, [0, 1) by 0.01 seconds
t2 = np.arange(2 * fs) / fs  # seconds, [0, 2) by 0.01 seconds
# print('time vector: ')
# print(t)
# print('time 2 vector: ')
# print(t2)
f1 = 2.0  # Hz, frequency of u1
f2 = 20.0 # Hz, frequency of u2

# three signals
u1 = np.sin(2 * np.pi * f1 * t2)
u2 = np.sin(2 * np.pi * f2 * t2)
u3 = u1 + u2
# client signal data end


# Butterworth filter service begin
Wn = fc / (fs / 2)  # normalized critical frequency
b, a = signal.butter(filter_order, Wn, filter_type)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
u3_filtered = signal.filtfilt(b, a, u3)

# visualization service begin
u1str = 'u1 = sin(' + str(f1) + ' * 2 pi t)'
u2str = 'u2 = sin(' + str(f2) + ' * 2 pi t)'
plt.plot(t2, u1, label=u1str, linewidth=3, alpha=0.7)
plt.plot(t2, u2, label=u2str)
plt.plot(t2, u3, label='u3 = u1 + u2')
plt.plot(t2, u3_filtered, label='u3 filtered', linestyle='dashed')
plt.legend()
plt.show()

