# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from OnlineModel import Facility
from OnlineModel.Export.HolyList import HolyList

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    SF=Facility.SwissFEL()
    HL=HolyList('test.xls')
    HL.append('Phase Current')
    SF.writeFacility(HL)
    HL.close()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
