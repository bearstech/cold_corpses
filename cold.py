#!/usr/bin/env python

import json

def parse(ast):
    name = ast[0]
    values = ast[1:]
    if name == u"StmtList":
        stmtlist(values)
    elif name == u"ExprStmt":
        exprStmt(values)
    elif name == "FinalDef":
        pass
    elif name == "FuncDef":
        funcDef(values)
    elif name == "Assign":
        assign(values)
    elif name == "Call":
        call(values)
    elif name == "If":
        if_(values)
    else:
        print "DON'T KNOW", name


def stmtlist(args):
    print "StmtList", len(args[0])
    #print "\t", args
    for e in args[0]:
        parse(e)


def exprStmt(args):
    """args[1] : token
    """
    print "ExprStmt", len(args)
    parse(args[0])


def assign(args):
    """args[0] = args[2]
    args[1] description
    """
    print "Assign", len(args), args[0]
    print "\t", args[2]
    parse(args[2])


def call(args):
    """args[0] function
    args[1]: token
    """
    print "Call", len(args), list(find_token(args))


def if_(args):
    """
    0: token

    """
    print "If", len(args)
    print "\t", args[1]


def find_token(args):
    if type(args) == list:
        for a in args:
            for r in find_token(a):
                yield r
    elif type(args) == dict:
        if u'token' in args:
            yield args['token'][1]


def funcDef(args):
    print "FuncDef"
    #print "\t", args
    #parse(args)


with open('test.json', 'r') as f:
    ast = json.load(f)
    for e in ast:
        parse(e)
    #for e in ast:
        #print "TYPE", e[0]
        #if e[0] == u'StmtList':
            #for s in e[1:]:
                #print "TYPE", s[0][0]
                #if s[0][0] == 'ExprStmt':
                    #exprs = s[0][1:]
                    #for expr in exprs:
                        #print "\t", expr
