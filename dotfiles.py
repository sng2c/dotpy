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
cur_path = os.path.dirname(__file__)
DOT_BASE = os.path.realpath("%s/dotfiles" % cur_path)

DotFile.homebase = HOME
DotFile.dotbase = DOT_BASE

argp = argparse.ArgumentParser(description="dotfiles helper")
# argp.add_argument()
args = argp.parse_args()

import re
# dotfile들을 나열한다.
home_dotfiles = set(DotFile(dot) for dot in os.listdir(HOME) if re.match(r"\.[^\.].*", dot))
base_dotfiles = set(DotFile(dot) for dot in os.listdir(DOT_BASE) if re.match(r"\.[^\.].*", dot))

if not os.path.exists(DOT_BASE): os.mkdir(DOT_BASE, 0755)

managed = set(dot for dot in home_dotfiles if dot.isManaged())
linkedwell = set(dot for dot in managed if dot.isLinkedWell())
broken = managed - linkedwell
notmanaged = home_dotfiles - managed
missed = set(dot for dot in base_dotfiles if not dot.isManaged())

def status():
    # 심볼릭 링크로 된 dotfile들
    print "[Managed]"
    print managed
    print "[Linked]"
    print linkedwell
    print "[Broken SymLinks]"
    print broken
    print "[Missed SymLinks]"
    print missed
    print "[Not Managed]"
    print notmanaged

def add(filename):
    dotfile = DotFile(os.path.basename(filename))
    if dotfile.isManaged():
        return False, "This file has already managed"
    if dotfile.isLink():
        return False, "This file is a symbolic link"

    print dotfile.path(), "->", dotfile.dotpath()
    os.rename(dotfile.path(), dotfile.dotpath())
    os.symlink(dotfile.dotpath(), dotfile.path())
    return True,


def remove(filename):
    dotfile = DotFile(os.path.basename(filename))
    if not dotfile.isManaged():
        return False, "This file is not being managed"
    if not dotfile.isLink():
        return False, "This file is not a symbolic link"

    print dotfile.realpath(), "->", dotfile.path()
    realpath = dotfile.realpath()
    path = dotfile.path()
    os.unlink(path)
    os.rename(realpath, path)
    return True,


def recover():
    # missed symlink
    print "[Missed Symlinks]"
    for dotfile in missed:
        print dotfile.path(), "->", dotfile.dotpath()
        os.symlink(dotfile.dotpath(), dotfile.path())
    return True,


print status()