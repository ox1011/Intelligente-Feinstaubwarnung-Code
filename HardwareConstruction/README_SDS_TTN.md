# Intelligente Feinstaubwarnung
## SDS Sensor bauen und programmieren
### verwendete Hardware und Software

Wir nutzen folgende Hardware:
* Dragino LoRa Iot Dev Kit v2
   * LG01-N LoRa Gateway
   * LoRa Shield
   * Arduino Uno
   * DHT11 Temperatur und Feuchtigkeits Sensor
   * diverse Kabel
* SDS011 Feinstaubsensor
* I/O Schalter
* USB D Verlaengerung
* USB D Kabel

Um die Hardware einzurichten, koennt ihr die Einleitung von Dragino nutzen.

[Dragino Manuel](http://www.dragino.com/downloads/downloads/LoRa_IoT_Kit/v2-Kit/Single%20Channel%20LoRa%20IoT%20Kit%20v2%20User%20Manual_v1.0.6.pdf)

In dieser Anleitung richtet ihr das Gateway ein, veraendert die
config.h und ladet das erste Skript auf die Arduinos.

Ihr braucht dazu folgende Software und Libraries:
* Arduino IDE
* SDS011 von R.Zschiegner
* DHT sensor library
* Und alle Libraries aus der Anleitungen von Dragino

Ganz wichtig ist es, die SDS011 von Herrn Zschiegner zu nehmen. Das war eine der
wenigen, die mit TTN funktioniert haben. Die anderen haben das Gesamtprogramm
zum abstuerzen gebracht.

Wenn die sleep und wakeup Methode des SDS Sensors verwendet werden soll und es
sich um einen aktuelle SDS Sensor handelt, muss die sds011.cpp noch modifiziert
werden, da es sonst zu Komplikationen kommt. Diese *.cpp liegt bei allen
anderen Libraries, welche ihr ueber die Arduino IDE geladen habt. Meist ist
das unter `/usr/documents/Arduino/libraries`

Hier eine mgl Loesung:

```Cpp
// --------------------------------------------------------
// SDS011:wakeup
// --------------------------------------------------------

static const byte WAKEUPCMD[19] = {
	0xAA,	// head
	0xB4,	// command id
	0x06,	// data byte 1
	0x01,	// data byte 2 (set mode)
	0x01,	// data byte 3 (wake up)
	0x00,	// data byte 4
	0x00,	// data byte 5
	0x00,	// data byte 6
	0x00,	// data byte 7
	0x00,	// data byte 8
	0x00,	// data byte 9
	0x00,	// data byte 10
	0x00,	// data byte 11
	0x00,	// data byte 12
	0x00,	// data byte 13
	0xFF,	// data byte 14 (device id byte 1)
	0xFF,	// data byte 15 (device id byte 2)
	0x06,	// checksum
	0xAB	// tail
};
// --------------------------------------------------------
// SDS011:wakeup
// --------------------------------------------------------
void SDS011::wakeup() {
	for (uint8_t i = 0; i < 19; i++) {
		sds_data->write(WAKEUPCMD[i]);
	}
	sds_data->flush();
	while (sds_data->available() > 0) {
		sds_data->read();
	}
}

```

### Arduinos flashen und in einem Gehaeuse verbauen

Nachdem Ihr alles vorbereitet habt, koennt ihr unser Skript auf eueren Arduino
laden und an eure Wuensche anpassen.

Das Skript funktioniert so, dass in Abhaengigkeit des schedule_TIME die Methode
do_send() aufgerufen wird. In dieser Methode werden die Feinstaubwerte und die
Werte des DHT11 Sensors gemessen und an in einem Byte-Array gespeichert. 
Dieses Array wird dann an TTN gesendet.

Wenn alles eingerichtet ist, koennt ihr die Arduinos in einem Gehaeuse verbauen,
damit es Outdoor spirtzwasser geschuetzt ist.

Dafuer haben wir auch eine Anleitung geschrieben. [Anleitung
Gehaeuse](README_CASING.md).

### Daten an Luftdaten.info senden

Momentan sendet das LoRa Shield die Feinstaub -und Temperaturwerte ueber das
Gateway an TTN. Um diese Daten auf luftdaten.info zu bekommen, haben wir eine
Dockerloesung genutzt. [Anleitung Docker](README_DATA_TO_LUFTDATEN.md)


