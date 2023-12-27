import simplefilter as slr
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

filename = slr.filename
ecg_data = pd.read_csv(filename)
ecg_signal = ecg_data.iloc[:, 0].values
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)

nk.events_plot(rpeaks['ECG_R_Peaks'][:5], ecg_signal[:6000])
plt.show()