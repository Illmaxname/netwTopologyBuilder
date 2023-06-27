# Network Topology Builder
A program that builds a logical network topology based on data received via the LLDP protocol<br />
Example of input data - **devices.txt**<br />
Example of output data - **topo_base_camp.html**
## Libs
Python graphing library - Pyvis. Pandas for data parsing
## Part of the resulting image
![image](https://github.com/Illmaxname/netwTopologyBuilder/assets/81902786/1c24ab33-88d0-48a5-b362-f1d938a6fabd)

## Requirements
The tb.py program builds the network topology based on the data in the devices.txt file, it must be located in the same directory as the program itself. The topology will be displayed in the topo_base_camp.html file.<br />
The devices.txt file should contain the data retrieved from the 'show lldp neighbors' command or the abbreviated version 'sh lldp nei'.<br />
The program processes data in blocks, where the lldp neighbors call line is the beginning of the block, and the line displaying the number of displayed devices is the end of the block, but not readable data. The character '--' is used to indicate the end of the read data, it must be on a new line after the number of displayed devices.<br />
An example of two (second - last) blocks with device neighbors:<br />
N3172-474-R3-1# sh lldp nei<br />
Capability codes:<br />
   (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device<br />
   (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other<br />
Device ID Local Intf Hold-time Capability Port ID<br />
SwitchBCBA03 mgmt0 120V gi22<br />
0433.8952.c944 Eth1/1 120 0433.8952.c944<br />
0433.8952.cc38 Eth1/2 120 0433.8952.cc38<br />
SW4500X-VSS.glavapu.local Eth1/47 120 BR Te1/1/15<br />
SW4500X-VSS.glavapu.local Eth1/48 120 BR Te2/1/15<br />
LE-474-1-LIG-CEE Eth1/49 60 ethernet0/0/1<br />
LE-474-1-LIG-CEE Eth1/50 60 ethernet1/0/1<br />
N3172-474-R3-2 Eth1/53 120 BR Ethernet1/53<br />
N3172-474-R3-2 Eth1/54 120BR Ethernet1/54<br />
<br />
Total entries displayed: 9<br />
<br />
STACK-474-R3-1>sh lldp nei<br />
Capability codes:<br />
   (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device<br />
   (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other<br />
Device ID Local Intf Hold-time Capability Port ID<br />
SW4500X-VSS.glavapu. Te2/0/2 120 V,R Te2/1/11<br />
SW4500X-VSS.glavapu. Te1/0/2 120 V,R Te1/1/11<br />
...<br />
ac22.0bdb.f094 Gi1/0/43 3601 ac22.0bdb.f094<br />
9c7b.ef2c.4157 Gi1/0/3 3601 9c7b.ef2c.4157<br />
<br />
Total entries displayed: 18<br />
--<br />
<br />
In the '<device>>sh lldp nei' command itself, the device must be followed by the '>' or '#' symbol, that is, the command must be invoked from user or privileged mode.<br />
The query command is followed by 4 lines, then the list of devices received after the query without extra lines.<br />
Separating characters between columns are space characters - ' ' or tabs - '\t' (any number). It is not allowed to use a newline as a column separator, if there is such a column separator, you need to correct it with a space (s) or tabulation (s)<br />
The list of devices is followed by an empty string, then the number of displayed neighbors in the format 'some record: <number of devices>', then another empty string.<br />
One block (if it is not the last one) must be formatted this way for the program to work correctly.<br />
If the block is the last, then at the end you need to put the characters '--', indicating the end of the data.<br />
It is not allowed to leave empty (without data) all columns except 4. If 1,2,3 and/or 5 columns are empty, then the program may not work correctly or not work.<br />
The program can draw repeated links if two non-end devices are connected via interfaces/ports 'Gi<num>' or the names of the same ports differ, for example, the names 'gi1' and 'gigabit1' of the same port/interface from two different devices.<br />
