import numpy as np
import scipy.fftpack as fftpack
import plotly.graph_objs as go
import plotly.io as pio


def TransFourierInv(S, f=None):
    """
    Transformée de Fourier inverse d'un signal `S`.

    Parameters
    ----------
    S : array_like
        Vecteur de taille N contenant les coefficients de la transformée de Fourier `S`.
    f : array_like
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de `S` : `S[n] = S(f[n])`.
        Le vecteur `f` doit être symétrique autour de `f=0` : `f = [-fmax, -fmax+df, ..., 0, ..., fmax-df]`.

    Returns
    -------
    s : ndarray
        Vecteur de taille N contenant les N échantillons `s[n]` de la transformée de Fourier inverse de `S`.
    t : ndarray
        Vecteur de taille N contenant les instants d'échantillonnage de `s`, tels que `s[n] = s(t[n])`.

    Notes
    -----
    Cette fonction effectue la transformée de Fourier inverse sur le vecteur de coefficients `S` et retourne
    le signal temporel correspondant `s` ainsi que les instants d'échantillonnage `t`.

    Exemples
    --------
    >>> from msicpe.ssl import TransFourierInv
    >>> import numpy as np
    >>> S = np.array([0, 1, 0, -1])  # Exemples de coefficients de Fourier
    >>> f = np.array([-2, -1, 0, 1]) # Fréquences correspondantes
    >>> s, t = TransFourierInv(S, f)
    >>> print(s)
    [ 0.  1.  0. -1.]
    >>> print(t)
    [-2. -1.  0.  1.]
    """
    S = np.array(S)
    M = len(S)

    if f is None:
        f = np.arange(-M / 2, M / 2)  # Fréquences correspondant à S

    f = np.array(f)

    if M != len(f):
        raise ValueError('Les vecteurs "S" et "f" doivent avoir la même longueur.')

    if np.std(np.diff(f)) > 10e4 * np.finfo(float).eps:
        raise ValueError('Le vecteur "f" doit être linéairement croissant et avoir un pas constant.')

    df = f[1] - f[0]
    Fe = 2 * np.abs(np.min(f))

    if np.abs(f[0] + (f[-1] + df)) > 1000 * np.finfo(float).eps:
        raise ValueError('Le vecteur "f" doit être symétrique autour de f=0.')

    Sshift = np.concatenate((S[f >= 0], S[f < 0]))  # Shift de S pour centrer la FFT
    Sshift = Sshift * Fe

    N = M
    s = fftpack.ifft(Sshift, N)
    s = fftpack.fftshift(s)
    t = np.arange(-N / 2, N / 2) / Fe

    return s, t


# # Exemple d'utilisation
# import matplotlib.pyplot as plt
#
# # Générer un signal à partir de sa transformée de Fourier
# f = np.linspace(-10, 10, 1000)  # Fréquences
# S = np.sinc(f)  # Transformée de Fourier du signal sinc
#
# # Reconstruction du signal dans le domaine temporel
# s, t = TransFourierInv(S, f)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=np.real(s), mode='lines', name='Reconstruction du signal'))
#
# fig.update_layout(title='Reconstruction de Signal à partir de Transformée de Fourier',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)
