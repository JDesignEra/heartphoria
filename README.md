<img src="heartphoria/static/images/logo/heartphoria_colored.png" />

Initial Setup
------
#### Install Required Modules / Libraries
```cmd
pip install -r requirements.txt
```
<br>

#### Initialize / Create heartphoria.sqlite if it does not exist:
Run ***init_db.bat***, you can do so in CMD or your IDE's Terminal.
<br><br>

#### Celery with RabbitMQ (Optional But Recommended)
<p>The purpose of Celery is for its background workers and periodic task.</p>
<p>
    With Celery running, users do not have to wait for the Sign Up or Forgot Password email to
    be sent out before continuing its next task.
    In other words, emails will be sent out in an ASynchronous way rather than a Synchronous way.
</p>
<p>
    Also, Celery has a periodic task feature where it's being used to delete all
    user's forgotten password tokens every 24 hours for security purpose.
</p>
 
#### <a href="https://www.rabbitmq.com/download.html">Install RabbitMQ</a>


How to Run?
------
#### Running Flask Web Server
*<small>
    <p>
        Note: If you are hosting the Flask Web Server on an internet connection that blocks port 587 (E.g. School Internet),
        emails will not be sent out.
        Additionally, you may experience slight delays on functionality that sends out an email (e.g. Sign Up and Forgot Password).
    </p>
</small>*

##### Pick ONLY ONE (Either option 1 or 2):
1. Run ***run.bat***, you can do so in CMD or your IDE's Terminal.
2. Run ***heartphoria/heartphoria/\_\_init\_\_.py*** with your choice of IDE and ensure FLASK_ENV is set to development.
<br><br>

#### Running RabbitMQ's Server and Celery's Worker and Beat (Optional But Recommended)
*<small>
    <p>
        Note: If you intend to run Celery, you will have to be using Python 3.6.8 or below
        as Celery has not updated their library to be compatible with Python 3.7 as of yet.
        If you are using Python 3.7 while running Celery, you will encounter a keyword error for <b>async</b>.
    </p>
</small>*

1. In ***heartphoria/heartphoria/\_\_init\_\_.py*** change { **broker_url** } and { **result_backend** }.
2. Run ***run_rabbitmq.bat***, you can do so in CMD or your IDE's Terminal.
3. Run ***run_celery_worker.bat***, you can do so in CMD or your IDE's Terminal.
4. Run ***run_celery_beat.bat***, you can do so in CMD or your IDE's Terminal.

*If you are using RabbitMQ without changing any settings*:
```python
broker_url='amqp://guest:password@localhost:5672/'
result_backend='rpc://'
```


Frameworks / Libraries / APIs / Languages
------
* [Python 3.6.8](https://www.python.org/)
* [Flask 1.0.2](http://flask.pocoo.org/)
* [Flask-SQLAlchemy 2.3.2](http://flask-sqlalchemy.pocoo.org)
* [Flask-SSLify 0.1.5](https://github.com/kennethreitz/flask-sslify)
* [Requests (http for humans) 2.21.0](https://github.com/requests/requests/)
* [yagmail 0.11.214](https://github.com/kootenpv/yagmail)
* [Celery 4.2.0](http://docs.celeryproject.org/en/latest/index.html) with
    [gevent 1.4.0](https://github.com/gevent/gevent/) and
    [RabbitMQ](https://www.rabbitmq.com/)
* [Bootstrap 4.2.1](https://getbootstrap.com/)
* [FontAwesome Pro 5.5.0](https://fontawesome.com/)
* [jQuery 3.3.1](https://code.jquery.com/)
* [AccuWeather](https://developer.accuweather.com)
* [Google Places](https://cloud.google.com/maps-platform/places/)
* [MapBox](https://www.mapbox.com/)


Commit Legends
------
| Format | Description |
|--------|-------------|
| + | Added |
| * | Updated |
| - | Removed |
| { Variable / Code } | Variable/Code
| \[ File ] | File (e.g. style.css) |
| ( Folder ) | Folder/Directory |
| < Notes > | Notes/Things to Note |
<br>

------
##### Collaborator's Github Profile
* [Joel [ JDesignEra ]](https://github.com/JDesignEra)
* [Arman [ Arman154khan ]](https://github.com/Arman154khan)
* [James [ ValianxD ]](https://github.com/ValianxD)
* [Dylan [ layzeera ]](https://github.com/layzeera)