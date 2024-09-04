## Pycompileo
This is a python code obfuscator. It works by compiling your code to .pyc.
Which cant be *easily* decompiled for python version 3.9 (and higher).

# Usage
The following code will take a package, obfuscate it 
and return a new package with .pyc files instead of .py files.
```python
import pycompileo
pycompileo.obfuscate_package('your_module', 'obfuscated_module')
```

Now you can import this new obfuscated module:
```python
import obfuscated_module

# Note that there wont be syntax highlighting
# for .pyc files. Only use when you dont need
# syntax highlighting.

obfuscated_module.super_secret_code()
```

Everything should really be self explanatory. 
You can reach out to me at `ahmadchawla1432@gmail.com` 
for additional questions.
