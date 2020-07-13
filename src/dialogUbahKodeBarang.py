# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtCore, uic


class DialogUbahKodeBarang(QtWidgets.QDialog):
    def __init__(self, dlgBarang):
        super().__init__(dlgBarang)
        uic.loadUi('data/dialogUbahKodeBarang.ui', self, '', 'gudangQt')

        self.txtKodeLama = self.findChild(QtWidgets.QLineEdit, "txtKodeLama")
        self.txtKodeBaru = self.findChild(QtWidgets.QLineEdit, "txtKodeBaru")
        self.btnUbahKodeBarang = self.findChild(QtWidgets.QPushButton,
                                                "btnUbahKodeBarang")

        # ngga usah konek signal manual selama nama prosedurnya udah
        # pas, misal: on_NAMAOBJEK_NAMASIGNAL(), dan jangan lupa dikasih
        # dekorator @QtCore.pyqtSlot()

        self.dlg = dlgBarang
        self.win = self.dlg.win
        self.db = self.win.db

    def show(self, kodeBarangLama):
        self.txtKodeLama.setText(kodeBarangLama)
        self.txtKodeBaru.setText(kodeBarangLama)

        self.txtKodeBaru.setFocus()
        super().show()

    @QtCore.pyqtSlot()
    def on_btnUbahKodeBarang_clicked(self):
        if self.db.eksekusi("UPDATE `barang` SET `kode` = '" +
                            self.txtKodeBaru.text() + "' WHERE `kode` = '" +
                            self.txtKodeLama.text() + "' "):
            self.dlg.txtKode.setText(self.txtKodeBaru.text())
            self.win.perbaruiModel()
            self.hide()

