
# Smart--mobile <img src="https://image.flaticon.com/icons/svg/306/306905.svg?raw=true" width =60>
[![License: GPL v3](https://img.shields.io/badge/licence-GPL%20v3-yellow.svg)](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/LICENSE)
<img src="https://img.shields.io/badge/python-%3E%3D3-brightgreen.svg">
[![Build Status](https://travis-ci.org/kuj0210/IoT-Pet-Home-System.svg?branch=master)](https://travis-ci.org/kuj0210/IoT-Pet-Home-System)

for 2018 KIT Creative Design project



### Smart mobile system for my baby with naver-talk-talk messenger



## Index
* [Introduction](#introduction)
* [Features](#features)
* [Requirement](#requirement)
* [Settings & Installation](#settings--installation)
  * [Settings](#settings)
  * [Installation](#installation)
* [Pet House Structure](#pet-house-structure)
* [Motor operation structure](#motor-operation-structure)
* [Client & Server Structure](#client--server-structure)
  * [Full server structure](#full-server-structure)
  * [Client & Main server structure](#client--main-server-structure)
  * [Main server & Pi-server structure](#main-server--pi-server-structure)
* [How to use](#how-to-use)
* [How to connect motor wires](#how-to-connect-motor-wires)
  * [Food Motor](#food-motor)
  * [Water Motor](#water-motor)
  * [Door Motor](#door-motor)
* [Notes](#notes)
* [LICENSE](#license)

## **introduction** 
<img src = "https://image.flaticon.com/icons/svg/187/187614.svg" width=60 >

Parents are always with their babies while raising their children. But they don't always have to stick for 24 hours. our system will keep you company with your baby even if you stay away from me for a while, like going to the bathroom or throwing away trash in front of me.


## **Features**
 - Usage through Messenger
 - Raspberry Pi with chat-bot based System
 - Using communication with flask server
 - Using 2 flask servers.(Main Server(in aws), PiServer(in raspberryPi))
 - You can check the status of your baby by using mobile system


## **Requirement**

 - Raspnerry Pi 3 module B (used in Pi Server)
 - 3 servo-motors(for meal,water,door) and PiCamera
 - Computer or Notebook(used to chat-bot API Server)
 - Smart Phone for using chat-bot(used in client)

## **Settings & Installation**

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

## **Mobile Structure**
Preparing


## **operation structure** 
Preparing


## **Client & Server Structure**

### **Full server structure**

![](https://github.com/kuj0210/opensourceproject/blob/master/.README/Client&Server_Structure.png?raw=true)

- Client: The client represents a user using messanger application.
- Server(Main Server): This server is main of full structure. It manage chatbot and commands for controlling PiServer.
- PiServer(RaspberryPi): This server manage to control mobile


### **Client & Main server structure**

![](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Structure_client&mainserver.png?raw=true)


 Client will order various commands. (regist user, control to pet-home etc) And the main-server get this commands. Before main-server get this commands, messages go to API server and API server give the data to main-server.(data:json type) After main-server get this type's data, it'll parse this data and make operation list for ordering to PiServer. The main-server send operation list to PiServer and make reply-message for sending to user.<br>
 But if a user don't register to server or don't registered in PiServer's userlist, this user can't use this chatbot. Main-server use database for managing user-data and registed Pi-servers. Below inform main-server and pi-server structure.


### **Main server & Pi-server structure**

![](https://github.com/kuj0210/IoT-Pet-Home-System/blob/master/.README/Structure_mainserver&piserver.png?raw=true)


This structure is main-server and pi-server(in RaspberryPi using flask framework) structure. Before the Pi-server open flask server, this server send user and this device's information(registed userlist and PiKey) to main server. If this communication come into existence(communication success), the pi-server is ready to get data from main-server. The main server send operation list to pi-server by user's order. Pi-Server parse these, order to each of motor or pi-camera for implement of user's commands. And then, after implement of user's commands, pi-server send result-data to main-server. The main-server parse this data, make the appropriate reply and finally send json type data to API server. (This json data will become reply message; it is shown reply message to user.)


## **How to use**
Preparing

## **How to connect wires for sensor**
Preparing


### sensor's

- Orange wired: 
- Red wired: 
- Brown wired: 


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
 Copyright (C) 2017-present, kuj0210, KeonHeeLee, seok8418

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
