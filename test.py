import csv

# csvfile = open('entries.csv', 'r+')
# csvfile.write('merhaba im sena')
# csvfile.close()
#
# csvfile = open('entries.csv', 'a')
# csvfile.write('and i dont know whats wrong')
# csvfile.close()

# for num, line in enumerate(csvfile, 1):
#     if  in line:
#         print 'found at line:', num

csvfile = open('entries.csv', 'r')
reader = csv.reader(csvfile)
rows = []
print(reader)
csvfile.close()
