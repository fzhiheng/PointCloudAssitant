import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from format_transformation.FormatTrans import FormatTrans
from main_windows import MyMainWindows


if __name__ == '__main__':
    # if os.path.exists(""):
    #     print('agag')
    myapp = QApplication(sys.argv)
    # main_window = QMainWindow()
    main_window = MyMainWindows()
    main_window.show()
    sys.exit(myapp.exec_())


