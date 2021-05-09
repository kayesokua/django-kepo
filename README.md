# K.E.P.O 🤓

***Kepo*** is a Bahasa slang that stands for *Know Every Particular Object*, originating from the word ***Kaypoh*** (鸡婆) in Hokkien.
Kepo is a word we can use to describe a very curious person, someone who wants to know everything, or how we may think of our relatives sometimes!

But there's nothing wrong with being ***kepo*** on things that matter most to you.

Kepo is a learning journal app designed to track your daily learnings and nurtures curious sharing.
It's a simple, dynamic website built with Python-Django 3.0 Framework. This repository contains the raw version of the project which may not follow the best practices, but a still decent starter template to help you setup a private learning network.

This project features:
 - My Feed: This app features Post (with file upload) and Comment forms, Posts List by User
 - My Journal: This app features a morning & evening journal forms, Calendar Display
 - My Account: This app includes basic user registration, authentication, change password, and updating account profile
 
 [Visit the demo app](http://kepo.pythonanywhere.com/) - Feel free to use this as your journal, no superuser was created for this demo.
 
## Running and Testing the Project Locally
1. Install required packages `pip install -r requirements.txt`
2. Initialize your database with `python3 manage.py makemigrations`
3. Apply the migration with `python3 manage.py migrate`
4. Run the project on local server with `python3 manage.py runserver`
5. (Optional) Create an admin user `python3 manage.py createsuperuser`

## Deploy at PythonAnywhere.com
1. Open the bash console and clone the repository `git clone https://github.com/kayesokua/kepo.git`
2. `workon kepo` Enter the project folder and create a virtual environment `mkvirtualenv --python=/usr/bin/python3.8 venv`
3. `workon venv` to activate
4. Modify the `settings.py` and set debug to false, change allowed host to your pythonanyware.com URL, update the directories
5. `pip install django-summernote` `pip install django-autoslug` ...etc. basically all the pip packages used in the project
6. Repeat 2,3,4 of Running and Testing Project Locally

### Project Errors
1. Unable to delete post, but can unpublish
2. No password reset option yet
3. Navigation is not responsive

### Project Resources & Inspiration
1. [Django Framework Documentation](https://www.djangoproject.com/) - 
2. Journal: [Five Minute Gratitude Journal](https://play.google.com/store/apps/details?id=com.intelligentchange.fiveminutejournal&hl=de&gl=US)
3. Calendar: [Hui Wen's Event Calendar Project](https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html)
4. Feed: [Django Summernote Editor](https://github.com/summernote/django-summernote)
5. Templates: [Bootstrap 5](https://getbootstrap.com/docs/5.0/examples/)
6. Python Anywhere [https://www.pythonanywhere.com/]
7. Journal: [Nick Walter's ToDoWoo Project](https://github.com/zappycode/django-api-todowoo)
