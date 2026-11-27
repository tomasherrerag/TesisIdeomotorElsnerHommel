import plotly.graph_objects as go
import pandas as pd

# ==========================================================
# Configuración
# ==========================================================

# ---------- Salida ----------

HTML_EXTENSION = ".html"

# ---------- Leyenda ----------

SHOW_LEGEND = True

# ---------- Marcadores ----------

MARKER_SIZE = 6

# ---------- Ejes ----------

X_AXIS = "dist_exp1"
Y_AXIS = "dist_exp2"
Z_AXIS = "dist_exp3"

X_AXIS_TITLE = "Distancia Experimento 1"
Y_AXIS_TITLE = "Distancia Experimento 2"
Z_AXIS_TITLE = "Distancia Experimento 3"

# ---------- Hover ----------

HOVER_COLUMNS = [
    "trial",
    "nombre_estudio",

    "score0_exp1",
    "score1_exp1",
    "dist_exp1",

    "score0_exp2",
    "score1_exp2",
    "dist_exp2",

    "score0_exp3",
    "score1_exp3",
    "dist_exp3"
]

HOVER_TEMPLATE = """
<b>Trial</b>: %{customdata[0]}<br>
<b>nombre_estudio</b>: %{customdata[1]}<br>

<br><b>Experimento 1</b><br>
Score0: %{customdata[2]:.3f}<br>
Score1: %{customdata[3]:.3f}<br>
Distancia: %{customdata[4]:.3f}<br>

<br><b>Experimento 2</b><br>
Score0: %{customdata[5]:.3f}<br>
Score1: %{customdata[6]:.3f}<br>
Distancia: %{customdata[7]:.3f}<br>

<br><b>Experimento 3</b><br>
Score0: %{customdata[8]:.3f}<br>
Score1: %{customdata[9]:.3f}<br>
Distancia: %{customdata[10]:.3f}<br>

<extra></extra>
"""

# ==========================================================
# Función principal
# ==========================================================

def graficar_3d(
    dataset,
    titulo="Gráfico 3D",
    guardar_html=True,
    mostrar=True
):

    customdata = dataset[HOVER_COLUMNS].values

    fig = go.Figure()


    for estudio in dataset["nombre_estudio"].unique():

        datos = dataset[
            dataset["nombre_estudio"] == estudio
        ]

        customdata = datos[HOVER_COLUMNS].values

        fig.add_trace(

            go.Scatter3d(

                x=datos[X_AXIS],
                y=datos[Y_AXIS],
                z=datos[Z_AXIS],

                mode="markers",

                name=estudio,

                customdata=customdata,

                hovertemplate=HOVER_TEMPLATE

            )

        )

    fig.update_traces(

        marker=dict(

            size=MARKER_SIZE

        )

    )

    fig.update_layout(

        title=titulo,

        showlegend=SHOW_LEGEND,

        scene=dict(

            xaxis_title=X_AXIS_TITLE,
            yaxis_title=Y_AXIS_TITLE,
            zaxis_title=Z_AXIS_TITLE

        )

    )

    if guardar_html:
        fig.write_html(titulo + HTML_EXTENSION)

    if mostrar:
        fig.show()

    return fig


# ==========================================================
# Main de prueba
# ==========================================================

from constructorDataset import construir_dataset
from metricas import calcular_metricas

if __name__ == "__main__":

    datasets = []

    for origen in [1, 2, 3]:

        dataset = construir_dataset(

            f"validacion_pareto{origen}Default.db",

            nombre_estudio=f"TransferDefault{origen}"

        )

        dataset = calcular_metricas(dataset)

        datasets.append(dataset)

    dataset_total = pd.concat(

        datasets,

        ignore_index=True

    )

    graficar_3d(

        dataset_total,

        titulo="TransferDefault"

    )