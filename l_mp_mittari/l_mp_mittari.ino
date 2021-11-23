#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>

#define ONE_WIRE_BUS 2

const int rs=13, en=12, d4=8, d5=9, d6=10, d7=11;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensor(&oneWire);
double temp1 = 0; //outside
double temp2 = 0; //inside

void setup() {
  sensor.begin();
  sensor.setResolution(12);
  lcd.begin(16, 2);
  Serial.begin(9600);
}

void loop() {
  sensor.requestTemperatures();
  temp1 = sensor.getTempCByIndex(0);
  temp2 = sensor.getTempCByIndex(1);

  Serial.print("Inside: ");
  Serial.print(temp2);
  Serial.print(" C");

  Serial.print(" Outside: ");
  Serial.print(temp1);
  Serial.println(" C");

  lcd_function();

  delay(200);
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
