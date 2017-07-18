# Intelligence Gathering
## Fierce
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/davidpepper/fierce-domain-scanner

Fierce is a semi-lightweight scanner that helps locate non-contiguous IP space and hostnames against specified domains. It's really meant as a pre-cursor to nmap, unicornscan, nessus, nikto, etc, since all of those require that you already know what IP space you are looking for. This does not perform exploitation and does not scan the whole internet indiscriminately. It is meant specifically to locate likely targets both inside and outside a corporate network. Because it uses DNS primarily you will often find mis-configured networks that leak internal address space. That's especially useful in targeted malware.

# Vulnerability Analysis
## Kismet
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://www.kismetwireless.net/index.shtml

Kismet is a wireless network detector, sniffer, and intrusion detection system. Kismet works predominately with Wi-Fi (IEEE 802.11) networks, but can be expanded via plug-ins to handle other network types.

## onesixtyone
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/trailofbits/onesixtyone

The approach taken by most SNMP scanners is to send the request, wait for n seconds and assume that the community string is invalid. If only 1 of every hundred scanned IP addresses responds to the SNMP request, the scanner will spend 99*n seconds waiting for replies that will never come. This makes traditional SNMP scanners very inefficient.

onesixtyone takes a different approach to SNMP scanning. It takes advantage of the fact that SNMP is a connectionless protocol and sends all SNMP requests as fast as it can. Then the scanner waits for responses to come back and logs them, in a fashion similar to Nmap ping sweeps.

## sslscan
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/rbsec/sslscan.git

sslscan tests SSL/TLS enabled services to discover supported cipher suites

# Post Exploitation
## CrackMapExec
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/byt3bl33d3r/CrackMapExec

CrackMapExec (a.k.a CME) is a post-exploitation tool that helps automate assessing the security of large Active Directory networks. Built with stealth in mind, CME follows the concept of 'Living off the Land': abusing built-in Active Directory features/protocols to achieve it's functionality and allowing it to evade most endpoint protection/IDS/IPS solutions.

## Empire
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** http://www.powershellempire.com/

Empire is a pure PowerShell post-exploitation agent built on cryptologically-secure communications and a flexible architecture. Empire implements the ability to run PowerShell agents without needing powershell.exe, rapidly deployable post-exploitation modules ranging from key loggers to Mimikatz, and adaptable communications to evade network detection, all wrapped up in a usability-focused framework.

# Exploitation
## hashID
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/psypanda/hashID

hashID is a tool written in Python 3 which supports the identification of over 220 unique hash types using regular expressions.

## Medusa
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** http://foofus.net/goons/jmk/medusa/medusa.html

Medusa is intended to be a speedy, massively parallel, modular, login brute-forcer. The goal is to support as m any services which allow remote authentication as possible. The author considers following items as some of the key features of this application:

* Thread-based parallel testing. Brute-force testing can be performed against multiple hosts, users or passwords concurrently.
* Flexible user input. Target information (host/user/password) can be specified in a variety of ways. For example, each item can be either a single entry or a file containing multiple entries. Additionally, a combination file format allows the user to refine their target listing.
* Modular design. Each service module exists as an independent .mod file. This means that no modifications are necessary to the core application in order to extend the supported list of services for brute-forcing.

## Metasploit
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://metasploit.com/

You might have heard of this one before...

## Responder
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-06-10

**Original URL:** https://github.com/lgandx/Responder

Responder is a LLMNR, NBT-NS and MDNS poisoner, with built-in HTTP/SMB/MSSQL/FTP/LDAP rogue authentication server supporting NTLMv1/NTLMv2/LMv2, Extended Security NTLMSSP and Basic HTTP authentication.

# Reporting
# Tunnels
## SSH Tunnel
**Module Author:** liam somerville (@leesoh)

**Last Updated:** 2017-07-17

**Original URL:** N/A

Creates an AutoSSH-powered SSH service that will persistently call home to the specified IP/host.

If priv_key is uncommented, it will upload the key to the target and use that to call home. If priv_key is not set, one will be generated and the corresponding public key downloaded to the files subfolder.

Since the most likely use for this is some sort of onsite dropbox, you'll likely not want to use a private key you use for other systems.


