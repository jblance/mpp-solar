# Installation #

## Latest Stable Version ##
note this version might lag behind current development changes

`sudo pip install mppsolar`

## venv Install - recommended if testing new features / release ##
for when you want to keep the install and dependencies separate from the rest of the environment
* create venv folder `mkdir ~/venv`
* create venv `python3 -m venv ~/venv/mppsolar`
    * might need python3-venv installed
* activate venv `source venv/mppsolar/bin/activate` (needed each time before using)
* pip install from git `pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mppsolar"` (only needed if the code is updated)

see worked example [here](venv.md)

### Install development version from github ###
`sudo pip install -e "git+https://github.com/jblance/mpp-solar.git#egg=mppsolar"`

### Ubuntu Install example ###
[Documented Ubuntu Install](ubuntu_install.md)
