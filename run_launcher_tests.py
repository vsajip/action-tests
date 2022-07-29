#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Vinay Sajip
#
import argparse
import datetime
import logging
import os
import subprocess
import sys
import time

DEBUGGING = 'PY_DEBUG' in os.environ

logger = logging.getLogger(__name__)

def tod():
    return datetime.datetime.now().strftime('%H:%M')

def main():
    fn = os.path.basename(__file__)
    fn = os.path.splitext(fn)[0]
    lfn = os.path.expanduser('~/logs/%s.log' % fn)
    if os.path.isdir(os.path.dirname(lfn)):
        logging.basicConfig(level=logging.DEBUG, filename=lfn, filemode='w',
                            format='%(message)s')
    adhf = argparse.ArgumentDefaultsHelpFormatter
    ap = argparse.ArgumentParser(formatter_class=adhf, prog=fn)
    aa = ap.add_argument
    # aa('input', metavar='INPUT', help='File to process')
    # aa('--flag', '-f', value=False, action='store_true', help='Option')
    options = ap.parse_args()
    print('%s Running console executable ...' % tod())
    cmd = [os.path.join('test', 'test.exe'), '10']
    p = subprocess.Popen(cmd)
    print('%s Waiting 5 secs ...' % tod())
    time.sleep(5)
    rc = p.poll()
    if rc is not None:
        raise ValueError('Console executable is not running!')
    print('%s Trying to stop console executable ...' % tod())
    p.kill()
    print('%s Waiting 500 msecs ...' % tod())
    time.sleep(0.5)
    rc = p.poll()
    if rc is None:
        raise ValueError('Failed to stop console executable')
    print('%s Console executable stopped with return code: %s' % (tod(), rc))
    print('%s Running windowed executable ...' % tod())
    cmd = [os.path.join('test', 'testw.exe')]
    p = subprocess.Popen(cmd)
    time.sleep(5)
    print('%s Trying to stop windowed executable ...' % tod())
    p.kill()
    time.sleep(0.5)
    rc = p.poll()
    if rc is None:
        raise ValueError('Failed to stop windowed executable')
    print('%s Windowed executable stopped with return code: %s' % (tod(), rc))


if __name__ == '__main__':
    try:
        rc = main()
    except KeyboardInterrupt:
        rc = 2
    except Exception as e:
        if DEBUGGING:
            s = ' %s:' % type(e).__name__
        else:
            s = ''
        sys.stderr.write('Failed:%s %s\n' % (s, e))
        if DEBUGGING: import traceback; traceback.print_exc()
        rc = 1
    sys.exit(rc)
