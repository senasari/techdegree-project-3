import csv
import re

csvfile = open('entries.csv', 'w', encoding='utf-8')
fieldnames = ['date', 'title', 'time_spent', 'notes']
entry_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
entry_writer.writeheader()
csvfile.close()


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
        # TODO: ONE MORE FORMAT CHECK
        entry['date'] = replace_with
    elif edit_option == 'TITLE':
        entry['title'] = replace_with
    elif edit_option == 'TIME SPENT':
        entry['time_spent'] = replace_with
    elif edit_option == 'NOTES':
        entry['notes'] = 'NOTES'
    add(entry)


def delete_entry(entry):
    entry_row = ','.join(entry.values())
    csvfile = open('entries.csv', 'r')
    reader = csv.reader(csvfile)
    rows = []
    for row in reader:
        row = ','.join(row)
        print(row)
        if row != entry_row:
            rows.append(row)
    csvfile.close()
    csvfile = open('entries.csv', 'w')
    writer = csv.writer(csvfile)
    for my_row in rows:
        csvfile.write(my_row+'\n')
    csvfile.close()
    return entry


def search_entry_by_date(date):  # TODO: FORMAT THE DATE INTO AN ACTUAL ONE IF NECESSARY
    searched_entries = []
    for entry in all_entries:
        if entry['date'] == date:
            searched_entries.append(entry)
    return searched_entries


def search_by_date_ranges(dates):  # TODO: FORMAT THE DATE FOR SEARCH
    searched_entries = []
    for entry in all_entries:
        pass


def search_by_exact_search(string):
    searched_entries = []
    for entry in all_entries:
        if string in entry['title'] or string in entry['notes']:
            searched_entries.append(entry)
    return searched_entries


def search_by_regex(pattern):
    searched_entries = []
    for entry in all_entries:
        if re.search(r"{}".format(pattern), entry['title']) or re.search(r"{}".format(pattern), entry['notes']):
            searched_entries.append(entry)
    return searched_entries


def search_by_time_spent(time):
    searched_entries = []
    for entry in all_entries:
        if time == entry['time_spent']:
            searched_entries.append(entry)
    return searched_entries
