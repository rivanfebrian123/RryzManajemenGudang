# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtCore, uic
from .dialogUbahKodeBarang import DialogUbahKodeBarang


class DialogBarang(QtWidgets.QDialog):
    def __init__(self, winUtama):
        super().__init__(winUtama)
        uic.loadUi('data/dialogBarang.ui', self, '', 'gudangQt')

        self.txtKode = self.findChild(QtWidgets.QLineEdit, "txtKode")
        self.btnUbahKode = self.findChild(QtWidgets.QPushButton, "btnUbahKode")
        self.txtNama = self.findChild(QtWidgets.QLineEdit, "txtNama")
        self.txtSatuan = self.findChild(QtWidgets.QLineEdit, "txtSatuan")
        self.txtHargaBeli = self.findChild(QtWidgets.QLineEdit, "txtHargaBeli")
        self.txtHargaJual = self.findChild(QtWidgets.QLineEdit, "txtHargaJual")
        self.txtJumlahStok = self.findChild(
            QtWidgets.QLineEdit, "txtJumlahStok")
        self.btnTambahPerbaruiBarang = self.findChild(
            QtWidgets.QPushButton, "btnTambahPerbaruiBarang")

        # ngga usah konek signal manual selama nama prosedurnya udah
        # pas, misal: on_NAMAOBJEK_NAMASIGNAL(), dan jangan lupa dikasih
        # dekorator @QtCore.pyqtSlot()

        self.win = winUtama
        self.db = self.win.db

        # kita inisialisasi objek2 ini terakhir2an aja, biar kinerja tetap
        # terjaga
        self.dialogUbahKodeBarang = None

    def showUntukTambahBarang(self):
        self.mode = "tambahBarang"
        self.txtKode.setEnabled(True)
        self.btnUbahKode.hide()

        self.txtKode.setText("")
        self.txtNama.setText("")
        self.txtSatuan.setText("")
        self.txtHargaBeli.setText("")
        self.txtHargaJual.setText("")
        self.txtJumlahStok.setText("")

        self.txtKode.setFocus()
        self.show("Tambah barang")

    def showUntukPerbaruiBarang(self, query):
        self.mode = "perbaruiBarang"
        self.txtKode.setEnabled(False)
        self.btnUbahKode.show()

        self.txtKode.setText(query.value(0))
        self.txtNama.setText(query.value(1))
        self.txtSatuan.setText(query.value(2))
        self.txtHargaBeli.setText(str(query.value(3)))
        self.txtHargaJual.setText(str(query.value(4)))
        self.txtJumlahStok.setText(str(query.value(5)))

        self.txtNama.setFocus()
        self.show("Perbarui barang")

    def show(self, txt):
        self.btnTambahPerbaruiBarang.setText(txt)
        self.setWindowTitle(txt)

        super().show()

    @QtCore.pyqtSlot()
    def on_btnTambahPerbaruiBarang_clicked(self):
        hasil = False

        if self.mode == "tambahBarang":
            hasil = self.db.eksekusi("INSERT INTO `barang` VALUES ('" +
                                     self.txtKode.text() + "', '" +
                                     self.txtNama.text() + "', '" +
                                     self.txtSatuan.text() + "', '" +
                                     self.txtHargaBeli.text() + "', '" +
                                     self.txtHargaJual.text() + "', '" +
                                     self.txtJumlahStok.text() + "')")
        elif self.mode == "perbaruiBarang":
            hasil = self.db.eksekusi("UPDATE `barang` SET " +
                                     "`nama` = '" + self.txtNama.text() +
                                     "', `satuan` = '" +
                                     self.txtSatuan.text() +
                                     "', `hargaBeli` = '" +
                                     self.txtHargaBeli.text() +
                                     "', `hargaJual` = '" +
                                     self.txtHargaJual.text() +
                                     "', `jumlahStok` = '" +
                                     self.txtJumlahStok.text() +
                                     "' WHERE `kode` = '" +
                                     self.txtKode.text() + "' ")

        if hasil:
            self.hide()
            self.win.perbaruiModel()

    @QtCore.pyqtSlot()
    def on_btnUbahKode_clicked(self):
        if not self.dialogUbahKodeBarang:
            self.dialogUbahKodeBarang = DialogUbahKodeBarang(self)

        self.dialogUbahKodeBarang.show(self.txtKode.text())

