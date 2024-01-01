"""
This is the main flask application - called by Gunicorn
"""
import subprocess
from flask import Flask, render_template, jsonify, request
from steppercontrol import httpstatus, parsecontrol, apistatus, runselftest
from settings import VERSION, settings

app = Flask(__name__)\



@app.route('/')
def index():
    """Main web page handler, shows status page via the index.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', locations=httpstatus(), version=VERSION, cputemperature=cputemperature)


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
    try:
        item = request.json['item']
        command = request.json['command']
        parsecontrol(item, command)
        return jsonify(apistatus()), 201
    except KeyError:
        return "badly formed json message", 201


@app.route('/selftest')
def selftest():
    """self-test routine that moves the stepper in each direction"""
    runselftest()
    return 'Self-Test started, please review logs and front panel to see results' \
           ' <A href="/pylog">Click here for logs</A>'


@app.route('/pylog')
def showplogs():
    """Displays the application log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logfilepath'], 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='X-Y log', version=VERSION, cputemperature=cputemperature)


@app.route('/guaccesslog')
def showgalogs():
    """Displays the Gunicorn access log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log', version=VERSION,
                           cputemperature=cputemperature)


@app.route('/guerrorlog')
def showgelogs():
    """Displays the Gunicorn error log file via the logs.html template"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r', encoding='utf-8') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log', version=VERSION,
                           cputemperature=cputemperature)


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
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature, version=VERSION)


if __name__ == '__main__':
    app.run()
