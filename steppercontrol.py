from RPi import GPIO
from time import sleep
from logmanager import *
from settings import version
from threading import Timer
from ADCPi import ADCPi




class PositionClass:
    def __init__(self):
        self.x = 0
        self.y = 0
        timerthread = Timer(0.5, self.getpositions)
        timerthread.start()

    def getpositions(self):
        self.x = adc.read_voltage(1) - 2.5
        self.y = adc.read_voltage(5) - 2.5
        # print('Read position')
        timerthread = Timer(0.25, self.getpositions)
        timerthread.start()

    def location(self, loc):
        if loc == 'x':
            return self.x
        elif loc == 'y':
            return self.y
        else:
            return -99.99

    def httpstatus(self):
        statuslist = ({'xpos': round(self.x, 4), 'ypos': round(self.y, 4)})
        # print(statuslist)
        return statuslist

    def apistatus(self):
        statuslist = ({'xpos': self.x, 'ypos': self.y})
        # print(statuslist)
        return statuslist


class StepperClass:
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
        self.channela = a
        self.channelaa = aa
        self.channelb = b
        self.channelbb = bb
        GPIO.setup(self.listchannels(), GPIO.OUT)

    def listchannels(self):
        return [self.channela, self.channelaa, self.channelb, self.channelbb]

    def current(self):
        return self.seq[self.sequenceindex]

    def movenext(self, fine=False):
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
        self.moving = False
        self.sequence = self.sequence + 1
        print('%s stopped, X = %s, Y = %s' % (self.axis, round(positions.location('x'), 4),
                                              round(positions.location('y'), 4)))
        self.output([0, 0, 0, 0])

    def move(self, steps):
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
                    print("step counter overrun %s" % stepcounter)
                    self.stop()
                    return
                if delta > 0:
                    if abs(target - positions.location(self.axis)) < 0.1:
                        self.movenext(True)
                        print('recheck stepper %s position %s - target %s' % (self.axis, round(
                            positions.location(self.axis), 4), target))
                        if positions.location(self.axis) > target:
                            self.moveprevious(True)
                            print("%s at %s and just passed %s so stepped back 1. Steps = %s"
                                  % (self.axis, positions.location(self.axis), target, stepcounter))
                            self.stop()
                            return
                    else:
                        self.movenext()
                else:
                    if abs(target - positions.location(self.axis)) < 0.1:
                        self.moveprevious(True)
                        print('recheck stepper %s position %s - target %s' % (self.axis, round(
                            positions.location(self.axis), 4), target))
                        if positions.location(self.axis) < target:
                            self.movenext(True)
                            print("%s at %s and just passed %s so stepped forward 1. Steps = %s"
                                  % (self.axis, positions.location(self.axis), target, stepcounter))
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
        GPIO.output(self.channela, channels[0])
        GPIO.output(self.channelaa, channels[1])
        GPIO.output(self.channelb, channels[2])
        GPIO.output(self.channelbb, channels[3])


def parsecontrol(item, command):
    try:
        if item != 'getxystatus':
            print('%s : %s ' % (item, command))
        if item == 'xmove':
            timerthread = Timer(1, lambda: stepperx.move(command))
            timerthread.start()
        elif item == 'ymove':
            timerthread = Timer(1, lambda: steppery.move(command))
            timerthread.start()
        elif item == 'xmoveto':
            timerthread = Timer(1, lambda: stepperx.moveto(command))
            timerthread.start()
        elif item == 'ymoveto':
            timerthread = Timer(1, lambda: steppery.moveto(command))
            timerthread.start()
        # print('X = %s, Y = %s' % (stepperx.listlocation(), steppery.listlocation()))
    except ValueError:
        print('incorrect json message')
    except IndexError:
        print('bad valve number')


def runselftest():
    print('Stopping both motors prior to testing')
    stepperx.stop()
    steppery.stop()
    print('Starting test sequence in 10 seconds')
    timerthread = Timer(10, testsequence)
    timerthread.start()


def testsequence():
    print('Self test started ************************************')
    print('Starting channel x tests')
    print('Setting all x channels to 1 for 5 seconds')
    stepperx.output([1, 1, 1, 1])
    sleep(5)
    print('Setting all x channels to 0 for 5 seconds')
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    print('step x 10 steps forward')
    stepperx.moveslow(10)
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    print('step x 10 steps backward')
    stepperx.moveslow(-10)
    stepperx.output([0, 0, 0, 0])
    sleep(5)
    print('Finished Channel x tests')
    print('Starting channel y tests')
    print('Setting all y channels to 1 for 5 seconds')
    steppery.output([1, 1, 1, 1])
    sleep(5)
    print('Setting all y channels to 0 for 5 seconds')
    steppery.output([0, 0, 0, 0])
    sleep(5)
    print('step y 10 steps forward')
    steppery.moveslow(10)
    steppery.output([0, 0, 0, 0])
    sleep(5)
    print('step y 10 steps backward')
    steppery.moveslow(-10)
    steppery.output([0, 0, 0, 0])
    sleep(5)
    print('Finished Channel y tests')
    print('Self test ended ************************************')


def reference():
    ref = abs(adc.read_voltage(8) - 4.935)
    return ref


def jsxplus():
    if GPIO.input(7):
        GPIO.output(12, GPIO.HIGH)
        print('joystick X+ High (Released)')
    else:
        GPIO.output(12, GPIO.LOW)
        print('joystick X+ Low (Pressed)')
        while not (GPIO.input(7)):
            stepperx.movenext()
            sleep(.05)
        stepperx.stop()


def jsxminus():
    if GPIO.input(16):
        GPIO.output(12, GPIO.HIGH)
        print('joystick X- High (Released)')
    else:
        GPIO.output(12, GPIO.LOW)
        print('joystick X- Low (Pressed)')
        while not (GPIO.input(16)):
            stepperx.moveprevious()
            sleep(.05)
        stepperx.stop()


def jsyplus():
    if GPIO.input(20):
        GPIO.output(12, GPIO.HIGH)
        print('joystick Y+ High (Released)')
    else:
        GPIO.output(12, GPIO.LOW)
        print('joystick Y+ Low (Pressed)')
        while not (GPIO.input(7)):
            steppery.movenext()
            sleep(.05)
        steppery.stop()


def jsyminus():
    if GPIO.input(21):
        GPIO.output(12, GPIO.HIGH)
        print('joystick Y- High (Released)')
    else:
        GPIO.output(12, GPIO.LOW)
        print('joystick Y- Low (Pressed)')
        while not (GPIO.input(16)):
            steppery.moveprevious()
            sleep(.05)
        steppery.stop()


print("xy controller started")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup([11, 16, 20, 21], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(12, 0)
adc = ADCPi(0x68, 0x69, 12)
adc.set_conversion_mode(1)
positions = PositionClass()
stepperx = StepperClass()
stepperx.axis = 'x'
stepperx.setchannels(18, 24, 23, 9)
stepperx.stop()
steppery = StepperClass()
steppery.axis = 'y'
steppery.setchannels(17, 22, 27, 13)
steppery.stop()
GPIO.add_event_detect(11, GPIO.BOTH, callback=jsxplus, bouncetime=50)
GPIO.add_event_detect(16, GPIO.BOTH, callback=jsxminus, bouncetime=50)
GPIO.add_event_detect(20, GPIO.BOTH, callback=jsyplus, bouncetime=50)
GPIO.add_event_detect(21, GPIO.BOTH, callback=jsyminus, bouncetime=50)
print('Running version %s' % version)
print("xy controller ready")
GPIO.output(12, 1)  # Set ready LED
