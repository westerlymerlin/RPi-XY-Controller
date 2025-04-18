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


---

