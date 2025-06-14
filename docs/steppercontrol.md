# None

<a id="steppercontrol"></a>

# steppercontrol

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

Manages the x and y positions obtained from ADC readings.

The class periodically reads position values from ADC inputs and
provides the location data along specified axes. It initializes
and starts a timer thread to fetch the positional data continuously.

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

Reads positional voltage data from an ADC and calculates the x and y positions
relative to a 2.5V reference. This is a continuous process that updates the
object's x and y attributes every 0.25 seconds while the ADC object is valid.

<a id="steppercontrol.PositionClass.location"></a>

#### location

```python
def location(table_axis)
```

Determines and returns the location value along a specified axis.

This method evaluates the given table axis ('x' or 'y') and
returns the corresponding coordinate value. If the provided axis
is invalid, a default value of -99.99 is returned.

Args:
    table_axis: A string indicating the axis ('x' or 'y').

Returns:
    float: The coordinate value for the specified axis, or -99.99
    if the axis is invalid.

<a id="steppercontrol.StepperClass"></a>

## StepperClass Objects

```python
class StepperClass()
```

Represents a stepper motor controller, enabling precise control over the stepper
motor's movement, configuration, and operational parameters.

This class provides methods for initializing and controlling a stepper motor's
movement such as stepping forward, stepping backward, stopping, or moving to
specific positions. It also supports setting GPIO channels, retrieving active
sequences, and managing limits for motor movement. The class incorporates
adjustable movement speeds (full speed or slow) and ensures proper handling of
stepper sequences during operation.

Attributes:
    axis: A string indicating the axis of operation for the stepper motor.
    seq: A list of lists, defining sequences for stepper coil activations.
    channela: An integer representing the GPIO channel for the first winding.
    channelaa: An integer representing the GPIO channel for the second winding.
    channelb: An integer representing the GPIO channel for the third winding.
    channelbb: An integer representing the GPIO channel for the fourth winding.
    sequenceindex: An integer representing the current sequence index of the motor.
    upperlimit: A float defining the maximum allowed position limit for movement.
    lowerlimit: A float defining the minimum allowed position limit for movement.
    sequence: An integer counter for the current movement sequence.
    pulsewidth: A float specifying the delay between steps, controlling speed.
    moving: A boolean flag indicating whether the motor is actively moving.

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

Sets up the channel attributes and configures them as output channels.

This method assigns input values to the corresponding channel attributes of
the object and configures the specified GPIO channels as outputs using the
GPIO setup method.

Args:
    a: The first channel to be assigned to 'channela'.
    aa: The second channel to be assigned to 'channelaa'.
    b: The third channel to be assigned to 'channelb'.
    bb: The fourth channel to be assigned to 'channelbb'.

<a id="steppercontrol.StepperClass.listchannels"></a>

#### listchannels

```python
def listchannels()
```

Returns a list of available channels.

This method retrieves and returns a list of channels available
within the current instance. It consolidates the individual channel
attributes defined in the object.

Returns:
    list: A list containing elements channela, channelaa, channelb,
    and channelbb.

<a id="steppercontrol.StepperClass.current"></a>

#### current

```python
def current()
```

Returns the current element from the sequence based on the sequence index.
It retrieves the element at the position indicated by 'sequenceindex' from
the sequence stored in 'seq'.

Returns:
    The element in the sequence located at the index defined by attribute 'sequenceindex'.

<a id="steppercontrol.StepperClass.movenext"></a>

#### movenext

```python
def movenext(fine=False)
```

Moves the axis motor to the next position within the defined range of movement.

This method increments the motor's sequence index to move the axis one step forward,
provided the current position of the motor's axis is less than the specified upper limit.
The movement can be divided between fine and coarse categories
based on whether the `fine` parameter is set to True or False.

Parameters:
    fine (bool, optional): If True, retains output state after a movement;
                           otherwise, resets the output state to zero.

<a id="steppercontrol.StepperClass.moveprevious"></a>

#### moveprevious

```python
def moveprevious(fine=False)
```

Moves to the previous position along a defined axis.

This function decreases the position index by one step unit and
updates the output according to the current sequence. The sequence index
is updated in a circular manner. If fine movement is not required,
the output is reset to neutral after the step.

Args:
    fine (bool): If True, the movement is fine and does not reset the output
                 to neutral after stepping. Defaults to False.

<a id="steppercontrol.StepperClass.stop"></a>

#### stop

```python
def stop()
```

Stops the current movement and updates the sequence counter.

Stops the movement of the device or component by setting its moving status to
False and increments the sequence number. Logs the current position of the
device/component on the x and y axes. Outputs a signal to indicate the stop
state.

<a id="steppercontrol.StepperClass.move"></a>

#### move

```python
def move(steps)
```

Moves a mechanism a specified number of steps in a defined sequence. The movement
can be either forward or backward depending on whether the step count is positive
or negative. The function halts movement if steps reach zero or if the moving
state becomes false. It includes a sequence update and enforces a delay between
steps based on a pulse width.

Parameters:
    steps (int): The number of steps to move. Positive values indicate forward
    movement, and negative values indicate backward movement.

<a id="steppercontrol.StepperClass.moveslow"></a>

#### moveslow

```python
def moveslow(steps)
```

Moves the object step-by-step in a specified direction. The method continues moving
the object one step at a time until the specified number of steps is completed or
movement is explicitly stopped. Movement is paused for a fixed time interval after
each step to simulate slow movement.

Parameters:
    steps (int): The number of steps to move. Positive values indicate forward
    movement; negative values indicate backward movement.

<a id="steppercontrol.StepperClass.moveto"></a>

#### moveto

```python
def moveto(target)
```

Moves the axis to the specified target position within predefined limits. The method adjusts
the axis position step by step until it reaches the target position or a defined condition
occurs, such as exceeding a step counter threshold or passing the target position.

If the target position is outside the lower and upper limits, the operation will not
proceed. Step adjustments are made iteratively to ensure the axis reaches the closest
possible location to the target. The sequence number ensures the operation is associated
with the intended move command and prevents interference from other simultaneous commands.

Parameters
----------
target : float
    The desired position to which the axis is moved.

<a id="steppercontrol.StepperClass.output"></a>

#### output

```python
def output(channels)
```

Controls the output state of specified GPIO channels using the provided channel states.

This function takes a list or tuple of four channel states and sets the associated
GPIO output for each corresponding channel. Each state in the list corresponds to
a specific GPIO channel, and the function utilizes the `output` method of the
GPIO module for assigning these states.

<a id="steppercontrol.httpstatus"></a>

#### httpstatus

```python
def httpstatus()
```

Provides a function to generate a list containing rounded positional status.

The `httpstatus` function creates a dictionary containing the keys `xpos` and `ypos`, where the values
are the rounded versions of `positions.x` and `positions.y` respectively.
It then adds this dictionary into a list and returns it as the function output.

Returns:
    list: A list with a single dictionary containing `xpos` and `ypos` keys, with their corresponding
    values being rounded to four decimal points.

<a id="steppercontrol.apistatus"></a>

#### apistatus

```python
def apistatus()
```

Retrieve the current status of the system including positions and movement states.

This function compiles the current x and y positions of the system, along with
the movement status of stepper motors for both axes, into a dictionary.

Returns:
    dict: A dictionary containing the x and y positions, as well as movement
    states for both stepper motors.

<a id="steppercontrol.parsecontrol"></a>

#### parsecontrol

```python
def parsecontrol(item, command)
```

Parses the control command and executes the corresponding action, such as
moving a stepper motor or issuing a system restart. The function supports
multiple control commands and executes them in separate timer threads when
required.

Parameters:
item (str): The control item indicating the action type, such as 'xmove',
'ymove', 'xmoveto', 'ymoveto', or 'restart'.
command (str): The associated command or argument required for the action.

<a id="steppercontrol.runselftest"></a>

#### runselftest

```python
def runselftest()
```

Stops both motors and initiates a test sequence with a delay.

This function ensures that the motors are stopped prior to running
the self-test, providing a safe starting point for the test. A delay
of 10 seconds is introduced before beginning the test sequence. The
test sequence is executed in a separate thread.

<a id="steppercontrol.reboot"></a>

#### reboot

```python
def reboot()
```

Reboots the system using an operating system command.

This function logs a warning message indicating that the system is
restarting and then executes the system's reboot command immediately.
This operation requires appropriate system permissions.

<a id="steppercontrol.testsequence"></a>

#### testsequence

```python
def testsequence()
```

Conducts a self-test sequence for channel x and channel y operations, verifying stepper motor
behaviors through various output states and movement actions. The function performs a series
of tests on both channels by setting their output states, moving them in forward and backward
directions, and ensuring their responses align with expected behavior.

<a id="steppercontrol.positions"></a>

#### positions

<a id="steppercontrol.stepperx"></a>

#### stepperx

<a id="steppercontrol.steppery"></a>

#### steppery

