import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt
import save_csv as sc

ecg_data = pd.read_csv(sc.new_file_path)
ecg_signal = ecg_data.iloc[:, 0].values
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)

# R、P、Q、S、T波峰
# Delineate the ECG signal
_, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=1000, method="peak",show=True,show_type='peaks')

plot = nk.events_plot([
                       waves_peak['ECG_T_Peaks'][:3],
                       waves_peak['ECG_P_Peaks'][:3],
                       waves_peak['ECG_Q_Peaks'][:3],
                       waves_peak['ECG_S_Peaks'][:3]], ecg_signal[:4000])
plt.show()