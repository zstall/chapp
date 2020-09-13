# chapp

This project is a python script that will randomly assign a list of chores to users and then send users a sms message to complete their chores. A quick overview of how the scripts works includes a csv with a list of daily and weekly chores. The script takes these chores and divides them up randomly and evenly. Each day users are assigned new chores, and the script tracks weekly chores and refreshes these every Monday.

To achieve this I use:
- Twilio to send sms messages
- AWS EC2 to run a small server to run the script on a cron
- AWS Lambda to start and stop the EC2 on a schedule
- Three csv files to store chores and track weekly chores for two users
- two py files, one for the script and a second to store credential/personal information (like names, phone numbers, and twilio api information)

**note** This is currently configured to work for two people, but I will be updating it to work for any number of people.

## What you'll need

### Files:
- chapp.py => main script
- all_chores.csv => list of chores, sample included
- user_one.csv and user_two.csv => empty csv for saving weekly chores
- config.py => more details below

### Twilio => To send sms messages:

I used twilio to build and send the sms messages. I made a free account [here](http://www.twilio.com)

You will have to add all the phone numbers you want to send messages to in Number -> Phone Numbers -> Add New Number. [Add New Numbers](https://www.twilio.com/console/phone-numbers/verified)

For twilio, you'll also need to install twilio with `pip install twilio`

Also, make sure to grab your account SID and auth token for the config.py file (more on that below).

### AWS => To audomate the script:
**note** I used an AWS EC2 instance to create a cron to schedule for the script to run. This is optional if you don't want the script to run on a schedule, or if you have another way to run the script.

I configured an AWS EC2 instance (t2.micro) to run the script. I configured my EC2 instance with Amazon linux 2, and followed this guide to setup python3 in a virtual environment (env) and had this environment start at login [link to python3 setup](https://www.youtube.com/watch?v=zwZ5hlxsLks)

Once your EC2 is up and running you can follow these steps to setup the script to run on a cron:

- Copy all files attached including a config.py file (more on that later) to the ec2-user home directory. I did this by using the following commands in the directory with my project:
   `scp -i /<path to pem file>/<my pem file> /<path to project>/*.py ec2-user@<ip of ec2>:~/`
   and
   `scp -i /<path to pem file>/<my pem file> /<path to project>/*.csv ec2-user@<ip of ec2>:~/`
      
- Chmod the files:
    `chmod 600 config.py`
    `chmod 600 *.csv`
    `chmod 700 chapp.py`
    
- Setup cron to schedule script execution. Enter crontab by entering the following:
    `crontab -e`
    Enter a new line in crontab. Example:
    
      `0 7 * * ? * /home/ec2-user/chapp.py`
      
     The example aboce will execute the script evert dat at 7 am. 
     :note: Run `date` on the ec2 to find the timezone on the serer, and configure your cron accordingly.

- **optional** Configure the EC2 instance to auto stop and start. Using this guide, configure the EC2 instance to stop and start on a schedule. [Stop and Start Ec2](https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/)

### config.py

In the directory with the script, you will need to create a config.py file with the twilio SID and auth token. Also, add a array with user names and phone numbers.
**note** Script is configured for two users, next update will allow for any number of users.
example config:

```
account_sid = '<your sid>'
auth_token = '<your auth token>'
people = [['<user 1>','15555555555'],['<user 2>','155555555555']]
``` 

### *.csv files

User1 and user2 csv files are to store the weekly chores and should not need to be changed.
all_chores.csv is where a user can enter daily or weekly chores. Append the chores with a comma. Chores can also be appended running the script with arguments:
   `./chapp.py <daily or weekly> <new chore to add>`
   

 
