all: resource

resource:
	rcc -binary resource.qrc -o resource.rcc

clean:
	echo ''
	
# GNOME Builder manggil target ini sebelum jalanin program ini
install:
	echo ''

# GNOME Builder manggil target ini buat jalanin program ini
run:
	./rryz.py

