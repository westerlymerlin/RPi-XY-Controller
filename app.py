"""
This is the main flask application - called by Gunicorn
"""
import subprocess
from threading import enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request
from steppercontrol import httpstatus, parsecontrol, apistatus, runselftest
from app_control import VERSION, settings
from logmanager import logger

app = Flask(__name__)
logger.info('Starting X-Y Controller web app version %s', VERSION)
logger.info('Api-Key = %s', settings['api-key'])

def read_cpu_temperature():
    """Get CPU temperature"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        cpu_temp_log = f.readline()
    cpu_temp = round(float(cpu_temp_log) / 1000, 1)
    return cpu_temp


def read_reversed_lines(path):
    """Reads a file's lines and returns them in reverse order"""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


def threadlister():
    """Get a list of all threads running"""
    appthreads = []
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads


@app.route('/')
def index():
    """Main web page handler, shows status page via the index.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', locations=httpstatus(), version=VERSION,
                           cputemperature=cputemperature, threads=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                item = request.json['item']
                command = request.json['command']
                parsecontrol(item, command)
                return jsonify(apistatus()), 201
            logger.warning('API: access attempt using an invalid token from %s', request.headers[''])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from  %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        return "badly formed json message", 401


@app.route('/selftest')
def selftest():
    """self-test routine that moves the stepper in each direction"""
    runselftest()
    return 'Self-Test started, please review logs and front panel to see results' \
           ' <A href="/pylog">Click here for logs</A>'


@app.route('/pylog')
def showplogs():
    """Displays the application log file via the logs.html template"""
    log = read_reversed_lines(settings['logfilepath'])
    return render_template('logs.html', rows=log, log='Data Node log', version=VERSION)


@app.route('/guaccesslog')   # display the gunicorn access log
def showgalogs():
    """Displays the Gunicorn access log file via the logs.html template"""
    log = read_reversed_lines(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=log, log='gunicorn access log', version=VERSION)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    """Displays the Gunicorn error log file via the logs.html template"""
    log = read_reversed_lines(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=log, log='gunicorn error log', version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """Displays the last 200 lines of the system log via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log',
                           cputemperature=cputemperature, version=VERSION)


if __name__ == '__main__':
    app.run()
