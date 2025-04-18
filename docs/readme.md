# Module Documentation


This document contains the documentation for all the modules in the **Helium Line XY Controler** version 2.1.3 application.

---

## Contents


[app](./app.md)  
This is the main flask application - called by Gunicorn

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.

[steppercontrol](./steppercontrol.md)  
Main controller classes

[tmpvoltage](./tmpvoltage.md)  
================================================
ABElectronics ADC Pi 8-Channel ADC demo
Requires python smbus to be installed
run with: python demo_readvoltage.py
================================================
Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers
Sample rate can be 12,14, 16 or 18


---

