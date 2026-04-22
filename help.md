# Q&A:
## How to activate venv for a repo?

On Windows (in root folder of a project):
~~~(PowerShell):
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
~~~

On Linux:
~~~
sudo apt update
sudo apt install python3
python3 -m venv .venv
source .venv/bin/activate
~~~
### To uninstall the venv:
Windows
~~~
Remove-Item -Recurse -Force .venv
~~~
Linux:
~~~
rm -r -f .venv
~~~

## How to install all the packages quickly?
Windows:
~~~
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
~~~

Linux:
~~~
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
~~~

## How to check the PEP8?
Linux:
(in current directory *reqursively*)
~~~
find . -name '*.py' -exec pycodestyle {} \;
~~~

## How to run tests?
Linux:
(in current directory)
~~~
python3 -B -m pytest -p no:cacheprovider tests
~~~
