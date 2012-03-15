# Knoatom

## Pre-requisites

* mysql database (you're on your own for this one)
* pip (for installing various python things)

        apt-get install python-pip python-dev build-essential

* django (python web framework)

        pip install django

* mysql-python (this is probably the trickiest one to install)

        pip install mysql-python

* south (database migration tool)

        pip install south

## Initial Setup

For an initial setup of knoatom-web, here's some of the things you need to do:

1. Clone and move into the repository
2. Copy `settings-example.py` to `settings.py` and set the various things that are required in it:
    * In the `DATABASES.default` dictionary, set
        * `NAME` - name of your database
        * `USER` - user for your database
        * `PASSWORD` - password for your user
    * `MEDIA_ROOT` - file system location for uploaded files
    * `MEDIA_URL` - url for getting to `MEDIA_ROOT`
    * `STATIC_ROOT` - file system location for static files (will be collected here)
    * `STATIC_URL` - url for getting to `STATIC_ROOT`
    * `ADMIN_MEDIA_PREFIX` - typically the value of `STATIC_URL` + `admin/`
    * `SECRET_KEY` - longer the better - [random.org](http://www.random.org/strings/) will help you out)
3. Set up your database running the following commands (errors in these will probably be fixed by reading the errors and adjusting `settings.py`):
    * `./manage.py syncdb` - creates the database tables and initial user
    * `./manage.py migrate` - brings the database schema up to speed
4. Cross your fingers, and run the server:

        ./manage.py runserver 8080

5. Open the url [http://localhost:8080](http://localhost:8080) and hopefully you'll see it (if you're running on your local machine).

## Migrating the Database

I think all that needs to be done to keep the database up to date is to do the following:

    ./manage.py migrate

If it becomes more complicated than that, I'll update this more, but I think that's it.