# Web Application Firewall (WAF) &copy;
###Nir Alon 
***
### Summary 
The project objective is building a Web Application Firewall that monitors and analyzes HTTP requests that are  designated to dedicated web server from common malicious  web attacks.

Based on deep learning algorithm (CNN) on TensorFlow. 

Deployed on AWS EC2 instance and based on REST API. 

WAF detects and prevents XSS, SQL injection, and CSRF cyberattacks on HTTP protocol.

The system activity and network traffic are shown in several ways:

∙ System textual smart log that is available in the hosting machine

∙ Web based log 

### Vulnerable web application:
To approve the waf detection of cyberattacks on web applications
the project contain a vulnerable website.

the purpose of the website is to get **!HACKED!** in different ways that the WAF can detect.

the website have 5 pages:
* Sql injection page: This page demonstrates login system page without the WAF protection anyone can use malicious SQL INJECTION code for hacking the database.
* Reflected XSS page: This page demonstrates posting page to the global network without the WAF protection anyone can use malicious JavaScript codes for damage the page and steal data from other users.
* Stored XSS page: This page demonstrates users in the database that use the user registration page for input XSS malicious code. for example instead of first name the user put XSS code to store in the database.
* CSRF page: this page can be hacked if you removed the *python annotation*, this type of attack use the csrf token to validate the user actions.
* Settings page: in this page you choose if you want to defend from the different attacks and activate the WAF protection. once you activate the WAF all the next malicious attacks will be blocked by the **WAF MODELS**

##**HOW TO MAKE IT WORKS?**

1. run pip install requirements.txt file
2. run python manage.py runserver

*Once your server is up go to  http://127.0.0.1:8000/demo_site*

3. Activate the models with docker:
* The models can be downloaded here : {Link}
* With docker run this two commands and make sure you set the right **path on source**

Deploy SQL container

sudo docker run -p 8500:8501 --name tfserving_sql --mount type=bind,source=/home/ubuntu/DockerModels/sqlmodel,target=/models/sql -e MODEL_NAME=sql -t tensorflow/serving &

Deploy XSS container

sudo docker run -p 8501:8501 --name tfserving_xss --mount type=bind,source=/home/ubuntu/DockerModels/xssmodel,target=/models/xss -e MODEL_NAME=xss -t tensorflow/serving &

***
Once docker is up you can use the WAF protection for the demo_site.

#Hope you all enjoy from it.



