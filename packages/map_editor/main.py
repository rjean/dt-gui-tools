# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator
from mainwindow import duck_window
from logger import init_logger

logger = init_logger()

LANG_DIR = './resources/lang/qm'

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Install translator
    translator = QTranslator(app)
    locale = sys.argv[1] if len(sys.argv) == 2 else 'en' 
    translator.load('{}/lang_{}.qm'.format(LANG_DIR, locale))
    app.installTranslator(translator)
    
    window = duck_window(locale)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
