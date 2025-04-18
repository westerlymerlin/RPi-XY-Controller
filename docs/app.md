# Contents for: app

* [app](#app)
  * [subprocess](#app.subprocess)
  * [enumerate\_threads](#app.enumerate_threads)
  * [Flask](#app.Flask)
  * [render\_template](#app.render_template)
  * [jsonify](#app.jsonify)
  * [request](#app.request)
  * [httpstatus](#app.httpstatus)
  * [parsecontrol](#app.parsecontrol)
  * [apistatus](#app.apistatus)
  * [runselftest](#app.runselftest)
  * [VERSION](#app.VERSION)
  * [settings](#app.settings)
  * [logger](#app.logger)
  * [app](#app.app)
  * [read\_cpu\_temperature](#app.read_cpu_temperature)
  * [read\_reversed\_lines](#app.read_reversed_lines)
  * [threadlister](#app.threadlister)
  * [index](#app.index)
  * [api](#app.api)
  * [selftest](#app.selftest)
  * [showplogs](#app.showplogs)
  * [showgalogs](#app.showgalogs)
  * [showgelogs](#app.showgelogs)
  * [showslogs](#app.showslogs)

<a id="app"></a>

# app

This is the main flask application - called by Gunicorn

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

Get CPU temperature

<a id="app.read_reversed_lines"></a>

#### read\_reversed\_lines

```python
def read_reversed_lines(path)
```

Reads a file's lines and returns them in reverse order

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Get a list of all threads running

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Main web page handler, shows status page via the index.html template

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file

<a id="app.selftest"></a>

#### selftest

```python
@app.route('/selftest')
def selftest()
```

self-test routine that moves the stepper in each direction

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Displays the application log file via the logs.html template

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

Displays the Gunicorn access log file via the logs.html template

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

Displays the Gunicorn error log file via the logs.html template

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Displays the last 200 lines of the system log via the logs.html template

