#include <SPI.h>
#include "RF24/nRF24L01.h"
#include "RF24/RF24.h"

RF24 radio(9, 10); // CE, CSN         
const byte address[6] = "00001";     //Byte of array representing the address. This is the address where we will send the data. This should be same on the receiving side.
int indoorSensorPin = 0;
int outdoorSensorPin = 1;

void setup()
{
    radio.begin();                  // Starting the Wireless communication
    radio.openWritingPipe(address); // Setting the address where we will send the data
    radio.setPALevel(RF24_PA_MIN);  // You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
    radio.stopListening();          // This sets the module as transmitter
}

void loop()
{
    float temperature = read_indoors_temperature();
    if (temperature != NAN)
    {
        send_temperature_data(temperature);
    }
    delay(1000);
}

float read_indoors_temperature()
{
    // Read temperature from arduino
    return 32;
}

float read_outdoors_temperature()
{
    // Read temperature from arduino
    return 64;
}

/**
 * @brief Send temperature data to receiver.
 * 
 * @param temperature Temperature in celsius.
 */
void send_temperature_data(float temperature)
{
    bool success = radio.write(&temperature, sizeof(temperature));
    if (success)
    {
        Serial.println("Transmitted temperature to receiver.");
    }
    else
    {
        Serial.print("Failed to transmit temperature: ");
        Serial.println(temperature);
    }
}
