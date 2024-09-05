import numpy as np
import scipy.fftpack as fftpack

def TransFourier(s, t=None):
    """
    Transformée de Fourier d'un signal `s`.

    Parameters
    ----------
    s : array_like
        Vecteur de taille N contenant les N échantillons s[n] du signal à analyser.
    t : array_like
        Vecteur de taille N contenant les instants d'échantillonnage de `s`. s[n] = s(t[n]).

    Returns
    -------
    S : ndarray
        Vecteur de taille N contenant les coefficients de la transformée de Fourier du signal `s`.
    f : ndarray
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de `S` : S[n] = S(f[n]).

    Examples
    --------
    >>> import numpy as np
    >>> from msicpe.ssl import TransFourier
    >>> t = np.linspace(0, 1, 1000, endpoint=False)
    >>> s = np.sin(2 * np.pi * 50 * t)
    >>> S, f = TransFourier(s, t)
    >>> S[:5]  # Affiche les premiers coefficients de la transformée de Fourier
    array([ ... ])
    >>> f
    """
    s = np.array(s)
    N = len(s)

    if t is None:
        t = np.arange(1, N + 1)

    t = np.array(t)

    if N != len(t):
        raise ValueError('Les vecteurs "s" et "t" doivent avoir la même longueur.')

    if np.std(np.diff(t)) > 1000 * np.finfo(float).eps:
        raise ValueError('Le vecteur "t" doit être linéairement croissant et avoir un pas constant.')

    dt = t[1] - t[0]
    Fe = 1 / dt
    sshift = np.concatenate((s[t >= 0], s[t < 0]))  # Shift de s pour centrer la FFT

    M = N
    S = fftpack.fft(sshift, M)
    S = fftpack.fftshift(S)
    S = S * dt
    f = np.linspace(-Fe / 2, Fe / 2, M + 1)
    f = f[:M]

    return S, f


# # Exemple d'utilisation
# import matplotlib.pyplot as plt
#
# # Générer un signal sinusoidal pour l'exemple
# t = np.linspace(0, 1, 1000)  # Temps
# s = np.sin(2 * np.pi * 10 * t)  # Signal sinusoidal à 10 Hz
#
# # Calcul de la transformée de Fourier
# S, f = TransFourier(s, t)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=f, y=np.abs(S), mode='lines', name='Module de S(f)'))
# fig.update_layout(title='Transformée de Fourier d\'un Signal',
#                   xaxis_title='Fréquence (Hz)',
#                   yaxis_title='Module de S(f)')
# pio.show(fig)