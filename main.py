import os, sys
import requests
import json
import random
import argparse

# Set some initial constants
manifest_location = "http://1.webseed.robertsspaceindustries.com/FileIndex/sc-alpha-2.0.0/"
BUILD_RANGE = 10
VERSION = "0.0.1"

#############################################################
#                  -- Argument Parsing -                    #
# Description: 						    					#
# This block parses the commandline with the argparse 		#
# library. https://docs.python.org/3/library/argparse.html	#
#############################################################
parser = argparse.ArgumentParser(prog="stellar_avarice")
parser.add_argument('-l', '--latest',
					help="Display the latest version")
parser.add_argument('-v', '--version',
					help="Display program version")

#############################################################
#               ---- latest_version() ----                  #
# Description: 						    					#
# Function searches the current directory for *.json files  #
# It returns the highest number it finds		    		#
#############################################################
def latest_version(json_num = 0):
	dir_contents = [f for f in os.listdir('.') if os.path.isfile(f)]	
	for item in dir_contents:
		last_json = 0
		if item.split('.')[-1] == 'json':
			json_num = item.split('.')[0]
			if last_json < json_num:
				last_json = json_num
		else:
			continue
	return json_num;

item_num = int(latest_version())

print "Found Latest: " + str(item_num)



for i in range (item_num + 1,item_num + BUILD_RANGE + 1):
	try:
		manifest_name = str(i) + ".json"
		
		# Print the latest json that we're trying to test for
		print 'Trying: {}\r'.format(manifest_name)
		manifest_response = requests.get(manifest_location + manifest_name)
		manifest_response.raise_for_status()
		
		# If it finds the file, doesn't throw an exception and writes the file to disk
		print "Writing: " + manifest_name
		manifest_fh = open(manifest_name, "w")
		manifest_fh.write(manifest_response.read())
		manifest_fh.close()
		item_num = manifest_name
	except Exception as e:
		if(r.status_code==404):
			print('%s: Page could not be found.' % e.reason)
		if(r.status_code>=500):
			print ('%s: Server error [%s]' % (e.reason,r.status_code))  


# Open up and parse JSON data
json_fh = open(str(item_num) + ".json", "r")
parsed_json = json.load(json_fh)

# Setting constants based on JSON data
base_webseed_url = random.choice(parsed_json["webseed_urls"])
key_prefix = parsed_json["key_prefix"]

print "Using: {}".format(item_num)

	
#for file_name in parsed_json["file_list"]:
#	list = []
#	file_url = base_webseed_url + "/" + key_prefix + "/" + file_name
#	if "/" in file_name:
#		for item in file_name.split('/'):
#			list.append(item)
#		file_name = list.pop(-1)
#		file_path = os.path.join(*list)
#		if not os.path.isdir(file_path):
#			try:
#				os.makedirs(file_path)
#			except OSError:
#				print "Error creating directory: " + file_path
#				
#	file = os.path.join(file_path, file_name)
#	# Begin Downloading Part
#	
#	print("Downloading: %s" % file)
#	
#	response = requests.get(file_url)
#	
#	if os.path.isfile(file):
#		print("File Exists - Updating")
#	
#	with open(file, "w") as fh:
#	    if not response.ok:
#	        print('File download was unsuccessful')
#	    else:
#	    	for block in response.iter_content(1024):
#	        fh.write(block)
