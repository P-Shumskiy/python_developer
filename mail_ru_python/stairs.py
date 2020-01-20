import sys


rows_number = int(sys.argv[1])
symbol = '#'

for current_row in range(1, rows_number + 1):
    print(" "*(rows_number - current_row), symbol*current_row, sep='')
