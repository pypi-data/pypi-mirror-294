# Just-Run
The simplest way to enable multiple python environment work togather.

## Example - call by version

caller.py
```python
# Windows 10
# python 3.6

import justrun as jr

# run work.py through python 3.12 (that you already installed),
# - and get the processing result in this python 3.6 script.
result = jr.call_version(
    312,                        # in Linux/MacOS it should be "3.12" or 3.12
    r"path\to\work.py",
    params=[var, another_var]
)
```

work.py
```python
# Windows 10
# python 3.12

import justrun as jr

# get parameters from other python interpreter.
params = jr.get_params()

# do your work here
# ...

# and send back the processing result.
jr.return_data(your_processing_result)
```

## Another Example - call by path

caller.py
```python
# Windows 10
# python 3.6

import justrun as jr

# run work.py through specified python virtual environment (created with any version),
# - and get processing result in this python 3.6 script.
result = jr.call_pathon(
    r"path\to\your\python312\environment",    # such as r"c:\python-sandbox\312-myvenv"
    r"path\to\work.py",
    params=[var, another_var]
)
```

This method allow you to run .py through specified python virtual environment, instead of main environment.
