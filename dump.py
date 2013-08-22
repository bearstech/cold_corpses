#!/usr/bin/env python

import sys
from os import walk
import codecs
from os.path import join, isfile

from phply.phplex import lexer
from phply.phpparse import parser
from phply import phpast as php


def visitor(l):
    if type(l) is list:
        for ll in l:
            visitor(ll)
    else:
        name = l[0]
        args = l[1:]
        if name == "FunctionCall":
            print l
        for arg in args:
            if type(arg) is list:
                for i in list:
                    visitor(l)
            if type(arg) is dict:
                for a in ['node', 'nodes', 'params']:
                    if a in arg:
                        visitor(arg[a])


def analyze(path):
    with codecs.open(path, 'r', 'latin1') as f:
        src = f.read()
        try:
            items = parser.parse(src, tracking=True, lexer=lexer.clone())
        except SyntaxError as e:
            print "Syntax Error", e.filename, e
        except ValueError as e:
            print "Syntax Error", e
        else:
            for ast in items:
                if hasattr(ast, 'generic'):
                    item = ast.generic(with_lineno=True)
                else:
                    item = ast
                print item
                #visitor(item)



p = sys.argv[1]
if isfile(p):
    analyze(p)
else:
    for root, dirname, names in walk(p):
        for name in names:
            path = join(root, name)
            if isfile(path):
                pp = name.split('.')
                if len(pp) > 1:
                    if pp[-1] == "php":
                        print path
                        analyze(path)
