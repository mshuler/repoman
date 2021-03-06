# -*- coding: utf-8 -*-
#
# © 2010 SimpleGeo, Inc. All rights reserved.
# Author: Ian Eure <ian@simplegeo.com>
#

"""Unit tests for the repoman client."""

import os
import repoman.client as client


def check_parsing(changefile, expected):
    """Verify that parsing succeds with problematic .changes files."""
    with open("%s/changefiles/%s" % (os.path.dirname(__file__), changefile),
                                     'r') as change:
        changes = change.read()
        parsed = client._parse_changes(changes)
        assert len(parsed) == 2
        assert set(parsed[1]) == set(expected), \
            "Incorrect result: %r" % \
            set(parsed[1]).symmetric_difference(set(expected))

        for file_ in parsed[1]:
            assert file_ in expected


def test_parsing():
    expected = ("puppet_0.25.5-sg1.dsc",
                "puppet_0.25.5.orig.tar.gz",
                "puppet_0.25.5-sg1.debian.tar.gz",
                "puppet_0.25.5-sg1_all.deb",
                "puppetmaster_0.25.5-sg1_all.deb",
                "puppet-common_0.25.5-sg1_all.deb",
                "vim-puppet_0.25.5-sg1_all.deb",
                "puppet-el_0.25.5-sg1_all.deb",
                "puppet-testsuite_0.25.5-sg1_all.deb")

    fixture_dir = os.path.dirname(__file__) + '/changefiles/'
    for change in (os.listdir(fixture_dir)):
        yield (check_parsing, change, expected)


def test_explode_slashes():
    unexploded = ['foo/bar', 'baz']
    expected = ('foo', 'bar', 'baz')
    func = lambda foo, bar, baz: (foo, bar, baz)
    exploded = client.explode_slashes(func)(*unexploded)
    assert exploded == expected, \
        "Expected %r, got %r" % (expected, exploded)


def test_bad_docs():
    """Make sure help works even if docblocks are missing."""
    client.cmd_fake = lambda: None
    help_str = client.get_commands()
    assert "fake" in help_str


def test_help_commands():
    """Make sure help with no args shows commands."""
    assert client.cmd_help() == client.get_commands()


def check_decorated_function_docs(name):
    assert getattr(getattr(client, 'cmd_%s' % name), '__doc__')


def test_decorated_function_docs():
    """Make sure decorated functions retain their documentation."""
    for func in ('rm', 'show', 'promote'):
        yield (check_decorated_function_docs, func)
