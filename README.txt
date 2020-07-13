Jangan lupa impor struktur datanya ke server SQL njenengan pake PHPMyAdmin
sebelum pake aplikasi ini, habis itu atur kolom gudang_qt.barang.kode sbg
primary key kalo PHPMyAdmin-nya ngga ngatur secara otomatis

Aku saranin njenengan pake frameworknya MSYS2 aja, jangan pake Anaconda;
soalnya Anaconda seingetku ngga ada library MySQL/MariaDB client-nya. Kalo
njenengan install MSYS2, jangan lupa uninstall Anaconda dan installer2 Python
yang lain

Kalo njenengan pake Qt Creator, jangan lupa atur run-nya kaya gini:
    executable  : python
    arguments   : rryz.py
    working dir : folder ini
