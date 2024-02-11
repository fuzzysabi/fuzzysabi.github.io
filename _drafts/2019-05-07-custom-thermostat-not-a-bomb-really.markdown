---
layout: post
title: Custom thermostat (not a bomb, really)
date: '2019-05-07 02:35:00'
tags:
- hash-import-2023-01-02-19-37
---

![](/assets/images/2019/05/IMG_1829_01.png)


Back in 2015, I wanted to make a thermostat for my shop. It had to be line powered (no batteries), and switch an outlet so that I could plug in an oil radiator to keep my shop at a reasonable temperature in the winter time (even 45 degrees is quite bearable if you're moving around).

So, I got to work. Inside this mess is an arduino pro micro, two M7 hot tub temperature sensors, a custom interface board (two resistors and a connector), a stripped down usb power supply, and a relay board. Combined with the code below, it maintained a consistent temperature for several winters without any issue.

Once I moved into my new shop in May of 2017, I knew I needed a 240v heater, so I revamped my electronics to use an actual house thermostat wired into a doorbell transformer and a 24v DPDT relay. Not quite as fun, but less of a fire hazard...



    //Thermostat, by fuzzy
    //turns on/off a relay based on a preset value.
    
    
    /*
    Thermistor test sketch, will return a value between 0 and 1024.
    Uses a 10k resistor at a0/gnd, in paralell with the thermistor at a0 and 5v.
    Can play with resistor values to create a good range within the target.
       ------------10k resistor -----------------10k thermistor --------
      | | |
      gnd arduino +5V
    */
    /*
    int thermistorpin = A0; //uses pin 0 for reference pin
    
    void setup(){
            Serial.begin(9600); //output to serial console for testing
    }
    
    void loop(){
            int thermistorReading = analogRead(thermistorpin);
    Serial.println(thermistorReading);
    delay(250);//slows down output for reading
    }
    */
    
    /*
    tiny Thermostat, by fuzzy
    turns on/off a relay based on a preset value, using an attiny85
    uses two thermistors for safety, in case one goes out of calibration.
    
    */    
    // initialize pins:
    int therm1 = A0; //first thermistor, pin 1  
    int therm2 = A1;//second thermistor, pin 7
    
    int relay = A2; //size the relay to the heater you're driving, I'm using a 
    //beefcake relay from sparkfun (10A max), pin 3
    
    int heatled = 13; //indicator led, tells us when we're heating and 
    //when we have sensor issues, pin 2
    
    int settemp = 195; //set a value to heat to, this value is roughly 54deg F
    //freezing is 114, not quite boiling is 695.
    int currenttemp;
    
    void setup() 
    {                
      pinMode(therm1, INPUT); 
      pinMode(therm2, INPUT); 
      pinMode(relay, OUTPUT); 
      pinMode(heatled, OUTPUT); 
      digitalWrite(relay, LOW);
      digitalWrite(heatled, LOW);
    Serial.begin(9600); //delete the serial to shrink code once calibration is set
    }
    
    
    
    void loop() 
    {
      delay(500);//don't start right away so we can get the serial monitor running
    //read the sensors with the averaging functions, and average that
      currenttemp = (averagetemp1() + averagetemp2()) / 2 ;
      //safety loop: if temp sensors are different or unplugged, blink and turn relay off
      //first, check if unplugged; then check if shorted; 
      //next check if sensors read roughly the same(+-20). If all checks out, proceed.
     
     if (currenttemp > 500 || currenttemp < 100 || abs(averagetemp1() - averagetemp2()) >= 20)
    {//blink like hell if there's an error
      Serial.println("error");
      Serial.print("Thermistor 1: ");
      Serial.println(averagetemp1());
      Serial.print("Thermistor 2: ");
      Serial.println(averagetemp2());
      Serial.print("Current temp: ");
      Serial.println(currenttemp);
     digitalWrite(heatled, HIGH);
     delay(100);
     digitalWrite(heatled, LOW);
     digitalWrite(relay, LOW);
     delay(100);
    }
    
    //logic for thermostat
      else 
    {
      if (currenttemp < settemp)
    {
      digitalWrite(relay, HIGH);
      digitalWrite(heatled, HIGH);
    //debug code
    
     Serial.print("Heating for 5 minutes, current reading: ");
     Serial.println(currenttemp);
     Serial.print("target:");
     Serial.println(settemp);
     Serial.print("Sensor a: ");
     Serial.println(averagetemp1());
     Serial.print("Sensor b: ");
     Serial.println(averagetemp2());
     
    //delay(1000);//test
    delay(300000);//let it run a full five minutes so we don't fry the heater
    }
      else //if it's hot, do nothing for five minutes
      {
      digitalWrite(relay, LOW);
      digitalWrite(heatled, LOW);
    //debug code
    
    
     Serial.print("Target reached, testing again in 5 minutes, current reading: ");
     Serial.println(currenttemp);
     Serial.print("Sensor a: ");
     Serial.println(averagetemp1());
     Serial.print("Sensor b: ");
     Serial.println(averagetemp2());
     
    
      }
    // delay(1000);
    delay(300000);    
    }} //end main loop
    
    int averagetemp1()
    { //read the first thermistor ten times over, then average values
    int i;
    int a = 0;
    for (i=0; i < 10; i++)//do the following 10 times
    { 
            a = a + analogRead(therm1);
    delay(5);
    }
    a = a/10;
    return a;
     }
    
    int averagetemp2()
    { //read the second thermistor ten times, then average values
    int i;
    int a = 0;
    for (i=0; i < 10; i++)//do the following 10 times
    { 
            a = a + analogRead(therm2);
    delay(5);
    }
    a = a/10;
    return a;
     }

