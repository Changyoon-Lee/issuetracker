#!/usr/bin/python3

##scrapy 실행하기

import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

print('crwaling...')
try:
    execute(['scrapy','crawl','issue'])
except SystemExit:
    pass

print('analysis...')
try:
    execute(['python3','analysis.py'])
except :
    print('fail to analysis')

print('done')
    
