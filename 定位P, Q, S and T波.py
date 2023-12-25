import neurokit2 as nk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# R波的定位
ecg_signal = nk.data(dataset="ecg_1000hz")
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)

# 展示前 5 R-peaks
# nk.events_plot(rpeaks['ECG_R_Peaks'][:5], ecg_signal[:6000])
# plt.show()

# R、P、Q、S、T波峰
# Delineate the ECG signal
_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=1000, method="peak",show=True,show_type='peaks')
plt.show()

plot = nk.events_plot([rpeaks['ECG_R_Peaks'][:3],
                       waves_peak['ECG_T_Peaks'][:3],
                       waves_peak['ECG_P_Peaks'][:3],
                       waves_peak['ECG_Q_Peaks'][:3],
                       waves_peak['ECG_S_Peaks'][:3]], ecg_signal[:4000])
plt.show()
# P峰的起始点和T峰的偏移量
# Delineate the ECG signal and visualizing all P-peaks boundaries
signal_peak, waves_peak = nk.ecg_delineate(ecg_signal,
                                           rpeaks,
                                           sampling_rate=1000,
                                           method="peak",
                                           show=True,
                                           show_type='bounds_P')
plt.show()
# Delineate the ECG signal and visualizing all T-peaks boundaries
signal_peaj, waves_peak = nk.ecg_delineate(ecg_signal,
                                           rpeaks,
                                           sampling_rate=1000,
                                           method="peak",
                                           show=True,
                                           show_type='bounds_T')
plt.show()

# 连续小波法（CWT）
# Delineate the ECG signal
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=1000,
                                         method="cwt",
                                         show=True,
                                         show_type='all')
plt.show()
# Visualize P-peaks and T-peaks
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=1000,
                                         method="cwt",
                                         show=True,
                                         show_type='peaks')
plt.show()
# Visualize T-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=1000,
                                         method="cwt",
                                         show=True,
                                         show_type='bounds_T')
plt.show()
# Visualize P-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=1000,
                                         method="cwt",
                                         show=True,
                                         show_type='bounds_P')
plt.show()
# Visualize R-waves boundaries
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=1000,
                                         method="cwt",
                                         show=True,
                                         show_type='bounds_R')
plt.show()
# 离散小波方法 （DWT） - 默认方法
# Delineate the ECG signal
signal_dwt, waves_dwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=3000,
                                         method="dwt",
                                         show=True,
                                         show_type='all')
plt.show()
# Visualize P-peaks and T-peaks
signal_dwt, waves_dwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=3000,
                                         method="dwt",
                                         show=True,
                                         show_type='peaks')
plt.show()
# visualize T-wave boundaries
signal_dwt, waves_dwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=3000,
                                         method="dwt",
                                         show=True,
                                         show_type='bounds_T')
plt.show()
# Visualize P-wave boundaries
signal_dwt, waves_dwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=3000,
                                         method="dwt",
                                         show=True,
                                         show_type='bounds_P')
plt.show()
# Visualize R-wave boundaries
signal_dwt, waves_dwt = nk.ecg_delineate(ecg_signal,
                                         rpeaks,
                                         sampling_rate=3000,
                                         method="dwt",
                                         show=True,
                                         show_type='bounds_R')
plt.show()
