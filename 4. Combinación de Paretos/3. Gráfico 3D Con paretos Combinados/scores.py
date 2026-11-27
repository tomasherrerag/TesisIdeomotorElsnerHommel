"""
scores.py

Funciones encargadas de calcular los scores de los tres experimentos
a partir de una fila del DataFrame.

Cada función devuelve:

(score0, score1)
"""

# ==========================================================
# EXPERIMENTO 1
# ==========================================================

def score_exp1(fila):

    coincidencia_no_rev = fila["exp1_noRev_pct_prom"]
    skips_no_rev        = fila["exp1_noRev_skip_prom"]
    tiempo_no_rev       = fila["exp1_noRev_tiempo_prom"]

    coincidencia_rev = fila["exp1_rev_pct_prom"]
    skips_rev        = fila["exp1_rev_skip_prom"]
    tiempo_rev       = fila["exp1_rev_tiempo_prom"]

    score0 = 0

    score0 += (coincidencia_no_rev - 98) ** 2
    score0 += skips_no_rev ** 2

    score0 += (coincidencia_rev - 2) ** 2
    score0 += skips_rev ** 2

    #----------------------------------------
    # Score de tiempos
    #----------------------------------------

    if tiempo_no_rev > tiempo_rev:

        score1 = -(tiempo_no_rev - tiempo_rev)

    else:

        score1 = tiempo_rev - tiempo_no_rev

    return score0, score1


# ==========================================================
# EXPERIMENTO 2
# ==========================================================

def score_exp2(fila):

    coincidencia = fila["exp2_pct_prom"]
    skips = fila["exp2_skip_prom"]

    score0 = (coincidencia - 54) ** 2
    score1 = skips ** 2

    return score0, score1


# ==========================================================
# EXPERIMENTO 3
# ==========================================================

def score_exp3(fila):

    coincidencia = fila["exp3_pct_prom"]
    skips_malos = fila["exp3_skipMalo_prom"]
    skips_respondidos = fila["exp3_skipRespondido_prom"]

    score0 = (coincidencia - 60) ** 2

    score1 = 0
    score1 += skips_malos ** 2
    score1 += skips_respondidos ** 2

    return score0, score1