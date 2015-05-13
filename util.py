
import sys
import os
import string

VERSION = 0.3

INTRODUCTION_TEXT = '''
+------------------------------------------------------------------+
| pq                      pqcom                             O - X  |
+------------------------------------------------------------------+
| + | > | = | H | X | i |                                          |
+------------------------------------------------------------------+
| |   |   |   |   |   +---> Open about dialog                      |
| |   |   |   |   |                                                |
| |   |   |   |   +-------> Clear received message                 |
| |   |   |   |                                                    |
| |   |   |   +-----------> Enable/Disable Hex View                |
| |   |   |                                                        |
| |   |   +---------------> Open settings dialog                   |
| |   |                                                            |
| |   +-------------------> Open/Close serial port                 |
| |                                                                |
| +-----------------------> Open a new window                      |
+------------------------------------------------------------------+
|  Keyboard Shortcut                                               |
|      Ctrl + Enter: Send                                          |
+------------------------------------------------------------------+
| + Normal | O Hex | O Extend | * | History |    | # Repeat | Send |
+------------------------------------------------------------------+
'''

TRANS_STRING = ''.join(chr(i) for i in range(0, 0x20) + range(0x80, 0x100))
TRANS_TABLE = string.maketrans(TRANS_STRING, ''.ljust(len(TRANS_STRING), '.'))


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', script_path)
    return os.path.join(base_path, relative_path)
