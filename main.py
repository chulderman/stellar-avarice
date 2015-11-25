import os, sys
import urllib2

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
# json_fh = open("item_num.json", "r")
item_num = int(item_num)

for i in range (item_num + 1,item_num + 1001):
	try:
		manifest_name = str(i) + ".json"
		print "Trying: " + manifest_name
		manifest_response = urllib2.urlopen(manifest_location + manifest_name)
		print "Writing: " + manifest_name
		manifest_fh = open(manifest_name, "w")
		manifest_fh.write(manifest_response.read())
		manifest_fh.close()
	except urllib2.HTTPError as e:
		pass
	except URLError as e:
		print 'We failed to reach a server.'
		print 'Reason: ', e.reason 

# for line in f:
	# list = []
	# file_url = line.split('\n')[0]
	# file_name = line.split('/StarCitizen/')[-1].split('\n')[0
	
	# if "/" in file_name:
		# for item in file_name.split('/'):
			# list.append(item)
		# file_name = list.pop(-1)
		# file_path = os.path.join(*list)
		# try:
			# os.makedirs(file_path)
		# except OSError:
			# pass
	# file = os.path.join(file_path, file_name)
	
	# # Begin Downloading Part
	
	# response = urllib2.urlopen(file_url)
	# print "Downloading: " + file
	# if os.path.isfile(file):
		# print "File Exists - Updating"
	
	# fh = open(file, "w")
	# fh.write(response.read())
	# fh.close()
	
# f.close()
