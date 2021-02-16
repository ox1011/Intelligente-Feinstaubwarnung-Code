# Anleitung zum Senden der Daten von TTN an Luftdaten.info
---
### TODO
* Account bei Luftdaten.info erstellen und Sensor konfigurieren
* Payload bei TTN richtig decoden
* Docker-Lösung/eigene Skripte nutzen, um die Daten von TTN an Luftdaten.info zu schicken

### Durchführung

#### Luftdaten.info einrichten

Ihr geht auf die [Devices-Seite](https://devices.sensor.community/login) von  Luftdaten.info und erstellt euch dort einen Account.

Daraufhin wählt ihr den Reiter "Meine Sensoren aus" und drückt im Anschluss den Button "Neuen Sensor registrieren".

Ist dies geschehen öffnet sich die Sensor-Registrierung/Konfiguration. Dort könnt ihr einige Informationen über den Sensor wie beispielsweise den Standort oder den Namen angeben. Wichtig jedoch ist, dass ihr die korrekte Sensor ID angebt und das richtige Sensor Board auswählt, da die später geschickten Daten anhand dieser zugewiesen werden.

Um die ID herauszufinden, öffnet ihr TTN(https://console.thethingsnetwork.org/applications/###yourapplicationID###/devices/###yourDevice###), wandelt die Device EUI in eine Deziamalzahl um und nehmt die ersten 16 Stellen. Mit dieser könnt ihr nun euren Sensor registrieren und alle anderen Werte ausfüllen. Für das Sensorboard stellt ihr "TTN" ein.

#### TTN konfigurieren

Nun müssen wir noch Sicherstellen, dass die Daten in TTN in der richtigen Form für den Docker vorliegen. Hierfür müssen wir den [Payload anpassen](https://console.thethingsnetwork.org/applications/###yourapplicationID###/payload-formats). Wir stellen dabei das Payload Format auf Custom und fügen den folgenden Code ein.

function Decoder(bytes, port) {

  var decoded = {};
  
  decoded.pm25 = bytes[2];
  decoded.pm10 = bytes[3];
  decoded.temperature = bytes[9];
  decoded.humidity = bytes[12];
  

  return {
    pm10: decoded.pm10,
    pm25: decoded.pm25,
    temperature: decoded.temperature,
    humidity:decoded.humidity
  }
}

#### Docker starten

Stellt hierfür sicher, dass ihr Docker auf eurem System installiert hat.

Für die Ausführung des Dockers benötigt ihr die ["Application ID"](https://console.thethingsnetwork.org/applications), der Name/Zahl in der gelben Box, und den ["ACCESS KEY"](https://console.thethingsnetwork.org/applications/###yourapplicationID), hierfür ist auch der Default Key in Ordnung. Der Prefix wird hierbei auf "TTN" gesetzt.

docker run --env appID=xxx --env accessKey=xxx  --env prefix=xxx cinezaster/ttn2luftdaten_forwarder:latest
