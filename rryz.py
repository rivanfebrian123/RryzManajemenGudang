#!/bin/python3

import sys
# TODO: untuk pengembangan berikutnya:
# folderInstalasi = “@DITENTUKAN_OLEH_INSTALLER@”
# sys.path.insert(1, folderInstalasi + “src”)

from PyQt5 import QtWidgets, QtCore
from src.dialogLogin import DialogLogin


if __name__ == "__main__":
    QtCore.QResource.registerResource("resource.rcc")

    app = QtWidgets.QApplication(sys.argv)
    win = DialogLogin()

    win.show()

    app.exec_()
