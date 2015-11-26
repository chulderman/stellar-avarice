import os, sys
import requests #urllib2
import json
import random

manifest_location = "http://1.webseed.robertsspaceindustries.com/FileIndex/sc-alpha-2.0.0/"

dir_contents = [f for f in os.listdir('.') if os.path.isfile(f)]
for item in dir_contents:
	last_num = 0
	if item.split('.')[-1] == 'json':
		item_num = item.split('.')[0]
		if last_num < item_num:
			last_num = item_num
	else:
		continue
item_num = int(item_num)
print "Found Latest: " + str(item_num)

for i in range (item_num + 1,item_num + 1001):
	try:
		manifest_name = str(i) + ".json"
		print "Trying: " + manifest_name
		#manifest_response = urllib2.urlopen(manifest_location + manifest_name)
		manifest_response = requests.get(manifest_location + manifest_name)
		manifest_response.raise_for_status()
		print "Writing: " + manifest_name
		manifest_fh = open(manifest_name, "w")
		manifest_fh.write(manifest_response.read())
		manifest_fh.close()
	except Exception as e:
		if(r.status_code==404):
			print('%s: Page could not be found.' % e.reason)
		if(r.status_code>=500):
			print ('%s: Server error [%s]' % (e.reason,r.status_code))  

		
json_fh = open(str(item_num) + ".json", "r")
parsed_json = json.load(json_fh)

print "Using Build: " + str(item_num)
#Grab constants from json
base_webseed_url = random.choice(parsed_json["webseed_urls"])
key_prefix = parsed_json["key_prefix"]
	
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
	
	response = requests.get(file_url)
	
	if os.path.isfile(file):
		print("File Exists - Updating")
	
	with open(file, "w") as fh:
	    if not response.ok:
	        print('File download was unsuccessful')
	    else:
	    	for block in response.iter_content(1024):
	        fh.write(block)