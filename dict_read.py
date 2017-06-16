#!/usr/bin/env python3

import io, sys

def verify_line(line):
  if not line:
    return -1
  if line == '\n':
    return 1
  return 0

def read_dict(fname, show_warning=True):
  content = dict()
  try:
    fd = io.open(fname, 'r')
  except BaseException:
    sys.exit("Unable to open the dictionary.")

  line_num = 1
  key_line = ""
  val_line = ""
  while True:
    key_line = fd.readline()
    check = verify_line(key_line)
    if check == -1:
      sys.exit("ERROR: Unexpected EOF at line {0}.".format(line_num))
    elif check == 1:
      break
    line_num += 1
    key_line = key_line[:-1]
    val_line = fd.readline()
    check = verify_line(val_line)
    if check == -1:
      sys.exit("ERROR: Unexpected EOF at line {0}.".format(line_num))
    elif check == 1 and show_warning:
      print("Warning: No translation found for {0} at line {1}.".format(key_line, line_num))
    line_num += 1
    val_line = val_line[:-1]
    if key_line in content and show_warning:
      print("Warning: Collision for {0} at line {1}. Overriding.".format(key_line, line_num - 1))
    content[key_line] = val_line

  key_line = fd.readline()
  if key_line and show_warning:
    print("Warning: EOF not found after ending literal at line {0}.".format(line_num))

  fd.close()
  return content