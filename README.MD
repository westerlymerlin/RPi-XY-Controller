# X-Y Controller

### X-Y Controller is a python app that can operate 24v stepper motors and is controlled via an HTTP API

Functional description and setup instructions are available in the file: [README.pdf](./README.pdf)

Python module documentation can be found in the folder: [docs](./docs/readme.md)

Change log can be found in the file [changelog.txt](./changelog.txt)


`app.py`			    Flask application that manages the API 

----------------------------------------------------

`stepperontrol.py`		Controls X-Y stage via bipolar stepper motors and an ADC controller to read positional information. 


### JSON Commands

`{'getxystatus', 1}` Return the current locations of the x and y steppers
 
`{'xmove', n}` move x stepper n steps (-n for backwards) (if n=0 then stop)

`{'ymove', n}` move y stepper n steps (-n for backwards) (if n=0 then stop)

`{'xmoveto', f}` move x stepper to position f (float)

`{'ymoveto', f}` move y stepper to position f (float)

`{'restart', 'pi'}` Restart the raspberry pi after a 15 secodn delay