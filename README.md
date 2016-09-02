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
* Following is the summary of the TCP SYN mitigation application:
** The Controller instructs OVS-1 and OVS-2 to send flow statistics every 1 sec.
** After the Packet IN event messages received from OVS-1 and OVS-2, the Controller: 
** Processes the packet, creates the flow information.
** This information includes; cookie to identify the flow, source/destination mac addresses, source/destination IP addresses, Idle timer, hard timer etc.
** Controller sends the Openflow messages to OVS-1 and OVS-2 to add flow entry in their flow tables. Idle timer and Hard timer is set for the flow on these switches.


