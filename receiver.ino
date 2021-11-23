#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";
boolean button_state = 0;
int led_pin = 3;

void setup()
{
    Serial.begin(9600);
    radio.begin();
    radio.openReadingPipe(0, address);   //Setting the address at which we will receive the data
    radio.setPALevel(RF24_PA_MIN);       //You can set this as minimum or maximum depending on the distance between the transmitter and receiver.
    radio.startListening();              //This sets the module as receiver
}

void loop()
{
    float temperature = read_temperature_data();
    if (temperature == NAN)
    {
        return;
    }
    
    delay(5);
}

float read_temperature_data()
{
    if (!radio.available())
    {
        return NAN;
    }

    float temperature;
    radio.read(&temperature, sizeof(temperature));
    return temperature;
}

void send_data_to_rpi(float temperature)
{
    
}
