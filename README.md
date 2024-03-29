# ai
* This documentation is assuming that the OS is ubuntu and user is ubuntu. Also the project has been downloaded in ~/ directory. If not make the corresponding changes in supervisord.conf.


### Installing Django
* ``` cd ```
* ``` git clone -v https://github.com/omkar0001/ai ```
* ``` sudo apt-get update```
* ``` sudo apt-get install python-virtualenv libffi-dev```
* ``` cd ai ```
* ``` sudo virtualenv myenv ``` Creates the virtual environment.
* ``` sudo chown -R ubuntu ../ai/ ```
* ``` source myenv/bin/activate ```

### Setting up Postgresql
* ``` deactivate ``` Exits out of the virtual environment
* ``` sudo apt-get install libpq-dev libxml2-dev libxslt1-dev python-dev ```
* ``` sudo apt-get install postgresql postgresql-contrib ```  
* ``` sudo -u postgres psql postgres ``` Logs in to the postgres with default user name. (ignore if using rds)
* ``` \password postgres ``` Set the password as password (ignore if using rds)
* ``` CREATE DATABASE ai; ``` Creates the database by name dbv2 (ignore if using rds)
* ``` \q ``` 
* ``` exit ```
* ``` source myenv/bin/activate ``` (enter the virtual env)
* ``` pip install -r requirements.txt ```

### Doing migrations ###
* ``` python manage.py migrate ``` Does the migration of database
* ``` python manage.py collectstatic ``` Prepares the static folder for css and javascript files.

### Configuring Redis ###
* ``` sudo apt-get install redis-server ```
* ``` sudo apt-get install vim ```
* ``` sudo vim /etc/redis/redis.conf ``` and edit the line ``` unixsocketperm 700 ``` to ``` unixsocketperm 777 ``` and uncomment
* press / to search followed by the search pattern and press enter, press 'n' to continue search, press 'i' for insert mode.
* to save - ESC - ':wq'

### Run supervisor
* ``` sudo apt-get install supervisor ```
* ``` source myenv/bin/activate ```
* ``` mkdir csv ```
* ``` mkdir output ```
* ```supervisord ```
* ``` sudo service redis-server restart ```

### Then you can check the processes in 
*  Go to http://ipaddress:9001
* Enter username: ai
* Enter password: password
* Context files are generated in csv/
* Output files are generated in output/
