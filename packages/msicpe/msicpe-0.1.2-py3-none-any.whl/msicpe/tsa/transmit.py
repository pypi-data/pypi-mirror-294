import numpy as np


def transmit(S, powB=5):
    """
    TRANSMIT modélise un canal de transmission bruité.

    Parameters
    ----------
    S : array_like
        signal à transmettre
    powB :float, optional
        puissance du bruit de transmission (valeur par défaut: 5)

    Returns
    -------
    X : ndarray
        signal dégradé après transmission
    B : ndarray
        bruit introduit par le canal de transmission
    """
    B = np.sqrt(powB) * np.random.randn(*S.shape)
    X = S + B
    return X, B

#
# # Exemple d'utilisation
# import plotly.graph_objs as go
# import plotly.io as pio
#
# # Signal d'exemple
# S = np.sin(2 * np.pi * np.linspace(0, 1, 1000))  # Signal sinusoïdal
#
# # Transmettre le signal avec bruit
# X, B = transmit(S)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=np.arange(len(S)), y=S, mode='lines', name='Signal original'))
# fig.add_trace(go.Scatter(x=np.arange(len(X)), y=X, mode='lines', name='Signal transmis'))
# fig.add_trace(go.Scatter(x=np.arange(len(B)), y=B, mode='lines', name='Bruit'))
#
# fig.update_layout(title='Transmission de Signal avec Bruit',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)
# # Exemple d'utilisation
# import plotly.graph_objs as go
# import plotly.io as pio
#
# # Signal d'exemple
# S = np.sin(2 * np.pi * np.linspace(0, 1, 1000))  # Signal sinusoïdal
#
# # Transmettre le signal avec bruit
# X, B = transmit(S)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=np.arange(len(S)), y=S, mode='lines', name='Signal original'))
# fig.add_trace(go.Scatter(x=np.arange(len(X)), y=X, mode='lines', name='Signal transmis'))
# fig.add_trace(go.Scatter(x=np.arange(len(B)), y=B, mode='lines', name='Bruit'))
#
# fig.update_layout(title='Transmission de Signal avec Bruit',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)