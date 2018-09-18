from datetime import datetime
from os import name, system

import csv_file
import logging
import sys

logging.basicConfig(filename='work_log.log', level=logging.DEBUG)


def clear():
    """clears the console before moving forward"""
    system('cls') if name == 'nt' else system('clear')


def add_entry_prompt():
    """prompts questions for user to enter info about the entry"""
    while True:
        print('Date of the task')
        date = input('Please use DD/MM/YYYY: ')
        # checks if the input is in date format
        try:
            datetime.strptime(date, '%d/%m/%Y')
        except ValueError as err:
            logging.info(err)
            print(err)
            print('Please try again. Date is not optional.')
            print()
        else:
            break
    while True:
        # checks if the input is empty or not
        title = input('Title of the task: ')
        if title != '':
            break
        else:
            print()
            print('Please type something. Title is not optional.')
    while True:
        # checks if the time spent is an integer
        time_spent = input('Time spent (rounded minutes): ')
        try:
            int(time_spent)
        except ValueError as err:
            logging.info(err)
            print('Time spent has to be an integer. Please try again.')
        else:
            break
    notes = input('Notes (Optional, you can leave this empty): ')
    if not notes:
        notes = ''

    csv_file.add({
        'date': date,
        'title': title,
        'time_spent': time_spent,
        'notes': notes
    })
    print('Your entry has been added. Press enter to return to the menu.')
    input()
    clear()
    first_menu()


def search_in_entry_prompt():
    """prompts options for search"""
    print('Do you want to search by: \n'
          'a) Exact Date \n'
          'b) Range of Dates\n'
          'c) Exact Search \n'
          'd) Regex Pattern\n'
          'e) Time Spent \n'
          'f) Return to menu \n')
    option = input('>')
    option = option.lower()
    while option not in list('abcdef'):
        print('Not a valid option please try again.')
        option = input('>')
    clear()
    csv_file.read()
    search_entry(option)


def search_entry(option):
    """based on the search choice of the user, prompts other questions"""
    global searched_entries
    if option == 'a':
        print()
        csv_file.show_all_entries_by_date()
        print('#These are the entries.')
        print()
        while True:
            try:
                print('Enter the date')
                date = input('Please use DD/MM/YYYY: ')
                datetime.strptime(date, '%d/%m/%Y')
                searched_entries = csv_file.search_entry_by_date(date)
            except ValueError as err:
                print('Invalid date format')
                logging.info(err)
            else:
                break
    elif option == 'b':
        while True:
            try:
                print('Enter the range of dates')
                date_ranges = input('Please use DD/MM/YYYY-DD/MM/YYYY format: ')
                dates = date_ranges.split('-')
                for date in dates:
                    datetime.strptime(date, '%d/%m/%Y')
                searched_entries = csv_file.search_by_date_ranges(dates)
                break
            except ValueError as err:
                print('Invalid format.')
                logging.info(err)
    elif option == 'c':
        string = input('Search in title and notes: ')
        searched_entries = csv_file.search_by_exact_search(string)
    elif option == 'd':
        pattern = input('Search by regex pattern: ')
        while not pattern:
            print('Input should not be entry. Please try again.')
            pattern = input('Search by regex pattern: ')
        searched_entries = csv_file.search_by_regex(pattern)
    elif option == 'e':
        while True:
            try:
                time = input('Search by time spent: ')
                int(time)
            except ValueError as err:
                print('Invalid date format')
                logging.info(err)
            else:
                break
        searched_entries = csv_file.search_by_time_spent(time)
    elif option == 'f':
        first_menu()

    if option != 'f' and not searched_entries:
        print('There is no such entry.'
              ' Press enter to return to the search menu.')
        input()
        clear()
        search_in_entry_prompt()
    if searched_entries is not None:
        format_(searched_entries)
    return searched_entries


def choose(option):
    """does what user chooses to do when the choice is valid,
    otherwise prints out the error message &
    redirects user to the first menu
    """
    option = option.lower()
    clear()
    if option == 'a':
        add_entry_prompt()
    elif option == 'b':
        search_in_entry_prompt()
    elif option == 'c':
        print('Thanks for using the Work Log program!')
        print('Come again soon.')
        sys.exit(0)
    else:
        print('Not a valid input! Please try a, b or c')
        first_menu()


def format_(my_entries):
    """formats the entry for a nice view"""
    i = 0
    bottom_option = None
    total_result = len(my_entries)
    while bottom_option != 'R':
        entry = my_entries[i]
        print('Date: {},'.format(entry['date']))
        print('Title: {},'.format(entry['title']))
        print('Time Spent: {},'.format(entry['time_spent']))
        print('Notes: {}'.format(entry['notes']))
        print()
        # creates options on the entry/entries
        if total_result == 1:
            print('[E]dit, [D]elete, [R]eturn to search menu')
        elif i == total_result - 1:
            print('[P]revious, [E]dit, [D]elete,'
                  ' [R]eturn to search menu')
        elif i == 0:
            print('[N]ext, [E]dit, [D]elete,'
                  ' [R]eturn to search menu')
        else:
            print('[N]ext, [P]revious, [E]dit, [D]elete,'
                  ' [R]eturn to search menu')

        bottom_option = input('>')
        bottom_option = bottom_option.upper()
        clear()
        while bottom_option not in list('NPEDR'):
            if total_result == 1:
                print('[E]dit, [D]elete, [R]eturn to search menu')
            else:
                print('[N]ext, [P]revious, [E]dit,'
                      ' [D]elete, [R]eturn to search menu')
            print('Invalid value! Please try again.')
            bottom_option = input('>')

        if bottom_option == 'N':
            if i == total_result-1:
                print('This is the last entry.')
            else:
                i += 1
            continue
        elif bottom_option == 'P':
            if i == 0:
                print('This is the first entry')
            else:
                i -= 1
            continue
        elif bottom_option == 'E':
            csv_file.edit_entry(entry)
            print('The entry has been edited. Press enter to return to menu')
            input()
            clear()
            search_in_entry_prompt()
            break
        elif bottom_option == 'D':
            csv_file.delete_entry(entry)
            print('The entry has been deleted. Press enter to return to menu')
            input()
            clear()
            search_in_entry_prompt()
            break
        elif bottom_option == 'R':
            search_in_entry_prompt()


def first_menu():
    """provides the user navigation based on the user's choice"""
    print('WORK LOG')
    print('What would you like to do?')
    print('a) Add new entry \n'
          'b) Search in existing entry \n'
          'c) Quit program')
    my_option = input('')
    choose(my_option)


if __name__ == '__main__':
    print('Welcome to the Work Log! Hope you like the program!')
    first_menu()
