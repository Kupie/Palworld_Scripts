#### CONFIG READER ####
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
SERVER_IP = str(config['default']['SERVER_IP'])
RCON_PORT = int(config['default']['RCON_PORT'])
RCON_PASSWORD = str(config['default']['RCON_PASSWORD'])

#### BEGIN REAL SCRIPT SHIT ####

from time import sleep
import sys
from datetime import datetime
import os
import logging


#logging.basicConfig(level=logging.DEBUG)

try:
	from importlib.metadata import version
except:
	logging.error('Missing module importlib_metadata. Install with: pip install importlib_metadata')
	sys.exit(1)
try:
	import rcon
	from rcon.source import Client
	rconVersion = version('rcon')
	rconVersionNum = rconVersion.split('.')
	rconVersionNum = [int(i) for i in rconVersionNum]
	logging.debug(rconVersionNum[0])
	logging.debug(rconVersionNum[1])
	logging.debug(rconVersionNum[2])
	
	if not (rconVersionNum[0] >= 2 and
			rconVersionNum[1] >= 4 and
			rconVersionNum[2] >= 6):
		raise Exception
except Exception as e:
	logging.debug(str(e))
	logging.error('RCON Version: ' + rconVersion)
	logging.error('Needs the dev rcon version! Palworld is dumb and needs the dev version currently. Install with:')
	logging.error('pip install git+https://github.com/conqp/rcon.git') 
	sys.exit(1)


def parsePlayersList(playersString):
	stringList = playersString.splitlines()
	playersDict = {}
	#remove header
	stringList.pop(0)
	logging.debug('stringList')
	for playerEntry in stringList:
		playerEntryListified = playerEntry.split(',')
		logging.debug(playerEntryListified)
		playersDict[playerEntryListified[0]] = {"playeruid": playerEntryListified[1], "steamid": playerEntryListified[2]}
	#name,playeruid,steamid
	#Kupie,4160040412,76561197993593793
	return playersDict

def printAllPlayersToconsole(PlayersList):
	PlayersStringList = []
	print('Current Players: Name, UID, SteamID')
	for PlayersDict in PlayersList:
		PlayersStringList.append(PlayersDict)
		playerInfo = PlayersDict + ', ' + PlayersList[PlayersDict]['playeruid'] + ', ' + PlayersList[PlayersDict]['steamid']
		print(playerInfo)

PlayersList = []
	

def rconSendCommand(command: str, args: str = ''):
	with Client(SERVER_IP, RCON_PORT, passwd=RCON_PASSWORD) as client:
		#palworld broadcast doesn't handle spaces
		#Palworld why Q.Q
		#Also yoinked this from: https://github.com/gavinnn101/palworld_dedi_helper/blob/main/src/palworld_rcon/source_rcon.py
		if command.lower() == "broadcast":
			command = command + " " + args.replace(" ", "\x1F")
		else:
			command = command + " " + " ".join(args)

		logging.debug('Sending command: ' + command)
		return client.run(command, enforce_id=False)
	
def main():
	PlayersList = parsePlayersList(rconSendCommand('ShowPlayers'))
	
	printAllPlayersToconsole(PlayersList)

	
if __name__ == "__main__":
	main()
