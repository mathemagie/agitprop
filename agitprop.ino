#include <Process.h>
#include <Bridge.h>
#include <Console.h>

int motorPin = 3;

void setup() {
  Bridge.begin();   // Initialize the Bridge
  Console.begin(); 
  pinMode(motorPin, OUTPUT);
 
}

void loop() {
  Process p;
  p.runShellCommand("/usr/bin/curl http://mathemagie.net/projects/pegman/index.php");
  Console.println("run curl command");
  
  while(p.running());  

  // Read command output. runShellCommand() should have passed "Signal: xx&":
  while (p.available()) {
    int result = p.parseInt();          // look for an integer
    if (result == 1) {
       analogWrite(motorPin, 255);
    
    }
       
    if (result == 0) {
        analogWrite(motorPin, 1);
    }
  
    
  } 
  delay(1000);  // wait 5 seconds before you do it again
}
