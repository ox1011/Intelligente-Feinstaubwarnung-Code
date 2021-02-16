# KI-Konzept

![KI-Konzept](Images/container_architecture-4.png)

<br>


## Klassifikation der Daten in Stadt oder Land/Dorf mit OpenStreetMap

  - [OpenStreetMap](https://www.openstreetmap.org/#map=19/48.55600/12.20001) - OpenSource
    - bietet viele Informationen zur Umgebung an - [Unterschiedliche Tags](https://wiki.openstreetmap.org/wiki/DE:Map_Features)
      - Beispiel 1 [Bushaltestelle HAW Landshut](https://www.openstreetmap.org/node/3998740083#map=18/48.55615/12.19940)
      - Beispiel 2 [Autobahnkreuz A92 Wörth an der Isar](https://www.openstreetmap.org/node/595349#map=19/48.62921/12.32553)

- Klassifikation mit OpenStreetMap und [Suchmaschine Nominatim](https://github.com/osm-search/Nominatim) (ebenfalls OpenSource)
  - [API von der Suchmaschine](https://nominatim.org/release-docs/develop/api/Reverse/)
  - Exemplarischer Aufruf (LATITUDE und LONGITUDE durch die Werte aus der Datenbank ersetzen): `https://nominatim.openstreetmap.org/reverse?format=geojson&lat=LATITUDE&lon=LONGITUDE`
  - 4 Beispieldatensätze aus der Luftdaten.info Datenbank
    - [Straße an und in Wohngebieten in Sofia - Stadt in Bulgarien](https://nominatim.openstreetmap.org/reverse?format=geojson&lat=42.632&lon=23.408)
    - [Haus in Amsterdam](https://nominatim.openstreetmap.org/reverse?format=geojson&lat=52.354&lon=4.924)
    - [Undefinierttes Gebäude in Regensburg](https://nominatim.openstreetmap.org/reverse?format=geojson&lat=49.01&lon=12.034)
    - [Gut ausgebaute Landsstraße in Berchères-les-Pierres - Ort in Frankreich](https://nominatim.openstreetmap.org/reverse?format=geojson&lat=48.384&lon=1.55)

<br>

Output vom letzten Beispiel:
```json
{
   "type":"FeatureCollection",
   "licence":"Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
   "features":[
      {
         "type":"Feature",
         "properties":{
            "place_id":176580060,
            "osm_type":"way",
            "osm_id":366069659,
            "place_rank":26,
            "category":"highway",
            "type":"secondary",
            "importance":0.09999999999999998,
            "addresstype":"road",
            "name":"Rue de la Mairie",
            "display_name":"Rue de la Mairie, Berchères-les-Pierres, Chartres, Eure-et-Loir, Zentrum-Loiretal, Metropolitanes Frankreich, 28630, Frankreich",
            "address":{
               "road":"Rue de la Mairie", 
               "village":"Berchères-les-Pierres",
               "municipality":"Chartres",
               "county":"Eure-et-Loir",
               "state":"Zentrum-Loiretal",
               "country":"Frankreich",
               "postcode":"28630",
               "country_code":"fr"
            }
         },
         "bbox":[
            1.5464086,
            48.3805796,
            1.5532592,
            48.3859995
         ],
         "geometry":{
            "type":"Point",
            "coordinates":[
               1.549994117832127,
               48.384009119795586
            ]
         }
      }
   ]
}
```

Anhand des ``` "category":"highway" ``` und ``` "type":"secondary"``` kommt man auf die Information "gut ausgebaute Landstraße" (Hilfreich ist die Tags-Liste). Das es ein Ort (und entsprechender Ortsname) ist kann man am Tag ```"village":"Berchères-les-Pierres"``` ablesen. Bei einer Stadt z.B Sofia sieht der Tag so aus: ```"city":"Sofia"```.

