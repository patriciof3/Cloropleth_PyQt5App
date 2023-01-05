import PyQt5.QtWidgets as qtw
import pandas as pd
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Add title
        self.setWindowTitle("App-Consultora")

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())

        #Create label

        load_label = qtw.QLabel("Introduzca su base de datos")

        #Change fontsize of label
        load_label.setFont(qtg.QFont("Helvetica", 12))

        self.layout().addWidget(load_label)

        #Create an entry box

        my_entry =qtw.QLineEdit()
        my_entry.setObjectName("csv_file")
        self.layout().addWidget(my_entry)

        #Create button

        my_button = qtw.QPushButton("Cargar archivo",
            clicked = lambda: press_it())
        self.layout().addWidget(my_button)

        loaded_label = qtw.QLabel("No ha cargado ningún archivo")
        loaded_label.setFont(qtg.QFont("Helvetica", 12))
        self.layout().addWidget(loaded_label)
           

        def press_it():
            loaded_label.setText(f"El archivo <{my_entry.text()}> se ha cargado con éxito")

            # Create a button and set its text
        load_btn = qtw.QPushButton('Import CSV', self)
        load_btn.move(20, 20)
        self.layout().addWidget(load_btn)

        # Connect the clicked signal to the import_csv method
        load_btn.clicked.connect(self.import_csv)

    def import_csv(self):
        options = qtw.QFileDialog.Options()
        options |= qtw.QFileDialog.ReadOnly
        file_name, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if file_name:
            # Read the CSV file into a DataFrame using pandas
            self.df = pd.read_csv(file_name, sep = ";")
            # Print the DataFrame to the console
            print(self.df.head())
            

        self.show()


app= qtw.QApplication([])

mw = MainWindow()


app.exec_()