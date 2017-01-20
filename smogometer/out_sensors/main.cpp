#include <DHT.h>
#include <Wire.h>
#include <WireData.h>

#define MYI2C_ADDR 0x08

#define COV_RATIO 0.2        // ug/mmm/mv
#define NO_DUST_VOLTAGE 400  // mv
#define SYS_VOLTAGE 5000           

#define DHTPIN 2
#define DHTTYPE DHT11

#define ILED_PIN 7 
#define AOUT_PIN 0

DHT dht(DHTPIN, DHTTYPE);

float voltage, hum, temp, dust;
int adcvalue;

int Filter(int m) {
  static int flag_first=0;
  static int _buff[10];
  static int sum;
  const  int _buff_max = 10;
  int i;
  
  if(flag_first == 0) {
    flag_first = 1;
    for(i=0, sum=0; i<_buff_max; i++) {
      _buff[i]=m;
      sum+=_buff[i];
    }
    return m;
  } else {
    sum-=_buff[0];
    for(i=0; i<(_buff_max-1); i++) _buff[i] =_buff[i+1];
    _buff[9] = m;
    sum+=_buff[9];
    i=sum/10.0;
    return i;
  }
}

void i2cRequest() {
  wireWriteData(temp);
  wireWriteData(hum);
  wireWriteData(dust);
}

void setup(void) {
  pinMode(ILED_PIN, OUTPUT);
  digitalWrite(ILED_PIN, LOW);
  dht.begin();
  Wire.begin(MYI2C_ADDR);
  Wire.onRequest(i2cRequest);
}


void loop(void) {
  digitalWrite(ILED_PIN, HIGH);
  delayMicroseconds(280);
  adcvalue = analogRead(AOUT_PIN);
  digitalWrite(ILED_PIN, LOW);
  
  adcvalue = Filter(adcvalue);
  voltage = (SYS_VOLTAGE/1024.0)*adcvalue*11;
  
  if(voltage >= NO_DUST_VOLTAGE) {
    voltage -= NO_DUST_VOLTAGE;
    dust = voltage * COV_RATIO;
  } else dust = 0.0;
  
  delay(2000);
  hum = dht.readHumidity();
  temp = dht.readTemperature();
  if (isnan(hum) || isnan(temp)) {
    hum = 0.0;
    temp = 0.0;
  }
}
