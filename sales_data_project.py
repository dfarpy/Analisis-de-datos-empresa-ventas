##Estudio geográfico y de categorías de productos: análisis de ventas y comportamiento del consumidor.

# En este trabajo se presenta un análisis de datos de ventas utilizando diferentes herramientas de visualización para analizar las ventas por estado, categoría, segmento y mes/año. Además, se presenta un mapa territorial de las ventas por estado, lo que permite tener una visión más detallada de las ventas en cada región geográfica y detectar oportunidades de crecimiento en áreas específicas.
## ANOTACION PARA EJECUTAR ESTE PROYECTO DESCARGA EL ARCHIVO DE KAGGLE COMPARTO LINK, Y LUEGO INDICA LA RUTA DEL ARCHIVO DONDE LO HAYAS DESCARGADO. Y DE IGUAL FORMA CON EL ARCHIVO JSON.
#https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting?select=train.csv (ARCHIVO DE DATOS)



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium 
import json

# Leer archivo CSV
ventas_df = pd.read_csv('train.csv')

# Seleccionar columnas necesarias y eliminar las no necesarias
columnas = ["Ship Mode", "Segment", "Country", "City", "State", "Region", "Category", "Sub-Category", "Sales", "Order Date", "Ship Date"]
ventas_df = ventas_df[columnas]

# Convertir las columnas de fecha a formato datetime
ventas_df["Order Date"] = pd.to_datetime(ventas_df["Order Date"])
ventas_df["Ship Date"] = pd.to_datetime(ventas_df["Ship Date"])

# Agregar nuevas columnas para el año, mes y día de la semana de la fecha de envío
ventas_df["Ship Year"] = ventas_df["Ship Date"].dt.year
ventas_df["Ship Month"] = ventas_df["Ship Date"].dt.month
ventas_df["Ship Day of Week"] = ventas_df["Ship Date"].dt.dayofweek

# Imprimir las primeras filas del dataframe resultante
print(ventas_df.head())

# Gráfico de barras horizontales de ventas por estado y categoría
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12,8))
sns.barplot(x="Sales", y="State", hue="Category", data=ventas_df)
plt.title("Ventas por estado y categoría")
plt.xlabel("Ventas")
plt.ylabel("Estado")
plt.show()

# Este gráfico de barras horizontales muestra las ventas por estado y categoría. La línea horizontal muestra el estado y las barras representan las ventas. Además, el color de cada barra representa la categoría a la que pertenece el producto vendido. El objetivo de este gráfico es permitirnos comparar las ventas por estado y por categoría de producto. Podemos ver que Texas es el estado con mayores ventas totales, seguido de California y New York. En cuanto a las categorías de productos, la categoría de muebles tiene un bajo desempeño en términos de ventas en comparación con las categorías de tecnología y suministros de oficina.
# Mapa de calor de las ventas por mes y año
ventas_pivot = ventas_df.pivot_table(values="Sales", index="Ship Month", columns="Ship Year", aggfunc="sum")
plt.figure(figsize=(10,8))
sns.heatmap(ventas_pivot, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("Ventas por mes y año")
plt.xlabel("Año")
plt.ylabel("Mes")
plt.show()

#Este tipo de gráfico es muy útil para ver cómo varían las ventas a lo largo del tiempo. En este caso, podemos observar que las ventas se mantuvieron constantes entre 2014 y 2015, pero aumentaron significativamente en 2016. Además, podemos ver que las ventas son mayores durante los meses de noviembre y diciembre, lo que sugiere que las compras navideñas tienen una gran influencia en las ventas totales.
# Gráfico de barras verticales de ventas por segmento
plt.figure(figsize=(10,8))
sns.barplot(x="Segment", y="Sales", data=ventas_df)
plt.title("Ventas por segmento")
plt.xlabel("Segmento")
plt.ylabel("Ventas")
plt.show()

# El tercer gráfico es un gráfico de barras verticales que muestra las ventas por segmento. Este gráfico nos muestra la proporción de ventas que provienen de cada segmento: consumidor, corporativo y hogar. En este caso, podemos ver que el segmento de consumidores es el que genera la mayoría de las ventas totales, seguido del segmento corporativo y hogar. Este tipo de información es muy valiosa para la empresa, ya que les permite enfocar sus esfuerzos de marketing en el segmento que está generando la mayoría de las ventas.
sales_by_state = ventas_df.groupby("State")["Sales"].sum().reset_index()
us_states = 'us-states.json'
geo_json_data = json.load(open(us_states))
map = folium.Map(location=[37,-102], zoom_start=4)
folium.Choropleth(
    geo_data=geo_json_data,
    name="choropleth",
    data=sales_by_state,
    columns=["State", "Sales"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Ventas por Estado",
    highlight=True,
    overlay=True,
    control=True,
    show=True,
    smooth_factor=0.5,
    nan_fill_color="white",
    nan_fill_opacity=0.4,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['name', 'Sales'],
        aliases=['Estado', 'Ventas'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12")
    )
).add_to(map)
map.save('ventas_por_estado.html')

#Por último, el mapa territorial de las ventas por estado muestra la distribución geográfica de las ventas. Este mapa nos permite ver claramente qué estados tienen las mayores ventas y cuáles tienen las menores. Podemos ver que los estados de la costa oeste y del este de los Estados Unidos tienen mayores ventas totales, mientras que los estados del medio oeste tienen ventas más bajas. Además, al pasar el cursor sobre cada estado, podemos ver el nombre del estado y la cantidad de ventas totales. Esto es útil para la empresa ya que les permite identificar las áreas geográficas que necesitan más atención y enfocar sus esfuerzos de marketing en esas áreas específicas.
# Mapa territorial de las ventas por estado
sales_by_state = ventas_df.groupby("State")["Sales"].sum().reset_index()
us_states = 'C:/Users/danie/Desktop/us-states.json'
geo_json_data = json.load(open(us_states))
map = folium.Map(location=[37,-102], zoom_start=4)
folium.Choropleth(
    geo_data=geo_json_data,
    name="choropleth",
    data=sales_by_state,
    columns=["State", "Sales"],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Ventas por Estado",
    highlight=True,
    overlay=True,
    control=True,
    show=True,
    smooth_factor=0.5,
    nan_fill_color="white",
    nan_fill_opacity=0.4,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['name', 'Sales'],
        aliases=['Estado', 'Ventas'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12")
    ),
    ).add_to(map)


#En conclusión, estos gráficos y mapas nos permiten entender mejor el rendimiento de las ventas de la empresa en diferentes áreas geográficas y categorías de productos. Esto a su vez les permite a los ejecutivos de la empresa tomar decisiones informadas sobre cómo mejorar su estrategia de marketing y aumentar sus ventas en el futuro. Espero que esta historia haya sido útil
