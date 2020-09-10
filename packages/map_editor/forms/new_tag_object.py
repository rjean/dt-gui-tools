from PyQt5.QtWidgets import QWidget, QComboBox, QDialog, QGroupBox, QDialogButtonBox, QFormLayout,QVBoxLayout

class NewTagForm(QDialog):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def dialog_accept(self):
        self.close()

    def dialog_reject(self):
        self.close()
    
    def init_UI(self):
        self.setWindowTitle('New tag')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.dialog_accept)   
        buttonBox.rejected.connect(self.dialog_reject)

        formGroupBox = QGroupBox("")

        layout = QFormLayout()
        combo_type = QComboBox(self)
        combo_type.addItems(["Localozation", "TrafficSigns"])
        combo_type.activated[str].connect(self.change_type)
        layout.addRow(combo_type)

        self.combo_id = QComboBox(self)
        self.combo_id.addItems(["1", "2"])
        layout.addRow(self.combo_id)

        formGroupBox.setLayout(layout)
        # layout
        mainLayout = QVBoxLayout() 
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def create_form(self):
        self.exec_()

    def change_type(self, text):
        print(text)
        if text == "TrafficSigns":
            self.combo_id.clear()
            self.combo_id.addItems(["3", "4"])
        else:
            self.combo_id.clear()
            self.combo_id.addItems(['1', "2"])
        