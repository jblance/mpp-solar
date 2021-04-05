# Using mpp-solar in a virtual environment (venv)
## Install
for when you want to keep the install and dependencies separate from the rest of the environment
* create venv folder `mkdir ~/venv`
* create venv `python3 -m venv ~/venv/mppsolar`
    * might need python3-venv installed
* activate venv `source venv/mppsolar/bin/activate` (needed each time before using)
* pip install from git `pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"` (only needed if the code is updated)


## Worked Example
### Check python version
```
pi@batteryshed:~ $ python3 --version
Python 3.7.3
```
### Try create venv (and fail)
```
pi@batteryshed:~ $ python3 -m venv ~/venv/mppsolar
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt-get install python3-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: ['/home/pi/venv/mppsolar/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']
```

### Install venv
`pi@batteryshed:~ $ sudo apt-get install python3-venv`
[output removed]

`pi@batteryshed:~ $ sudo apt-get install python3.7-venv`
[output removed]

### Create venv
`pi@batteryshed:~ $ python3 -m venv ~/venv/mppsolar`

### Activate venv
```
pi@batteryshed:~ $ source ~/venv/mppsolar/bin/activate
(mppsolar) pi@batteryshed:~ $
```

### Install mpp-solar using PIP

```
(mppsolar) pi@batteryshed:~ $ pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Obtaining mpp-solar from git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar
  Updating ./venv/mppsolar/src/mpp-solar clone
Collecting pyserial (from mpp-solar)
  Downloading https://files.pythonhosted.org/packages/07/bc/587a445451b253b285629263eb51c2d8e9bcea4fc97826266d186f96f558/pyserial-3.5-py2.py3-none-any.whl (90kB)
    100% |████████████████████████████████| 92kB 444kB/s
Installing collected packages: pyserial, mpp-solar
  Running setup.py develop for mpp-solar
Successfully installed mpp-solar pyserial-3.5
```

### Run mpp-solar
```
(mppsolar) pi@batteryshed:~ $ mpp-solar -v
MPP Solar Command Utility, version: 0.7.0, First refactor version - under development
```
```
(mppsolar) pi@batteryshed:~ $ mpp-solar -c QID
Parameter                     	Value           Unit
serial_number                 	92000000000666
```

### Update to latest from github
make sure you have activated the virtual environment beforehand
```
(mppsolar) pi@batteryshed:~ $ pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar"
Obtaining mpp-solar from git+https://github.com/jblance/mpp-solar.git#egg=mpp-solar
  Updating ./venv/mppsolar/src/mpp-solar clone
  Running command git fetch -q --tags
  Running command git reset --hard -q 071ca0cd9feea458b1e36dc020aa704b2000e431
Requirement already satisfied: pyserial in ./venv/mppsolar/lib/python3.8/site-packages (from mpp-solar) (3.5)
Installing collected packages: mpp-solar
  Attempting uninstall: mpp-solar
    Found existing installation: mpp-solar 0.7.3
    Uninstalling mpp-solar-0.7.3:
      Successfully uninstalled mpp-solar-0.7.3
  Running setup.py develop for mpp-solar
Successfully installed mpp-solar

```
