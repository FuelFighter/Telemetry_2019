/*
******************************************************************************************************

lora Programs for Arduino

Copyright of the author Stuart Robinson

These programs may be used free of charge for personal, recreational and educational purposes only.

This program, or parts of it, may not be used for or in connection with any commercial purpose without
the explicit permission of the author Stuart Robinson.

The programs are supplied as is, it is up to individual to decide if the programs are suitable for the
intended purpose and free from errors.

Changes:

To Do:

******************************************************************************************************
*/

//*******  Setup hardware pin definitions here ! ***************

//These are the pin definitions for one of my own boards, be sure to change them to match
//your own setup

#define NSS 10
#define RFBUSY A1
#define NRESET 9
#define LED1 8
#define DIO1 2
#define DIO2 -1                 //not used 
#define DIO3 -1                 //not used                      
#define BUZZER A0               //connect a buzzer here if wanted



#define SX1280_TXBUFF_SIZE 32
#define SX1280_RXBUFF_SIZE 32


//*******  Setup Test Parameters Here ! ***************

//LoRa Modem Parameters
const uint32_t  Frequency = 2445000000;          //frequency of transmissions
const int32_t Offset = 0;                        //offset frequency for calibration purposes  

#define Bandwidth LORA_BW_0400                   //LoRa bandwidth
#define SpreadingFactor LORA_SF10                //LoRa spreading factor
#define CodeRate LORA_CR_4_8                     //LoRa coding rate
#define RangingTXPower 0                         //Transmit power used 
#define TXaddress 16                             //must match address in recever

uint16_t const CalibrationStart = 9600;          //calibration value for ranging, SF10, BW400      
uint16_t const CalibrationEnd = 12000;           //calibration value for ranging, SF10, BW400

#define waittimemS 5000                          //wait this long in mS for packet before assuming timeout
#define rangingTXTimeoutmS 10000                 //ranging TX timeout in mS
#define range_count 5
#define range_result_count 4                     //number of ranging results required   
const bool reset_device = true;                  //enable device reset between ranging requests.    

const uint16_t packet_delaymS = 250;             //mS delay between packets, minimum 130mS for BW400, SF10 ranging packets

const float adjustment_correction = 0.8967;      //adjustment to calculated distance   

