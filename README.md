# Defending Against Denial-of-Service Attacks in Software Defined Networks

## Problem Statement
Dos and DDos attacks are becoming more common as the cloud traffic is exponentially growing and more services are put on the cloud.
In this project, investigation was carried out to identify and mitigate Dos/DDoS attacks in the SDN (Software Defined Networks) environment. 
SDN offers a new centralized control plane paradigm approach, to control the network elements dynamically – this can significantly improve efficiency and lower the cost to establish the network systems. 
Dos/DDos detection and mitigation applications were designed and written in Python to identify and also mitigate some of the important Dos/DDoS attacks.

## TCP SYN Attack mitigation
Utilizing the capabilities of SDN, an application is written in Python on the SDN controller to identify and mitigate TCP SYN attack.

The SDN POX controller Version 1.0 is used as the source development platform to create SDN based Dos mitigation application.

POX is an open source and is becoming more commonly used SDN controller development platform.

The TCP SYN attack detection and mitigation application written for this use case provides: 
* The defense when there is a malicious flow by deleting the flow.
* Black listing the source IP.
* At the same time, allows legitimate flows that do not exceed the SYN packet threshold condition.

Following is the summary of the TCP SYN mitigation application:
* The Controller instructs OVS-1 and OVS-2 to send flow statistics every 1 sec.
* After the Packet IN event messages received from OVS-1 and OVS-2, the Controller: 
* Processes the packet, creates the flow information.
* This information includes; cookie to identify the flow, source/destination mac addresses, source/destination IP addresses, Idle timer, hard timer etc.
* Controller sends the Openflow messages to OVS-1 and OVS-2 to add flow entry in their flow tables. Idle timer and Hard timer is set for the flow on these switches.
* Based on the flow statistics, Controller detects whether the flow is malicious. This is achieved on the malicious flow condition:
    * If the SYN packets/sec is < 40 of a flow, the flow is treated as normal flow
    * If the SYN packets/sec is > 40 of a flow, the flow is treated as malicious flow, the controller instructs the switch to drop the
    * packets and delete the flow.
* POX Controller application controls the Open virtual switches
    * Adds the flows
    * Allows flows that are not treated malicious
    * Delete the flows that are malicious.
    * Black lists the source IP addresses of the offender (malicious flows originator)
    * Blocks the packets originating from the black listed sources.
    * Allows packets of different flow of clients when these flows do not reach malicious threshold condition.
    * The Botnet attack detection and mitigation application sets a malicious flow threshold condition to identify Botnet attack.
    * The malicious threshold condition is set based on the number of packets (with destination http port) received per second for a particular flow.  
    * Based on the flow statistics, Controller detects whether the flow is malicious. This is achieved on the malicious flow condition:
      * If the packets/sec is < 40 of a flow and packet destination port is 8080, the flow is treated as normal flow.
      * If the packets/sec is > 40 of a flow and packet destination port is 8080, the flow is treated as malicious flow, the controller instructs the switch to drop the packets and delete the flow.



## Botnet Attack Mitigation

* Utilizing the capabilities of SDN, an application is written in Python on the SDN controller to identify and mitigate Botnet attacks.
* The SDN POX controller Version 1.0 is used as the source development platform to create SDN based Dos mitigation application.
* The Botnet attack detection and mitigation application written for this use case provides: 
   * The defense when there is a malicious flow by deleting the flow pertaining to Bots 
   * Black listing the Bots
   * At the same time,  allows legitimate flows that do not exceed the malicious threshold condition of Botnet attacks
* Two Bots (Bot-1 and Bot-2) are used to simulate Bonet attacks, these Bots are compromised hosts and are controlled by Bot-Master. 
* Http request is sent from Bot-1 and Bot-2 to Bot-Master. 
* These Bots download the malicious attack instructions file (Example, “Attack.txt”) as intended by the Bot-Master.
* This file has the following information:
   * Server IP and http port number of to victim server
   * File name to request the victim server.
   * Sting name to start the attack, for example “start attack”.
* The Bots, based on the instruction received from Bot-Master (input from the file “Attack.txt”), the Bots floods http requests to the server (victim).
* The Botnet attack detection and mitigation application on the controller reacts to the flow statistics received from the Open virtual switches and blocks the flow if the packets in the flow exceed the malicious threshold condition.
* In parallel, the Open virtual switches forward a legitimate request from the client to the server, as this flow did not exceed the malicious flow condition. 



   



