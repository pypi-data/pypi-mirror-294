import numpy as np
from scipy import signal
from scipy.fft import rfft, rfftfreq


class FrequencyAnalysis:

    @staticmethod
    def calc_fft(data, sample_rate):
        """Calculate FFT. Transfrom Signal data from
        Time domain to Frequenct domain.

        Args:
            data (numpy.ndarray): Signal data in Time domain
            sample_rate (scalar): Sampling rate [Hz]

        Returns:
            1. numpy.ndarray: x-axis value: frequency
            2. numpy.ndarray: y-axis value: magnitude
        """
        sample_size = len(data)

        # yf = fft(data)
        # xf = fftfreq(sample_size, 1 / sample_rate)

        # yf = rfft(data)  # only get the right side
        yf = rfft(data, norm='forward')  # norm='forward' 'ortho'

        # as used rfft, need to use to rfftfreq to map
        xf = rfftfreq(sample_size, 1 / sample_rate)

        # How to plot:
        # plt.plot(xf, np.abs(yf))
        # plt.show()
        return xf, np.abs(yf)

    @staticmethod
    def calc_spectogram(data, sample_rate):
        f, t, Sxx = signal.spectrogram(data, sample_rate)

        # How to plot:
        # fig, ax = plt.subplots()
        # spectro = ax.pcolormesh(t, f, Sxx, shading='gouraud')
        # fig.colorbar(spectro, label='|FFT Amplitude|')
        # ax.set_ylabel('Frequency [Hz]')
        # ax.set_xlabel('Time [sec]')
        # plt.show()
        return f, t, Sxx
