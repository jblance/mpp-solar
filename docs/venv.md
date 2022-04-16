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
(mppsolar) pi@batteryshed:~ $ pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mppsolar"
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Obtaining mppsolar from git+https://github.com/jblance/mpp-solar.git#egg=mppsolar
  Cloning https://github.com/jblance/mpp-solar.git to ./venv/mppsolar/src/mppsolar
  Running command git clone -q https://github.com/jblance/mpp-solar.git /home/pi/venv/mppsolar/src/mppsolar
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Collecting paho-mqtt
  Using cached https://www.piwheels.org/simple/paho-mqtt/paho_mqtt-1.6.1-py3-none-any.whl (75 kB)
Collecting pyserial
  Using cached https://www.piwheels.org/simple/pyserial/pyserial-3.5-py2.py3-none-any.whl (90 kB)
Installing collected packages: pyserial, paho-mqtt, mppsolar
  Running setup.py develop for mppsolar
Successfully installed mppsolar paho-mqtt-1.6.1 pyserial-3.5
```

### Run mpp-solar
```
(mppsolar) pi@batteryshed:~ $ mpp-solar -v
Solar Device Command Utility, version: 0.9.10, PI18 ammendments from preussal
```
```
(mppsolar) pi@batteryshed:~ $ mpp-solar -c QID
Parameter                     	Value           Unit
serial_number                 	92000000000666
```

### Update to latest from github
make sure you have activated the virtual environment beforehand
```
(mppsolar) pi@batteryshed:~ $  pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mppsolar"
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Obtaining mppsolar from git+https://github.com/jblance/mpp-solar.git#egg=mppsolar
  Updating ./venv/mppsolar/src/mppsolar clone
  Running command git fetch -q --tags
  Running command git reset --hard -q 88b0d406c31094380532bb22d6a1f975374a5930
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Requirement already satisfied: paho-mqtt in ./venv/mppsolar/lib/python3.9/site-packages (from mppsolar) (1.6.1)
Requirement already satisfied: pyserial in ./venv/mppsolar/lib/python3.9/site-packages (from mppsolar) (3.5)
Installing collected packages: mppsolar
  Attempting uninstall: mppsolar
    Found existing installation: mppsolar 0.9.10
    Uninstalling mppsolar-0.9.10:
      Successfully uninstalled mppsolar-0.9.10
  Running setup.py develop for mppsolar
Successfully installed mppsolar
```
