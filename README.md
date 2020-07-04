# Slots Project
A django web app for a school project.
It is hosted on Heroku [here](https://slots-app.herokuapp.com/).

## Local Setup
Setting up the project locally is fairly simple.

Requirements:
 * `python3`
 * `pip3`

First, clone the repo down to your system.
```sh
$ git clone https://github.com/ollydevulder/slots-project.git
```

Then, install django with `pip`.
```sh
$ pip3 install django
```

Next, run `local_setup.py` with your `python3` distribution. 
```sh
$ python3 ./local_setup.py
```

This creates the `local_settings.py` file and performs the initial migrations
for the project. For local testing and development a `superuser` should also be
created.
```sh
$ python3 manage.py createsuperuser
```

This is used to access the `admin/` path.

:zap: **Thus concludes the local setup!** If everything worked properly then
the app can now be ran locally.
```sh
$ python3 manage.py runserver
```

