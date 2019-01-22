# ESVnote
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ESVnote is a simple Django app to take notes that are accessible online.

## Overview
------------
The main features that have currently been implemented are:

* Simple ,easy to use nav bar
* Search the ESV Bible using [Crossway's](https://www.crossway.org/) awesome [ESV API](https://api.esv.org/)
   ** search any term, like `eden`, and see passages that contains that term
   ** seach for a specific passage reference, such as `John+3:16`
   ** the API can handle many variations and abbreviations
* Browse the ESV Bible specific books, chapters, verses, and (*comming soon) contextual information.

Note: I have deliberately chosen not to redact this workflow's approved API key, and kept it unhidden in the source code. Your use of the API key is subject to the conditions laid out in the ESV API usage guidelines.

## Quick start
-------------
To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).

1. I recommend using a Python virtual environment.

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
   ```
    INSTALLED_APPS = [
        ...
        'esvnote',
    ]
    ```
2. Include the esvnote URLconf in your project urls.py like this::
    `path('esvnote/', include('esvnote.urls')),`
    `path('admin/', admin.site.urls),`

3. Run `python manage.py migrate` to create the esvnote models.

4. Start the development server and visit `http://127.0.0.1:8000/admin/`.

1. Create a few test objects of each type.

1. Open tab to `http://127.0.0.1:8000` to see the main site, with new objects.

To delpoy to Heroku on Windows 10
---------------------------------
1. Register for an account an create an app on Heroku
    You can use git from CLI or GitHub Desktop to commit and push changes from your project directly to Heroku
    
2. Install postgreSQL locally and execute `CREATE DATABASE <your_local_db_name>; and USE <your_local_db_name>;`

1. Add to your root directory: 'Procfile' which has    
       `web: gunicorn mysite.wsgi --log-file -`
    
1. Then add a 'requirements.txt' using '$ pip freeze > requirements.txt'
    
3. Use '$ pip install django-heroku' and at the bottom of <your_project_name>/settings.py add
    `django_heroku.settings(locals())`

If you need to migrate a local db to a Heroku db
------------------------------------------------
1. `$ heroku run python manage.py makemigrations -a <your_heroku_app_name>`
2. `$ heroku run python manage.py migrate -a <your_heroku_app_name>`

*OR*

1. Reset Heroku remote database
    `$ heroku pg:reset <remote_db_resource_name> -a <your_heroku_app_name>`
2. Run
    `$ heroku pg:push <your_local_db_name> <remote_db_resource_name> -a <your_heroku_app_name>`

*OR*

1. Reset Heroku remote database
    `$ heroku pg:reset <remote_db_resource_name> -a <your_heroku_app_name>`
1. Dump localdb from command terminal:   
    `$ pg_dump -h localhost -p 5432 -U <your_local_db_username> -F c -b -v -f <your_file_name>.dump <your_local_db_name>`
2. Restore Heroku postgre db with dump file
    `$ pg_restore --verbose --no-acl --no-owner -U <remote_db_username> -h <remote_db_host> -p 5432 -d <remote_db_name> <your_path_to_dump_file/your_file_name.dump>`
3. Visit `https://<your_heroku_app_name>.herokuapp.com/esvnote` to use

4.`Visit https://<your_heroku_app_name>.herokuapp.com/admin` to manage esvnote

## ToDo
------------------------
1. Add detailed documentation to "docs" directory
2. Error handling for empty search query
3. Populate ESV Bible directory in 'Browser'(esvbible) views
4. Style improvements

Future objectives
---------------------
1. Add audio results 
2. User registration and management
3. Note/file mangament system for storing text, images, drawing, music, and tags with associated passages
4. More navigation ease
