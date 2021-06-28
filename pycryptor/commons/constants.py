'''This module contains constants that will be used everywhere.
'''

import os

MODULE_DIRECTORY = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
DATA_DIRECTORY = os.path.join(os.path.split(MODULE_DIRECTORY)[0], 'data')