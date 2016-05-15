import json
import random

class BuildInfo(object):

  def __init__(self, build_json):
    self.parsed_json = parse_json(build_json)
    self._collect_info(self.parsed_json)
    self.file_count = 0
    self.byte_count = 0
    self.build_num = ""
    self.base_webseed_url = ""
    self.key_prefix = ""

  def parse_json(f):
    json_fh = open(f, "r")
    parsed = json.load(json_fh)
    return parsed

  def _collect_info(self, j):
    self.file_count = j["file_count_total"]
    self.byte_count = j["file_count_total"]
    
    # The key prefix is the file prefix for this specific build
    # looks like - "key_prefix": "GameBuilds/sc-alpha-x.x.x/######/StarCitizen"
    self.key_prefix = parsed_json["key_prefix"]

    self.build_num = parsed_json["key_prefix"].split("/")[2]

    # Choose a random webseed
    self.base_webseed_url = random.choice(parsed_json["webseed_urls"])