import sys
import pandas as pd
import geopandas as gpd
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generador de Mapas de Calor")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.csv_label = QLabel("No CSV file selected.")
        layout.addWidget(self.csv_label)

        self.csv_button = QPushButton("Seleccione archivo CSV")
        self.csv_button.clicked.connect(self.select_csv)
        layout.addWidget(self.csv_button)

        self.shp_label = QLabel("No SHP file selected.")
        layout.addWidget(self.shp_label)

        self.shp_button = QPushButton("Seleccione archivo SHP")
        self.shp_button.clicked.connect(self.select_shp)
        layout.addWidget(self.shp_button)

        self.variable_input = QLineEdit()
        self.variable_input.setPlaceholderText("Nombre de la variable:")
        layout.addWidget(self.variable_input)

        self.atributo_input = QLineEdit()
        self.atributo_input.setPlaceholderText("Atributo de la variable")
        layout.addWidget(self.atributo_input)

        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Título de la imagen")
        layout.addWidget(self.titulo_input)

        self.guardar_input = QLineEdit()
        self.guardar_input.setPlaceholderText("Guardar como:")
        layout.addWidget(self.guardar_input)

        self.run_button = QPushButton("Ejectutar")
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.csv_file = ""
        self.shp_file = ""

    def select_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "",
                                                  "CSV Files (*.csv);;All Files (*)", options=options)
        if filename:
            self.csv_file = filename
            self.csv_label.setText(f"Selected CSV file: {self.csv_file}")

    def select_shp(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select SHP File", "",
                                                  "Shapefiles (*.shp);;All Files (*)", options=options)
        if filename:
            self.shp_file = filename
            self.shp_label.setText(f"Selected SHP file: {self.shp_file}")

    def run_code(self):

        variable = self.variable_input.text()
        atributo = self.atributo_input.text()
        titulo = self.titulo_input.text()
        guardar_como = self.guardar_input.text()


        if self.csv_file:
                                        # Load CSV file into a pandas DataFrame
                df = pd.read_csv(self.csv_file, sep = ";")

                # change lat and long format
                df.latitud.replace(to_replace=",",value=".", inplace=True, regex=True)

                df.longitud.replace(to_replace=",", value=".", inplace=True, regex=True)

                #drop cases where there is no localization data
                df = df[~df.latitud.str.contains(" ")]

                df = df[~df.longitud.str.contains(" ")]


                #Transform df into a geodataframe
                dfgeo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitud, df.latitud))

                #Set crs of coordinates in dfgeo to match distritos
                dfgeo = dfgeo.set_crs("EPSG:4326")

        else:
            print("No CSV file selected.")

        if self.shp_file:
            # Load SHP file into a GeoPandas DataFrame
                distritos = gpd.read_file(self.shp_file)
                geojoined = gpd.sjoin(dfgeo, distritos, op="within")

                list_porc = []

                def porcentaje(distri):
                    geodist=geojoined[geojoined.Name == distri]

                    porcdist = geodist[variable][geodist[variable] == atributo].count() *100 / geodist[variable].count()

                    list_porc.append(porcdist)

                    return list_porc

                dist= distritos.Name.values

                list_porc=[]

                for i in dist:
                    porcentaje(i)


                #ADD LIST AS A COLUMN IN DISTRICTS DATAFRAME

                distritos["new_var"]=list_porc
                distritos["new_var"]=distritos["new_var"].round(decimals=1)

                fig, ax = plt.subplots(figsize=(8, 8))

                distritos.plot(ax=ax,
                                column="new_var",
                                cmap="Blues",
                                legend=False,
                                edgecolor="0")


                distritos.apply(lambda x: ax.annotate(text=x['new_var'],
                                xy=x.geometry.centroid.coords[0],
                                ha='center',
                                fontsize=13,
                                color="white",
                                path_effects=[pe.withStroke(linewidth=3, foreground="black")]),
                                axis=1)

                ax.axis("off")

                ax.set_title(titulo, fontsize=18, font="monospace", ha="center")

                plt.savefig(guardar_como + ".png", transparent=True)

        else:
            print("No SHP file selected.")

        image_path = os.path.join(os.getcwd(), guardar_como + ".png")
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



