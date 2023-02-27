# AtomicThreatProfile
AtomicThreatProfile is a Python script that creates custom adversary profiles for use in Caldera using json formatted data generated from Control Validation Compass.
Caldera is a cyber security framework designed to easily run autonomous breach-and-simulation exercises, this tool provides great funtionality depending on the use case. However, when using this tool I realised that creating custom adversay profiles can be tedious and saw an oppurtuntity to enhance Caldera by automating profile creation 
underpinned by threat intelligence provided by Control Validation Compass.

# Requirements
- Linux 
- Python 3.8+
- Caldera (https://github.com/mitre/caldera)

# Installation 
`git clone https://github.com/NerdChip/AtomicThreatProfile`  
`cd AtomicThreatProfile`  
`pip3 install -r requirements.txt` 

# Usage 
Before executing Atomic threat profile you will need to retrieve data generated by Control Validation Comapass(CVC). CVC is a great resource that has a number of uses but AtomicThreatProfile only uterlises the Threat Model feature which can be used to categrise potential threats based on motive, location and industy(https://controlcompass.github.io/). This data is what will be passed to AtomicThreatProfile to produce the custom adversary profile within Caldera.

## Select Threat Group
Fill in the one or multiple critera and select a single adversary on the right hand side. For the purpose of this example i have choosen Lazarus Group. 

![image](https://user-images.githubusercontent.com/67340007/221676871-380ff4d6-dd67-4dee-acba-c11cb61f8bbd.png)

