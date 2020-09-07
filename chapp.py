#!/home/ec2-user/venv/python3/bin/python

"""
Author: Zachary Stall
Date: 9/6/2020
Description: This script take a dictionary of 'chores' and assigns them randomly
to users. The users and their information are saved in a seperate config file along with
other sensitive information. The script then uses these lists of chores to send them to
the users via sms message through an api request to twilio.
"""


# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import csv
import datetime
import random
import config
import sys

# Send a message using twilio. The follow vars are needed:
#   chr     - array of Chores
#   nm      - str name of user
#   phone   - str phone number of user
#   wchr    - array of weekly chores
#   Day     - string var of which day of the week it is, Mon - 0 Sunday - 6
#   trace   - trace is a var for debugging defaults to False

def send_message(chr, nm, phone, wchr, day, trace=False):

    # client config information for twilio for config file
    client = Client(config.account_sid, config.auth_token)

    # Building the message for the users
    msg = '****************************************' + '\n'
    msg += nm + ' here are your Chores: '

    for i in chr:
        msg += '\n' + '- ' + i

    if day == 0:
        msg += '\n' + '****************************************'
        msg += '\n' 'Here is your weekly chores:'
        for i in wchr:
            msg += '\n' + '- ' + str(i)
    else:

        msg += '\n' + '****************************************'
        msg += '\n' "Don't forget your weekly chores: "
        for i in wchr:
            msg += '\n' + '- ' + str(i)

    msg += '\n' + '****************************************'

    # debugging if trace true will print message to command line
    if trace:
        print()
        print("*********** MESSAGE DEBUG **************")
        print(msg)
        print("********* END MESSAGE DEBUG ************")
        print()

    # if trace is false, send message!
    else:
        message = client.messages \
            .create(
                body=msg,
                from_='+19704239976',
                to=phone
            )

        print(message.status)

#
def build_list(chrs, interval, trace = False):
        # original array of full list of chores
        lst = chrs[interval]
        # Seperate lists of random chores to be done
        lst_one = []
        lst_two = []

        # num is a var used to switch between lists
        num = 0

        # while loop to randomize selections for lists
        while len(lst) > 0:

            if num == 0:
                # Randomly remove one item from full list and add it to list one
                lst_one.append(lst.pop(random.randint(0,len(lst)-1)))
                num += 1
            else:
                # Randomly remove one item from full list and add it to list two
                lst_two.append(lst.pop(random.randint(0,len(lst)-1)))
                num -= 1

        lst.append(lst_one)
        lst.append(lst_two)

        if trace:
            n = 0
            print()
            print("******** Build List DEBUG MODE **********")
            for i in lst:
                print('List Number: ' + str(n))
                print(i)
                n += 1
            print("******* END Build List DEBUG MODE *******")
            print()
        return lst

def get_chores_dic(file):

    rd = csv.reader(open(file))
    dic = {}

    for row in rd:
        key = row[0]
        dic[key] = row[1:]

    return dic

def add_chores_dic(chores, file):

    daily = ['daily']
    weekly = ['weekly']

    for c in chores['daily']:
        daily.append(c)

    for c in chores['weekly']:
        weekly.append(c)

    file = open(file, "w")
    writer = csv.writer(file)

    writer.writerow(daily)
    writer.writerow(weekly)

    file.close()

def get_chores_array(chr_file):
    with open(chr_file, newline='') as csvfile:
        chr_array = list(csv.reader(csvfile))

    return chr_array

def add_chores_array(file, chr):
    arr = []
    arr.append(chr)
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in arr:
            writer.writerow(i)

def main():

    # Trace is a var used for testing. If True messages wont be sent and methods will
    # print outputs to command line
    trace = True
    # Get all chores from csv file and create a dictionary
    chrs = get_chores_dic('all_chores.csv')
    # Check for user inputs, -h or -help will print help text, or if user appends
    # <interval> <new chore> it will be added to csv file
    if len(sys.argv) == 2:
        if sys.argv[1]=='-h' or sys.argv[1]=='-help':
            print("""
                This script will randomly divide and send chores stored in the all_chores.csv file.
                To add new chores run ./chapp.py <interval> <new chore> and the script will add the
                new chore to the csv file.
            """)
            exit()
        else:
            print('Invalid input')
            exit()
    # Checking for new chores
    elif len(sys.argv) > 2:
        interval = sys.argv[1].islower()
        new_chore = sys.argv[2]
        chrs[interval].append(new_chore)
        add_chores_dic(chrs, 'all_chores.csv')

    # Get names and phone numbers from seperate file
    phones = config.people
    # Get day to determine if new weekly chores are needed
    day = datetime.datetime.today().weekday()
    # Buile list of daily chores for users
    todo = build_list(chrs, 'daily', trace)

    # if Day is Monday (0) then build a new list of weekly chores
    if day == 0:
        wk = build_list(chrs, 'weekly', trace)
        # Add the new lists to the user csvs
        add_chores_array('zach.csv', wk[0])
        add_chores_array('caitlin.csv', wk[1])

    # If not monday, used the weekly chores stored in the csv
    else:
        wk = get_chores_array('zach.csv')
        wk_two = get_chores_array('caitlin.csv')
        for i in wk_two:
            wk.append(i)

    # Send the messages to the users!
    send_message(todo[0], phones[0][0], phones[0][1], wk[0], day, trace)
    send_message(todo[1], phones[1][0], phones[1][1], wk[1], day, trace)


if __name__=="__main__":
    main()
