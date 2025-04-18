# Contents for: steppercontrol

* [steppercontrol](#steppercontrol)
  * [sleep](#steppercontrol.sleep)
  * [os](#steppercontrol.os)
  * [Timer](#steppercontrol.Timer)
  * [GPIO](#steppercontrol.GPIO)
  * [ADCPi](#steppercontrol.ADCPi)
  * [logger](#steppercontrol.logger)
  * [PositionClass](#steppercontrol.PositionClass)
    * [\_\_init\_\_](#steppercontrol.PositionClass.__init__)
    * [getpositions](#steppercontrol.PositionClass.getpositions)
    * [location](#steppercontrol.PositionClass.location)
  * [StepperClass](#steppercontrol.StepperClass)
    * [\_\_init\_\_](#steppercontrol.StepperClass.__init__)
    * [setchannels](#steppercontrol.StepperClass.setchannels)
    * [listchannels](#steppercontrol.StepperClass.listchannels)
    * [current](#steppercontrol.StepperClass.current)
    * [movenext](#steppercontrol.StepperClass.movenext)
    * [moveprevious](#steppercontrol.StepperClass.moveprevious)
    * [stop](#steppercontrol.StepperClass.stop)
    * [move](#steppercontrol.StepperClass.move)
    * [moveslow](#steppercontrol.StepperClass.moveslow)
    * [moveto](#steppercontrol.StepperClass.moveto)
    * [output](#steppercontrol.StepperClass.output)
  * [httpstatus](#steppercontrol.httpstatus)
  * [apistatus](#steppercontrol.apistatus)
  * [parsecontrol](#steppercontrol.parsecontrol)
  * [runselftest](#steppercontrol.runselftest)
  * [reboot](#steppercontrol.reboot)
  * [testsequence](#steppercontrol.testsequence)
  * [positions](#steppercontrol.positions)
  * [stepperx](#steppercontrol.stepperx)
  * [steppery](#steppercontrol.steppery)

<a id="steppercontrol"></a>

# steppercontrol

Main controller classes

<a id="steppercontrol.sleep"></a>

## sleep

<a id="steppercontrol.os"></a>

## os

<a id="steppercontrol.Timer"></a>

## Timer

<a id="steppercontrol.GPIO"></a>

## GPIO

<a id="steppercontrol.ADCPi"></a>

## ADCPi

<a id="steppercontrol.logger"></a>

## logger

<a id="steppercontrol.PositionClass"></a>

## PositionClass Objects

```python
class PositionClass()
```

reads positions from ADCs

<a id="steppercontrol.PositionClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="steppercontrol.PositionClass.getpositions"></a>

#### getpositions

```python
def getpositions()
```

Regular timer to read positions form ADCs

<a id="steppercontrol.PositionClass.location"></a>

#### location

```python
def location(table_axis)
```

Returns the location along specified axis

<a id="steppercontrol.StepperClass"></a>

## StepperClass Objects

```python
class StepperClass()
```

Class to control a stepper motor

<a id="steppercontrol.StepperClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="steppercontrol.StepperClass.setchannels"></a>

#### setchannels

```python
def setchannels(a, aa, b, bb)
```

Setus up the GPIO channels for the stepper windings

<a id="steppercontrol.StepperClass.listchannels"></a>

#### listchannels

```python
def listchannels()
```

lists teh chanells used

<a id="steppercontrol.StepperClass.current"></a>

#### current

```python
def current()
```

Return current sequence, used for debugging

<a id="steppercontrol.StepperClass.movenext"></a>

#### movenext

```python
def movenext(fine=False)
```

Move +1 step

<a id="steppercontrol.StepperClass.moveprevious"></a>

#### moveprevious

```python
def moveprevious(fine=False)
```

Move -1 step

<a id="steppercontrol.StepperClass.stop"></a>

#### stop

```python
def stop()
```

Stop moving

<a id="steppercontrol.StepperClass.move"></a>

#### move

```python
def move(steps)
```

Move **steps** at full speed

<a id="steppercontrol.StepperClass.moveslow"></a>

#### moveslow

```python
def moveslow(steps)
```

Moce **steps** slowly

<a id="steppercontrol.StepperClass.moveto"></a>

#### moveto

```python
def moveto(target)
```

Move the motor to a specific target value on the ADC

<a id="steppercontrol.StepperClass.output"></a>

#### output

```python
def output(channels)
```

Output the value to teh coils on the stepper

<a id="steppercontrol.httpstatus"></a>

#### httpstatus

```python
def httpstatus()
```

Return the psotion status to the web page

<a id="steppercontrol.apistatus"></a>

#### apistatus

```python
def apistatus()
```

Return the ststus as a json message for the api

<a id="steppercontrol.parsecontrol"></a>

#### parsecontrol

```python
def parsecontrol(item, command)
```

Parser that recieves messages from the API or web page posts and directs messages to the correct function

<a id="steppercontrol.runselftest"></a>

#### runselftest

```python
def runselftest()
```

Run a selftest defined in the **testsequence** method

<a id="steppercontrol.reboot"></a>

#### reboot

```python
def reboot()
```

API call to reboot the Raspberry Pi

<a id="steppercontrol.testsequence"></a>

#### testsequence

```python
def testsequence()
```

test sequence for the x-y table

<a id="steppercontrol.positions"></a>

#### positions

<a id="steppercontrol.stepperx"></a>

#### stepperx

<a id="steppercontrol.steppery"></a>

#### steppery

