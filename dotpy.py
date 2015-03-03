#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'sng2c'


class DotFile:
    homebase = None
    dotbase = None

    def __init__(self, filename):
        self.filename = filename

    def path(self):
        return os.path.join(self.homebase, self.filename)

    def dotpath(self):
        return os.path.join(self.dotbase, self.filename)

    def realpath(self):
        return os.path.realpath(os.path.join(self.homebase, self.filename))

    def isLink(self):
        return os.path.islink(self.path())

    def isManaged(self):
        contained = os.path.dirname(self.realpath())
        return self.isLink() and contained == self.dotbase

    def isLinkedWell(self):
        return self.isManaged() and os.path.exists(self.realpath())

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return self.filename

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.path())

    def __eq__(self, other):
        return hash(self) == hash(other)


import argparse
import os

HOME = os.environ.get("HOME")
DOT_BASE = os.path.abspath("%s/dotfiles" % HOME)
if not os.path.exists(DOT_BASE): os.mkdir(DOT_BASE, 0755)

DotFile.homebase = HOME
DotFile.dotbase = DOT_BASE

import re
# dotfile들을 나열한다.
home_dotfiles = set(DotFile(dot) for dot in os.listdir(HOME) if re.match(r"\.[^\.].*", dot))
base_dotfiles = set(DotFile(dot) for dot in os.listdir(DOT_BASE) if re.match(r"\.[^\.].*", dot))
managed = set(dot for dot in home_dotfiles if dot.isManaged())
linkedwell = set(dot for dot in managed if dot.isLinkedWell())
broken = managed - linkedwell
notmanaged = home_dotfiles - managed
missed = set(dot for dot in base_dotfiles if not dot.isManaged())
missed -= set([DotFile('.git'), DotFile('.gitmodules'), DotFile('.gitignore')])


def status():
    # 심볼릭 링크로 된 dotfile들
    print "[Managed]"
    print managed
    print
    print "[Linked]"
    print linkedwell
    print
    print "[Broken SymLinks]"
    print broken
    print
    print "[Missed SymLinks]"
    print missed
    print
    print "[Not Managed]"
    print notmanaged


def attach(filename):
    dotfile = DotFile(os.path.basename(filename))
    if dotfile.isManaged():
        return False, "'%s' file has already managed" % dotfile
    if dotfile.isLink():
        return False, "'%s' file is a symbolic link" % dotfile

    print dotfile.path(), "->", dotfile.dotpath()
    os.rename(dotfile.path(), dotfile.dotpath())
    os.symlink(dotfile.dotpath(), dotfile.path())
    return True, ""


def detach(filename):
    dotfile = DotFile(os.path.basename(filename))
    if not dotfile.isManaged():
        return False, "'%s' is not being managed" % dotfile
    if not dotfile.isLink():
        return False, "'%s' file is not a symbolic link" % dotfile

    print dotfile.realpath(), "->", dotfile.path()
    realpath = dotfile.realpath()
    path = dotfile.path()
    os.unlink(path)
    os.rename(realpath, path)
    return True, ""


def recover():
    # missed symlink
    print "[Missed Symlinks]"
    for dotfile in missed:
        print dotfile.path(), "->", dotfile.dotpath()
        if os.path.exists(dotfile.path()):
            print "'%s' is already exists. Try again." % dotfile
        else:
            os.symlink(dotfile.dotpath(), dotfile.path())
    return True, ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="dotfiles helper")
    subparsers = parser.add_subparsers(title="Commands", dest="action")
    parser_status = subparsers.add_parser('status', help='show dotfiles', )
    parser_attach = subparsers.add_parser('attach', help='attach dotfiles to manage', )
    parser_attach.add_argument('files', nargs='+')
    parser_detach = subparsers.add_parser('detach', help='detach dotfiles managing', )
    parser_detach.add_argument('files', nargs='+')

    parser_recover = subparsers.add_parser('recover', help='recover missing symlinks', )

    args = parser.parse_args()

    if args.action == 'status':
        status()
    elif args.action == 'attach':
        for f in args.files:
            res, msg = attach(f)
            if not res:
                print msg
    elif args.action == 'detach':
        for f in args.files:
            res, msg = detach(f)
            if not res:
                print msg
    elif args.action == 'recover':
        recover()
    else:
        parser.print_help()
