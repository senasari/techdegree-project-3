from datetime import datetime
from os import name, system

import csv
import logging
import re

csvfile = open('entries.csv', 'w', encoding='utf-8')
fieldnames = ['date', 'title', 'time_spent', 'notes']
entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
entry_writer.writeheader()
csvfile.close()

logging.basicConfig(filename='csv_file.log', level=logging.DEBUG)


def clear():
    system('cls') if name == 'nt' else system('clear')


def add(entry):
    csvfile = open('entries.csv', 'a', encoding='utf-8')
    entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    entry_writer.writerow({
            'date': entry['date'],
            'title': entry['title'],
            'time_spent': entry['time_spent'],
            'notes': entry['notes']
        })
    csvfile.close()
    read()


def read():
    csvfile = open('entries.csv', 'r', encoding='utf-8')
    entry_reader = csv.DictReader(csvfile)
    global all_entries
    all_entries = list(entry_reader)
    csvfile.close()


def edit_entry(entry):
    delete_entry(entry)

    edit_option = input('What do you want to edit? ')
    edit_option = edit_option.upper()
    replace_with = input('What do you want to replace with? ')
    while edit_option not in ['DATE', 'TITLE', 'TIME SPENT', 'NOTES']:
        print('Not a valid option please try again.')
        edit_option = input('What do you want to edit? ')
        edit_option = edit_option.upper()
    if edit_option == 'DATE':
        while True:
            try:
                datetime.strptime(replace_with, '%d/%m/%Y')
            except ValueError as err:
                print('Invalid date type. Please try again.')
                logging.info(err)
                print('Please use DD/MM/YYYY')
                replace_with = input('What do you want to replace with? ')
            else:
                break
        entry['date'] = replace_with
    elif edit_option == 'TITLE':
        while not replace_with:
            print('You need to enter something to replace with')
            replace_with = input('What do you want to replace with? ')
        entry['title'] = replace_with
    elif edit_option == 'TIME SPENT':
        while True:
            try:
                timespent = int(replace_with)
            except ValueError as err:
                logging.info(err)
                print('Time spent is an integer value. Please try again.')
            else:
                break
        entry['time_spent'] = timespent
    elif edit_option == 'NOTES':
        while not replace_with:
            print('You need to enter something to replace with.')
            replace_with = input('What do you want to replace with? ')
        entry['notes'] = 'NOTES'
    add(entry)


def delete_entry(entry):
    entry_row = ','.join(entry.values())
    csvfile = open('entries.csv', 'r')
    reader = csv.reader(csvfile)
    rows = []
    for row in reader:
        row = ','.join(row)
        if row != entry_row:
            rows.append(row)
    csvfile.close()
    csvfile = open('entries.csv', 'w')
    for my_row in rows:
        csvfile.write(my_row+'\n')
    csvfile.close()
    return entry


def search_entry_by_date(date):
    searched_entries = []
    for entry in all_entries:
        if entry['date'] == date:
            searched_entries.append(entry)
    return searched_entries


def search_by_date_ranges(dates):
    searched_entries = []
    for entry in all_entries:
        if datetime.strptime(dates[0], '%d/%m/%Y') <= \
                datetime.strptime(entry['date'], '%d/%m/%Y') \
                <= datetime.strptime(dates[1], '%d/%m/%Y'):
            searched_entries.append(entry)
    return searched_entries


def search_by_exact_search(string):
    searched_entries = []
    for entry in all_entries:
        if string in entry['title'] or string in entry['notes']:
            searched_entries.append(entry)
    return searched_entries


def search_by_regex(pattern):
    searched_entries = []
    for entry in all_entries:
        if re.search(r"{}".format(pattern), entry['title']) or\
                re.search(r"{}".format(pattern), entry['notes']):
            searched_entries.append(entry)
    return searched_entries


def search_by_time_spent(time):
    searched_entries = []
    for entry in all_entries:
        if time == entry['time_spent']:
            searched_entries.append(entry)
    return searched_entries


def show_all_entries_by_date():
    for entry, i in zip(all_entries, range(1, len(all_entries)+1)):
        print('Date of the {}. entry: '.format(i)+entry['date'])
