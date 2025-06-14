"""
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
"""

from time import sleep
import os
from threading import Timer
from RPi import GPIO
from ADCPi import ADCPi
from logmanager import logger


class PositionClass:
    """
    Manages the x and y positions obtained from ADC readings.

    The class periodically reads position values from ADC inputs and
    provides the location data along specified axes. It initializes
    and starts a timer thread to fetch the positional data continuously.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        timerthread = Timer(0.5, self.getpositions)
        timerthread.name = 'Postition Thread'
        timerthread.start()

    def getpositions(self):
        """
        Reads positional voltage data from an ADC and calculates the x and y positions
        relative to a 2.5V reference. This is a continuous process that updates the
        object's x and y attributes every 0.25 seconds while the ADC object is valid.
        """
        while adc is not None:
            self.x = adc.read_voltage(1) - 2.5
            self.y = adc.read_voltage(5) - 2.5
            # print('Read position')
            sleep(0.25)

    def location(self, table_axis):
        """
        Determines and returns the location value along a specified axis.

        This method evaluates the given table axis ('x' or 'y') and
        returns the corresponding coordinate value. If the provided axis
        is invalid, a default value of -99.99 is returned.

        Args:
            table_axis: A string indicating the axis ('x' or 'y').

        Returns:
            float: The coordinate value for the specified axis, or -99.99
            if the axis is invalid.
        """
        if table_axis == 'x':
            return self.x
        if table_axis == 'y':
            return self.y
        return -99.99

class StepperClass:
    """
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
    """
    def __init__(self):
        self.axis = 'n'
        self.seq = [[1, 0, 1, 0],
                    [1, 0, 0, 0],
                    [1, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 1, 0, 1],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0]
                    ]
        self.channela = 0
        self.channelaa = 0
        self.channelb = 0
        self.channelbb = 0
        self.sequenceindex = 0
        self.upperlimit = 2.1
        self.lowerlimit = -2.1
        self.sequence = 0
        self.pulsewidth = 0.025
        self.moving = False

    def setchannels(self, a, aa, b, bb):
        """
        Sets up the channel attributes and configures them as output channels.

        This method assigns input values to the corresponding channel attributes of
        the object and configures the specified GPIO channels as outputs using the
        GPIO setup method.

        Args:
            a: The first channel to be assigned to 'channela'.
            aa: The second channel to be assigned to 'channelaa'.
            b: The third channel to be assigned to 'channelb'.
            bb: The fourth channel to be assigned to 'channelbb'.
        """
        self.channela = a
        self.channelaa = aa
        self.channelb = b
        self.channelbb = bb
        GPIO.setup(self.listchannels(), GPIO.OUT)

    def listchannels(self):
        """
        Returns a list of available channels.

        This method retrieves and returns a list of channels available
        within the current instance. It consolidates the individual channel
        attributes defined in the object.

        Returns:
            list: A list containing elements channela, channelaa, channelb,
            and channelbb.
        """
        return [self.channela, self.channelaa, self.channelb, self.channelbb]

    def current(self):
        """
        Returns the current element from the sequence based on the sequence index.
        It retrieves the element at the position indicated by 'sequenceindex' from
        the sequence stored in 'seq'.

        Returns:
            The element in the sequence located at the index defined by attribute 'sequenceindex'.
        """
        return self.seq[self.sequenceindex]

    def movenext(self, fine=False):
        """
        Moves the axis motor to the next position within the defined range of movement.

        This method increments the motor's sequence index to move the axis one step forward,
        provided the current position of the motor's axis is less than the specified upper limit.
        The movement can be divided between fine and coarse categories
        based on whether the `fine` parameter is set to True or False.

        Parameters:
            fine (bool, optional): If True, retains output state after a movement;
                                   otherwise, resets the output state to zero.
        """
        stepincrement = 1
        if positions.location(self.axis) < self.upperlimit:
            self.sequenceindex += stepincrement
            if self.sequenceindex > 7:
                self.sequenceindex = 0
            self.output(self.seq[self.sequenceindex])
            sleep(self.pulsewidth)
            if not fine:
                self.output([0, 0, 0, 0])
            # print('Move %s' % stepincrement)

    def moveprevious(self, fine=False):
        """
        Moves to the previous position along a defined axis.

        This function decreases the position index by one step unit and
        updates the output according to the current sequence. The sequence index
        is updated in a circular manner. If fine movement is not required,
        the output is reset to neutral after the step.

        Args:
            fine (bool): If True, the movement is fine and does not reset the output
                         to neutral after stepping. Defaults to False.
        """
        stepincrement = -1
        if positions.location(self.axis) > self.lowerlimit:
            self.sequenceindex += stepincrement
            if self.sequenceindex < 0:
                self.sequenceindex = 7
            self.output(self.seq[self.sequenceindex])
            sleep(self.pulsewidth)
            if not fine:
                self.output([0, 0, 0, 0])
            # print('Move %s' % stepincrement)

    def stop(self):
        """
        Stops the current movement and updates the sequence counter.

        Stops the movement of the device or component by setting its moving status to
        False and increments the sequence number. Logs the current position of the
        device/component on the x and y axes. Outputs a signal to indicate the stop
        state.
        """
        self.moving = False
        self.sequence = self.sequence + 1
        logger.info('%s stopped, X = %s, Y = %s', self.axis, round(positions.location('x'), 4),
                    round(positions.location('y'), 4))
        self.output([0, 0, 0, 0])

    def move(self, steps):
        """
        Moves a mechanism a specified number of steps in a defined sequence. The movement
        can be either forward or backward depending on whether the step count is positive
        or negative. The function halts movement if steps reach zero or if the moving
        state becomes false. It includes a sequence update and enforces a delay between
        steps based on a pulse width.

        Parameters:
            steps (int): The number of steps to move. Positive values indicate forward
            movement, and negative values indicate backward movement.
        """
        self.sequence = self.sequence + 1
        self.moving = True
        if steps == 0:
            self.stop()
        while steps != 0 and self.moving:
            if steps > 0:
                steps -= 1
                self.movenext()
            else:
                steps += 1
                self.moveprevious()
            sleep(self.pulsewidth * 2)
        self.stop()

    def moveslow(self, steps):
        """
        Moves the object step-by-step in a specified direction. The method continues moving
        the object one step at a time until the specified number of steps is completed or
        movement is explicitly stopped. Movement is paused for a fixed time interval after
        each step to simulate slow movement.

        Parameters:
            steps (int): The number of steps to move. Positive values indicate forward
            movement; negative values indicate backward movement.
        """
        self.sequence = self.sequence + 1
        self.moving = True
        while steps != 0 and self.moving:
            if steps > 0:
                steps -= 1
                self.movenext(True)
                print(self.seq[self.sequenceindex])
            else:
                steps += 1
                self.moveprevious(True)
                print(self.seq[self.sequenceindex])
            sleep(1)

    def moveto(self, target):
        """
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

        """
        self.moving = True
        self.sequence = self.sequence + 1
        seq = self.sequence
        if self.lowerlimit <= target <= self.upperlimit:
            stepcounter = 0
            delta = target - positions.location(self.axis)
            # print('delta = %s' % delta)
            while positions.location(self.axis) != target and seq == self.sequence:
                stepcounter += 1
                if stepcounter > 8000:
                    logger.info('step counter overrun %s', stepcounter)
                    self.stop()
                    return
                if delta > 0:
                    if abs(target - positions.location(self.axis)) < 0.1:
                        self.movenext(True)
                        logger.info('recheck stepper %s position %s - target %s', self.axis,
                                    round(positions.location(self.axis), 4), target)
                        if positions.location(self.axis) > target:
                            self.moveprevious(True)
                            logger.info('%s at %s and just passed %s so stepped back 1. Steps = %s',
                                  self.axis, positions.location(self.axis), target, stepcounter)
                            self.stop()
                            return
                    else:
                        self.movenext()
                else:
                    if abs(target - positions.location(self.axis)) < 0.1:
                        self.moveprevious(True)
                        logger.info('recheck stepper %s position %s - target %s', self.axis,
                                    round(positions.location(self.axis), 4), target)
                        if positions.location(self.axis) < target:
                            self.movenext(True)
                            logger.info('%s at %s and just passed %s so stepped forward 1. Steps = %s',
                                  self.axis, positions.location(self.axis), target, stepcounter)
                            self.stop()
                            return
                    else:
                        self.moveprevious()
                difference = abs(target - positions.location(self.axis))
                # print('difference %f' % difference )
                if difference > 0.05:
                    sleep(self.pulsewidth * 2)
                else:
                    sleep(0.3)
        self.moving = False

    def output(self, channels):
        """
        Controls the output state of specified GPIO channels using the provided channel states.

        This function takes a list or tuple of four channel states and sets the associated
        GPIO output for each corresponding channel. Each state in the list corresponds to
        a specific GPIO channel, and the function utilizes the `output` method of the
        GPIO module for assigning these states.
        """
        GPIO.output(self.channela, channels[0])
        GPIO.output(self.channelaa, channels[1])
        GPIO.output(self.channelb, channels[2])
        GPIO.output(self.channelbb, channels[3])

def httpstatus():
    """
    Provides a function to generate a list containing rounded positional status.

    The `httpstatus` function creates a dictionary containing the keys `xpos` and `ypos`, where the values
    are the rounded versions of `positions.x` and `positions.y` respectively.
    It then adds this dictionary into a list and returns it as the function output.

    Returns:
        list: A list with a single dictionary containing `xpos` and `ypos` keys, with their corresponding
        values being rounded to four decimal points.
    """
    statuslist = ({'xpos': round(positions.x, 4), 'ypos': round(positions.y, 4)})
    return statuslist

def apistatus():
    """
    Retrieve the current status of the system including positions and movement states.

    This function compiles the current x and y positions of the system, along with
    the movement status of stepper motors for both axes, into a dictionary.

    Returns:
        dict: A dictionary containing the x and y positions, as well as movement
        states for both stepper motors.
    """
    statuslist = ({'xpos': positions.x, 'xmoving': stepperx.moving, 'ypos': positions.y, 'ymoving': steppery.moving })
    return statuslist

def parsecontrol(item, command):
    """
    Parses the control command and executes the corresponding action, such as
    moving a stepper motor or issuing a system restart. The function supports
    multiple control commands and executes them in separate timer threads when
    required.

    Parameters:
    item (str): The control item indicating the action type, such as 'xmove',
    'ymove', 'xmoveto', 'ymoveto', or 'restart'.
    command (str): The associated command or argument required for the action.
    """
    try:
        if item != 'getxystatus':
            logger.info('%s : %s ', item, command)
        if item == 'xmove':
            timerthread = Timer(1, lambda: stepperx.move(command))
            timerthread.name = 'xmove thread'
            timerthread.start()
        elif item == 'ymove':
            timerthread = Timer(1, lambda: steppery.move(command))
            timerthread.name = 'ymove thread'
            timerthread.start()
        elif item == 'xmoveto':
            timerthread = Timer(1, lambda: stepperx.moveto(command))
            timerthread.name = 'ymove to %s thread' % command
            timerthread.start()
        elif item == 'ymoveto':
            timerthread = Timer(1, lambda: steppery.moveto(command))
            timerthread.name = 'ymove to %s thread' % command
            timerthread.start()
        elif item == 'restart':
            if command == 'pi':
                logger.warning('Restart command recieved: system will restart in 15 seconds')
                timerthread = Timer(15, reboot)
                timerthread.start()
        # print('X = %s, Y = %s' % (stepperx.listlocation(), steppery.listlocation()))
    except ValueError:
        logger.error('incorrect json message')
    except IndexError:
        logger.error('bad valve number')


def runselftest():
    """
    Stops both motors and initiates a test sequence with a delay.

    This function ensures that the motors are stopped prior to running
    the self-test, providing a safe starting point for the test. A delay
    of 10 seconds is introduced before beginning the test sequence. The
    test sequence is executed in a separate thread.
    """
    logger.info('Stopping both motors prior to testing')
    stepperx.stop()
    steppery.stop()
    logger.info('Starting test sequence in 10 seconds')
    timerthread = Timer(10, testsequence)
    timerthread.name = 'selftest thread'
    timerthread.start()

def reboot():
    """
    Reboots the system using an operating system command.

    This function logs a warning message indicating that the system is
    restarting and then executes the system's reboot command immediately.
    This operation requires appropriate system permissions.

    """
    logger.warning('System is restarting now')
    os.system('sudo reboot')

def testsequence():
    """
    Conducts a self-test sequence for channel x and channel y operations, verifying stepper motor
    behaviors through various output states and movement actions. The function performs a series
    of tests on both channels by setting their output states, moving them in forward and backward
    directions, and ensuring their responses align with expected behavior.
    """
    logger.info('Self test started ************************************')
    logger.info('Starting channel x tests')
    logger.info('Setting all x channels to 1 for 5 seconds')
    stepperx.output([1, 1, 1, 1])
    sleep(5)
    logger.info('Setting all x channels to 0 for 5 seconds')
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    logger.info('step x 10 steps forward')
    stepperx.moveslow(10)
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    logger.info('step x 10 steps backward')
    stepperx.moveslow(-10)
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    logger.info('Finished Channel x tests')
    logger.info('Starting channel y tests')
    logger.info('Setting all y channels to 1 for 5 seconds')
    steppery.output([1, 1, 1, 1])
    sleep(5)
    logger.info('Setting all y channels to 0 for 5 seconds')
    steppery.output([0, 0, 0, 0])
    sleep(5)
    logger.info('step y 10 steps forward')
    steppery.moveslow(10)
    steppery.output([0, 0, 0, 0])
    sleep(5)
    logger.info('step y 10 steps backward')
    steppery.moveslow(-10)
    steppery.output([0, 0, 0, 0])
    sleep(5)
    logger.info('Finished Channel y tests')
    logger.info('Self test ended ************************************')


logger.info("xy controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup([11, 16, 20, 21], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(12, 0)
try:
    adc = ADCPi(0x68, 0x69, 12)
    adc.set_conversion_mode(1)
except OSError:
    adc = None
    logger.error('Error: No ADCPi Board Found')
positions = PositionClass()
stepperx = StepperClass()
stepperx.axis = 'x'
stepperx.setchannels(18, 24, 23, 9)
stepperx.stop()
steppery = StepperClass()
steppery.axis = 'y'
steppery.setchannels(17, 22, 27, 13)
steppery.stop()
logger.info("xy controller ready")
GPIO.output(12, 1)  # Set ready LED
