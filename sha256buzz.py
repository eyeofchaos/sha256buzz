# sha256buzz v0.1
#
# Copyright (c) 2024 Dieter Schmitt
# Released under the MIT license - https://opensource.org/licenses/MIT
#

#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import hashlib
import re
import codecs
import time

arg      =  sys.argv[1] if len(sys.argv) > 1 else ''
self     =  os.path.basename(__file__)
sums     =  'sha256buzz-checksums.txt'
results  =  'sha256buzz-results.html'

def create():

    def readsum(obj):
        s = hashlib.sha256()
        while True:
            BLOCKSIZE = 8192
            data = obj.read(BLOCKSIZE)
            if not data:
                break
            s.update(data)
        return s.hexdigest()

    output = ''

    for root, dirs, files in os.walk(u'.'):
        for name in files:
            if name == self or name == sums or name == results:
                continue
            checkfile = root + '/' + name
            try:
                f = open(checkfile, 'rb')
                g = readsum(f)
                checkfile = re.sub(r'\\', '/', checkfile)
                l = g + ' *' + checkfile
                print(l)
                l = l + '\r\n'
            except IOError as e:
                errno, strerror = e.args
                l = ''
                print('File "' + checkfile + '" could not be read!')
            output = output + l

    f = codecs.open(sums, encoding='UTF-8', mode='w')
    f.write(output)
    f.close()

def check():

    def readsum(obj):
        s = hashlib.sha256()
        while True:
            BLOCKSIZE = 8192
            data = obj.read(BLOCKSIZE)
            if not data:
                break
            s.update(data)
        return s.hexdigest()

    c = codecs.open(sums, encoding='UTF-8', mode='r').read()
    c = c.splitlines()
    error = 0

    r = codecs.open(results, encoding='UTF-8', mode='w')
    t = time.strftime('%d.%m.%Y %H:%M:%S')

    r.write('<!DOCTYPE html>\r\n\r\n<html lang="en">\r\n')
    r.write('<head>\r\n<meta charset="utf-8">\r\n<title>sha256buzz</title>\r\n<style>\r\nbody { font-family: monospace; font-size: 12px; }\r\ntable { border: 1px solid gray; width: 1150px; table-layout: fixed; }\r\ntr.green { background-color: #88be67; }\r\ntr.yellow { background-color: #fff15f; }\r\ntr.red { background-color: #f18f4e; }\r\ntd { padding: 2px; vertical-align: top; overflow: hidden; }\r\n</style>\r\n</head>\r\n')
    r.write('<body>\r\n\r\n<p>' + t + '</p>\r\n<h1>Ergebnisse von sha256buzz</h1>\r\n\r\n')
    r.write('<table>\r\n<colgroup>\r\n<col style="width: 270px;">\r\n<col style="width: 700px;">\r\n<col>\r\n</colgroup>\r\n')

    for i in range(len(c)):
        c[i] = c[i].split(' *')
        try:
            f = open(c[i][1], 'rb')
            g = readsum(f)
        except IOError as e:
            errno, strerror = e.args
            g = 'No checksum possible'
        if c[i][0] == g:
            print(g + ' *' + c[i][1] + ' => Ok')
            r.write('<tr class="green"><td>' + g + '</td><td>' + c[i][1] + '</td><td>Ok</td></tr>\r\n')
        elif c[i][0] != g and g != 'No checksum possible':
            print(g + ' *' + c[i][1] + ' => Changed')
            r.write('<tr class="yellow"><td>' + g + '</td><td>' + c[i][1] + '</td><td>Changed</td></tr>\r\n')
            error = 1
        elif c[i][0] != g and g == 'No checksum possible':
            print(g + ' *' + c[i][1] + ' => File not found')
            r.write('<tr class="red"><td>' + g + '</td><td>' + c[i][1] + '</td><td>File not found</td></tr>\r\n')
            error = 1

    r.write('</table>\r\n')

    if error == 0:
        print('\r\nAll files are Ok.')
        r.write('\r\n<p>All files are Ok.</p>\r\n')

    elif error == 1:
        print('\r\nNot all files are identical! Check output.')
        r.write('\r\n<p>Not all files are identical! Check output.</p>\r\n')

    r.write('\r\n</body>\r\n</html>')
    r.close()


if arg == '':
    create()
elif arg == '-c':
    check()
else:
    print('\r\nNo suitable argument found.')

print('\r\nDone.')
