//Settings.h


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

#define NSS 9
#define RFBUSY -1
#define NRESET 24
#define LED1 -1
#define DIO1 -1
#define DIO2 -1                 //not used 
#define DIO3 -1                 //not used                      
#define BUZZER A0               //connect a buzzer here if wanted                  


//*******  Setup FLRC Test Parameters Here ! ***************

//FLRC Modem Parameters
#define Frequency 2445000000                     //frequency of transmissions
#define Offset 0                                 //offset frequency for calibration purposes  

#define BandwidthBitRate FLRC_BR_1_300_BW_1_2    //FLRC bandwidth and bit rate, 1.3Mbs               
#define CodingRate FLRC_CR_1_2                   //FLRC coding rate
#define BT RADIO_MOD_SHAPING_BT_1_0              //FLRC BT
#define Sample_Syncword 0x01234567               //FLRC uses syncword

#define PowerTX  1                               //power for transmissions in dBm

#define packet_delay 1000                        //mS delay between packets

#define TXBUFFER_SIZE 16                         //default TX buffer size  
#define RXBUFFER_SIZE 16                         //default RX buffer size  

 
