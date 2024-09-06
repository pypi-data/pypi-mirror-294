import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go
def fenetre(nfen=40):
    """
    Programme fenetre.

    Étude des fenêtres de pondération.

    Ce module permet de :
        - Visualiser l'allure de 6 fenêtres de pondération.
        - Afficher leur spectre en échelle linéaire.
        - Afficher leur spectre en échelle logarithmique.

    Les fenêtres ont une longueur de `nfen` points.

    Parameters
    ----------
    nfen : int
        Longueur des fenêtres à étudier.

    Affiche
    -------
    Les 6 fenêtres de pondération.
    Le spectre de chaque fenêtre en échelle linéaire.
    Le spectre de chaque fenêtre en échelle logarithmique.

    Notes
    -----
    Ce programme est utilisé pour analyser visuellement et spectrale les caractéristiques des fenêtres de pondération,
    souvent utilisées en traitement du signal pour des tâches comme la fenêtrage de signaux temporels.

    Example
    -------
    >>> from msicpe.tsa import fenetre
    >>> fenetre(256)
    """
    # Define the windows
    w1 = np.ones(nfen)
    w2 = np.bartlett(nfen)
    w3 = np.hanning(nfen)
    w4 = np.hamming(nfen)
    w5 = np.blackman(nfen)
    w6 = signal.windows.gaussian(nfen, std=7)  # Example standard deviation

    windows = [w1, w2, w3, w4, w5, w6]
    titles = ['Fenêtre Rectangulaire', 'Fenêtre Triangulaire', 'Fenêtre de Hanning',
              'Fenêtre de Hamming', 'Fenêtre de Blackman', 'Fenêtre de Gauss']

    # Time domain plots
    fig_time = go.Figure()
    for i, w in enumerate(windows):
        fig_time.add_trace(go.Scatter(
            x=np.arange(-2, nfen + 2),
            y=np.concatenate(([0, 0], w, [0, 0])),
            mode='lines',
            name=titles[i]
        ))

    fig_time.update_layout(
        title=f'Windows of {nfen} points',
        xaxis=dict(title='Points'),
        yaxis=dict(title='Amplitude'),
        height=1000,
        width=800,
        grid=dict(rows=3, columns=2, pattern="independent")
    )
    fig_time.show()

    # Frequency domain analysis
    nfft = 16 * 2 ** int(np.ceil(np.log2(nfen)))
    freqs = np.fft.fftfreq(nfft, d=1)[:nfft // 2]

    spectra = []
    for w in windows:
        sp = np.abs(np.fft.fft(w, nfft))
        sp = np.concatenate((sp[nfft // 2:], sp[:nfft // 2]))
        spectra.append(sp)

    fig_freq_lin = go.Figure()
    fig_freq_log = go.Figure()

    for i, sp in enumerate(spectra):
        fig_freq_lin.add_trace(go.Scatter(
            x=freqs,
            y=sp[:nfft // 2],
            mode='lines',
            name=titles[i]
        ))

        fig_freq_log.add_trace(go.Scatter(
            x=freqs,
            y=20 * np.log10(sp[:nfft // 2] / np.max(sp)),
            mode='lines',
            name=titles[i]
        ))

    fig_freq_lin.update_layout(
        title='Spectre en échelle linéaire',
        xaxis=dict(title='Fréquence'),
        yaxis=dict(title='Amplitude'),
        height=1000,
        width=800,
        grid=dict(rows=3, columns=2, pattern="independent")
    )

    fig_freq_log.update_layout(
        title='Spectre en échelle logarithmique',
        xaxis=dict(title='Fréquence'),
        yaxis=dict(title='Amplitude (dB)'),
        height=1000,
        width=800,
        grid=dict(rows=3, columns=2, pattern="independent")
    )

    fig_freq_lin.show()
    fig_freq_log.show()


# Call the function to visualize the windows
#fenetre(40)
