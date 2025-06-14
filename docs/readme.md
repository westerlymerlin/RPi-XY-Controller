# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[app](./app.md)  
X-Y Controller Web Application

A Flask-based web application that provides both a user interface and API endpoints
for controlling and monitoring an X-Y positioning system. The application offers:

- Status monitoring via web interface
- API endpoints for programmatic control (API key required)
- Self-test functionality for system validation
- Access to various log files (application, Gunicorn, system)
- System information including CPU temperature and running threads

The application is designed to be run by Gunicorn in a production environment,
but can also be run directly for development purposes.

Routes:
  - / : Main status page
  - /api : API endpoint for programmatic control (POST, requires API key)
  - /selftest : Runs a system self-test
  - /pylog : Displays application logs
  - /guaccesslog : Displays Gunicorn access logs
  - /guerrorlog : Displays Gunicorn error logs
  - /syslog : Displays system logs

Configuration is managed through settings imported from app_control.

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.

[steppercontrol](./steppercontrol.md)  
Stepper Motor Control System for XY Table

This module provides classes and functions to control an XY positioning table
using stepper motors with ADC feedback for position tracking. It includes:

- Position tracking via ADC readings
- Stepper motor control with multiple movement modes (step, continuous, targeted)
- Web API endpoints for remote control
- Self-test capabilities for system diagnostics

The system uses GPIO pins on a Raspberry Pi to control the stepper motors and
reads position data through an ADC interface. It supports both programmatic
control and web-based interaction through status reporting functions.

Dependencies:
    - RPi.GPIO: For GPIO control
    - ADCPi: For analog position reading
    - threading: For non-blocking motor control


---


  
-------
#### Copyright (C) 2025 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  
