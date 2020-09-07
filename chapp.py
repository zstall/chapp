#!/home/ec2-user/venv/python3/bin/python

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import csv
import datetime
import random
import config

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

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    #account_sid = 'AC86ec70bb391abb2456dc9083df2e9bb5'
    #auth_token = 'd170ffae8a37336aa2bf90e641961446'
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
        print(msg)

    else:
        message = client.messages \
            .create(
                body=msg,
                from_='+19704239976',
                to=phone
            )

        print(message.status)

def build_list(chrs, interval, trace = False):
        lst = []
        lst_one = []
        lst_two = []

        num = 0
        for i in chrs[interval]:
            if num == 0:
                lst_one.append(i)
                num += 1
            else:
                lst_two.append(i)
                num -= 1
        lst.append(lst_one)
        lst.append(lst_two)

        if trace:
            for i in lst:
                print(i)
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

    phones = config.people
    day = datetime.datetime.today().weekday()

    chrs = all_chores()
    todo = build_list(chrs, 'daily')

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
