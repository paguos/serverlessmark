
import time
import sys
import os
import json

sys.stderr.write("Starting Python Function\n")

seconds = 0

try:
  if not os.isatty(sys.stdin.fileno()):
    try:
      obj = json.loads(sys.stdin.read())
      if obj["seconds"] != "":
        seconds = int(obj["seconds"])		
    except ValueError:
      # ignore it
      sys.stderr.write("no input, but that's ok\n")
except:
  pass

time.sleep(seconds)

print ""
