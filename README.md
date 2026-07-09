# S1lent DDoS Tool – Multi‑Layer Stress Tester

![made by S1lent](https://img.shields.io/badge/made%20by-S1lent-red)
![discord](https://img.shields.io/badge/Discord-s1lent0x1-blue)

A highly advanced, multi‑protocol DDoS simulation framework for security testing and network stress analysis.  
Supports all OSI layers (3, 4, 7) plus amplification vectors and multi‑vector starvation attacks.

## Disclaimer
**This tool is intended for educational and authorized stress‑testing only.**  
The author assumes no liability for any misuse or damage caused.

## Features
- Layer 3: SYN, ACK, ICMP, IP fragment, Smurf, LAND
- Layer 4: UDP, TCP connect, RST, Xmas, FIN, NULL
- Layer 7: HTTP GET/POST, Slowloris, Slow Read, XML‑RPC, Joomla brute
- Amplification: DNS, NTP, SSDP, Memcached, CharGen, SNMP
- SSL/TLS handshake flood & renegotiation
- Proxy support for Layer 7
- Multi‑vector combined attack (starvation)
- Raw socket engine with custom IP/TCP/ICMP crafting

## Installation
```bash
git clone https://github.com/Cyberthreatalliance-cta/S1lent-ddos
cd DDoS-Tool
pip install -r requirements.txt




## Usage
```Usage
text
python ddos.py -t <target IP/domain> -p <port> -f <flood> -th <threads> -d <seconds>
Examples:

SYN flood on port 80:
python ddos.py -t 192.168.1.100 -p 80 -f syn -l 3 -th 1000 -d 120

UDP flood on port 53:
python ddos.py -t 192.168.1.100 -p 53 -f udp -l 4 -th 500

HTTP GET flood with proxies:
python ddos.py -t http://example.com -f httpget -l 7 --proxy-file proxies.txt

Slowloris:
python ddos.py -t http://example.com -f slowloris -l 7

DNS amplification (spoofed):
python ddos.py -t victim.com -p 53 --amp dns --spoof-ip 1.2.3.4

Multi‑vector starvation:
python ddos.py -t 192.168.1.100 --multi

Command Line Arguments
Flag	Description	Default
-t	Target IP/domain (required)	
-p	Port	80
-th	Number of threads	500
-d	Duration in seconds	60
-f	Attack type (syn, udp, httpget, slowloris, etc.)	syn
-l	Layer (3,4,7)	4
--amp	Amplification vector (dns, ntp, ssdp, …)	
--spoof-ip	Spoofed source IP (amplification)	
--proxy-file	File with proxies (L7)	
--multi	Multi‑vector starvation mode	
Supported Attack Vectors
Layer 3: syn, ack, icmp, ipfrag, smurf, land
Layer 4: udp, tcpconnect, rst, xmas, fin, null
Layer 7: httpget, httppost, slowloris, slowread, httphead, httpoptions, xmlrpc, joomla
Amplification: dns, ntp, ssdp, memcached, chargen, snmp
SSL/TLS: sslhandshake, tlsreneg
Multi: --multi

Contributing
Pull requests are welcome. For major changes, please open an issue first.

License
CC0 1.0 Universal – No rights reserved.

Contact
Discord: s1lent0x1

Warning: This tool generates massive traffic. Use only on systems you own or have explicit permission to test.```
