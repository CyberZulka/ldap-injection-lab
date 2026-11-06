# LDAP Injection Lab Journal

## Project Overview
A hands-on cybersecurity lab exploring LDAP,
LDAP Injection, vulnerability testing and remediation.

## Day 1 – Environment Preparation

### Objective
Prepare Parrot OS for the LDAP Injection lab.

### Environment
- Operating System: Parrot OS
- Python: 3.13.5
- Git: 2.47.3

### Project Structure
- app/: Application source code
- documentation/: Lab notes and technical documentation
- screenshots/: Evidence of practical activities
- terminal-session.log: Recorded terminal session

### Completed Tasks
- Verified Python installation.
- Verified Git installation.
- Created the project directory.
- Created documentation and screenshots folders.
- Started terminal session recording.

### Challenges
A locale warning appeared when starting terminal recording.
The recording nevertheless started successfully.

### Lessons Learned
Verified the development environment and established
a documentation and evidence collection structure.

## Stage 2 – Python Environment Setup

### Objective
Prepare an isolated Python environment and install
the libraries required for the LDAP Injection lab.

### Virtual Environment
Created and activated a Python virtual environment.

### Dependencies Installed
- Flask 3.1.3
- ldap3 2.9.1

### Package Manager
- pip 26.3

### Challenges
Initial PyPI connection timeouts occurred during
the pip upgrade attempt. The upgrade later succeeded.

### Outcome
Successfully installed Flask and ldap3.

### Lessons Learned
- Virtual environments isolate project dependencies.
- Flask provides the web application framework.
- ldap3 provides LDAP communication capabilities.


## Stage 3 – OpenLDAP Installation

### Objective
Install and start a local LDAP directory server.

### Packages Installed
- slapd: OpenLDAP server daemon
- ldap-utils: LDAP command-line utilities

### Verification
Command:
sudo systemctl status slapd

Result:
Active: active (running)

Service:
Enabled

### Outcome
OpenLDAP was successfully installed and started.

### Lessons Learned
- slapd runs the OpenLDAP directory service.
- systemctl allows us to manage and inspect Linux services.
- An enabled service starts automatically during system boot.

## Stage 4 – LDAP Configuration Discovery

### Objective
Identify the configured LDAP suffix and administrator DN.

### Command Executed
sudo slapcat -n 0 | grep -E 'olcSuffix|olcRootDN'

### Results
- Current directory suffix: dc=nodomain
- Directory administrator: cn=admin,dc=nodomain
- Configuration administrator: cn=admin,cn=config

### Lessons Learned
- Base DN identifies the root of an LDAP directory.
- DN means Distinguished Name.
- cn means Common Name.
- dc means Domain Component.
- OpenLDAP has separate configuration and directory databases.

## Stage 4 – OpenLDAP Configuration

### Objective
Configure OpenLDAP with a custom fictional domain for the Cyber Zulka lab.

### Configuration
- DNS Domain: cyberzulka.lab
- Organization: Cyber Zulka
- Base DN: dc=cyberzulka,dc=lab
- Directory Administrator DN: cn=admin,dc=cyberzulka,dc=lab

### Verification
Command:
sudo slapcat -n 0 | grep -E 'olcSuffix|olcRootDN'

Result:
- olcSuffix: dc=cyberzulka,dc=lab
- olcRootDN: cn=admin,dc=cyberzulka,dc=lab

### Lessons Learned
- The Base DN identifies the root of an LDAP directory.
- The directory administrator DN identifies the administrative account.
- OpenLDAP has a separate configuration database.
