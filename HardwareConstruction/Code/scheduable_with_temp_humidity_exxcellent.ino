/*******************************************************************************
 * Copyright (c) 2021 Florian Paul and Sassan Asnaashari
 *
 * Dieses Skript kann als Vorlage fuer jede Anwenung mit LoRaWan 
 * genutzt werden. Es kann kopiert, veraendert und weitergeleitet werden.
 * Es gibt keine Einschraenkungen aber auch keine Garantie.
 * 
 * Achtet darauf die sds011.cpp und die config.h anzupassen, damit auch 
 * alle Funktionen einwandfrei laufen.
 * 
 * Achtet auf 
 * Viel Erfolg
 * 
 * Achtet bitte auf TTN-Richtlinien zur fairer Nutzung.
 *******************************************************************************/
#include "SDS011.h"
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>
#include <dht.h>

dht DHT;
#define DHT11_PIN A2

int vcc = 13;
float pm10 = 0;
float pm25 = 0;
//
uint8_t rxPin = 3;
uint8_t txPin = 4;
SDS011 sds;

static const u1_t PROGMEM APPEUI[8]={ 0x80, 0xA3, 0x03, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };   //<- mit TTN abgleichen 
//static const u1_t PROGMEM APPEUI[8]={ 0xAD, 0x8B, 0x03, 0xD0, 0x7E, 0xD5, 0xB3, 0x70 };
void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8);}
// This should also be in little endian format, see above.
static const u1_t PROGMEM DEVEUI[8]={ 0xFD, 0x50, 0x4B, 0xCB, 0x69, 0x4E, 0xAF, 0x00 }; //<- mit TTN abgleichen
//static const u1_t PROGMEM DEVEUI[8]={  0x90, 0x78, 0x56, 0x34, 0x12, 0x41, 0x40, 0xA8 };
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8);}

static const u1_t PROGMEM APPKEY[16] ={ 0x3F, 0xB1, 0x45, 0x7B, 0x79, 0x23, 0x9F, 0x5E, 0x6D, 0x09, 0xB6, 0x3B, 0x76, 0x97, 0xBE, 0x5A };  //<- mit TTN abgleichen
//static const u1_t PROGMEM APPKEY[16] ={  0x51, 0x70, 0xAB, 0x22, 0xDE, 0x4D, 0x95, 0x77, 0x5D, 0x67, 0xC0, 0x45, 0xCC, 0x8A, 0x75, 0xFB };
void os_getDevKey (u1_t* buf) {  memcpy_P(buf, APPKEY, 16);}

static float temperature,humidity,tem,hum;
static uint8_t LPP_data[13] = {0x01,0x67,0x00,0x00,0x02,0x68,0x00,0x03,0x01,0x00,0x04,0x00,0x00};
static uint8_t opencml[4]={0x03,0x00,0x64,0xFF},closecml[5]={0x03,0x00,0x00,0xFF,0x00}; 
static unsigned int count = 1; 
static osjob_t sendjob;

static unsigned schedule_TIME = 5;

const lmic_pinmap lmic_pins = {
    .nss = 10,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = 9,
    .dio = {2, 6, 7},
};

void onEvent (ev_t ev) {
    
    Serial.print(os_getTime());
    Serial.print(": ");
    switch(ev) {
        case EV_SCAN_TIMEOUT:
            Serial.println(F("EV_SCAN_TIMEOUT"));
            break;
        case EV_BEACON_FOUND:
            Serial.println(F("EV_BEACON_FOUND"));
            break;
        case EV_BEACON_MISSED:
            Serial.println(F("EV_BEACON_MISSED"));
            break;
        case EV_BEACON_TRACKED:
            Serial.println(F("EV_BEACON_TRACKED"));
            break;
        case EV_JOINING:
            Serial.println(F("EV_JOINING"));
            break;
        case EV_JOINED:
            Serial.println(F("EV_JOINED"));
            // Disable link check validation (automatically enabled
            // during join, but not supported by TTN at this time).
            LMIC_setLinkCheckMode(0);
            break;
        case EV_RFU1:
            Serial.println(F("EV_RFU1"));
            break;
        case EV_JOIN_FAILED:
            Serial.println(F("EV_JOIN_FAILED"));
            break;
        case EV_REJOIN_FAILED:
            Serial.println(F("EV_REJOIN_FAILED"));
            break;
            break;
        case EV_TXCOMPLETE:
            Serial.println(F("EV_TXCOMPLETE (includes waiting for RX windows)"));
            if (LMIC.txrxFlags & TXRX_ACK)
              Serial.println(F("Received ack"));
           if(LMIC.dataLen>0)
            {
              int i,j=0;
              uint8_t received[4]={0x00,0x00,0x00,0x00};
               Serial.println("Received :");
              for(i=9;i<(9+LMIC.dataLen);i++)   //the received buf
              {
                Serial.print(LMIC.frame[i],HEX);
                received[j]=LMIC.frame[i];
                j++;
                Serial.print(" ");
               }
              Serial.println(); 
              Serial.println("*****************Set ScheduleTIME *******************");
              schedule_TIME = received[0] * 3600 + received[1] * 60 + received[2];
              Serial.print("schuedule time : ");
              Serial.print(schedule_TIME);
              Serial.print(" Sekunden");
              Serial.println();
            }
           
            // Schedule next transmission
            os_setTimedCallback(&sendjob, os_getTime()+sec2osticks(schedule_TIME), do_send);
            break;
        case EV_LOST_TSYNC:
            Serial.println(F("EV_LOST_TSYNC"));
            break;
        case EV_RESET:
            Serial.println(F("EV_RESET"));
            break;
        case EV_RXCOMPLETE:
            // data received in ping slot
            Serial.println(F("EV_RXCOMPLETE"));
            break;
        case EV_LINK_DEAD:
            Serial.println(F("EV_LINK_DEAD"));
            break;
        case EV_LINK_ALIVE:
            Serial.println(F("EV_LINK_ALIVE"));
            break;
         default:
            Serial.println(F("Unknown event"));
            break;
    }
}


void sdsSens()
{     
       sds.wakeup(); 
       if(schedule_TIME > 300){
          Serial.println("HEATING");
          for(int i = 0;i<20;i++){
             Serial.print("#");
             delay(3000);
          }
          Serial.println();
       }
       else{
          Serial.println("HEATING");
          for(int i = 0;i<20;i++){
             Serial.print("#");
             delay(1000);
          }
          Serial.println();  
       }
       
       sds.read(&pm25,&pm10);
       Serial.print("###########");
       Serial.print("COUNT=");
       Serial.print(count);
       Serial.println("###########");            
       Serial.println(F("The pm25 and pm10:"));
       Serial.print("[PM25:");
       Serial.print(pm25);
       Serial.print(", PM10:");
       Serial.print(pm10);
       Serial.print("");
       Serial.print("]");
       Serial.println("");
       count++;
       LPP_data[2] = uint8_t(pm25);
       LPP_data[3] = uint8_t(pm10);
       
       
       if(schedule_TIME >= 300){
          Serial.println("SLEEPING");
          sds.sleep();
       }
      
}

void dhtSens() 
{
       temperature = DHT.read11(DHT11_PIN);    //Read Tmperature data
       tem = DHT.temperature*1.0;      
       humidity = DHT.read11(DHT11_PIN);      //Read humidity data
       hum = DHT.humidity* 1.0; 
       Serial.println(F("The temperature and humidity:"));
       Serial.print("[");
       Serial.print(tem);
       Serial.print("℃,");
       Serial.print(hum);
       Serial.println("%]");
       LPP_data[9] = uint8_t(tem);
       LPP_data[12] = uint8_t(hum);
       

}

void do_send(osjob_t* j){
    // Check if there is not a current TX/RX job running
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, not sending"));
    } else {
        sdsSens();
        dhtSens();
        
        // Prepare upstream data transmission at the next possible time.
        LMIC_setTxData2(1,LPP_data, sizeof(LPP_data), 0);
        Serial.println(F("Packet queued"));
    }
    // Next TX is scheduled after TX_COMPLETE event.
}

void setup() {
    
    //while(!Serial);
    Serial.println("Connect to TTN and Send data to mydevice cayenne(Use DHT11 Sensor):");
    sds.begin(rxPin,txPin);
    Serial.begin(9600);
    
    //Reading Pins for DustSensor
    pinMode(vcc,OUTPUT);
    digitalWrite(vcc,LOW);
    #ifdef VCC_ENABLE
    // For Pinoccio Scout boards
    pinMode(VCC_ENABLE, OUTPUT);
    digitalWrite(VCC_ENABLE, HIGH);
    delay(1000);
    #endif
    // LMIC init
    os_init();
    // Reset the MAC state. Session and pending data transfers will be discarded.
    LMIC_reset();
    // Start job (sending automatically starts OTAA too)
    do_send(&sendjob);
}


void loop() {
    os_runloop_once();
}
