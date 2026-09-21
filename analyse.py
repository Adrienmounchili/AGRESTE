# Adrien Mounchili

import numpy as np


def moyenne(valeurs):
    return float(np.mean(valeurs)) if len(valeurs) else 0.0


def mediane(valeurs):
    return float(np.median(valeurs)) if len(valeurs) else 0.0


def ecart_type(valeurs):
    return float(np.std(valeurs, ddof=1)) if len(valeurs) > 1 else 0.0


def regression_lineaire(x, y):
    """Régression linéaire simple par la méthode des moindres carrés.
    x, y : listes ou séries de même longueur.
    Retourne la pente (a), l'ordonnée à l'origine (b) et le R².
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    if n < 2:
        return None

    x_moy, y_moy = x.mean(), y.mean()
    ssxy = np.sum((x - x_moy) * (y - y_moy))
    ssxx = np.sum((x - x_moy) ** 2)
    a = ssxy / ssxx if ssxx != 0 else 0.0
    b = y_moy - a * x_moy

    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y_moy) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot != 0 else 0.0

    return {"a": a, "b": b, "r2": r2, "n": n}


def interpreter_r2(r2):
    if r2 > 0.7:
        return "Forte corrélation — l'utilisation de l'IA est fortement liée à l'autonomie."
    elif r2 > 0.3:
        return "Corrélation modérée — une relation existe mais d'autres facteurs interviennent."
    else:
        return "Faible corrélation — l'utilisation de l'IA n'explique pas significativement l'autonomie."
