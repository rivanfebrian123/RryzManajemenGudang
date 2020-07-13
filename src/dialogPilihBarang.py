# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtCore, uic
from .dialogBarang import DialogBarang


class DialogPilihBarang(QtWidgets.QDialog):
    def __init__(self, winUtama):
        super().__init__(winUtama)
        uic.loadUi('data/dialogPilihBarang.ui', self, '', 'gudangQt')

        self.txtKode = self.findChild(QtWidgets.QLineEdit, "txtKode")
        self.lblJumlah = self.findChild(QtWidgets.QLabel, "lblJumlah")
        self.txtJumlah = self.findChild(QtWidgets.QLineEdit, "txtJumlah")
        self.btnLanjut = self.findChild(QtWidgets.QPushButton, "btnLanjut")

        # ngga usah konek signal manual selama nama prosedurnya udah
        # pas, misal: on_NAMAOBJEK_NAMASIGNAL(), dan jangan lupa dikasih
        # dekorator @QtCore.pyqtSlot()

        self.win = winUtama
        self.db = self.win.db

    def showUntukPilihBarang(self):
        self.mode = "pilihBarang"
        self.show("Pilih barang")

    def showUntukHapusBarang(self):
        self.mode = "hapusBarang"
        self.show("Hapus barang")

    def showUntukTambahStok(self):
        self.lblJumlah.setText("Jumlah yang akan ditambah")
        self.mode = "tambahStok"
        self.show("Tambah stok")

    def showUntukAmbilStok(self):
        self.lblJumlah.setText("Jumlah yang akan diambil")
        self.mode = "ambilStok"
        self.show("Ambil stok")

    def show(self, txt):
        self.btnLanjut.setText(txt)
        self.setWindowTitle(txt)
        self.txtKode.setText("")

        if self.mode == "pilihBarang" or self.mode == "hapusBarang":
            self.lblJumlah.hide()
            self.txtJumlah.hide()
        elif self.mode == "tambahStok" or self.mode == "ambilStok":
            self.txtJumlah.setText("")
            self.lblJumlah.show()
            self.txtJumlah.show()

        self.txtKode.setFocus()
        super().show()
        self.resize(366, 0)

    @QtCore.pyqtSlot()
    def on_btnLanjut_clicked(self):
        kodeBrg = self.txtKode.text()

        if self.db.eksekusi("SELECT * FROM `barang` WHERE `kode` = '" +
                            kodeBrg + "'"):
            hslQuery = self.db.ambilQueryPertama()  # hasil queri pencarian

            if hslQuery:
                if self.mode == "tambahStok" or self.mode == "ambilStok":
                    jmlStokLama = hslQuery.value(5)
                    jmlStokBaru = 0
                    hslJmlStokBaru = 0  # hasil penjumlahan / pengurangan stok

                    try:
                        jmlStokBaru = int(self.txtJumlah.text())
                    except ValueError:
                        self.db.beritahuKegagalan(
                            "Angka yang njenengan masukkan salah")
                    else:
                        if self.mode == "tambahStok":
                            hslJmlStokBaru = jmlStokLama + jmlStokBaru
                        elif self.mode == "ambilStok":
                            hslJmlStokBaru = jmlStokLama - jmlStokBaru

                        if self.db.eksekusi(
                            "UPDATE `barang` SET `jumlahStok` = '" +
                            str(hslJmlStokBaru) + "' WHERE `kode` = '" +
                                kodeBrg + "'", "", "Gagal mengubah stok."):
                            self.win.perbaruiModel()
                            self.hide()
                if self.mode == "pilihBarang":
                    if not self.win.dialogBarang:
                        self.win.dialogBarang = DialogBarang(self.win)

                    self.hide()
                    self.win.dialogBarang.showUntukPerbaruiBarang(hslQuery)
                elif self.mode == "hapusBarang":
                    if self.db.eksekusi(
                        "DELETE FROM `barang` WHERE `kode` = '" + kodeBrg +
                        "'", "Barang berhasil dihapus",
                            "Gagal menghapus barang"):
                        self.win.perbaruiModel()
                        self.hide()

