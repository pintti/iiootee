#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include <LowPower.h>

#define ONE_WIRE_BUS 5

//91:EB:E9:EC:B6:01

const int rs=13, en=12, d4=8, d5=9, d6=10, d7=11;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

long tenMin = 600000;
enum state {
  SEND,
  SLEEP
};
enum state mchState;

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensor(&oneWire);
SoftwareSerial bluetooth(2, 3);
double temp1 = 0; //outside
double temp2 = 0; //inside
int idleTimeSeconds = 600;

void setup() {
  sensor.begin();
  sensor.setResolution(12);
  lcd.begin(16, 2);
  bluetooth.begin(9600);
  mchState=SEND;
  
  Serial.begin(9600);
  Serial.println("Bluetooth on!");
}

void loop() {
  sensor.requestTemperatures();
  temp1 = sensor.getTempCByIndex(0);
  temp2 = sensor.getTempCByIndex(1);

  //serial_function();
  if (mchState==SEND){
    send_bluetooth();
    if (read_bluetooth()){
      mchState=SLEEP;
    }
  }
  
  lcd_function();

  if (mchState==SLEEP){
    idle(idleTimeSeconds);
    Serial.println("Returning from idle. Sending temperature data.");
    mchState=SEND;
  }

  delay(200);
}


void idle(int seconds)
{
  char buffer[50];
  sprintf(buffer, "Idling for %d seconds.", seconds);
  Serial.println(buffer);

  period_t sleepTime = SLEEP_8S;
  int cycleTime = 8;
  if (seconds % 8 != 0)
  {
    sleepTime = SLEEP_1S;
    cycleTime = 1;
  }

  int elapsed = 0;
  while (elapsed <= seconds)
  {
    LowPower.idle(sleepTime, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, 
                  USART0_OFF, TWI_OFF);

    elapsed += cycleTime;
    // TODO: Check if temperatures should be coming soon
  }
}


void lcd_function(){
  lcd.clear();
  
  lcd.setCursor(0, 0);
  lcd.print("Sis");
  lcd.print((char)225);
  lcd.print(": ");
  lcd.print(temp2);
  lcd.print((char)223);
  lcd.print("C");

  lcd.setCursor(0, 1);
  lcd.print("Ulko: ");
  lcd.print(temp1);
  lcd.print((char)223);
  lcd.print("C");
}


void send_bluetooth(){
  //bluetooth.print("");
  bluetooth.print(temp2);
  bluetooth.print(",");
  bluetooth.print(temp1);
  bluetooth.println();
  Serial.println("Sent data");
}


bool read_bluetooth(){
  unsigned long start = millis();
  Serial.println("Waiting for ACK");
  while(millis()-start<10000){
    if (bluetooth.available()){
      int ack = bluetooth.read();
      Serial.println(ack);
      if (ack==1){
        Serial.println("ACKnowledged");
        bluetooth.print(1);
        bluetooth.println();
        return true;
      }
    }
  }
  Serial.println("ACK failed");
  return false;
}


void serial_function(){
  Serial.print("Sisä: ");
  Serial.print(temp2);
  Serial.print(" C");

  Serial.print(" Sisä: ");
  Serial.print(temp1);
  Serial.println(" C");
}
