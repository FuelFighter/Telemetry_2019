// -------------------------------------------------------------
// CANtest for Teensy 3.6 dual CAN bus
// by Collin Kidder, Based on CANTest by Pawelsky (based on CANtest by teachop)
//
// Both buses are left at default 250k speed and the second bus sends frames to the first
// to do this properly you should have the two buses linked together. This sketch
// also assumes that you need to set enable pins active. Comment out if not using
// enable pins or set them to your correct pins.
//
// This sketch tests both buses as well as interrupt driven Rx and Tx. There are only
// two Tx buffers by default so sending 5 at a time forces the interrupt driven system
// to buffer the final three and send them via interrupts. All the while all Rx frames
// are internally saved to a software buffer by the interrupt handler.
//

#include "FlexCAN.h"

#ifndef __MK66FX1M0__
#error "Teensy 3.6 with dual CAN bus is required to run this example"
#endif

#define CAN_BAUDRATE 500000                                         //CANbus in the FF car runs at 500k

static CAN_message_t msg;
static uint8_t hex[17] = "0123456789abcdef";

// -------------------------------------------------------------
static void hexDump(uint8_t dumpLen, uint8_t *bytePtr)
{
  uint8_t working;
  while ( dumpLen-- ) {
    working = *bytePtr++;
    Serial.write( hex[ working >> 4 ] );
    Serial.write( hex[ working & 15 ] );
  }
  Serial.write('\r');
  Serial.write('\n');
}

// -------------------------------------------------------------
void setup(void)
{
  delay(1000);
  Serial.println(F("Hello Teensy 3.6 CAN Test."));

  Can0.begin(CAN_BAUDRATE);
  //Can1.begin();

  //if using enable pins on a transceiver they need to be set on
  //pinMode(2, OUTPUT);
  //pinMode(35, OUTPUT);

  //digitalWrite(2, HIGH);
  //digitalWrite(35, HIGH);

  msg.ext = 0;
  msg.id = 0x100;
  msg.len = 8;
  msg.buf[0] = 101;            // decimal value
  msg.buf[1] = 101;
  msg.buf[2] = 101;
  msg.buf[3] = 101;
  msg.buf[4] = 101;
  msg.buf[5] = 101;
  msg.buf[6] = 101;
  msg.buf[7] = 101;
}


// -------------------------------------------------------------
void loop(void)
{
  Can0.write(msg);            // send 4 msgs pr. sec
  Serial.println("Sent msg");
  delay(250);
  msg.buf[0]++;

}
