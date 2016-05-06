import os, sys
import requests
import json
import random
import argparse
import shutil


# Set some initial constants
manifest_location = "http://2.webseed.robertsspaceindustries.com/FileIndex/sc-alpha-2.4.0/"
BUILD_RANGE = 10
VERSION = "0.0.3"

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
			print '\rTrying: {}'.format(manifest_name),
			manifest_response = requests.get(manifest_location + manifest_name)
			manifest_response.raise_for_status()
			
			# If it finds the file, doesn't throw an exception and writes the file to disk
			print "\rWriting: {}".format(manifest_name),
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

#############################################################
#               ---- parse_json() ----   	                #
# Description:												#
# Function grabs the latest json and parses it into an 		#
# object and then returns that parsed json object			#
#############################################################
def parse_json():

	latest_json = str(latest_build())
	print "Using: {}".format(latest_json)
	json_fh = open(latest_json + ".json", "r")
	parsed_json = json.load(json_fh)
	return parsed_json
	
#############################################################
#               ---- download_build() ----                  #
# Description:												#
# Function grabs latest json object and then uses this 		#
# to create directories it needs. It then starts to 		#
# download the build via a stream in blocks of 1024			#
#############################################################
def download_build():
	parsed_json = parse_json()

	# Choose a random webseed
	base_webseed_url = random.choice(parsed_json["webseed_urls"])
	# The key prefix is the build version that gets appended to the base seed location
	key_prefix = parsed_json["key_prefix"]
	build_name = parsed_json["key_prefix"].split("/")[2] #Grab Build # so that we store build's appropriately

	for file_name in parsed_json["file_list"]:
		list = [] # A list to hold temporary values

		# Construct the URI based on each file
		file_url = base_webseed_url + "/" + key_prefix + "/" + file_name
		
		# We iterate through the full file list to discover any folders that might be contained within
		# If we find a folder that doesn't exist, we create this folder
		if "/" in file_name:
			for item in file_name.split('/'):
				list.append(item)
			file_name = list.pop(-1)
			file_path = os.path.join(build_name, *list)
			if not os.path.isdir(file_path):
				try:
					os.makedirs(file_path)
				except OSError:
					print "\nError creating directory: " + file_path
		
		file = os.path.join(file_path, file_name)
		# Begin Downloading Part
		
		print("\rDownloading: %-100s" % file),
		
		# Create the response object, ensure that it's a stream
		# so we can start downloading right away
		response = requests.get(file_url, stream=True)
		
		# Let the user know if they're downloading a new file or not
		# This should have more functionality later
		if os.path.isfile(file):
			print "File Exists - Updating",
			continue
			# if <local hash matches remote>
				# print "Skipping..."
				# continue
			# else:
				# print "Updating..."
		else:
			pass
		# For each file start writing it.
		with open(file, "wb") as fh:
		    if not response.ok:
		        print('File download was unsuccessful')
		    else:
		    	for block in response.iter_content(chunk_size=1024, decode_unicode=False):
					fh.write(block)
def main():
	# Used for our just checking the latest build information
	if args.latest:
		print "Latest Build: {}".format(latest_build())
		sys.exit(0)
	else:
		## This isn't working right now
		new_build_check()
		print "\nLatest Build: {}".format(latest_build())
		prompt = raw_input("Would you like to download this version [y|n]?\n>").lower()
		if prompt.strip() == 'y': 
			download_build()
		else:
			print "Exiting..."
		sys.exit(0)

if __name__ == "__main__":
	main() #Run our code
