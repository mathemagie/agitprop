#include <Process.h>
#include <Bridge.h>
#include <Console.h>

int motorPin = 3;

void setup() {
  Bridge.begin();   // Initialize the Bridge
  Console.begin(); 
  pinMode(motorPin, OUTPUT);
  pinMode(13, OUTPUT);
  Serial.begin(9600);
 
}

void loop() {
  Process p;
  p.runShellCommand("/usr/bin/curl http://mathemagie.net/projects/pegman/index.php");
  Console.println("run curl command");
  
  while(p.running());  

  // Read command output. runShellCommand() should have passed "Signal: xx&":
  while (p.available()) {
    int result = p.parseInt();      // look for an integer
    Serial.println("nb boucle vibration = ");
    Serial.println(result);
    if (result >= 1) {
       for (int nbPegman = 0; nbPegman < result ; nbPegman=nbPegman + 1) {
          digitalWrite(13, HIGH);
          for (int thisPin = 100; thisPin <= 255 ; thisPin=thisPin +10 ) {
             Serial.println(thisPin);
             analogWrite(motorPin, thisPin);
              delay(100);
            
          } 
          delay(500);
          for (int thisPin = 255; thisPin >= 1 ; thisPin=thisPin - 20 ) {
             Serial.println(thisPin);
             delay(100);
             analogWrite(motorPin, thisPin);
            
          } 
           analogWrite(motorPin, 0);
           digitalWrite(13, LOW);
          
         }
    }
       
    if (result == 0) {
        analogWrite(motorPin, 1);
        digitalWrite(13, LOW);
    }
  
    
  } 
  delay(1000);  // wait 5 seconds before you do it again
}
