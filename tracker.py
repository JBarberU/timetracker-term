#!/usr/bin/env python

import argparse
import os
import json
from datetime import datetime
from calendar import timegm

class TimeObject:

  stop = None

  def __init__(self, json_object=None):
    if json_object:
      self.session_start = json_object["session_start"]
      self.start = json_object["start"]
      self.stop = json_object["stop"] if "stop" in json_object else None
    else:
      self.session_start = str(datetime.now())
      self.start = timegm(datetime.utcnow().utctimetuple())

  def stop(self):
    self.stop = timegm(datetime.utcnow().utctimetuple())

  def serialize(self):
    ret = {"session_start": self.session_start}
    ret["start"] = self.start
    if self.stop:
      ret["stop"] = self.stop
    return ret

  def print_stats(self):
    print("%s: %s" % (self.session_start, (self.stop - self.start) if self.stop else "Still running"))

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
    with open(self.file_name, "w") as f:
      lines = []
      f.write(json.dumps(self.serialize(), sort_keys=True, indent=2, separators=(',',': ')))

  def add_timeobject(self, time_object):
    self.time_objects.append(time_object)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--track-file", help="The file to save the \
                                                 tracking info to")
  parser.add_argument("-s", "--stats", "--statistics", action="store_true", help="Print statistics")
  args = parser.parse_args()
  print args

  to = TimeObject()
  print(to.serialize())
  tracker = TimeTracker(args.track_file)
  to.stop()
  tracker.add_timeobject(to)
  print(tracker.serialize())
  tracker.print_stats()
  tracker.save()

if __name__ == "__main__":
  main()

