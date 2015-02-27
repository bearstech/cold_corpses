#!/usr/bin/env python

import sys
from os import walk
from os.path import join, isfile, getmtime

from pygments.lexers.web import PhpLexer
from pygments.token import Token


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


class Hazardous(object):
    def __init__(self):
        self.hazardous = set()
        raw = {
            'eval': u'eval',
            'obfscure': u'str_rot13 base64_decode',
            'network': u'curl_exec mail socket_connect',
            #'dynamic_func': u'call_user_func call_user_func_array call_user_method call_user_method_array',
            'compression': u'lzw_decompress', # Check if it's inline compression.
            'shell': u'exec system passthru pcntl_exec popen proc_open shell_exec'
        }
        for kind, functions in raw.items():
            self.hazardous |= set(functions.split(u' '))

    def __contains__(self, needle):
        return needle in self.hazardous


SUSPICIOUS = Hazardous()

# http://fr.php.net/manual/en/features.safe-mode.functions.php
TOO_LARGE = 512


def analyze_suspicious_native(tokens):
    for token in tokens:
        if token[0] in [Token.Literal.String.Double, Token.Literal.String.Single]:
            if len(token[1]) > TOO_LARGE:
                yield 'large_string', len(token[1])
        if token[0] == Token.Name.Builtin:
            if token[1] in SUSPICIOUS:
                yield 'suspicious_builtin', token[1]


def lex(path, analyze):
    with open(path, 'r') as f:
        l = PhpLexer()
        for t in analyze(l.get_tokens(f.read())):
            yield t


def suspicious(path):
    suspicious = list(lex(path, analyze_suspicious_native))
    if suspicious:
        print
        print path
        for s in suspicious:
            print "\t", s[0], s[1]


p = sys.argv[1]
last_time = 0
if isfile(p):
    suspicious(p)
else:
    for root, dirname, names in walk(p):
        for name in names:
            path = join(root, name)
            if not isfile(path):
                continue
            pp = name.split('.')
            if len(pp) > 1 and pp[-1] in ["php", "module", "inc", "txt"]:
                mtime = getmtime(path)
                if mtime <= last_time:  # deja vue
                    continue
                suspicious(path)
