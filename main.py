import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from format_transformation.FormatTrans import FormatTrans




if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    # main_window = QMainWindow()
    format_widget = FormatTrans()
    format_widget.show()
    sys.exit(myapp.exec_())


