#include<LiquidCrystal.h>
#include <TimerOne.h>
LiquidCrystal lcd(2,3,4,5,6,7);

#define lm35 A0

void setup() {
  
  lcd.begin(16,4);
  lcd.print("TEMP READING");
  lcd.setCursor(0,1);
  pinMode(lm35,INPUT);
   
}

void loop() {
  
  int rs;
  float temp;
  rs= analogRead(lm35);
  temp=(rs*301)/1024;
  lcd.print(temp);
  lcd.setCursor(0,1);
  delay(500);
}
