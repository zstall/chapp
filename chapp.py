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

# Get all chores.
def all_chores():

    chrs = {'daily':['Start/fold/put away load of laundry',
                    'Clean litterbox',
                    'Sweep kitchen/dining/litterbox area',
                    'Wash bottles/pump parts',
                    'Wipe down surfaces',
                    'Clean kitchen',
                    'Pick up living room',
                    'Make bed', 'Poop worms',
                    'Load/run dishwasher',
                    'Empty dishwasher',
                    'Empty garbages/recycling',
                    'Potty pads',
                    'Brush Leelas teeth'],
            'weekly':['Clean bathrooms',
                    'Vacuum',
                    'Mop floors',
                    'Clean out refrigerator'],
            'bi-weekly':['Dust',
                        'Wash sheets',
                        'Organize shelves'],
            'monthly':['Fully empty/clean litterbox and replace litter]']}

    return chrs


def send_message(chr, nm, phone, wchr, day, trace=False):

    client = Client(config.account_sid, config.auth_token)
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

    if trace:
        print()
        print("*********** MESSAGE DEBUG **************")
        print(msg)
        print("********* END MESSAGE DEBUG ************")
        print()

    else:
        message = client.messages \
            .create(
                body=msg,
                from_='+19704239976',
                to=phone
            )

        print(message.status)

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

def get_chores(chr_file):
    with open(chr_file, newline='') as csvfile:
        chr_array = list(csv.reader(csvfile))

    return chr_array

def add_chores(file, chr):
    arr = []
    arr.append(chr)
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in arr:
            writer.writerow(i)

def main():

    trace = True

    chrs = all_chores()

    if len(sys.argv) > 1:
        interval = sys.argv[1]
        new_chore = sys.argv[2]
        chrs[interval].append(new_chore)
        print(chrs[interval])
    phones = config.people
    day = datetime.datetime.today().weekday()


    todo = build_list(chrs, 'daily', trace)

    k = random.randint(0, 1)


    if day == 0:
        wk = build_list(chrs, 'weekly')

        if k == 1:
            add_chores('zach.csv', wk[0])
            add_chores('caitlin.csv', wk[1])
            send_message(todo[0], phones[0][0], phones[0][1], wk[0], day, trace)
            send_message(todo[1], phones[1][0], phones[1][1], wk[1], day, trace)
        else:
            add_chores('zach.csv', wk[1])
            add_chores('caitlin.csv', wk[0])
            send_message(todo[1], phones[0][0], phones[0][1], wk[1], day, trace)
            send_message(todo[0], phones[1][0], phones[1][1], wk[0], day, trace)
    else:
        wk = get_chores('zach.csv')
        wk_two = get_chores('caitlin.csv')

        for i in wk_two:
            wk.append(i)

        send_message(todo[0], phones[0][0], phones[0][1], wk[0], day, trace)
        send_message(todo[1], phones[1][0], phones[1][1], wk[1], day, trace)


if __name__=="__main__":
    main()
