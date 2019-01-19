=====
# **ESVnote
=====

ESVnote is a simple Django app to take notes that are accessible online.
Detailed documentation is in the "docs" directory.

## Overview

The main features that have currently been implemented are:

* There are models for books, book copies, genre, language and authors.
* Users can view list and detail information for books and authors.
* Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).
* Librarians can renew reserved books

## Quick start
-----------
To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser 
   python3 manage.py runserver
   ```

1. Add "esvnote" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'esvnote',
    ]

2. Include the esvnote URLconf in your project urls.py like this::

    path('esvnote/', include('esvnote.urls')),
    path('admin/', admin.site.urls),

3. Run `python manage.py migrate` to create the esvnote models.

4. Start the development server and visit `http://127.0.0.1:8000/admin/`.

1. Create a few test objects of each type.

1. Open tab to `http://127.0.0.1:8000` to see the main site, with new objects.

To delpoy to Heroku on Windows 10
---------------------------------
1. Register for an account an create an app on Heroku
    You can use git from CLI or GitHub Desktop to commit and push changes from your project directly to Heroku
    
2. Install postgreSQL locally and execute CREATE DATABASE <your_local_db_name>; and USE <your_local_db_name>;
    Aslo add to your root directory: 'Procfile' which has
    
        web: gunicorn mysite.wsgi --log-file -
    
    and a 'requirements.txt' using '$ pip freeze > requirements.txt'
    
3. Use '$ pip install django-heroku' and at the bottom of <your_project_name>/settings.py add

    django_heroku.settings(locals())


If you need to migrate a local db to a Heroku db
------------------------------------------------
1. Reset Heroku remote database

    $ heroku pg:reset <remote_db_resource_name> -a <your_heroku_app_name>

2. Run

   $ heroku pg:push <your_local_db_name> <remote_db_resource_name> -a <your_heroku_app_name>

*OR*

2. Dump localdb from command terminal:
    
    $ pg_dump -h localhost -p 5432 -U <your_local_db_username> -F c -b -v -f <your_file_name>.dump <your_local_db_name>

3. Restore Heroku postgre db with dump file

    $ pg_restore --verbose --no-acl --no-owner -U <remote_db_username> -h <remote_db_host> -p 5432 -d <remote_db_name> <your_path_to_dump_file/your_file_name.dump>

7. Visit https://<your_heroku_app_name>.herokuapp.com/esvnote to use
    Visit https://<your_heroku_app_name>.herokuapp.com/admin to manage esvnote
  
