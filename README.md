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
The purpose of Celery is for it's background workers and periodic task.
The purpose for the background worker's is to mainly to send emails in an ASync way without having to
wait for the emails to be send out.
As for the periodic task is used to remove all registered account's forgotten password token every 24 hours for security purposes.
#### <a href="https://www.rabbitmq.com/download.html">Install RabbitMQ</a>


How to Run?
------
<small>*Note: If you are running Flask Web Server on an Internet Connection that blocks port 587 (E.g. School Internet), emails will not be send out.*</small>
<br><br>

#### Running Flask Web Server
Run ***heartphoria/heartphoria/\_\_init\_\_.py*** as Flask Server or alternatively with ***run.bat***.
<br><br>

#### Running RabbitMQ's Server with Celery's Worker and Beat (Optional But Recommended)
<small>*Note: If you intend to run celery, you will have to be using Pyhon 3.6 or below
as Celery has not updated their library to be compatible with Python 3.7 yet.
If you are using Python 3.7 while running celery you will encounter a keyword error for **async***.</small>

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
* [Python 3.6.0](https://www.python.org/)
* [Flask 1.0.2](http://flask.pocoo.org/)
* [Flask-SQLAlchemy 2.3.2](http://flask-sqlalchemy.pocoo.org)
* [requests 2.21.0](https://github.com/requests/requests/)
* [yagmail 0.11.214](https://github.com/kootenpv/yagmail)
* [Celery 4.2.0](http://docs.celeryproject.org/en/latest/index.html) with [RabbitMQ](https://www.rabbitmq.com/)
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
