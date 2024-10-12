import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Bottled Water Production Monitoring')
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Layout for the first machine and conveyor
        blowing_layout = QHBoxLayout()
        self.blowing_machine = QPushButton('Bottle Blowing Machine')
        self.blowing_machine.setStyleSheet('background-color: green; color: white;')
        self.blowing_machine.clicked.connect(lambda: self.machine_clicked('Blowing Machine'))
        blowing_layout.addWidget(self.blowing_machine)
        
        conveyor1 = QLabel('Conveyor')
        conveyor1.setAlignment(Qt.AlignCenter)
        conveyor1.setStyleSheet('background-color: lightgray;')
        blowing_layout.addWidget(conveyor1)
        
        main_layout.addLayout(blowing_layout)
        
        # Spacer to move to next row
        main_layout.addSpacing(20)
        
        # Layout for the second machine and conveyor
        filling_layout = QHBoxLayout()
        main_layout.addLayout(filling_layout)
        
        conveyor2_1 = QLabel('Conveyor')
        conveyor2_1.setAlignment(Qt.AlignCenter)
        conveyor2_1.setStyleSheet('background-color: lightgray;')
        filling_layout.addWidget(conveyor2_1)
        
        self.filling_machine = QPushButton('Bottle Filling Machine')
        self.filling_machine.setStyleSheet('background-color: green; color: white;')
        self.filling_machine.clicked.connect(lambda: self.machine_clicked('Filling Machine'))
        filling_layout.addWidget(self.filling_machine)
        
        conveyor2_2 = QLabel('Conveyor')
        conveyor2_2.setAlignment(Qt.AlignCenter)
        conveyor2_2.setStyleSheet('background-color: lightgray;')
        filling_layout.addWidget(conveyor2_2)
        
        # Spacer to move to next row
        main_layout.addSpacing(20)
        
        # Layout for the third machine and conveyor
        labeling_layout = QHBoxLayout()
        main_layout.addLayout(labeling_layout)
        
        conveyor3_1 = QLabel('Conveyor')
        conveyor3_1.setAlignment(Qt.AlignCenter)
        conveyor3_1.setStyleSheet('background-color: lightgray;')
        labeling_layout.addWidget(conveyor3_1)
        
        self.labeling_machine = QPushButton('Bottle Labeling Machine')
        self.labeling_machine.setStyleSheet('background-color: green; color: white;')
        self.labeling_machine.clicked.connect(lambda: self.machine_clicked('Labeling Machine'))
        labeling_layout.addWidget(self.labeling_machine)
        
        conveyor3_2 = QLabel('Conveyor')
        conveyor3_2.setAlignment(Qt.AlignCenter)
        conveyor3_2.setStyleSheet('background-color: lightgray;')
        labeling_layout.addWidget(conveyor3_2)
        
        # Spacer to move to next row
        main_layout.addSpacing(20)
        
        # Layout for the fourth machine and conveyor
        packing_layout = QHBoxLayout()
        main_layout.addLayout(packing_layout)
        
        conveyor4_1 = QLabel('Conveyor')
        conveyor4_1.setAlignment(Qt.AlignCenter)
        conveyor4_1.setStyleSheet('background-color: lightgray;')
        packing_layout.addWidget(conveyor4_1)
        
        self.packing_machine = QPushButton('Bottle Packing Machine')
        self.packing_machine.setStyleSheet('background-color: green; color: white;')
        self.packing_machine.clicked.connect(lambda: self.machine_clicked('Packing Machine'))
        packing_layout.addWidget(self.packing_machine)
        
        conveyor4_2 = QLabel('Conveyor')
        conveyor4_2.setAlignment(Qt.AlignCenter)
        conveyor4_2.setStyleSheet('background-color: lightgray;')
        packing_layout.addWidget(conveyor4_2)
        
        central_widget.setLayout(main_layout)

    def machine_clicked(self, machine_name):
        print(f'{machine_name} clicked')
        # Example: Change color to indicate different state
        if machine_name == 'Blowing Machine':
            self.blowing_machine.setStyleSheet('background-color: yellow; color: black;')
        elif machine_name == 'Filling Machine':
            self.filling_machine.setStyleSheet('background-color: yellow; color: black;')
        elif machine_name == 'Labeling Machine':
            self.labeling_machine.setStyleSheet('background-color: yellow; color: black;')
        elif machine_name == 'Packing Machine':
            self.packing_machine.setStyleSheet('background-color: yellow; color: black;')

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
