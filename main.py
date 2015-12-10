import os, sys
import requests
import json
import random
import argparse

# Set some initial constants
manifest_location = "http://1.webseed.robertsspaceindustries.com/FileIndex/sc-alpha-2.0.0/"
BUILD_RANGE = 10
VERSION = "0.0.2"

#############################################################
#                  -- Argument Parsing -                    #
# Description: 						    					#
# This block parses the commandline with the argparse 		#
# library. https://docs.python.org/3/library/argparse.html	#
#############################################################
parser = argparse.ArgumentParser(prog="stellar_avarice", description="An Automated Star Citizen Download Utility")
parser.add_argument('-l', '--latest',
					help="Display the latest version", action="store_true")
parser.add_argument('-v', '--version',
					help="Display program version", action="version", version='%(prog)s - v{}'.format(VERSION))
args = parser.parse_args()

#############################################################
#               ---- latest_version() ----                  #
# Description: 						    					#
# Function searches the current directory for *.json files  #
# It returns the highest number it finds		    		#
#############################################################
def latest_build(json_num = 0):
	dir_contents = [f for f in os.listdir('.') if os.path.isfile(f)]	
	last_json = json_num
	for item in dir_contents:
		if item.split('.')[-1] == 'json':
			json_num = item.split('.')[0]
			if last_json < json_num:
				last_json = json_num
		else:
			continue
	return last_json
#############################################################
#               ---- new_build_check() ----                 #
# Description:												#
# Function checks the manifest_location for a new build		#
# it does this by utilizing the latest version information	#
# it currently has											#
#############################################################
def new_build_check():
	item_num = int(latest_build())
	print "Found Latest: " + str(item_num)

	for i in range (item_num + 1,item_num + BUILD_RANGE + 1):
		try:
			manifest_name = str(i) + ".json"
			
			# Print the latest json that we're trying to test for
			print 'Trying: {}\r'.format(manifest_name)
			manifest_response = requests.get(manifest_location + manifest_name)
			manifest_response.raise_for_status()
			
			# If it finds the file, doesn't throw an exception and writes the file to disk
			print "Writing: " + manifest_name + '\r'
			manifest_fh = open(manifest_name, "w")
			manifest_fh.write(manifest_response.content)
			manifest_fh.close()
		except Exception as e:
			if(manifest_response.status_code==404):
				print('%s: Page could not be found.' % e.reason)
			if(manifest_response.status_code>=500):
				print ('%s: Server error [%s]' % (e.reason, manifest_response.status_code))

#############################################################
#               ---- version_compare() ----                 #
# Description:												#
# Function compares two versions by each portion of the		#
# version number. This allows double digit parts to be 		#
# compared individually, such as 2.11.0, which would be a 	#
# newer version than 2.8.0									#
#############################################################
def version_compare(num_check):
	num_split = num_check.split('.')
	try:
		latest_num_list=latest_num.split('.')
		if(isinstance(latest_num_list,list)):	
			for ind,part in enumerate(num_split):
				if(part>latest_num_list[ind]):
					latest_num_list=num_split
				elif(part==latest_num_list[ind]):
					continue
				else:
					break
		else:
			latest_num=num_check
	except:
		latest_num=num_check
	return latest_num

# # Open up and parse JSON data
def parse_json():

	latest_json = str(latest_build())
	print "Using: {}".format(latest_json)
	json_fh = open(latest_json + ".json", "r")
	parsed_json = json.load(json_fh)
	return parsed_json
	

def download_build():
	parsed_json = parse_json()

	base_webseed_url = random.choice(parsed_json["webseed_urls"])
	key_prefix = parsed_json["key_prefix"]

	# Setting constants based on JSON data
	for file_name in parsed_json["file_list"]:
		list = []
		file_url = base_webseed_url + "/" + key_prefix + "/" + file_name
		if "/" in file_name:
			for item in file_name.split('/'):
				list.append(item)
			file_name = list.pop(-1)
			file_path = os.path.join(*list)
			if not os.path.isdir(file_path):
				try:
					os.makedirs(file_path)
				except OSError:
					print "Error creating directory: " + file_path
					
		file = os.path.join(file_path, file_name)
		# Begin Downloading Part
		
		print("Downloading: %s" % file)
		
		response = requests.get(file_url, stream=True)
		
		if os.path.isfile(file):
			print("File Exists - Updating")
		
		with open(file, "w") as fh:
		    if not response.ok:
		        print('File download was unsuccessful')
		    else:
		    	for block in response.iter_content(1024):
		        	fh.write(block)
def main():
	if args.latest:
		print "Latest Build: {}".format(latest_build())
		sys.exit(0)
	else:
		## This isn't working right now
		new_build_check()
		download_build()
		sys.exit(0)
main()