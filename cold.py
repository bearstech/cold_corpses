#!/usr/bin/env python

import sys
from os import walk
import codecs
from os.path import join, isfile

from phply.phplex import lexer
from phply.phpparse import parser
from phply import phpast as php

from pygments.lexers.web import PhpLexer
from pygments.token import Token


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
                print ast
                #if hasattr(ast, 'generic'):
                    #item = ast.generic(with_lineno=True)
                #else:
                    #item = ast
                #print item
                #visitor(item)


def analyze_tokens(tokens):
    for token in tokens:
        if token[0] == Token.Name.Other:
            before = token[1]
        elif token[0] == Token.Name.Builtin:
            yield token
        elif token[0] == Token.Keyword:
            before = token[1]
        elif token == (Token.Punctuation, u'(') and before:
            yield before
        else:
            before = None


SUSPICIOUS = set(u'eval curl_exec base64_decode mail'.split(' '))


def analyze_suspicious_native(tokens):
    for token in tokens:
        if token[0] == Token.Name.Builtin:
            if token[1] in SUSPICIOUS:
                yield token[1]


def lex(path, analyze):
    with open(path, 'r') as f:
        l = PhpLexer()
        for t in analyze(l.get_tokens(f.read())):
            print "\t", t


p = sys.argv[1]
if isfile(p):
    lex(p)
else:
    for root, dirname, names in walk(p):
        for name in names:
            path = join(root, name)
            if isfile(path):
                pp = name.split('.')
                if len(pp) > 1:
                    if pp[-1] == "php":
                        print
                        print path
                        print
                        lex(path, analyze_suspicious_native)
