SignaLytica
===========

A Python package for feature extraction in time series and EEG signals.

Installation
------------

.. code-block:: bash

    pip install signalytica

Dependencies
------------

* `NumPy <https://numpy.org/>`_
* `SciPy <https://scipy.org/>`_

Utilization
-----------

**Import modules**

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from signalytica import SignaLytica

**Example time series data**

.. code-block:: python

    np.random.seed(1234)
    x = np.random.normal(size=128)
    plt.figure(figsize=(6,2))
    plt.plot(x)
    plt.title('Example time serie'); plt.xlabel('Samples'); plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig('example_time_serie.png')

*Output:*

.. image:: https://github.com/Edgar-La/signalytica/blob/main/signalytica/example_time_serie.png
   :alt: Example time series plot

**List all the available metrics in the package**

.. code-block:: python

    signa = SignaLytica()
    available_metrics = signa.list_metrics()
    print(available_metrics)

*Output:*

::

    ['mean', 'std', 'coeff_var', 'median', 'mode', 'max', 'min', 'first_quartile', 'third_quartile', 'inter_quartile_range', 'kurtosis', 'skewness', 'activity_hjorth_param', 'mobility_hjorth_param', 'complexity_hjorth_param', 'total_power_spectral_density', 'centroid_power_spectral_density', 'relative_delta_power', 'relative_theta_power', 'relative_alpha_power', 'relative_beta_power', 'relative_gamma_power', 'determinism', 'trapping_time', 'diagonal_line_entropy', 'average_diagonal_line_length', 'compute_recurrence_rate', 'spectral_edge_frequency_25', 'spectral_edge_frequency_50', 'spectral_edge_frequency_75', 'delta_amplitude', 'theta_amplitude', 'beta_amplitude', 'alpha_amplitude', 'gamma_amplitude', 'hurst_exponent']

**Extract specific features from time series/EEG signal**

.. code-block:: python

    features = ['coeff_var', 'inter_quartile_range', 'kurtosis', 'total_power_spectral_density', 'trapping_time']
    signa.extract_features(x, features)
*Output:*

::

    {
      'coeff_var': 0.9296511098623816,
      'inter_quartile_range': 1.1642928949004765,
      'kurtosis': 0.9355744131054928,
      'total_power_spectral_density': 1.03503685376608,
      'trapping_time': 2.2205882352941178
    }

Calculate individual features
-----------------------------

**Activity Hjorth Parameter**

.. code-block:: python

    activity = signa.activity_hjorth_param(x)
    print(activity)

*Output:*

::

    0.9296511098623816

**Total power spectral density**

.. code-block:: python

    tpsd = signa.total_power_spectral_density(x)
    print(tpsd)

*Output:*

::

    1.03503685376608

**Determinism**

.. code-block:: python

    determ = signa.determinism(x)
    print(determ)

*Output:*

::

    4.315972222222222

**Alpha amplitude**

.. code-block:: python

    alpha_amp = signa.alpha_amplitude(x)
    print(alpha_amp)

*Output:*

::

    0.19518190403498442

**Hurst Exponent**

.. code-block:: python

    hurst_exp = signa.hurst_exponent(x)
    print(hurst_exp)

*Output:*

::

    0.5074992385199263

Extract all features
----------------------

Instead of using a list to indicate the features, you can use the parameter *all* to calculate all the features.

.. code-block:: python

    all_features_calculated = signa.extract_features(x, 'all')
    all_features_calculated

*Output:*

::

    {'mean': 0.006880339575229891,
     'std': 0.9641841680210175,
     'coeff_var': 0.9296511098623816,
     'median': 0.07802095042293272,
     'mode': 0.47143516373249306,
     'max': 2.390960515463033,
     'min': -3.5635166606247353,
     'first_quartile': -0.4874633299633267,
     'third_quartile': 0.6768295649371497,
     'inter_quartile_range': 1.1642928949004765,
     'kurtosis': 0.9355744131054928,
     'skewness': -0.5940081255524681,
     'activity_hjorth_param': 0.9296511098623816,
     'mobility_hjorth_param': 1.5772426970445614,
     'complexity_hjorth_param': 1.1381489369369338,
     'total_power_spectral_density': 1.03503685376608,
     'centroid_power_spectral_density': 39.785545239633095,
     'relative_delta_power': 0.014199533696614332,
     'relative_theta_power': 0.024773922507739236,
     'relative_alpha_power': 0.06670507211034518,
     'relative_beta_power': 0.16222741368578988,
     'relative_gamma_power': 0.1944461143387118,
     'determinism': 4.315972222222222,
     'trapping_time': 2.2205882352941178,
     'diagonal_line_entropy': 2.794104878439014,
     'average_diagonal_line_length': 26.28700906344411,
     'compute_recurrence_rate': 0.063720703125,
     'spectral_edge_frequency_25': 27.0,
     'spectral_edge_frequency_50': 46.0,
     'spectral_edge_frequency_75': 55.0,
     'delta_amplitude': 0.332883261842357,
     'theta_amplitude': 0.1334128596782051,
     'beta_amplitude': 0.44829663314331475,
     'alpha_amplitude': 0.19518190403498442,
     'gamma_amplitude': 0.36127348831240264,
     'hurst_exponent': 0.5074992385199263}

**Convert the features into a feature vector**

.. code-block:: python

    feature_vector = list(all_features_calculated.values())
    print('features:', feature_vector)
    print('n_features:', len(feature_vector))

*Output:*

::

    features: [0.006880339575229891, 0.9641841680210175, 0.9296511098623816, 0.07802095042293272, 0.47143516373249306, 2.390960515463033, -3.5635166606247353, -0.4874633299633267, 0.6768295649371497, 1.1642928949004765, 0.9355744131054928, -0.5940081255524681, 0.9296511098623816, 1.5772426970445614, 1.1381489369369338, 1.03503685376608, 39.785545239633095, 0.014199533696614332, 0.024773922507739236, 0.06670507211034518, 0.16222741368578988, 0.1944461143387118, 4.315972222222222, 2.2205882352941178, 2.794104878439014, 26.28700906344411, 0.063720703125, 27.0, 46.0, 55.0, 0.332883261842357, 0.1334128596782051, 0.44829663314331475, 0.19518190403498442, 0.36127348831240264, 0.5074992385199263]

    n_features: 36

Development
-----------

SignaLytica was created and is maintained by `Edgar Lara <https://accidental-bard-367.notion.site/Edgar-Lara-a8828a758e5242f4981b65a2fdc1d44f>`_. Contributions are more than welcome, so feel free to contact me, open an issue, or submit a pull request!

To see the code or report a bug, please visit the `GitHub repository <https://github.com/Edgar-La/signalytica>`_.

Note that this program is provided with **NO WARRANTY OF ANY KIND**. Always double-check the results.

Acknowledgement
---------------

This package was inspired by the research work of Hernández Nava, G. (2023). *Predicción de eventos epilépticos mediantes técnicas de aprendizaje profundo usando señales de EEG.
