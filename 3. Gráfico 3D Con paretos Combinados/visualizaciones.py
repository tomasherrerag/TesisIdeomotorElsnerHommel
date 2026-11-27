import pandas as pd
import plotly.graph_objects as go


# ==========================================================
# Configuración
# ==========================================================

# ---------- Salida ----------

HTML_EXTENSION = ".html"

# ---------- Marcadores ----------

MARKER_SIZE = 6

SHOW_LEGEND = True

# ---------- Ejes gráfico 3D ----------

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
<b>Estudio</b>: %{customdata[1]}<br>

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
# Configuración gráficos 2D
# ==========================================================

GRAFICOS_2D = [

    (
        "dist_exp1",
        "dist_exp2",
        "Distancia Experimento 1",
        "Distancia Experimento 2",
        "Exp1_vs_Exp2"
    ),

    (
        "dist_exp1",
        "dist_exp3",
        "Distancia Experimento 1",
        "Distancia Experimento 3",
        "Exp1_vs_Exp3"
    ),

    (
        "dist_exp2",
        "dist_exp3",
        "Distancia Experimento 2",
        "Distancia Experimento 3",
        "Exp2_vs_Exp3"
    )

]

# ==========================================================
# Gráfico 3D
# ==========================================================

def graficar_3d(
    dataset,
    titulo="Gráfico 3D",
    guardar_html=True,
    mostrar=True
):

    fig = go.Figure()

    # ------------------------------------------------------
    # Un trace por estudio
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Apariencia
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Salida
    # ------------------------------------------------------

    if guardar_html:

        fig.write_html(
            titulo + "_3D" + HTML_EXTENSION
        )

    if mostrar:

        fig.show()

    return fig

# ==========================================================
# Gráfico 2D
# ==========================================================

def graficar_2d(
    dataset,
    eje_x,
    eje_y,
    xaxis_title,
    yaxis_title,
    titulo="Gráfico 2D",
    guardar_html=True,
    mostrar=True
):

    fig = go.Figure()

    # ------------------------------------------------------
    # Un trace por estudio
    # ------------------------------------------------------

    for estudio in dataset["nombre_estudio"].unique():

        datos = dataset[
            dataset["nombre_estudio"] == estudio
        ]

        customdata = datos[HOVER_COLUMNS].values

        fig.add_trace(

            go.Scatter(

                x=datos[eje_x],
                y=datos[eje_y],

                mode="markers",

                name=estudio,

                customdata=customdata,

                hovertemplate=HOVER_TEMPLATE

            )

        )

    # ------------------------------------------------------
    # Apariencia
    # ------------------------------------------------------

    fig.update_traces(

        marker=dict(

            size=12

        )

    )

    fig.update_layout(

        title=titulo,

        showlegend=SHOW_LEGEND,

        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title

    )

    # ------------------------------------------------------
    # Salida
    # ------------------------------------------------------

    if guardar_html:

        fig.write_html(
            titulo + HTML_EXTENSION
        )

    if mostrar:

        fig.show()

    return fig

# ==========================================================
# Generación automática de gráficos
# ==========================================================

def generar_graficos(
    dataset,
    titulo_base,
    guardar_html=True,
    mostrar=True
):

    figuras = {}

    # ------------------------------------------------------
    # Gráfico 3D
    # ------------------------------------------------------

    figuras["3D"] = graficar_3d(

        dataset,

        titulo=f"{titulo_base}_3D",

        guardar_html=guardar_html,

        mostrar=mostrar

    )

    # ------------------------------------------------------
    # Gráficos 2D
    # ------------------------------------------------------

    for eje_x, eje_y, titulo_x, titulo_y, nombre in GRAFICOS_2D:

        figuras[nombre] = graficar_2d(

            dataset,

            eje_x=eje_x,

            eje_y=eje_y,

            xaxis_title=titulo_x,

            yaxis_title=titulo_y,

            titulo=f"{titulo_base}_{nombre}",

            guardar_html=guardar_html,

            mostrar=mostrar

        )

    return figuras

# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    from constructorDataset import construir_dataset
    from metricas import calcular_metricas

    # ------------------------------------------------------
    # Construcción de datasets
    # ------------------------------------------------------

    dataset1 = construir_dataset(

        "validacion_valid1Default.db",

        nombre_estudio="TransferDefault1"

    )

    dataset2 = construir_dataset(

        "validacion_valid2Default.db",

        nombre_estudio="TransferDefault2"

    )


#    dataset3 = construir_dataset(
#
#        "validacion_valid3Default.db",
#
#        nombre_estudio="TransferDefault3"
#
#    )

    # ------------------------------------------------------
    # Unión de datasets
    # ------------------------------------------------------

    dataset_total = pd.concat(

        [

            dataset1,
            dataset2
#            dataset3

        ],

        ignore_index=True

    )

    # ------------------------------------------------------
    # Cálculo de métricas
    # ------------------------------------------------------

    dataset_total = calcular_metricas(

        dataset_total

    )

    # ------------------------------------------------------
    # Generación de gráficos
    # ------------------------------------------------------

    figuras = generar_graficos(

        dataset_total,

        titulo_base="TransferDefault",

        guardar_html=True,

        mostrar=False

    )

    # Mostrar únicamente el gráfico 3D

    figuras["3D"].show()