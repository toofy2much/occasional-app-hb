import os
import json


def reminder_json_exists():
    return os.path.isfile('reminder.json')


def read_reminder_json():
    if reminder_json_exists():
        with open('reminder.json') as reminder_json:
            data = json.load(reminder_json)
            return data['reminders']
    else:
        return {}


def create_reminder_json(reminder):
    if not reminder_json_exists():
        data = {}
        data['reminders'] = []
        data['reminders'].append(reminder)
        write_reminder_json(data)
    else:
        update_reminder_json(reminder)


def update_reminder_json(reminder):
    with open('reminder.json') as reminder_json:
        data = json.load(reminder_json)
        reminders = data['reminders']
        reminders.append(reminder)
        write_reminder_json(data)


def write_reminder_json(data, filename='reminder.json'):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)