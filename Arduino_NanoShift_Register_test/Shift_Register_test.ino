int clk = 5;
int data = 6;
int strobe = 4;
int oe = 3;

int clk_speed = 1;

int index = 0;

int brightness = 0;
int btime = 20000;

int data_written[] = {1, 0, 1, 0, 1, 0, 1, 0};

char keystroke;
void setup() {

  pinMode(clk, OUTPUT);
  pinMode(data, OUTPUT);
  pinMode(strobe, OUTPUT);
  pinMode(oe, OUTPUT);
  Serial.begin(9600);
  Serial.print("start");

}

void loop()

{
  // set values
  if (brightness < btime){
      if (brightness % (btime - brightness)/20 == 0){
        digitalWrite(oe, HIGH);
      }
      else {
        digitalWrite(oe, LOW);
      }
      brightness = brightness + 1;
  }
  else {
    brightness = 0;
    Serial.print("brightness done ");
  }

    if (data_written[index] == 1) {
      digitalWrite(data, HIGH);
    }
    else {
      digitalWrite(data, LOW);
    }
  index = index + 1;
  if (index == 8) {
    index = 0;
    digitalWrite(strobe, HIGH);
  }


  //if (Serial.available() > 0){      //user input to test strobe
  //  keystroke = Serial.read();
  //  if (keystroke == '1'){
  //    digitalWrite(strobe,HIGH);
  //  }
  //  else if (keystroke == '0') {
  //    digitalWrite(strobe,LOW);
  //  }
  //  Serial.print(keystroke);
  //}
  digitalWrite(strobe, LOW);
  delay(clk_speed / 3);
  digitalWrite(clk, HIGH);
  delay(clk_speed / 3);
  digitalWrite(clk, LOW);
}