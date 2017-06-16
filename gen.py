#!/usr/bin/env python3

import argparse, sys, io

from dict_read import read_dict

DEFAULT_SUFFIX = "-translated"

def main(fname, nfname):
  if not nfname:
    nfname = fname + DEFAULT_SUFFIX
  try: 
    rfd = io.open(fname, 'r')
    wfd = io.open(nfname, 'w')
    translations = read_dict(fname + ".dict", False)
  except BaseException:
    sys.exit("Unable to open the file.")

  sorted_dict_keys = sorted(list(translations.keys()), key=lambda s:len(s), reverse=True)
  for line in rfd:
    for key in sorted_dict_keys:
      if translations[key]:
        line = line.replace(key, translations[key])
    wfd.write(line)

  rfd.close()
  wfd.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="Path to the file to be translated.")
  parser.add_argument("--newfile", help="Path to the output file.")
  args = parser.parse_args()
  main(args.file, args.newfile)
