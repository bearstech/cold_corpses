Cold corpses
============

Mad scientist engine for analyzing PHP code.

The analysis is simple, the code is parsed and builtin funcion are extracted.
A list of potentialy dangerous function is used to seek hazardous file.

Usage
-----

Debian:

    apt-get install python-pygments

Virtualenv:

    virtualenv .
    source bin/activate
    pip install -r requirements.txt

Use it:

    ./cold.py /path/to/file/or/folder/with/php

Example:

    $ ./cold.py ~/Downloads/drupal-7.22

    /Users/bob/Downloads/drupal-7.22/modules/simpletest/drupal_web_test_case.php
        ('suspicious_builtin', u'curl_exec')
        ('suspicious_builtin', u'call_user_func_array')

My hazardous function list is short, but Drupal handles it well.
Wordpress is far more evil, and I didn't test plugins yet!

Todo
----

 * √ read and parse PHP source file
 * √ compare builtin with a hazardous function lists
 * _ withelist file (with a sha1 and a path)
 * _ iterative checking with mtime
 * _ using *rdup* for optimizing folder watching

Licence
-------
GPL v3.
