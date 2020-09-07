# chapp

This project is to create a python script that will randomly assign a list of chores to users and then send users a sms message to complete there chores.

## What you'll need

### To send sms messages:

I used twilio to build and send the sms messages. I made a free account [here](http://www.twilio.com)

You will have to add all the phone numbers you want to send messages to in Number -> Phone Numbers -> Add New Number. [Add New Numbers](https://www.twilio.com/console/phone-numbers/verified)

For twiliom, you'll also need to install twilio with `pip install twilio`

Also, make sure to grab your account sid and auth token.

### To audomate the script:
**note** I used a aws ec2 to create a cron to schedule the script to run. This is optional if you don't want the script to run on a schedule, or if you have another way to run the script.

I configured a AWS ec2 instance (t2.micro) to run the script. I configured my ec2 instance with Amazon linux 2, and followed this guide to setup python3 in a env and have the env start at login [link to python3 setup](https://www.youtube.com/watch?v=zwZ5hlxsLks)

Once you Ec2 is up and running you can follow these steps to setup the script to run on a cron:

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

- **optional** Configure ec2 to auto stop and start. Using this guide, configure the ec2 to stop and start on a schedule. [Stop and Start Ec2](https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-cloudwatch/)

### config.py

In the directory with the script, you will need to create a config.py file with the twilio sid and auth token. Also, add a array with user names and phone numbers.
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
   

 
