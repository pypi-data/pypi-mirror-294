# mm-base1

To build a docker it's necessary to give .netrc and pip.conf with access to the private pypi.

.env file:
```
PIPCONF_PATH=$HOME/.config/pip/pip.conf
NETRC_PATH=$HOME/.netrc
```

$HOME/.config/pip/pip.conf
```
[global]
index-url = https://myprivaterepo.com/pypi/simple
extra-index-url= https://pypi.org/simple
```
$HOME/.netrc
```
machine myprivaterepo.com
	login usr
	password secretsecret
```
