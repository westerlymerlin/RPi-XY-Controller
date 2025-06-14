"""
X-Y Controller Web Application

A Flask-based web application that provides both a user interface and API endpoints
for controlling and monitoring an X-Y positioning system. The application offers:

- Status monitoring via web interface
- API endpoints for programmatic control (API key required)
- Self-test functionality for system validation
- Access to various log files (application, Gunicorn, system)
- System information including CPU temperature and running threads

The application is designed to be run by Gunicorn in a production environment,
but can also be run directly for development purposes.

Routes:
  - / : Main status page
  - /api : API endpoint for programmatic control (POST, requires API key)
  - /selftest : Runs a system self-test
  - /pylog : Displays application logs
  - /guaccesslog : Displays Gunicorn access logs
  - /guerrorlog : Displays Gunicorn error logs
  - /syslog : Displays system logs

Configuration is managed through settings imported from app_control.
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
    """
    Reads the CPU temperature from the file specified in the settings and converts
    it to Celsius.

    Reads the raw CPU temperature value from the file path defined in the settings
    dictionary under the 'cputemp' key. The value is retrieved as a string,
    converted to a floating-point number, divided by 1000 to get the temperature
    in Celsius, rounded to one decimal place, and returned.

    Returns:
        float: The CPU temperature in Celsius.

    Raises:
        KeyError: If the 'cputemp' key is missing from the settings dictionary.
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an error reading the file.
    """
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        cpu_temp_log = f.readline()
    cpu_temp = round(float(cpu_temp_log) / 1000, 1)
    return cpu_temp


def read_reversed_lines(path):
    """
    Reads lines from a file, reverses their order, and returns the reversed list of lines.

    Summary:
    This function reads all the lines from a specified file, reverses the order of those lines,
    and returns the reversed list. The file is expected to be encoded in UTF-8.

    Args:
        path (str): The path to the file from which lines will be read.

    Returns:
        list[str]: A list containing the lines from the file in reversed order.
    """
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


def threadlister():
    """
    Get the list of active threads with their names and native IDs.

    This function gathers all currently active threads, retrieves their names
    and native IDs, and organizes them into a list. Each thread is represented
    as a sublist containing its name and native ID. This is useful for debugging
    or monitoring thread activity in the application.

    Returns:
        List[List[str, int]]: A list of active threads where each thread is
        represented as a list containing its name (str) and native ID (int).
    """
    appthreads = []
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads


@app.route('/')
def index():
    """
    Handles the root route of the application, retrieves CPU temperature, and renders
    the main index page with relevant data such as locations, application version,
    CPU temperature, and active threads.

    Returns:
        str: Rendered HTML template for the index page.
    """
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    return render_template('index.html', locations=httpstatus(), version=VERSION,
                           cputemperature=cputemperature, threads=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """
    Handles API requests for executing commands on specific items by verifying the provided API key.

    The function is intended to handle POST requests to the '/api' endpoint. It verifies the validity of the
    API key provided in the request headers before processing the request. If the API key is valid, it extracts
    the required parameters from the JSON payload (item and command), processes the command, and returns the API
    status. If the key is missing or invalid, it logs the attempt and returns an appropriate HTTP response.

    The function also handles malformed JSON messages gracefully by returning an error response.

    Returns:
        JSONResponse: A JSON-formatted response containing the API status with a status code of 201 if the request
        is processed successfully.
        String: An error message with an appropriate HTTP status code if the API key is missing, invalid, or the
        request JSON is malformed.
    """
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
    """
    Handles the self-test endpoint for a web application. This function triggers
    a self-test operation to assess system functionality and provides a response
    indicating that the test process has started. Users are instructed to review
    logs and the front panel for results.

    Returns
    -------
    str
        A message indicating that the self-test operation has started, along with
        a link to access system logs.
    """
    runselftest()
    return 'Self-Test started, please review logs and front panel to see results' \
           ' <A href="/pylog">Click here for logs</A>'


@app.route('/pylog')
def showplogs():
    """
    Handles the retrieval and rendering of application logs in reverse order.

    This function is mapped to the '/pylog' endpoint and fetches the log entries
    for a Data Node from the specified log file. The logs are reversed so that
    recent entries are displayed first. It then renders an HTML template with
    the logs, title, and version information, providing a user interface to
    analyze the log data.

    Returns:
        Response: Renders an HTML template populated with log data, log title,
                  and version details.
    """
    log = read_reversed_lines(settings['logfilepath'])
    return render_template('logs.html', rows=log, log='Data Node log', version=VERSION)


@app.route('/guaccesslog')   # display the gunicorn access log
def showgalogs():
    """
    Displays the Gunicorn access log by reading and reversing the lines of the
    log file. The log is formatted into a web page showing the most recent
    entries first.

    Returns
    -------
    str
        Rendered HTML template for displaying the Gunicorn access log.

    Raises
    ------
    KeyError
        If 'gunicornpath' is not defined in the settings dictionary.
    """
    log = read_reversed_lines(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=log, log='gunicorn access log', version=VERSION)


@app.route('/guerrorlog')  # display the gunicorn error log
def showgelogs():
    """
    Displays the Gunicorn error log.

    This function handles the web endpoint for retrieving and displaying the
    Gunicorn error log file. It reads the log file in reverse order, formats
    it, and renders it in an HTML page for easy viewing.

    Returns:
        Response: A rendered HTML page containing the Gunicorn error log.
    """
    log = read_reversed_lines(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=log, log='gunicorn error log', version=VERSION)


@app.route('/syslog')  # display the raspberry pi system log
def showslogs():
    """
    Display the Raspberry Pi system logs along with CPU temperature.

    Opens and reads the system log file and CPU temperature from the specified
    file path within the `settings` dictionary. Retrieves the most recent 200
    log entries using the `journalctl` command. The log entries are reversed to
    show the latest log entries first. The CPU temperature data is converted
    and rounded to a single decimal point before being rendered in the HTML
    template.

    Raised exceptions during file access or subprocess execution are not
    explicitly handled here.

    Returns:
        flask.Response: Rendered HTML template containing system log entries,
        CPU temperature, and the software version.
    """
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    f.close()
    cputemperature = round(float(log)/1000, 1)
    log = subprocess.Popen('/bin/journalctl -n 200', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log',
                           cputemperature=cputemperature, version=VERSION)


if __name__ == '__main__':
    app.run()
