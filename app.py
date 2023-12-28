from flask import Flask, render_template, jsonify, request
import subprocess
from steppercontrol import *
from settings import version, settings

app = Flask(__name__)\



@app.route('/')
def index():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', locations=httpstatus(), version=version, cputemperature=cputemperature)


@app.route('/api', methods=['POST'])
def api():
    try:
        item = request.json['item']
        command = request.json['command']
        parsecontrol(item, command)
        return jsonify(apistatus()), 201
    except KeyError:
        return "badly formed json message", 201


@app.route('/selftest')
def selftest():
    runselftest()
    return 'Self-Test started, please review logs and front panel to see results' \
           ' <A href="/pylog">Click here for logs</A>'


@app.route('/pylog')
def showplogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='X-Y log', version=version, cputemperature=cputemperature)


@app.route('/guaccesslog')
def showgalogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-access.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log', version=version,
                           cputemperature=cputemperature)


@app.route('/guerrorlog')
def showgelogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['gunicornpath'] + 'gunicorn-error.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log', version=version,
                           cputemperature=cputemperature)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    with open(settings['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature, version=version)


if __name__ == '__main__':
    app.run()
