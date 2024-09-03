import sys
import os
added_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(added_path)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename=f"LabelSIG.log",
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - [%(name)s] %(message)s')
logger = logging.getLogger("LabelSIG")


from labelsig.widget.MainView import MainWindow
from labelsig.utils import get_parent_directory

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    root_labelsig = get_parent_directory(levels_up=1)
    icon_path = os.path.join(root_labelsig, 'resource', 'logo.ico')
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



