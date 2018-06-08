#!/usr/bin/python

import argparse
import json
import re
import sys
import subprocess
import yaml

def parse_dmidecode(string):
  last_header = None
  last_attribute = None
  dmidecode_parsed = []
  tmp_obj = {}

  for line in string.split('\n'):
    if len(line) == 0: continue
    elif not re.match('^\s',line):
      #if len(tmp_obj.keys()) > 1: print tmp_obj
      if len(tmp_obj.keys()) > 1: dmidecode_parsed.append(tmp_obj)
      tmp_obj = {}
      tmp_obj['header'] = line.strip()
    elif ':' in line:
      tmp_obj['attributes'] = tmp_obj.get('attributes', {})

      splitted = line.split(':')
      key = splitted[0].strip()
      value = ':'.join(splitted[1:]).strip()

      last_attribute = key
      tmp_obj['attributes'][key] = value
    else:
      if tmp_obj['attributes'][last_attribute] == '':
        tmp_obj['attributes'][last_attribute] = []
      tmp_obj['attributes'][last_attribute].append(line.strip())
  
  return dmidecode_parsed

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Process dmidecode output.')
  parser.add_argument('filename', type=str, help='Filename to decode.', default=None, nargs='?')
  parser.add_argument('--json', default=True, help='Output as JSON.', action='store_true')
  parser.add_argument('--yaml', default=False, help='Output as YAML.', action='store_true')

  stdin = True if not sys.stdin.isatty() else False

  args = parser.parse_args()

  if args.filename:
    with open(args.filename, 'r') as f:
      string = f.read()
  elif stdin:
    string = sys.stdin.read()
  else:
    parser.print_help()
    sys.exit()

  if args.yaml:
    print yaml.dump(parse_dmidecode(string))
  else:
    print json.dumps(parse_dmidecode(string), indent=2, sort_keys=True)
