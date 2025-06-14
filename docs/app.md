# None

<a id="app"></a>

# app

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

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.httpstatus"></a>

## httpstatus

<a id="app.parsecontrol"></a>

## parsecontrol

<a id="app.apistatus"></a>

## apistatus

<a id="app.runselftest"></a>

## runselftest

<a id="app.VERSION"></a>

## VERSION

<a id="app.settings"></a>

## settings

<a id="app.logger"></a>

## logger

<a id="app.app"></a>

#### app

<a id="app.read_cpu_temperature"></a>

#### read\_cpu\_temperature

```python
def read_cpu_temperature()
```

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

<a id="app.read_reversed_lines"></a>

#### read\_reversed\_lines

```python
def read_reversed_lines(path)
```

Reads lines from a file, reverses their order, and returns the reversed list of lines.

Summary:
This function reads all the lines from a specified file, reverses the order of those lines,
and returns the reversed list. The file is expected to be encoded in UTF-8.

Args:
    path (str): The path to the file from which lines will be read.

Returns:
    list[str]: A list containing the lines from the file in reversed order.

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Get the list of active threads with their names and native IDs.

This function gathers all currently active threads, retrieves their names
and native IDs, and organizes them into a list. Each thread is represented
as a sublist containing its name and native ID. This is useful for debugging
or monitoring thread activity in the application.

Returns:
    List[List[str, int]]: A list of active threads where each thread is
    represented as a list containing its name (str) and native ID (int).

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Handles the root route of the application, retrieves CPU temperature, and renders
the main index page with relevant data such as locations, application version,
CPU temperature, and active threads.

Returns:
    str: Rendered HTML template for the index page.

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

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

<a id="app.selftest"></a>

#### selftest

```python
@app.route('/selftest')
def selftest()
```

Handles the self-test endpoint for a web application. This function triggers
a self-test operation to assess system functionality and provides a response
indicating that the test process has started. Users are instructed to review
logs and the front panel for results.

Returns
-------
str
    A message indicating that the self-test operation has started, along with
    a link to access system logs.

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Handles the retrieval and rendering of application logs in reverse order.

This function is mapped to the '/pylog' endpoint and fetches the log entries
for a Data Node from the specified log file. The logs are reversed so that
recent entries are displayed first. It then renders an HTML template with
the logs, title, and version information, providing a user interface to
analyze the log data.

Returns:
    Response: Renders an HTML template populated with log data, log title,
              and version details.

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

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

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Displays the Gunicorn error log.

This function handles the web endpoint for retrieving and displaying the
Gunicorn error log file. It reads the log file in reverse order, formats
it, and renders it in an HTML page for easy viewing.

Returns:
    Response: A rendered HTML page containing the Gunicorn error log.

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

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

