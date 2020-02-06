/*
******************************************************************************************************

 lora Programs for Arduino

  Copyright of the author Stuart Robinson 24/10/19

  These programs may be used free of charge for personal, recreational and educational purposes only.

  This program, or parts of it, may not be used for or in connection with any commercial purpose without
  the explicit permission of the author Stuart Robinson.

  The programs are supplied as is, it is up to individual to decide if the programs are suitable for the
  intended purpose and free from errors.

  Changes:

  To Do:

******************************************************************************************************
*/

/*
******************************************************************************************************

  Program Operation

  This program tranmits a text meassage using the LoRa settings in the 'Settings.h' file. Use the
  companion program simple_RX to display the packets on another node.


******************************************************************************************************
*/

#define programversion "V1.0"
#define Serial_Monitor_Baud 115200

#include <SPI.h>
#include "Settings.h"
#include "SX1280LT.h"

SX1280Class SX1280LT;

boolean SendOK;
int8_t TXPower = 1;
uint8_t TXPacketL;
float temp;


void loop()
{
  digitalWrite(LED1, HIGH);
  Serial.print(TXPower);
  Serial.print(F("dBm "));
  Serial.print(F("TestPacket> "));
  Serial.flush();

  if (Send_Test_Packet())
  {
    //Serial.println(F("Send_Test_Packet"));
    packet_is_OK();
  }
  else
  {
    //Serial.println(F("packet_is_error()"));
    packet_is_Error();
  }
  Serial.println();
  delay(packet_delay);
}


void packet_is_OK()
{
  Serial.print(F(" "));
  Serial.print(TXPacketL);
  Serial.print(F(" Bytes SentOK"));
}


void packet_is_Error()
{
  Serial.print("Packet_is_error");
  uint16_t IRQStatus;
  IRQStatus = SX1280LT.readIrqStatus();          //get the IRQ status
  Serial.print(F("SendError,"));
  Serial.print(F("Length,"));
  Serial.print(TXPacketL);
  Serial.print(F(",IRQreg,"));
  Serial.print(IRQStatus, HEX);
  SX1280LT.printIrqStatus();
  digitalWrite(LED1, LOW);                       //this leaves the LED on slightly longer for a packet error
}


bool Send_Test_Packet()
{
  uint8_t buffersize;
  uint8_t buff[] = "Hello World!";
  buff[12] = '#';                                //replace last null character in buffer
  
  if (sizeof(buff) > TXBUFFER_SIZE)              //check that defined buffer is not larger than TX_BUFFER
  {
    Serial.println("104");
    buffersize = TXBUFFER_SIZE;
  }
  else
  {
    Serial.println("109");
    buffersize = sizeof(buff);
  }

  TXPacketL = buffersize;
  Serial.println("114");
  SX1280LT.printASCIIPacket(buff, buffersize);

  digitalWrite(LED1, HIGH);

  if (SX1280LT.sendPacketLoRa(buff, buffersize, 10000, TXPower, DIO1))
  {
    Serial.println("121");
    digitalWrite(LED1, LOW);
    return true;
  }
  else
  {
    Serial.println("127");
    return false;
  }
}


void led_Flash(uint16_t flashes, uint16_t delaymS)
{
  unsigned int index;
  for (index = 1; index <= flashes; index++)
  {
    digitalWrite(LED1, HIGH);
    delay(delaymS);
    digitalWrite(LED1, LOW);
    delay(delaymS);
  }
}


void setup()
{
  pinMode(LED1, OUTPUT);
  led_Flash(2, 125);

  Serial.begin(Serial_Monitor_Baud);
  Serial.println();
  Serial.print(__TIME__);
  Serial.print(F(" "));
  Serial.println(__DATE__);
  Serial.println(F(programversion));
  Serial.println();

  Serial.println(F("3_X1280LT_LoRa_Simple_TX Starting"));

  SPI.begin();
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE0));

  digitalWrite(LED1, HIGH);
  while(!SX1280LT.begin(NSS, NRESET, RFBUSY, DIO1, DIO2, DIO3)) {
    Serial.println(F("Device not found!"));
    delay(1);
  }
  digitalWrite(LED1, LOW);
  Serial.println(F("WE IN BITCHES!!!"));
  
  /*
  if (SX1280LT.begin(NSS, NRESET, RFBUSY, DIO1, DIO2, DIO3))
  {
    Serial.println(F("Device found"));
    led_Flash(2, 125);
    delay(1000);
  }
  else
  {
    Serial.println(F("No device responding"));
    while (1)
    {
      led_Flash(50, 50);            //long fast speed flash indicates device error
    }
  }

  */
  SX1280LT.setupLoRaTX(Frequency, Offset, SpreadingFactor, Bandwidth, CodeRate);

  Serial.print(F("Transmitter ready - TXBUFFER_SIZE "));
  Serial.println(TXBUFFER_SIZE);
  Serial.println();
}
