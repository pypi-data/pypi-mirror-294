#import antropy as ant
import numpy as np
from collections import Counter
from scipy.stats import kurtosis, skew
from scipy.signal import welch, butter, filtfilt


class SignaLytica:
    def __init__(self):
        self.features_map = {
            'mean': self.mean,
            'std': self.std,
            'coeff_var': self.coeff_var,
            'median': self.median,
            'mode': self.mode,
            'max': self.max,
            'min': self.min,
            'first_quartile': self.q1,
            'third_quartile': self.q3,
            'inter_quartile_range': self.IQR,

            'kurtosis': self.kurt,
            'skewness': self.skewness,
            #'detrended_fluctuation_analysis': self.dfa,
            'activity_hjorth_param': self.activity_hjorth_param,
            'mobility_hjorth_param': self.mobility_hjorth_param,
            'complexity_hjorth_param': self.complexity_hjorth_param,
            #'permutation_entropy': self.permutation_entropy,
            #'approximate_entropy': self.approximate_entropy,
            #'spectral_entropy': self.spectral_entropy,
            #'higuchi_fractal_dimmension': self.higuchi_fractal_dimmension,
            'total_power_spectral_density': self.total_power_spectral_density,
            'centroid_power_spectral_density': self.centroid_power_spectral_density,

            'relative_delta_power': self.relative_delta_power,
            'relative_theta_power': self.relative_theta_power,
            'relative_alpha_power': self.relative_alpha_power,
            'relative_beta_power': self.relative_beta_power,
            'relative_gamma_power': self.relative_gamma_power,
            'determinism': self.determinism,
            'trapping_time': self.trapping_time,
            'diagonal_line_entropy': self.diagonal_line_entropy,
            'average_diagonal_line_length': self.average_diagonal_line_length,

            'compute_recurrence_rate': self.compute_recurrence_rate,
            'spectral_edge_frequency_25': self.sef_25,
            'spectral_edge_frequency_50': self.sef_50,
            'spectral_edge_frequency_75': self.sef_75,
            'delta_amplitude': self.delta_amplitude,
            'theta_amplitude': self.theta_amplitude,
            'beta_amplitude': self.beta_amplitude,
            'alpha_amplitude': self.alpha_amplitude,
            'gamma_amplitude': self.gamma_amplitude,
            'hurst_exponent': self.hurst_exponent,

            #'singular_valued_decomposition_entropy': self.singular_valued_decomposition_entropy,
            #'petrosian_fractal_dimension': self.petrosian_fractal_dimension,
            #'katz_fractal_dimension': self.katz_fractal_dimension,
        }

    def list_metrics(self):
        return list(self.features_map.keys())

    def extract_features(self, time_serie, func_names):
        results = {}
        if func_names == 'all':
            func_names = ['mean', 'std', 'coeff_var', 'median', 'mode', 'max', 'min', 'first_quartile',
                          'third_quartile', 'inter_quartile_range', 'kurtosis', 'skewness',
                          #'detrended_fluctuation_analysis',
                          'activity_hjorth_param', 'mobility_hjorth_param',
                          'complexity_hjorth_param',
                          #'permutation_entropy',
                          #'sample_entropy',
                          #'approximate_entropy',
                          #'spectral_entropy', 'higuchi_fractal_dimmension',
                          'total_power_spectral_density',
                          'centroid_power_spectral_density', 'relative_delta_power', 'relative_theta_power',
                          'relative_alpha_power', 'relative_beta_power', 'relative_gamma_power', 'determinism',
                          'trapping_time', 'diagonal_line_entropy', 'average_diagonal_line_length',
                          'compute_recurrence_rate', 'spectral_edge_frequency_25', 'spectral_edge_frequency_50',
                          'spectral_edge_frequency_75', 'delta_amplitude', 'theta_amplitude', 'beta_amplitude',
                          'alpha_amplitude', 'gamma_amplitude', 'hurst_exponent',
                          #'singular_valued_decomposition_entropy', 'petrosian_fractal_dimension', 'katz_fractal_dimension',
                          ]

        for func_name in func_names:
            if func_name in self.features_map:
                # results.append(self.features_map[func_name](time_serie))
                results[func_name] = self.features_map[func_name](time_serie)
            else:
                raise ValueError(f"Function '{func_name}' is not defined.")
        return results

    def mean(self, time_serie):
        return np.mean(time_serie)

    # 2) Standard Deviation
    def std(self, time_serie):
        return np.std(time_serie)

    # 3) Coefficient of variation
    def coeff_var(self, time_serie):
        return np.var(time_serie)

    # 4) Median
    def median(self, time_serie):
        return np.median(time_serie)

    # 5) Mode
    def mode(self, time_serie):
        frequency = Counter(time_serie)
        max_count = max(list(frequency.values()))
        modes = [key for key, count in frequency.items() if count == max_count]

        if len(modes) == 1:
            return modes[0]
        else:
            return modes[0]  # Return the first elements of the list of modes if there are multiple

    # 6) Maximum value
    def max(self, time_serie):
        return np.max(time_serie)

    # 7) Minimum vlue
    def min(self, time_serie):
        return np.min(time_serie)

    # 8) First quartile (Q1)
    def q1(self, time_serie):
        return np.percentile(time_serie, 25)

    # 9) Third quartile (Q3)
    def q3(self, time_serie):
        return np.percentile(time_serie, 75)

    # 10) Interquartile range (IQR)
    def IQR(self, time_serie):
        return self.q3(time_serie) - self.q1(time_serie)

    # 11) Kurtosis
    def kurt(self, time_serie):
        return kurtosis(time_serie)

    # 12) Skewness
    def skewness(self, time_serie):
        return skew(time_serie)

    # 13) Detrended fluctuation analysis (DFA)
    #def dfa(self, time_serie):
    #    return ant.detrended_fluctuation(time_serie)

    # 14) Hjorth parameters
    def hjorth(self, time_serie, axis=-1):

        x = np.asarray(time_serie)
        # Calculate derivatives
        dx = np.diff(x, axis=axis)
        ddx = np.diff(dx, axis=axis)
        # Calculate variance
        x_var = np.var(x, axis=axis)  # = activity
        dx_var = np.var(dx, axis=axis)
        ddx_var = np.var(ddx, axis=axis)
        # Mobility and complexity
        mobility = np.sqrt(dx_var / x_var)
        complexity = np.sqrt(ddx_var / dx_var) / mobility

        # mobility, complexity = ent.hjorth_params(test_serie)
        activity = np.var(time_serie)
        return activity, mobility, complexity

    def activity_hjorth_param(self, test_serie):
        return self.hjorth(test_serie)[0]

    def mobility_hjorth_param(self, test_serie):
        return self.hjorth(test_serie)[1]

    def complexity_hjorth_param(self, test_serie):
        return self.hjorth(test_serie)[2]

    # 15) Permutation entropy (PE)
    #def permutation_entropy(self, time_serie):
    #    return ant.perm_entropy(time_serie, normalize=True)


    # 17) Approximate entropy (ApEn)
    #def approximate_entropy(self, time_serie):
    #    return ant.app_entropy(time_serie)

    # 18) Spectral Entropy
    #def spectral_entropy(self, time_serie):
    #    return ant.spectral_entropy(time_serie, sf=128, method='fft', normalize=True)

    # 19) Higuchi fractal dimension (HFD)
    #def higuchi_fractal_dimmension(self, time_serie):
    #    return ant.higuchi_fd(time_serie.astype(float))

    # 20) total Power Spectral Density (total PSD)
    def total_power_spectral_density(self, time_serie):
        freqs, psd = welch(time_serie, fs=128, nperseg=128)
        total_power = np.trapz(psd, freqs)
        return total_power

    # 20_1) centroid Power Spectral Density (centroid PSD)
    def centroid_power_spectral_density(self, time_serie):
        freqs, psd = welch(time_serie, fs=128, nperseg=128)
        centroid = np.sum(freqs * psd) / np.sum(psd)
        return centroid

    # 21) Relative delta power
    def bandpass_filter(self, data, lowcut, highcut, fs, order=4):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return filtfilt(b, a, data)

    def compute_relative_band_power(self, time_serie, fs, band=(0.5, 4), total_band=(0.5, 30)):
        # Bandpass filter for delta band
        delta_filtered = self.bandpass_filter(time_serie, band[0], band[1], fs)

        # Compute the Power Spectral Density (PSD)
        f, psd = welch(time_serie, fs, nperseg=128)

        # Calculate delta power (integrate PSD within delta range)
        band_power = np.trapz(psd[(f >= band[0]) & (f <= band[1])], f[(f >= band[0]) & (f <= band[1])])

        # Calculate total power (integrate PSD within total range)
        total_power = np.trapz(psd[(f >= total_band[0]) & (f <= total_band[1])],
                               f[(f >= total_band[0]) & (f <= total_band[1])])

        # Calculate relative delta power
        relative_band_power = band_power / total_power

        return relative_band_power

    def relative_delta_power(self, time_serie):
        return self.compute_relative_band_power(time_serie, 128, band=(0.5, 4), total_band=(0.5, 100))

    # 22) Relative theta power
    def relative_theta_power(self, time_serie):
        return self.compute_relative_band_power(time_serie, 128, band=(4, 8), total_band=(0.5, 100))

    # 23) Relative alpha power
    def relative_alpha_power(self, time_serie):
        return self.compute_relative_band_power(time_serie, 128, band=(8, 13), total_band=(0.5, 100))

    # 24) Relative beta power
    def relative_beta_power(self, time_serie):
        return self.compute_relative_band_power(time_serie, 128, band=(13, 30), total_band=(0.5, 100))

    # 25) Relative gamma power
    def relative_gamma_power(self, time_serie):
        return self.compute_relative_band_power(time_serie, 128, band=(30, 40), total_band=(0.5, 100))

    # 26) Laminar

    # 27) Determinism
    def recurrence_plot(self, time_serie, epsilon_type='std'):
        if epsilon_type == 'minmax':
            epsilon = 0.1 * (max(time_serie) - min(time_serie))
        elif epsilon_type == 'std':
            epsilon = 0.2 * np.std(time_serie)
        else:
            raise ValueError('normalization parameter not valid')
        """Constructs a recurrence plot from a 1D time series."""
        N = len(time_serie)
        RP = np.zeros((N, N), dtype=int)

        for i in range(N):
            for j in range(N):
                if abs(time_serie[i] - time_serie[j]) < epsilon:
                    RP[i, j] = 1
        return RP

    def determinism(self, time_serie, l_min=2):
        RP = self.recurrence_plot(time_serie)

        """Calculates determinism from a recurrence plot."""
        N = RP.shape[0]
        diagonal_line_lengths = []

        for i in range(N):
            for j in range(N):
                if RP[i, j] == 1:
                    length = 1
                    k = 1
                    while i + k < N and j + k < N and RP[i + k, j + k] == 1:
                        length += 1
                        k += 1
                    if length >= l_min:
                        diagonal_line_lengths.append(length)

        if not diagonal_line_lengths:
            return 0

        determinism_ = sum(diagonal_line_lengths) / np.sum(RP)
        return determinism_

    # 28) Trapping time
    def trapping_time(self, time_serie, l_min=2):
        RP = self.recurrence_plot(time_serie)
        """Calculates the trapping time from a recurrence plot."""
        N = RP.shape[0]
        vertical_line_lengths = []

        for j in range(N):
            length = 0
            for i in range(N):
                if RP[i, j] == 1:
                    length += 1
                else:
                    if length >= l_min:
                        vertical_line_lengths.append(length)
                    length = 0
            if length >= l_min:
                vertical_line_lengths.append(length)

        if not vertical_line_lengths:
            return 0

        trapping_time_ = np.mean(vertical_line_lengths)
        return trapping_time_

    # 29) Diagonal Line Entropy
    def diagonal_line_lengths(self, time_serie, l_min=2):
        RP = self.recurrence_plot(time_serie)
        """Calculates the lengths of diagonal lines in the recurrence plot."""
        N = RP.shape[0]
        line_lengths = []

        for i in range(N):
            for j in range(N):
                if RP[i, j] == 1:
                    length = 1
                    k = 1
                    while i + k < N and j + k < N and RP[i + k, j + k] == 1:
                        length += 1
                        k += 1
                    if length >= l_min:
                        line_lengths.append(length)

        return line_lengths

    def diagonal_line_entropy(self, time_serie):
        line_lengths = self.diagonal_line_lengths(time_serie)
        """Calculates the Shannon entropy of the diagonal line lengths."""
        if len(line_lengths) == 0:
            return 0

        # Calculate the probability distribution of line lengths
        unique_lengths, counts = np.unique(line_lengths, return_counts=True)
        probabilities = counts / counts.sum()

        # Calculate the Shannon entropy
        entropy = -np.sum(probabilities * np.log(probabilities))

        return entropy

    # 30) Average Diagonal Line Length
    def average_diagonal_line_length(self, time_serie):
        line_lengths = self.diagonal_line_lengths(time_serie)
        """Calculates the average diagonal line length."""
        if len(line_lengths) == 0:
            return 0

        avg_length = np.mean(line_lengths)

        return avg_length

    # 31) Recurrence rate
    def compute_recurrence_plot(self, time_serie, threshold):
        N = len(time_serie)
        recurrence_matrix = np.zeros((N, N))

        for i in range(N):
            for j in range(N):
                distance = abs(time_serie[i] - time_serie[j])
                if distance < threshold:
                    recurrence_matrix[i, j] = 1
        return recurrence_matrix

    def compute_recurrence_rate(self, time_serie, threshold=0.1):
        recurrence_matrix = self.compute_recurrence_plot(time_serie, threshold)
        recurrence_rate = np.sum(recurrence_matrix) / recurrence_matrix.size
        return recurrence_rate

    # 32) Spectral Edge Frecuency 25
    def calculate_sef(self, signal, fs, edge):
        # Compute the Power Spectral Density (PSD)
        f, psd = welch(signal, fs, nperseg=128)

        # Calculate the cumulative sum of the PSD
        cumulative_sum = np.cumsum(psd)

        # Normalize cumulative sum by total power to get cumulative distribution
        cumulative_distribution = cumulative_sum / cumulative_sum[-1]

        # Find the SEF25: the frequency where the cumulative distribution reaches 0.25
        sef = f[np.where(cumulative_distribution >= edge)[0][0]]

        return sef

    def sef_25(self, time_serie):
        return self.calculate_sef(time_serie, 128, 0.25)

    # 33) Spectral Edge Frecuency 50
    def sef_50(self, time_serie):
        return self.calculate_sef(time_serie, 128, 0.50)

    # 34) Spectral Edge Frecuency 75
    def sef_75(self, time_serie):
        return self.calculate_sef(time_serie, 128, 0.75)

    # 35) Delta amplitude
    def compute_band_amplitude(self, signal, fs, band):

        # Apply bandpass filter to isolate delta waves
        band_signal = self.bandpass_filter(signal, band[0], band[1], fs)

        # Calculate the amplitude (RMS value)
        band_amplitude = np.sqrt(np.mean(band_signal ** 2))

        return band_amplitude

    def delta_amplitude(self, time_serie):
        return self.compute_band_amplitude(time_serie, 128, (0.5, 4))

    # 36) Theta amplitude
    def theta_amplitude(self, time_serie):
        return self.compute_band_amplitude(time_serie, 128, (4, 8))

    # 37) Alpha amplitude
    def alpha_amplitude(self, time_serie):
        return self.compute_band_amplitude(time_serie, 128, (8, 13))

    # 38) Beta amplitude
    def beta_amplitude(self, time_serie):
        return self.compute_band_amplitude(time_serie, 128, (13, 30))

    # 39) Gamma amplitude
    def gamma_amplitude(self, time_serie):
        return self.compute_band_amplitude(time_serie, 128, (30, 40))

    # 40) Hurst exponent
    def rs_analysis(self, time_serie):
        N = len(time_serie)
        T = np.arange(1, N + 1)
        Y = np.cumsum(time_serie - np.mean(time_serie))
        R = np.max(Y) - np.min(Y)
        S = np.std(time_serie)
        if S == 0:
            return R / 1E-4  # If the data has 0 deviation replace 0 to a very small number
        else:
            return R / S

    def hurst_exponent(self, time_serie):

        normalized_serie = (time_serie - np.mean(time_serie)) / np.std(time_serie)
        N = len(normalized_serie)
        max_k = int(np.log2(N))

        rs_values = []
        for k in range(1, max_k + 1):
            n = 2 ** k
            chunks = [normalized_serie[i:i + n] for i in range(0, len(normalized_serie), n)]
            rs_chunk = [self.rs_analysis(chunk) for chunk in chunks if len(chunk) == n]
            rs_mean = np.mean(rs_chunk)
            rs_values.append(rs_mean)

        log_rs = np.log(rs_values)
        log_n = np.log([2 ** k for k in range(1, max_k + 1)])

        hurst_exponent = np.polyfit(log_n, log_rs, 1)[0]
        # plt.scatter(log_n, log_rs)
        return hurst_exponent

    # Singular value decomposition entropy
    #def singular_valued_decomposition_entropy(self, time_serie):
    #    return ant.svd_entropy(time_serie, normalize=True)

    # Petrosian fractal dimension
    #def petrosian_fractal_dimension(self, time_serie):
    #    return ant.petrosian_fd(time_serie)

    # Katz fractal dimension
    #def katz_fractal_dimension(self, time_serie):
    #    return ant.katz_fd(time_serie)