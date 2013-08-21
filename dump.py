#!/usr/bin/env python

import sys
from os.path import walk, join, isfile

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
    with open(path, 'r') as f:
        try:
            items = parser.parse(f.read(), tracking=True, lexer=lexer)
        except SyntaxError as e:
            print "Syntax Error", e
            raise e
        else:
            for ast in items:
                if hasattr(ast, 'generic'):
                    item = ast.generic(with_lineno=True)
                else:
                    item = ast
                print item
                #visitor(item)


def tree(arg, dirname, names):
    for name in names:
        path = join(dirname, name)
        if isfile(path):
            pp = name.split('.')
            if len(pp) > 1:
                if pp[-1] == "php":
                    print path
                    analyze(path)

p = sys.argv[1]
if isfile(p):
    analyze(p)
else:
    walk(p, tree, None)
