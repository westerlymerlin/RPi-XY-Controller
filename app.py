from flask import Flask, render_template, jsonify, request
import os
from steppercontrol import *
from settings import version, settings

app = Flask(__name__)\



@app.route('/')
def index():
    with open(settings['logging']['cputemp'], 'r') as f:
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
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['logfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='X-Y log', version=version, cputemperature=cputemperature)


@app.route('/guaccesslog')
def showgalogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['gunicornpath'] + 'gunicorn-access.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn access log', version=version,
                           cputemperature=cputemperature)


@app.route('/guerrorlog')
def showgelogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['gunicornpath'] + 'gunicorn-error.log', 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='gunicorn error log', version=version,
                           cputemperature=cputemperature)


@app.route('/syslog')
def showslogs():
    with open(settings['logging']['cputemp'], 'r') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    with open(settings['logging']['syslogfilepath'], 'r') as f:
        log = f.readlines()
    f.close()
    log.reverse()
    logs = tuple(log)
    return render_template('logs.html', rows=logs, log='system log', version=version, cputemperature=cputemperature)


@app.route('/uscHALT')
def shutdown_the_server():
    os.system('sudo halt')
    return 'The server is now shutting down, please give it a minute before pulling the power. Cheers G'


if __name__ == '__main__':
    app.run()
