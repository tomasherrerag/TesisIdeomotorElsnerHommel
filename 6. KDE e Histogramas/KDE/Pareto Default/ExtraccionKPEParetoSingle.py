import optuna
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def obtener_top_trials(db_path, study_name):

    study = optuna.load_study(
        study_name=study_name,
        storage=f"sqlite:///{db_path}"
    )

    trials = study.best_trials

    filas = []
    
    for t in trials:
    
        fila = {}
    
        for i, valor in enumerate(t.values):
            fila[f"objetivo_{i+1}"] = valor
    
        fila.update(t.params)
    
        filas.append(fila)

    return pd.DataFrame(filas)






#bloque MAIN

#Extraccion de los mejores trials de cada experimento (10% mejores)
exp1 = obtener_top_trials(
    "exp1Default.db",
    "exp1Default"
)

exp2 = obtener_top_trials(
    "exp2Default.db",
    "exp2Default"
)

exp3 = obtener_top_trials(
    "exp3Default.db",
    "exp3Default"
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
    sns.kdeplot(exp3[parametro], color="tab:green", linewidth=2, label="Exp3")

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
    print(exp3[parametro].mean())

    minimo_comun = max(
        exp1[parametro].min(),
        exp2[parametro].min(),
        exp3[parametro].min()
    )

    maximo_comun = min(
        exp1[parametro].max(),
        exp2[parametro].max(),
        exp3[parametro].max()
    )

    resumen.append({
        "parametro": parametro,
        "min": minimo_comun,
        "max": maximo_comun
    })

rangos = pd.DataFrame(resumen)

print(rangos)