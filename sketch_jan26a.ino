// Моторы подключаются к клеммам M1+,M1-,M2+,M2-  
// Motor shield использует четыре контакта 6,5,7,4 для управления моторами 
 
#define SPEED_LEFT      6
#define SPEED_RIGHT     5 
#define DIR_LEFT        7
#define DIR_RIGHT       4

#define GO_F_PIN   8
#define GO_B_PIN   9
#define GO_L_PIN   10
#define GO_R_PIN   11

 
void go(int speed, bool reverseLeft, bool reverseRight, int duration)
{
    // Для регулировки скорости `speed` может принимать значения от 0 до 255,
    // чем болше, тем быстрее. 
    analogWrite(SPEED_LEFT, speed);
    analogWrite(SPEED_RIGHT, speed);
    digitalWrite(DIR_LEFT, reverseLeft ? LOW : HIGH); 
    digitalWrite(DIR_RIGHT, reverseRight ? LOW : HIGH) ; 
    delay(duration); 
}
 
void setup() 
{
    // Настраивает выводы платы 4,5,6,7 на вывод сигналов 
    for(int i = 4; i <= 7; i++)     
        pinMode(i, OUTPUT);  

    pinMode(GO_F_PIN, INPUT);
    pinMode(GO_B_PIN, INPUT);
    pinMode(GO_L_PIN, INPUT);
    pinMode(GO_R_PIN, INPUT);
        
    Serial.begin(9600);
    Serial.println("START");
} 
 
void loop() 
{ 
  delay(3000);
  int delayAvoidBounce = 10;
  
  while (true) {
    boolean shouldGoF = digitalRead(GO_F_PIN);
    boolean shouldGoB = digitalRead(GO_B_PIN);
    boolean shouldGoL = digitalRead(GO_L_PIN);
    boolean shouldGoR = digitalRead(GO_R_PIN);
    
    if (shouldGoF) {
      delay(delayAvoidBounce);
      shouldGoF = digitalRead(GO_F_PIN);
      if (shouldGoF) {
        Serial.println("shouldGoF");
        go(150, false, false, 50);
        go(0, false, false, 0);
      }
    }
    
    if (shouldGoB) {
      delay(delayAvoidBounce);
      shouldGoB = digitalRead(GO_B_PIN);
      if (shouldGoB) {
        Serial.println("shouldGoB");
        go(150, true, true, 50);
        go(0, false, false, 0);
      }
    }
    
    if (shouldGoL) {
      delay(delayAvoidBounce);
      shouldGoL = digitalRead(GO_L_PIN);
      if (shouldGoL) {
        Serial.println("shouldGoL");
        go(150, true, false, 50);
        go(0, false, false, 0);
      }
    }
    
    if (shouldGoR) {
      delay(delayAvoidBounce);
      shouldGoR = digitalRead(GO_R_PIN);
      if (shouldGoR) {
        Serial.println("shouldGoR");
        go(150, false, true, 50);
        go(0, false, false, 0);
      }
    }
  
    go(0, false, false, 0);
  }
  
  go(0, false, false, 0);
}
