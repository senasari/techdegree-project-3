import csv_file
import sys


def new_entry_prompt():
    print('Date of the task')
    date = input('Please use DD/MM/YYYY: ')
    title = input('Title of the task: ')
    time_spent = input('Time spent (rounded minutes): ')
    notes = input('Notes (Optional, you can leave this empty): ')
    if not notes:
        notes = ''

    csv_file.add({
        'date': date,
        'title': title,
        'time_spent': time_spent,
        'notes': notes
    })
    print('Your entry has been added. Press enter to return to the menu.')  # TODO: GET BACK WHEN PRESSED ENTER
    input()
    first_menu()


def search_in_entry_prompt():
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
    csv_file.read()
    if option != 'f' and search_entry(option) is None:
        print('There is no such entry. Press enter to return to the search menu.')
        input()
        search_in_entry_prompt()


def search_entry(option):
    entries = None
    if option == 'a':
        print('Enter the date')
        date = input('Please use DD/MM/YYYY: ')
        entries = csv_file.search_entry_by_date(date)
        format_(entries)
    elif option == 'b':
        print('Enter the range of dates')
        date_ranges = input('Please use DD/MM/YYYY-DD/MM/YYYY format: ')
        entries = csv_file.search_by_date_ranges(date_ranges.split('-'))
        format_(entries)
    elif option == 'c':
        string = input('Search in title and notes: ')
        entries = csv_file.search_by_exact_search(string)
        format_(entries)
    elif option == 'd':
        pattern = input('Search by regex pattern: ')
        entries = csv_file.search_by_regex(pattern)
        format_(entries)
    elif option == 'e':
        time = input('Search by time spent: ')
        entries = csv_file.search_by_time_spent(time)
        format_(entries)
    elif option == 'f':
        first_menu()
    return entries


def choose(option):
    option = option.lower()
    if option == 'a':
        new_entry_prompt()
    elif option == 'b':
        # if csv_file.csvfile.exists():
        #     search_in_entry_prompt()
        # else:
        #     print('There is nothing in the folder')
        search_in_entry_prompt()
    elif option == 'c':
        print('Thanks for using the Work Log program!')
        print('Come again soon.')
        csv_file.csvfile.close()
        sys.exit(0)  # TODO: LOOK HERE AGAIN! SEARCH AGAIN!
    else:
        'Not a valid input! Please try a, b, or c.'
        # TODO: BREAK THE LOOP


def format_(my_entries):
    total_result = len(my_entries)
    for entry in my_entries:
        print('Date: {},'.format(entry['date']))
        print('Title: {},'.format(entry['title']))
        print('Time Spent: {},'.format(entry['time_spent']))
        print('Notes: {}'.format(entry['notes']))
        print()
        if total_result == 1:
            print('[E]dit, [D]elete, [R]eturn to search menu')
        else:
            print('[N]ext, [E]dit, [D]elete, [R]eturn to search menu')

        option = input('>')
        option = option.upper()
        while option not in list('NEDR'):
            print('Invalid value! Please try again.')
            option = input('>')

        if option == 'N':
            continue
        elif option == 'E':
            csv_file.edit_entry(entry)
            print('The entry has been deleted. Press enter to return to menu')
            input()
            search_in_entry_prompt()
        elif option == 'D':
            csv_file.delete_entry(entry)
            print('The entry has been deleted. Press enter to return to menu')
            input()
            search_in_entry_prompt()
        elif option == 'R':
            search_in_entry_prompt()


def first_menu():
    print('WORK LOG')
    print('What would you like to do?')
    print('a) Add new entry \n'
          'b) Search in existing entry \n'
          'c) Quit program')
    my_option = input('>')
    choose(my_option)


# with open('entries.csv', 'r') as myfile:
#     reader = csv.DictReader(myfile)
#     for row in reader:
#         print(row['title'])  #TODO: CAN DELETE AFTER DONE WITH

first_menu()  # TODO: Learn what being in --main-- does vs normal
