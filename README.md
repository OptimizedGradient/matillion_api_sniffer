# matillion_api_sniffer
Sniffs the matillion api and looks for any SQL within the variety of tasks.

# Prerequisites
## Python

Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule. Python is dynamically typed and garbage-collected. Python is what was used to create this script.

### Install Python on Mac

```
$ brew install python
```

### Install Python on Linux

```
$ sudo apt install python
```

### Windows

This can be downloaded and installed on windows from [here](https://www.python.org/downloads/windows/).

## Python Virtual Environment
### Creating Virtual Environment
#### Linux/Mac:

```
$ python -m venv /path/to/new/virtual/environment
```

#### Windows:

```
$ python -m venv c:\path\to\new\virtual\environment
```

### Activating Virtual Environment
#### Linux/Mac:

```
$ <venv>/bin/activate
```

#### Windows:

```
$ <venv>\Scripts\activate
```

### Install Requests API

From within the virtual environment run:

```
$ pip install requests
```

## Environment Variables:

For this script to run, three environment variables need to be provided to access Matillion.

### Mac/Linux:

```
$ export MATILLION_API_BASE=https://base_url.com
$ export MATILLION_API_USER=user_name
$ export MATILLION_API_PASS='secure_password'
```

### Windows:

```
$ set MATILLION_API_BASE=https://base_url.com
$ set MATILLION_API_USER=user_name
$ set MATILLION_API_PASS='secure_password'
```

## Calling python script:

```
$ python3 scan_matillion.py
```

This will start by taking the API base and credentials and will do an initial scan for all groups, it will then iterate through each group to identify all projects, identify all versions of a project, and then it will start looping through all the jobs. Once it is looping through a job, it'll work to identify any SQL components that exist within the job and generate a SQL count. This script could be used later to extract all of the SQL from those components.
