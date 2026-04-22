import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
import os
import numba

@numba.njit
def sieve_of_eratosthenes(limit):
    """
    Ein effizientes Sieb des Eratosthenes, um Primzahlen bis zum Limit zu finden.
    """
    primes = np.ones(limit + 1, dtype=np.bool_)
    primes[0:2] = False
    for p in range(2, int(np.sqrt(limit)) + 1):
        if primes[p]:
            primes[p*p : limit+1 : p] = False
    return np.nonzero(primes)[0]

def calculate_prime_gaps(limit):
    """Berechnet die Abstände aufeinanderfolgender Primzahlen."""
    primes = sieve_of_eratosthenes(limit)
    gaps = np.diff(primes)
    return gaps

def plot_prime_gaps_histogram(gaps, html_file='prime_gaps_histogram_1e9.html', png_file='prime_gaps_histogram_1e9.png'):
    """Erstellt ein Histogramm der aggregierten Abstände mit Plotly, exportiert als PNG und öffnet es."""
    # Aggregiere die Daten: Abstände in 1er-Bins von 0 bis 300
    counts, bin_edges = np.histogram(gaps, bins=range(0, 302, 1))
    
    # Histogramm mit den vorab aggregierten Daten erstellen
    fig = go.Figure(data=[go.Bar(x=bin_edges[:-1], y=counts)])
    fig.update_layout(
        title='Histogramm der Abstände aufeinanderfolgender Primzahlen bis 10^9 (Bin-Größe 1)',
        xaxis_title='Abstand',
        yaxis_title='Häufigkeit (log)',
        yaxis_type='log'
    )
    
    # Als HTML speichern
    fig.write_html(html_file)
    print(f'Histogramm wurde in {html_file} gespeichert.')
    
    # Als PNG speichern
    fig.write_image(png_file)
    print(f'Histogramm wurde in {png_file} gespeichert.')

    # HTML Datei im Browser öffnen
    webbrowser.open('file://' + os.path.realpath(html_file))

# Limit auf 10^9 setzen.
LIMIT = 1_000_000_000 
gaps = calculate_prime_gaps(LIMIT)
plot_prime_gaps_histogram(gaps)
