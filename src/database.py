# Dikembangkan oleh Tim Pengembang RRYZ IT Telkom Purwokerto
# Lisensi : GPLv3

from PyQt5 import QtWidgets, QtSql


class Database():
    def __init__(self, tipe="QMYSQL"):
        self.db = QtSql.QSqlDatabase.addDatabase(tipe)
        self.qw = QtSql.QSqlQuery(self.db)
        self.md = QtSql.QSqlQueryModel()

        self.msgInfo = QtWidgets.QMessageBox()

        # biar ngga nge-hang kalo ada masalah jaringan dll.
        if tipe == "QMYSQL":
            opsi = ("MYSQL_OPT_READ_TIMEOUT=5;MYSQL_OPT_WRITE_TIMEOUT=5;" +
                    "MYSQL_OPT_CONNECT_TIMEOUT=5")
        elif tipe == "QODBC":
            opsi = "SQL_ATTR_LOGIN_TIMEOUT=5;SQL_ATTR_CONNECTION_TIMEOUT=5"
        elif tipe == "QPSQL":
            opsi = "connection_timeout=5"
        elif tipe == "QDB2":
            opsi = "SQL_ATTR_LOGIN_TIMEOUT=5"
        elif tipe == "QSQLITE":
            opsi = "QSQLITE_BUSY_TIMEOUT=5"

        self.db.setConnectOptions(opsi)

    def login(self, alamat, namaDB, username, passwd, port=3306,
              ucapanSelamat="", ucapanGagal="Gagal login. Mungkin salah " +
              "server, alamat, atau kata sandi; atau salah kofigurasi; " +
              "koneksi terputus; atau kemungkinan kesalahan lainnya."):
        hasil = False

        self.db.setHostName(alamat)
        self.db.setDatabaseName(namaDB)
        self.db.setUserName(username)
        self.db.setPassword(passwd)
        self.db.setPort(port)

        hasil = self.db.open()

        if hasil:
            if ucapanSelamat != "":
                self.beritahuKabarBaik(ucapanSelamat)
        else:
            if ucapanGagal != "":
                self.beritahuKegagalan(ucapanGagal)

        return hasil

    def logout(self):
        self.db.close()

    def eksekusi(self, perintah, ucapanSelamat="",
                 ucapanGagal="Gagal submit / mengambil data."):
        hasil = False

        # self.qw.exec(perintah) kadang ngga nge-return value (void),
        # jadi kita ngga bisa nulis: "hasil = self.qw.exec(perintah)"
        if self.qw.exec(perintah):
            hasil = True
        else:
            # coba lagi barangkali koneksi terputus. kita ngga pake
            # if self.db.isOpen: ... soalnya ngga stabil
            self.db.open()

            if self.qw.exec(perintah):
                hasil = True

        if hasil:
            if ucapanSelamat != "":
                self.beritahuKabarBaik(ucapanSelamat)
        else:
            if ucapanGagal != "":
                self.beritahuKegagalan(ucapanGagal)

        return hasil

    def beritahuKegagalan(self, teks):
        self.msgInfo.setWindowTitle("Oh, tidak!")
        self.msgInfo.setText(teks)
        self.msgInfo.setIcon(QtWidgets.QMessageBox.Critical)
        self.msgInfo.show()

    def beritahuKabarBaik(self, teks):
        self.msgInfo.setWindowTitle("Info!")
        self.msgInfo.setText(teks)
        self.msgInfo.setIcon(QtWidgets.QMessageBox.Information)
        self.msgInfo.show()

    def beritahuKegagalanAmbilQuery(self):
        self.beritahuKegagalan(
            "Data tidak ditemukan. Kalo ada yang salah, coba pastikan " +
            "eksekusi query terakhir udah bener. Cari tahu juga kemungkinan " +
            "masalah lainnya.")

    def perbaruiModel(self, perintah):
        hasil = False

        # baris perintah di bawah ini ngga nge-return nilai keberhasilan,
        # jadi kita kudu panggil lastError().isValid() supaya tau berhasil
        # nggaknya
        self.md.setQuery(perintah, self.db)

        if self.md.lastError().isValid():
            # coba lagi barangkali koneksi terputus. kita ngga pake
            # if self.db.isOpen: ... soalnya ngga stabil
            self.db.open()
            self.md.setQuery(perintah, self.db)

            if self.md.lastError().isValid():
                self.beritahuKegagalan("Gagal mengambil data. Mungkin ada " +
                                       "masalah koneksi atau yang lain.")

        return self.md

    def ambilQueryPertama(self):
        if self.qw.first():
            return self.qw
        else:
            self.beritahuKegagalanAmbilQuery()

    def ambilQueryTerakhir(self):
        if self.qw.last():
            return self.qw
        else:
            self.beritahuKegagalanAmbilQuery()

    def ambilQueryBerikutnya(self):
        if self.qw.next():
            return self.qw
        else:
            self.beritahuKegagalanAmbilQuery()

    def ambilQuerySebelumnya(self):
        if self.qw.previous():
            return self.qw
        else:
            self.beritahuKegagalanAmbilQuery()

    def ambilQueryPadaIndeks(self, indeks, relatif=False):
        if self.qw.seek(indeks, relatif):
            return self.qw
        else:
            self.beritahuKegagalanAmbilQuery()

