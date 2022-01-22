#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Red Dove Consultants Limited
#
import argparse
import logging
import os
import subprocess
import sys

DEBUGGING = 'PY_DEBUG' in os.environ

logger = logging.getLogger(__name__)

def get_ipy():
    if sys.platform == 'darwin':
        return '/Library/Frameworks/IronPython.framework/Versions/2.7.11/bin/ipy.exe'
    return 'ipy'

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
    # aa('--example', help='Example argument')
    options, args = ap.parse_known_args()
    cmd = [get_ipy(), '-X:FullFrames',  '-X:Debug', 'ptest.py']
    cmd.extend(args)
    subprocess.check_call(cmd)

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
