# Anleitung Gehaeuse Bau

---


### Anforderungen 
* Aufbau mit Akkubetrieb
* Wasserdichtigkeit (Spritzwasserschutz)

### der Zusammenbau

#### Materialen:
* Marley HT-Bogen (87° DIN75)
* Marley 2x HT-Muffenstopfen(DIN75)
* Marley HT-Überschiebmuff(DIN75)

![Materialien](BilderAufbau/IMG_9920.jpeg)
#### Vorbereitungen
Zunächst habe ich zwei Löcher bohren müssen. Einmal für den Schlauch des SDS Dust Sensors. Und einmal für die Antenne des Lora Boards. 
Für den Schlauch habe ich einen 7mm Bohrer genutzt und für die Antenne einen 8mm Bohrer. 
![](Bilder/IMG_9925.jpeg)

Daraufhin habe ich dann den SDS Dust Sensor in einen Muffenstopfengeschoben. Der Sensor passt genau in den Stopfen und es ist nicht nötig ihn zusätzlich zu befästigen. Der Schlauch hält den Sensor zusätzlich.


![](Bilder/IMG_9929.jpeg)

Das Lora-Board zu befästigen war etwas schwieriger, da die Antenne zuerst eingefädelt werden muss und dann das Board in das Rohr eingeführt werden kann.


![](Bilder/IMG_9936.jpeg)
Mit ein wenig Fingerspitzen Gefühl kann dann die Antenne an das Board geschraubt werden. Die Antenne hält das Board fest. Allerdings musste ich zusätzlich das Board noch mit Klettband befestigen.

![](Bilder/IMG_9937.jpeg)


Dann kann der Sensor angeschlossen werden und die Muffe geschlossen werden.

An das Board kommt nun noch die 9V Spannungsversorgung. Ich habe den Anschluss für die Batterie im unteren Muffenstopfen angeklebt. Jetzt kann die Batterie angeschlossen werden. Der Sensor ist in Betrieb und sendet nun kontinuirlich Daten an TTN.


![](Bilder/IMG_9944.jpeg)

Wenn der Sensor neu geflasht werden soll, kann dies ganz einfach dadurch geschehen, indem der untere Muffenstopfen geöffnet wird und das USB Kabel angeschlossen wird.


![](Bilder/IMG_9947.jpeg)

#### Zu Diskutierende Features: 
* Akkubetrieb, mittels USB Aufladbar
* I/O Schalter
