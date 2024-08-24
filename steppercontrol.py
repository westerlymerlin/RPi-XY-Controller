"""
Main controller classes
"""

from time import sleep
import os
from threading import Timer
from RPi import GPIO
from ADCPi import ADCPi
from logmanager import logger


class PositionClass:
    """reads positions from ADCs"""
    def __init__(self):
        self.x = 0
        self.y = 0
        timerthread = Timer(0.5, self.getpositions)
        timerthread.name = 'Postition Thread'
        timerthread.start()

    def getpositions(self):
        """Regular timer to read positions form ADCs"""
        while adc is not None:
            self.x = adc.read_voltage(1) - 2.5
            self.y = adc.read_voltage(5) - 2.5
            # print('Read position')
            sleep(0.25)

    def location(self, table_axis):
        """Returns the location along specified axis"""
        if table_axis == 'x':
            return self.x
        if table_axis == 'y':
            return self.y
        return -99.99

class StepperClass:
    """Class to control a stepper motor"""
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
        """Setus up the GPIO channels for the stepper windings"""
        self.channela = a
        self.channelaa = aa
        self.channelb = b
        self.channelbb = bb
        GPIO.setup(self.listchannels(), GPIO.OUT)

    def listchannels(self):
        """lists teh chanells used"""
        return [self.channela, self.channelaa, self.channelb, self.channelbb]

    def current(self):
        """Return current sequence, used for debugging"""
        return self.seq[self.sequenceindex]

    def movenext(self, fine=False):
        """Move +1 step"""
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
        """Move -1 step"""
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
        """Stop moving"""
        self.moving = False
        self.sequence = self.sequence + 1
        logger.info('%s stopped, X = %s, Y = %s', self.axis, round(positions.location('x'), 4),
                    round(positions.location('y'), 4))
        self.output([0, 0, 0, 0])

    def move(self, steps):
        """Move **steps** at full speed"""
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
        """Moce **steps** slowly"""
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
        """Move the motor to a specific target value on the ADC"""
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
        """Output the value to teh coils on the stepper"""
        GPIO.output(self.channela, channels[0])
        GPIO.output(self.channelaa, channels[1])
        GPIO.output(self.channelb, channels[2])
        GPIO.output(self.channelbb, channels[3])

def httpstatus():
    """Return the psotion status to the web page"""
    statuslist = ({'xpos': round(positions.x, 4), 'ypos': round(positions.y, 4)})
    return statuslist

def apistatus():
    """Return the ststus as a json message for the api"""
    statuslist = ({'xpos': positions.x, 'xmoving': stepperx.moving, 'ypos': positions.y, 'ymoving': steppery.moving })
    return statuslist

def parsecontrol(item, command):
    """Parser that recieves messages from the API or web page posts and directs messages to the correct function"""
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
    """Run a selftest defined in the **testsequence** method"""
    logger.info('Stopping both motors prior to testing')
    stepperx.stop()
    steppery.stop()
    logger.info('Starting test sequence in 10 seconds')
    timerthread = Timer(10, testsequence)
    timerthread.name = 'selftest thread'
    timerthread.start()

def reboot():
    """API call to reboot the Raspberry Pi"""
    logger.warning('System is restarting now')
    os.system('sudo reboot')

def testsequence():
    """test sequence for the x-y table"""
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
except:
    adc = None
    logger.exception('Error: No ADCPi Board Found')
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
