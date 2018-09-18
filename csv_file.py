from datetime import datetime
from os import name, system, path

import csv
import logging
import re

fieldnames = ['date', 'title', 'time_spent', 'notes']
# to record the entries into csv file we need to initialize the csv file
if not path.isfile('entries.csv'):
    csvfile = open('entries.csv', 'w', encoding='utf-8')
    entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    entry_writer.writeheader()
    csvfile.close()

logging.basicConfig(filename='csv_file.log', level=logging.DEBUG)


def clear():
    """clears the console"""
    system('cls') if name == 'nt' else system('clear')


def add(entry):
    """records the entry into a row of the csv file."""
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
    """to get all the recent entries we're opening and reading the file
    & store the entries in global variable called all_entries
    """
    csvfile = open('entries.csv', 'r', encoding='utf-8')
    entry_reader = csv.DictReader(csvfile)
    global all_entries
    all_entries = list(entry_reader)
    csvfile.close()


def edit_entry(entry):
    """to edit the entry, we first delete the entry
    & resubmit the entry
    """
    delete_entry(entry)

    edit_option = input('What do you want to edit? ')
    edit_option = edit_option.upper()
    replace_with = input('What do you want to replace with? ')
    # checks if the option is one of the following
    while edit_option not in ['DATE', 'TITLE', 'TIME SPENT', 'NOTES']:
        print('Not a valid option. Please use one of the following.')
        print('[DATE, TITLE, TIME SPENT, NOTES]')
        edit_option = input('What do you want to edit? ')
        edit_option = edit_option.upper()
    if edit_option == 'DATE':
        while True:
            try:
                # checking if the entry fits the date format
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
        # checks if the thing that's going to be replaced is empty
        while not replace_with:
            print('You need to enter something to replace with')
            replace_with = input('What do you want to replace with? ')
        entry['title'] = replace_with
    elif edit_option == 'TIME SPENT':
        # checks if time spent is an integer as it supposed to be.
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
        entry['notes'] = replace_with
    add(entry)


def delete_entry(entry):
    """deletes the entry by rewriting everything except the entry"""
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
    """when given date returns the entry/entries with that date"""
    searched_entries = []
    for entry in all_entries:
        if entry['date'] == date:
            searched_entries.append(entry)
    return searched_entries


def search_by_date_ranges(dates):
    """when given dates, returns the date/dates within those dates"""
    searched_entries = []
    for entry in all_entries:
        if datetime.strptime(dates[0], '%d/%m/%Y') <= \
                datetime.strptime(entry['date'], '%d/%m/%Y') \
                <= datetime.strptime(dates[1], '%d/%m/%Y'):
            searched_entries.append(entry)
    return searched_entries


def search_by_exact_search(string):
    """when given a string, returns the entry/entries that contain the string"""
    searched_entries = []
    for entry in all_entries:
        if string in entry['title'] or string in entry['notes']:
            searched_entries.append(entry)
    return searched_entries


def search_by_regex(pattern):
    """returns the entry/entries, notes of which conforms to the regex pattern given"""
    searched_entries = []
    for entry in all_entries:
        if re.search(r"{}".format(pattern), entry['title']) or\
                re.search(r"{}".format(pattern), entry['notes']):
            searched_entries.append(entry)
    return searched_entries


def search_by_time_spent(time):
    """returns the entry/entries with the same time_spent value"""
    searched_entries = []
    for entry in all_entries:
        if time == entry['time_spent']:
            searched_entries.append(entry)
    return searched_entries


def show_all_entries_by_date():
    """to show all the dates of the entries before asking for a certain date"""
    for entry, i in zip(all_entries, range(1, len(all_entries)+1)):
        print('Date of the {}. entry: '.format(i)+entry['date'])
