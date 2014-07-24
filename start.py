#!/usr/bin/python
from lxml import etree
from cmd import Cmd
from sys import stdout
CFG_FILE = "hazelcast.xml"

class HazelcatXMLEditor(Cmd):

	prompt = None
	xmlparser = None
	tree = None
	hazelcast_node = None
	map_node = None
	backup_count_node = None
	async_backup_count_node = None
	read_backup_data_node = None
	time_to_live_seconds_node = None
	max_idle_seconds_node = None
	eviction_policy_node = None
	max_size_node = None
	eviction_percentage_node = None
	
	def initialize(self,name,text):
		node = self.map_node.find("{http://www.hazelcast.com/schema/config}" + name )
		if node is None:
			node = etree.SubElement(self.map_node, "{http://www.hazelcast.com/schema/config}"+name)
			node.text = text
		return node

	def get_and_validate(self,func,prompt,error):
		input = raw_input(prompt)
		try:
			func(input)
		except Exception:
			raise Exception(error)
		return input

	def bool(self,input):
		if input not in ["true","false"]:
			raise Exception

	def eviction(self,input):
		if input not in ["LRU","LFU","NONE"]:
			raise Exception

	def preloop(self):
		self.prompt = '> '
		self.xmlparser = etree.XMLParser(remove_comments=False,encoding="UTF-8")
		self.tree = etree.parse( CFG_FILE , parser=self.xmlparser)
		self.hazelcast_node = self.tree.getroot()
		self.map_node = self.hazelcast_node.find("{http://www.hazelcast.com/schema/config}map")

		self.backup_count_node = self.initialize( "backup-count" , "1" )
		self.async_backup_count_node = self.initialize( "async-backup-count" , "1" )
		self.read_backup_data_node = self.initialize( "read-backup-data" , "false" )
		self.time_to_live_seconds_node = self.initialize( "time-to-live-seconds" , "0" )
		self.max_idle_seconds_node = self.initialize( "max-idle-seconds" , "0" )
		self.eviction_policy_node = self.initialize( "eviction-policy" , "NONE" )
		self.max_size_node = self.initialize( "max-size" , "0" )
		self.eviction_percentage_node = self.initialize( "eviction-percentage" , "25" )

	def do_backup(self,args):
		try:
			backup_count = self.get_and_validate(int,"backup count :",
							"backup count must be int!")
			async_backup_count = self.get_and_validate(int,"async backup count :",
							"async backup count must be int!")
			read_backup_data = self.get_and_validate(self.bool,"read backup data :",
							"read backup data must be true or false!")
		except Exception as e:
			print e
			return

		self.backup_count_node.text = backup_count
		self.async_backup_count_node.text = async_backup_count
		self.read_backup_data_node.text = read_backup_data

	def do_eviction(self,args):
		try:
			backup_count = self.get_and_validate(int,"backup count :",
							"backup count must be int!")
			time_to_live_seconds = self.get_and_validate(int,"time to live seconds :",
							"time to live seconds must be int!")
			max_idle_seconds = self.get_and_validate(self.bool,"max idle seconds :",
							"max idle seconds must be int!")
			eviction_policy = self.get_and_validate(self.eviction,"eviction policy :",
							"eviction policy must be LRU,LFU or NONE")
			max_size = self.get_and_validate(int,"max size count :",
							"max size must be int!")
			eviction_percentage = self.get_and_validate(int,"eviction percentage :",
							"eviction percentage must be int!")
		except Exception as e:
			print e
			return

		self.backup_count_node.text = backup_count
		self.time_to_live_seconds_node.text = time_to_live_seconds
		self.max_idle_seconds_node.text = max_idle_seconds
		self.eviction_policy_node.text = eviction_policy
		self.max_size_node.text = max_size
		self.eviction_percentage_node.text = eviction_percentage

def main():
	prompt = HazelcatXMLEditor()
	prompt.cmdloop("Chose what to configure!")
	#prompt.tree.write(stdout)

if __name__ == '__main__':
	main()