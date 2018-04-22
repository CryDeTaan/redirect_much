#!/usr/bin/env python

"""
    Main program.

"""
import logging
import os
import argparse

import app.core as app

__author__ = 'CryDeTaan'

app_name = 'Redirect Much'
version = '0.1'

ascii_art = f'''
  _____          _ _               _     __  __            _     
 |  __ \        | (_)             | |   |  \/  |          | |    
 | |__) |___  __| |_ _ __ ___  ___| |_  | \  / |_   _  ___| |__  
 |  _  // _ \/ _` | | '__/ _ \/ __| __| | |\/| | | | |/ __| '_  \\ 
 | | \ \  __/ (_| | | | |  __/ (__| |_  | |  | | |_| | (__| | | |
 |_|  \_\___|\__,_|_|_|  \___|\___|\__| |_|  |_|\__,_|\___|_| |_|
                                            v{version} - @{__author__}
'''

"""
URL Redirect Checker
"""
app_log = f'/var/log/{app_name}.log'


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.dirname(os.path.realpath(__file__)) + app_log,
    filemode='a'
)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    '''
    Main entry point
    '''
    print(ascii_art)
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', dest='hosts', help='Input file, one host per line',
                        metavar='<file name>', type=argparse.FileType('rt'), required=True)

    parser.add_argument('--output', dest='output_file', help='Output file name (Optional)',
                        metavar='<file name>',
                        type=argparse.FileType('wt'), required=False)

    args = parser.parse_args()

    if len(os.sys.argv) == 1:
        print(parser.parse_args(['-h']))
        os.sys.exit(1)

    app.run(args.hosts)
    app.output(args.output_file)





