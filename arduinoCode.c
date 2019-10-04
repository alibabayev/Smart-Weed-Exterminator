#include <Servo.h>
int val[] = {0,0,0,0,0,0};

int times[] = {0,0,0,0,0,0};

int turnDelay = 1000;
int contTurnDelay = 2000;
//char uselessChar = '';

//Servo servo0;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
//Servo servo5;
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(50);

  pinMode(13, OUTPUT);

  //servo0.attach(3);
  servo1.attach(5);
  servo2.attach(6);
  servo3.attach(9);
  servo4.attach(10);
  //servo5.attach(11);

  //servo0.write(90);
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  //servo5.write(90);
}

void loop(){
  if (Serial.available() > 0) {
    //Serial.println("IF GIRDI");
    for(int i = 0; i < 3;i++){
      //Serial.print(i);
      //Serial.println(". FOR GIRDI");
      for(int k = 5; k >= 0; k--){
        val[k] = Serial.parseInt();
        //if(k == 5 || k == 0) {
        //  val[k] = 0;
        //}
      }
      /*for(int m = 0; m <= 5; m++){
        Serial.print(val[m]);
        Serial.print(" ");
      }*/
      //Serial.println();
      /*for(int count = 5; count >= 0; count--){
        
        //inString = Serial.readStringUntil(' ');
        int intTemp = Serial.read();
        inString = (char)intTemp;
        val[count] = inString.toInt();
        Serial.print(count);
        Serial.print(". val is ");
        Serial.print(val[count]);
        Serial.println();
        myChar = Serial.read();
      }*/
      //2 2 2 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 
      //2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
      //2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2
      
    //}

      //CONTINUOUS ROTATION SERVO
      /*if(val[0] == 2){
        Serial.println("Opened 0");
        times[0] = millis();
        servo0.write(0);
        //Serial.println(millis());
        digitalWrite(13, HIGH);
        val[0] = 0;
      }*/
      
      if(val[1] == 2){
        //Serial.println("Opened 1");
        times[1] = millis();
        servo1.write(90);
        //Serial.println(millis());
        digitalWrite(13, HIGH);
        val[1] = 0;
      }
    
  
      if(val[2] == 2){
        ////Serial.println("Opened 2");
        times[2] = millis();
        servo2.write(90);
        ////Serial.println(millis());
        digitalWrite(13, HIGH);
        val[2] = 0;
      }
      
      if(val[3] == 2){
        //Serial.println("Opened 3");
        times[3] = millis();
        servo3.write(90);
        ////Serial.println(millis());
        digitalWrite(13, HIGH);
        val[3] = 0;
      }
      
      if(val[4] == 2){
        //Serial.println("Opened 4");
        times[4] = millis();
        servo4.write(90);
        ////Serial.println(millis());
        digitalWrite(13, HIGH);
        val[4] = 0;
      }

      /*//CONTINUOUS ROTATION SERVO
      if(val[5] == 2){
        Serial.println("Opened 5");
        times[5] = millis();
        servo5.write(0);
        //Serial.println(millis());
        digitalWrite(13, HIGH);
        val[5] = 0;
      }*/
      
      delay(1000);
  
      //CONTINUOUS ROTATION SERVO
      /*if(times[0] != 0 ){//&& millis() - times[0] >= contTurnDelay){
        Serial.println("Closed 0");
        servo0.write(90);
        times[0] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }*/
      
      if(times[1] != 0 ){//&& millis() - times[1] >= turnDelay){
        //Serial.println("Closed 1");
        servo1.write(0);
        times[1] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }
      if(times[2] != 0 ){//&& millis() - times[2] >= turnDelay){
        //Serial.println("Closed 2");
        servo2.write(0);
        times[2] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }
      if(times[3] != 0 ){//&& millis() - times[3] >= turnDelay){
        //Serial.println("Closed 3");
        servo3.write(0);
        times[3] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }

      if(times[4] != 0 ){//&& millis() - times[4] >= turnDelay){
        //Serial.println("Closed 4");
        servo4.write(0);
        times[4] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }
  
      //CONTINUOUS ROTATION SERVO
      /*if(times[5] != 0 ){//&& millis() - times[4] >= contTurnDelay){
        Serial.println("Closed 5");
        servo5.write(90);
        times[5] = 0;
        //Serial.println(millis());
        digitalWrite(13, LOW);
      }*/
      
      
    //delay(1636);
    delay(350);
    //Serial.print(i);
    //Serial.println(". FOR CIXDI\n");
    }//end of for
    int availables = Serial.available();
    for(int a = 0; a < availables; a++){
      char uselessChar = Serial.read();
    }
    //Serial.println("IF CIXDI\n");
  }
}
