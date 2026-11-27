import optuna
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def obtener_trials_filtrados(db_path, study_name, filtro):

    study = optuna.load_study(
        study_name=study_name,
        storage=f"sqlite:///{db_path}"
    )

    filas = []

    for t in study.trials:

        if t.values is None:
            continue

        score0, score1 = t.values

        if not filtro(score0, score1):
            continue

        fila = {
            "score0": score0,
            "score1": score1
        }

        fila.update(t.params)

        filas.append(fila)

    return pd.DataFrame(filas)






#bloque MAIN

#Extraccion de los mejores trials de cada experimento (filtro de score)
exp1 = obtener_trials_filtrados(
    "exp1Default.db",
    "exp1Default",
    lambda s0, s1: s0 < 4 and s1 > 0
)

exp2 = obtener_trials_filtrados(
    "exp2Default.db",
    "exp2Default",
    lambda s0, s1: s0 <= 1 and s1 == 0
)



# extraccion de parametros y graficado de KDE (para buscar rangos de valores optimos)
parametros = [
    c for c in exp1.columns
    if c != "score"
]

for parametro in parametros:

    plt.figure(figsize=(8,5))  
    
    # KDE
    sns.kdeplot(exp1[parametro], color="tab:blue", linewidth=2, label="Exp1")
    sns.kdeplot(exp2[parametro], color="tab:orange", linewidth=2, label="Exp2")

    plt.title(parametro)

    plt.legend()

    plt.tight_layout()

    plt.savefig(f"kde_{parametro}.png")

    plt.close()

    resumen = []

for parametro in parametros:

    print(parametro)

    print(exp1[parametro].mean())
    print(exp2[parametro].mean())

    minimo_comun = max(
        exp1[parametro].min(),
        exp2[parametro].min()
    )

    maximo_comun = min(
        exp1[parametro].max(),
        exp2[parametro].max()
    )

    resumen.append({
        "parametro": parametro,
        "min": minimo_comun,
        "max": maximo_comun
    })

rangos = pd.DataFrame(resumen)

print(rangos)