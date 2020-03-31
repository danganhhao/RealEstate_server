# RealEstate_server
## Installation

### Linux
At root folder
Require: Python 3.x, MySQL
```sh
$ virtualenv env
$ source env/bin/activate
$ pip install django
$ pip install djangorestframework
$ pip install -r requirements.txt
$ cd project
$ python manage.py runserver
```
### Window

1. Install MySQL
Download at link https://dev.mysql.com/downloads/windows/installer/8.0.html. Need install Visual Studio Build Tools and Component C++ build tools if have not

2. Open Cmd at root folder, run following command
```sh
$ virtualenv env
$ cd env\Scripts && activate
$ pip install django
$ pip install djangorestframework
$ cd ..\..\ && pip install -r requirements.txt
```

3. Use xampp-control to start server MySQL and create user

4. Run server
```sh
cd project && python manager.py runserver
```



