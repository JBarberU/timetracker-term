#!/usr/bin/env python

import argparse
import os
import json
from datetime import datetime
from calendar import timegm

class TimeObject:

  stop = None
  entries = []

  def __init__(self, json_object=None):
    if json_object:
      self.session_start = json_object["session_start"]
      for jsobj in json_object["entries"]:
        entry = {"start": jsobj["start"], "stop": jsobj["stop"] if "stop" in jsobj else None}
        self.entries.append(entry)
    else:
      self.session_start = str(datetime.now())
      entries.append({"start": timegm(datetime.utcnow().utctimetuple()), stop: None })

  def stop(self):
    for e in entries:
      if not e.stop:
        e.stop = timegm(datetime.utcnow().utctimetuple())

  def serialize(self):
    ret = {"session_start": self.session_start}
    entries = []
    for e in self.entries:
      entry = {"start": e.start}
      if "stop" in e:
        entry["stop"] = e.stop
      entrie.append(entry)

    ret["entries"] = entries
    return ret

  def print_stats(self):
    sum_time = 0
    running = False
    for e in self.entries:
      if "stop" in e:
        running = True
      else:
        sum_time += e.stop - e.start


    print("%s: %s %s" % (self.session_start, sum_time, "Still running" if running else ""))

  def running(self):
    if len(self.entries) == 0:
      return None
    else:
      last_entry = self.entries[len(self.entries) - 1]
      return last_entry if "stop" in last_entry else None

class TimeTracker():

  time_objects = []
  file_name = None

  def __init__(self, track_file):
    self.file_name = track_file
    if os.path.isfile(self.file_name):
      json_obj = json.load(open(self.file_name))
      for to in json_obj["time"]:
        self.time_objects.append(TimeObject(to))

  def serialize(self):
    time_objects = []
    for to in self.time_objects:
      time_objects.append(to.serialize())
    return { "time": time_objects }

  def print_stats(self):
    print("Stats for \"%s\": " % self.file_name)
    for to in self.time_objects:
      to.print_stats()
    print("-" * 20)

  def save(self):
    print(json.dumps(self.serialize(), sort_keys=True, indent=2, separators=(',',': ')))
    return
    with open(self.file_name, "w") as f:
      lines = []
      f.write(json.dumps(self.serialize(), sort_keys=True, indent=2, separators=(',',': ')))

  def add_timeobject(self, time_object):
    self.time_objects.append(time_object)

  def running(self):
    if len(self.time_objects) == 0:
      return None
    else:
      last_object = self.time_objects[len(self.time_objects) - 1]
      return last_object if last_object.running() else None
   

def run(tracker):
  keep_running = True

  cmds = ["stop",
          "pause",
          "resume",
          "stats",
          "help",
         ]

  running_object = tracker.running()
  if not running_object:
    running_object = TimeObject()
    tracker.add_timeobject(running_object)

  while keep_running:

    cmd = raw_input()
    if cmd == cmds[0]:
      keep_running = False
    elif cmd == cmds[1]:
      running_object.pause()
    elif cmd == cmds[2]:
      running_object.resume()
    elif cmd == cmds[3] or cmd == "":
      tracker.print_stats()
    elif cmd == cmds[4]:
      print("Available commands: \n")
      for c in cmds:
        print("\t{0}".format(c))
    else:
      print("Unrecognized command \"{0}\", try help".format(cmd))

  tracker.save()


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--track-file", help="The file to save the \
                                                 tracking info to")
  parser.add_argument("-s", "--stats", "--statistics", action="store_true", help="Print statistics")
  args = parser.parse_args()
  print args

  tracker = TimeTracker(args.track_file)
  run(tracker)

if __name__ == "__main__":
  main()

