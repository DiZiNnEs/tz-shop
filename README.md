# tz-shop

## About
### Rest API for shop


## Requirements:
1) Python 3.9.5 ([Installation guide](https://www.python.org/downloads/))
2) Installed `pip` ([Installation guide](https://pip.pypa.io/en/latest/installing/))
3) Installed `pipenv` (command to install: `pip install pipenv`)
4) Installed `git` ([Installation guide](https://www.linode.com/docs/guides/how-to-install-git-on-linux-mac-and-windows/))

## Installation

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/DiZiNnEs/tz-shop
$ cd tz-shop
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ pipenv install
$ pipenv shell
```

Then install the dependencies:

```sh
(env)$ pipenv install -all
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `pipenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py migrate
(env)$ python manage.py createsuperuser
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/` (the page will be empty no big deal keep reading).

Admin panel `http://127.0.0.1:8000/admin`
and enter the name with the superuser password created earlier.

Next, create the data you need in the admin panel.
