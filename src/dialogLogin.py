# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtCore, uic
from .database import Database
from .windowUtama import WindowUtama


class DialogLogin(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/dialogLogin.ui', self, '', 'gudangQt')

        self.txtAlamatServer = self.findChild(QtWidgets.QLineEdit,
                                              "txtAlamatServer")
        self.txtNamaPengguna = self.findChild(QtWidgets.QLineEdit,
                                              "txtNamaPengguna")
        self.txtKataSandi = self.findChild(QtWidgets.QLineEdit, "txtKataSandi")
        self.btnLogin = self.findChild(QtWidgets.QPushButton, "btnLogin")

        # ngga usah konek signal manual selama nama prosedurnya udah
        # pas, misal: on_NAMAOBJEK_NAMASIGNAL(), dan jangan lupa dikasih
        # dekorator @QtCore.pyqtSlot()

        # kita inisialisasi objek2 ini terakhir2an aja, biar kinerja tetap
        # terjaga
        self.db = None
        self.win = None

    @QtCore.pyqtSlot()
    def on_btnLogin_clicked(self):
        if not self.db:
            self.db = Database()

        if self.db.login(self.txtAlamatServer.text(), "gudang_qt",
                         self.txtNamaPengguna.text(),
                         self.txtKataSandi.text()):
            if not self.win:
                self.win = WindowUtama(self)

            self.hide()
            self.win.show()

    def show(self):
        self.txtAlamatServer.setText("")
        self.txtNamaPengguna.setText("")
        self.txtKataSandi.setText("")

        self.txtAlamatServer.setFocus()
        super().show()

