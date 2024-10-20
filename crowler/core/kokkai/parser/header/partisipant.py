#!-*- coding:utf-8 -*-
'''
Created on 2017/04/22

@author: master
'''
import re
tabPattern = re.compile(r"^\s+", re.U)
whiteSpace = re.compile(r"\s", re.U)
symbolOnly = re.compile(r"^[\w\s]+$", re.U)


def countTab(line):
    global tabPattern, whiteSpace
    match = tabPattern.search(line)
    if not match:
        return 0
    return len(whiteSpace.split(match.group(0)))


class Service(object):
    def __init__(self):
        self.depth = -1
        self.startLevel = -1
        self.mode = 0
        self.Ministry = False
        self.pending = None

    def isActivate(self, line):
        match = re.search(r"^(\s*)出席小?委員", line, re.U)
        if match:
            self.startLevel = self.depth = countTab(line)
            return True
        return False

    def isDeactivate(self, line):
        if self.startLevel >= countTab(line):
            self.startLevel = self.depth = -1
            self.mode = 0
            return True
        return False

    def execute(self, line, log):
        global symbolOnly,

        if symbolOnly.search(line):
            return

        depth = countTab(line)
        vector = 0
        if depth > self.depth:
            self.mode += 1
            vector = +1

        elif depth < self.depth:
            self.mode -= 1
            vector = -1
        self.depth = depth
        if not line.count(r"君"):
            self.pending = line
            return
        if self.pending:
            if vector == 0:

            for split in line.split(r"君"):
                split = tabPattern.sub(split, r"")
                position, name = whiteSpace.split(split, 2)
                self.pending += position
                data = datas.get(name, {})
                data['atnd'] = True
                positions = data.get('positions', [])
                if not position in positions:
                    positions.append(position)
                data['position'] = positions
                ret[name] = ret.get(name, {}).update({'atnd': True})

        if self.mode == 0:
            return
        if self.mode == 1:
            data = self.withPosition(line, log)
        if self.mode == 2:
            data = self.noPosition(line, log)

    def withPosition(self, line):
        global tabPattern, whiteSpace
        ret = {}

        for split in line.split(r"君"):
            split = tabPattern.sub(split, r"")
            position, name = whiteSpace.split(split, 2)
            data = ret.get(name, {})
            data['atnd'] = True
            positions = data.get('positions', [])
            if not position in positions:
                positions.append(position)
            data['position'] = positions
            ret[name] = ret.get(name, {}).update({'atnd': True})
        return ret

    def noPosition(self, line):
        global tabPattern
        ret = {}

        for split in line.split(r"君"):
            name = tabPattern.sub(split, r"")
            ret[name] = ret.get(name, {}).update({'atnd': True})
        return ret
