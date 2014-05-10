#! /usr/bin/env python

import fileinput
import csv
import os
import sys
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Load the spouse dictionary for distant supervision
spouses = defaultdict(lambda: None)
with open (BASE_DIR + "/../../data/spouses.csv") as csvfile:
  reader = csv.reader(csvfile)
  for line in reader:
    spouses[line[0].strip().lower()] = line[1].strip().lower()


# For each input tuple
for row in fileinput.input():
  parts = row.strip().split('\t')
  if len(parts) != 5: 
    print >>sys.stderr, 'Failed to parse row:', row
    continue
  
  sentence_id, p1_id, p1_text, p2_id, p2_text = parts

  p1_text_lower = p1_text.lower()
  p2_text_lower = p2_text.lower()

  # See if the combination of people is in our supervision dictionary
  # If so, set is_correct to true or false
  is_true = '\N'
  if spouses[p1_text_lower] == p2_text_lower:
    is_true = 'true'
  elif (p1_text == p2_text) or (p1_text in p2_text) or (p2_text in p1_text):
    is_true = 'false'

  print '\t'.join([
    p1_id, p2_id, sentence_id, 
    "%s-%s" %(p1_text, p2_text),
    is_true,
    '\N',  # leave relation_id blank and fill later
    '\N'   # leave "id" blank for system!
    ])

  # TABLE FORMAT: CREATE TABLE has_spouse(
  # person1_id bigint,
  # person2_id bigint,
  # sentence_id bigint,
  # description text,
  # is_true boolean,
  # relation_id bigint, -- unique identifier for has_spouse
  # id bigint   -- reserved for DeepDive
  # );