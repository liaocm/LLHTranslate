#!/usr/bin/env python3

import argparse, sys, io, re
import itertools

from dict_read import read_dict

#import pdb; pdb.Pdb(skip=['django.*']).set_trace()

OUTPUT_SUFFIX = ".dict"

MAX_PARSE_LEN = 3000
MATCH_PATTERN = r"([a-zA-Z\+\-_0-9\;\:\. \u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+)"
CHINESE_PATTERN = r"[\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+"
PAT_DBL_QUOTE = r"\"" + MATCH_PATTERN + "\""
PAT_SGL_QUOTE = r"\'" + MATCH_PATTERN + "\'"
PAT_ENTIRE_LINE = r"^" + MATCH_PATTERN + r"$"
PAT_BETWEEN_BRKT = r">" + MATCH_PATTERN + r"<"
PAT_BRKT_LB = r">" + MATCH_PATTERN + r"$"
PAT_LB_BRKT = r"^" + MATCH_PATTERN + r"<"

PATTERN = PAT_DBL_QUOTE + "|" + PAT_SGL_QUOTE + "|"\
+ PAT_ENTIRE_LINE + "|" + PAT_BETWEEN_BRKT + "|" + PAT_BRKT_LB\
+ "|" + PAT_LB_BRKT

def main(fname, parse_only=False):
  output = set()
  try:
    fd = io.open(fname, 'r')
  except BaseException:
    sys.exit("Unable to read the file.")

  # Assuming no line break between texts
  for line in fd:
    if len(line) > MAX_PARSE_LEN:
      # Too long: might be the JSON string. Skip.
      continue
    match = re.findall(PATTERN, line)
    if match:
      flatten_match = list(itertools.chain.from_iterable(match))
      all_matches = list(filter(lambda x: x and len(x) > 0, flatten_match))
      true_matches = list(filter(
                          lambda x: re.search(CHINESE_PATTERN, x),
                          all_matches))
      if true_matches:
        for match in true_matches:
          output.add(match)
  fd.close()

  if parse_only:
    translate_dict = read_dict(fname + OUTPUT_SUFFIX)
    for key in output:
      if key not in translate_dict:
        print("Warning: {0} is not in the translation dict.".format(key))
    print("Parsed {0} keywords.".format(len(output)))
    sys.exit(0)

  fd = io.open(fname + OUTPUT_SUFFIX, 'w')
  sorted_output = sorted(output, key=lambda s:len(s), reverse=True)
  for item in sorted_output:
    fd.write(item)
    fd.write('\n')
    fd.write('\n')
  fd.write('\n')
  fd.close()
  print("Parsed {0} keywords.".format(len(sorted_output)))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="Path to the file to be parsed.")
  parser.add_argument("--parse", help="Parse only.", action="store_true")
  args = parser.parse_args()
  main(args.file, args.parse)
