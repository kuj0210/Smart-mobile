
# Smart-mobile <img src="https://image.flaticon.com/icons/svg/306/306905.svg?raw=true" width =60> <img src = "https://user-images.githubusercontent.com/33398268/38657401-f795fc16-3e5a-11e8-9fb1-87eab8b4176e.png" width=63 >
[![License: GPL v3](https://img.shields.io/badge/licence-GPL%20v3-yellow.svg)](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/LICENSE)
<img src="https://img.shields.io/badge/python-%3E%3D3-brightgreen.svg">
<br/>
### Smart mobile system for my baby with naver-talk-talk messenger

## Index
* [Introduction](#introduction)
* [Features](#-features)
* [Requirement](#requirement)
* [Settings & Installation](#settings--installation)
  * [Settings](#settings)
  * [Installation](#installation)
* [Mobile-Structure](#mobile-structure)
* [Full server structure](#full-server-structure)
* [How to use](#how-to-use)
* [How to connect motor wires](#how-to-connect-motor-wires)
  * [sensor](#sensor)
* [Notes](#notes)
* [LICENSE](#license)

## <img src = "https://image.flaticon.com/icons/svg/187/187614.svg" width=60 >**introduction** 

Parents are always with their babies while raising their children. But they don't always have to stick for 24 hours. our system will keep you company with your baby even if you stay away from me for a while, like going to the bathroom or throwing away trash in front of me.


## <img src = "https://image.flaticon.com/icons/svg/321/321777.svg" width=60 > **Features**

 - Usage through Messenger
 - Raspberry Pi with chat-bot based System
 - Using communication with flask server
 - Using 2 flask servers.(Main Server(in aws), PiServer(in raspberryPi))
 - You can check the status of your baby by using mobile system


## <img src = "https://image.flaticon.com/icons/svg/715/715585.svg" width=60 > **Requirement**

 - Raspnerry Pi 3 module B (used in Pi Server)
 - 3 servo-motors(for meal,water,door) and PiCamera
 - Computer or Notebook(used to chat-bot API Server)
 - Smart Phone for using chat-bot(used in client)

## <img src = "https://image.flaticon.com/icons/svg/138/138849.svg" width=60 > **Settings & Installation**

### **Settings** 


 - Using 2 static ip address.
 - Main server is in AWS.(This server manage chat-bot API.)
 - PiServer is in RaspberryPi (This server manage RaspberryPi)
 - Using python 3.x version. Because Hangul generate error with uni-code/utf8.
 
### **Installation** 

 **1) Server side**
  - Install MySQL.
  ```
  sudo apt-get update
  sudo apt-get install mysql-server
  ```
  
  - Install python3 modules; requests, flask, pymysql 
  ```
  sudo pip3 install requests
  sudo pip3 install flask
  sudo pip3 install pymsql
  ```
   
 **2) PiServer side**
  - Install GPIO modules.
  ```
  sudo apt-get install python-dev
  sudo apt-get install python-rpi.gpio
  ```
   
  - Install flask, requests modules.
  ```
  sudo pip3 install flask
  sudo pip3 install requests
  ```

## **Mobile-Structure**
Preparing

### **Full server structure**
![](https://user-images.githubusercontent.com/33398268/41038128-3f27e2ba-69d0-11e8-88c3-03cf5e941de8.png)






## **How to use**
Preparing

## **How to connect wires for sensor**
![](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/raspberry-pi-pinout.png?raw=true)

Preparing


### **sensor**
![image](https://user-images.githubusercontent.com/24354747/40634592-ca4e7350-6330-11e8-9494-97157efaea55.png)
DHT22(Humidity and temperature sensor)
- Green wired: (BCM:22)(GPIO.3)(Physical:15)(Data)
- Red wired: (Physical:1)(3.3V)
- Black wired: (Physical:9)(GND)

PPD42NS(Dust sensor)
- Orange wired: None
- White wired: None
- Yellow wired: (BCM:23)(GPIO.4)(Physical:16)(Data)
- Red wired: (Physical:4)(5V)
- Black wired: (Physical:6)(GND)


 ## **Notes**
 
 - Installation method of Rasbian<br>
   https://www.raspberrypi.org/documentation/installation/installing-images/

 - [DB Query description (MySQL)](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Notes/DB_Query_description.md)
 
 - Apply from public IP to HTTPS
   1. [AWS EC2 setting guide](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Notes/AWS_EC2_setting.md)
   2. [Domain setting description](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Notes/Domain_setting.md)
   3. [How to use SSL Certificates and apply HTTPS](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Notes/How_to_use_SSL_Certificates_and_apply_HTTPS.md)

 ## **LICENSE**
 
Smart mobile is licensed under [the GNU GENERAL PUBLIC LICENSE v3](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/LICENSE).
 
 ```
 Copyright (C) 2018-present, Team NAC(Need a Anti Cancer) - kuj0210, HaebinKim, ras120, Kownby         
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
