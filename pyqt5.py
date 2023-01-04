import PyQt5.QtWidgets as qtw

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
            

        self.show()


app= qtw.QApplication([])

mw = MainWindow()


app.exec_()