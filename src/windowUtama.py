# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtCore, uic
from .dialogBarang import DialogBarang
from .dialogPilihBarang import DialogPilihBarang


class WindowUtama(QtWidgets.QMainWindow):
    def __init__(self, dlgLogin):
        super().__init__()
        uic.loadUi('data/windowUtama.ui', self, '', 'gudangQt')

        self.btnTambahStok = self.findChild(QtWidgets.QPushButton,
                                            "btnTambahStok")
        self.btnAmbilStok = self.findChild(QtWidgets.QPushButton,
                                           "btnAmbilStok")
        self.tableBarang = self.findChild(QtWidgets.QTableView, "tableBarang")
        self.btnHapusBarang = self.findChild(QtWidgets.QPushButton,
                                             "btnHapusBarang")
        self.btnTambahBarang = self.findChild(QtWidgets.QPushButton,
                                              "btnTambahBarang")
        self.btnPerbaruiBarang = self.findChild(QtWidgets.QPushButton,
                                                "btnPerbaruiBarang")
        self.actRefresh = self.findChild(QtWidgets.QAction, "actRefresh")
        self.actLogout = self.findChild(QtWidgets.QAction, "actLogout")
        self.actTentang = self.findChild(QtWidgets.QAction, "actTentang")

        # ngga usah konek signal manual selama nama prosedurnya udah
        # pas, misal: on_NAMAOBJEK_NAMASIGNAL(), dan jangan lupa dikasih
        # dekorator @QtCore.pyqtSlot()

        self.dlg = dlgLogin
        self.db = self.dlg.db

        self.tableBarang.setModel(self.db.md)

        # kita inisialisasi objek2 ini terakhir2an aja, biar kinerja tetap
        # terjaga
        self.dialogBarang = None
        self.dialogPilihBarang = None
        self.dialogTentang = None

    def perbaruiModel(self):
        return self.db.perbaruiModel(
            "SELECT `kode` as 'Kode', `nama` as 'Nama barang', " +
            "`satuan` as 'Satuan', `hargaBeli` as 'Harga beli (kulak)', " +
            "`hargaJual` as 'Harga jual', `jumlahStok` as 'Jumlah stok' " +
            "FROM `barang`")

    def show(self):
        self.setWindowTitle(self.dlg.txtNamaPengguna.text() + "@" +
                            self.dlg.txtAlamatServer.text() +
                            " - Manajemen Gudang RRYZ")
        super().show()
        self.perbaruiModel()

    def initDialogPilihBarang(self):
        if not self.dialogPilihBarang:
            self.dialogPilihBarang = DialogPilihBarang(self)

    @QtCore.pyqtSlot()
    def on_btnTambahBarang_clicked(self):
        if not self.dialogBarang:
            self.dialogBarang = DialogBarang(self)
        self.dialogBarang.showUntukTambahBarang()

    @QtCore.pyqtSlot()
    def on_btnPerbaruiBarang_clicked(self):
        self.initDialogPilihBarang()
        self.dialogPilihBarang.showUntukPilihBarang()

    @QtCore.pyqtSlot()
    def on_btnHapusBarang_clicked(self):
        self.initDialogPilihBarang()
        self.dialogPilihBarang.showUntukHapusBarang()

    @QtCore.pyqtSlot()
    def on_btnTambahStok_clicked(self):
        self.initDialogPilihBarang()
        self.dialogPilihBarang.showUntukTambahStok()

    @QtCore.pyqtSlot()
    def on_btnAmbilStok_clicked(self):
        self.initDialogPilihBarang()
        self.dialogPilihBarang.showUntukAmbilStok()

    @QtCore.pyqtSlot()
    def on_actRefresh_triggered(self):
        self.perbaruiModel()

    @QtCore.pyqtSlot()
    def on_actLogout_triggered(self):
        self.db.logout()
        self.hide()
        self.dlg.show()

    @QtCore.pyqtSlot()
    def on_actTentang_triggered(self):
        if not self.dialogTentang:
            self.dialogTentang = QtWidgets.QDialog(self)
            uic.loadUi('data/dialogTentang.ui', self.dialogTentang,
                       '', 'gudangQt')
        self.dialogTentang.show()

