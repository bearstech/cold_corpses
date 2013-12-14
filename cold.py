#!/usr/bin/env python

import sys
from os import walk
import codecs
from os.path import join, isfile

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


SUSPICIOUS = set(u'eval curl_exec base64_decode mail call_user_func \
                 call_user_func_array call_user_method call_user_method_array\
                 socket_connect'.split(' '))
TOO_LARGE = 512


def analyze_suspicious_native(tokens):
    for token in tokens:
        #if token[0] in [ Token.Literal.String.Double, Token.Literal.String.Single]:
            #if len(token[1]) > TOO_LARGE:
                #yield 'large_string', token[1]
        if token[0] == Token.Name.Builtin:
            if token[1] in SUSPICIOUS:
                yield 'suspicious_builtin', token[1]


def lex(path, analyze):
    with open(path, 'r') as f:
        l = PhpLexer()
        for t in analyze(l.get_tokens(f.read())):
            yield t


p = sys.argv[1]
if isfile(p):
    lex(p, analyze_suspicious_native)
else:
    for root, dirname, names in walk(p):
        for name in names:
            path = join(root, name)
            if isfile(path):
                pp = name.split('.')
                if len(pp) > 1:
                    if pp[-1] == "php":
                        suspicious = list(lex(path, analyze_suspicious_native))
                        if suspicious:
                            print
                            print path
                            for s in suspicious:
                                print "\t", s
