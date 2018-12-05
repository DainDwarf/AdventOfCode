#!/usr/bin/python3
from __future__ import print_function
import datetime
from dateutil import parser
import pandas as pd
import re


guard_re = re.compile(
    r"""\[(?P<date>[^]]*)\]             # Datetime portion
        \ Guard\ \#(?P<id>\d+)          # Guard ID
    """, re.X)                          # Discard the rest of the line.
sleep_re = re.compile(
    r"""\[(?P<date>[^]]*)\]             # Datetime portion
        \ (?P<state> falls | wakes )    # State change
    """, re.X)                          # Discard the rest of the line.


def parseDT(date):
    """Returns the two relevant parts of the datetime, dealing with the 23h issue.

    Returns (date, minute)."""
    dt = parser.parse(date) + datetime.timedelta(hours=1)
    return (dt.date(), dt.minute)


def getGuardsDict(inp):
    ret = dict()
    for line in inp.split("\n"):
        match = guard_re.match(line)
        if match:
            date, _ = parseDT(match.group('date'))
            ret[date] = int(match.group('id'))
    return ret


def getSleepDF(inp):
    guards = getGuardsDict(inp)
    def __parseSleep(inp):
        for line in inp.split("\n"):
            match = sleep_re.match(line)
            if match:
                date, minute = parseDT(match.group('date'))
                dt = datetime.datetime(date.year+500, date.month, date.day, 0, minute)
                state = 1 if match.group('state') == "falls" else 0
                yield (dt, guards[date], state)
    df = pd.DataFrame(__parseSleep(inp), columns=["dt", "id", "state"])
    df["dt"] = pd.to_datetime(df["dt"])
    df = df.set_index("dt")
    df = df.resample('1T').ffill()
    df = df[df.index.hour == 0]
    df["minute"] = df.index.minute
    return df


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

    print("Unit test for Part One.")
    print("Test on given input gives {res}".format(inp=ex, res=partOne(ex)))


def testTwo():
    ex = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

    print("Unit test for Part Two.")
    print("Test on given input gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    sleep_df = getSleepDF(inp)
    mostSleepingGuard = sleep_df.groupby('id')["state"].sum().idxmax()
    mostSleepingMinute = sleep_df[sleep_df["id"] == mostSleepingGuard][sleep_df["state"] == 1]["minute"].value_counts().idxmax()
    return mostSleepingGuard*mostSleepingMinute


def partTwo(inp):
    sleep_df = getSleepDF(inp)
    guard, minute =  sleep_df[sleep_df["state"] == 1].groupby("id")["minute"].value_counts().idxmax()
    return guard*minute


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
