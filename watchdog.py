### BEGIN CONFIG AREA ###
SERVER_IP = '127.0.0.1'
RCON_PORT = 25575
RCON_PASSWORD = 'RCON_SERVER_PASSWORD_HERE'

#Seconds between loops
LOOP_INTERVAL = 5
JOIN_LEAVE_NOTIFICATIONS = True

#how often to print the entire players list out
PRINT_PLAYERS_LIST_INTERVAL = 900



#### CONFIG AREA ABOVE ####

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

def sendJoinedOrLeftPlayers(NewPlayersList, OldPlayersList):
	
	#Check for players not loaded yet, skip till next iteration if they exist
	#print(NewPlayersList)
	for playerList in NewPlayersList:
		if NewPlayersList[playerList]['playeruid'] == '00000000':
			print('Unloaded player found, skipping joined/left messages this run')
			return OldPlayersList

	set1 = set(NewPlayersList)
	set2 = set(OldPlayersList)
	
	if (set1 == set2):
		return NewPlayersList
		
	joinedPlayers = list(sorted(set1 - set2))
	leftPlayers = list(sorted(set2 - set1))
	
	if joinedPlayers:
		#Send info about joined/left players. Palworld doesn't currently support spaces in broadcasts so we use ascii character 1F....
		for playerJoined in joinedPlayers:
			sendString = 'Joined: ' + playerJoined
			rconSendCommand('broadcast', sendString)
			print(sendString + str(NewPlayersList[playerJoined]))
	if leftPlayers:
		for playerLeft in leftPlayers:
			sendString = 'Left: ' + playerLeft
			rconSendCommand('broadcast', sendString)
			print(sendString + str(OldPlayersList[playerLeft]))
	return NewPlayersList
		
	

def printAllPlayersToconsole(timePrintedPlayersLast, PlayersList):
	if ((datetime.now()- timePrintedPlayersLast).total_seconds() > PRINT_PLAYERS_LIST_INTERVAL):
		PlayersStringList = []
		print('Current Players: Name, UID, SteamID')
		for PlayersDict in PlayersList:
			PlayersStringList.append(PlayersDict)
			playerInfo = PlayersDict + ', ' + PlayersList[PlayersDict]['playeruid'] + ', ' + PlayersList[PlayersDict]['steamid']
			print(playerInfo)
		#print('Current Players: ' + ",".join(PlayersStringList)) 
		return datetime.now()
	else:
		return timePrintedPlayersLast


PlayersList = []
NewPlayersList = []	

def rconBroadcast(message):
	#palworld broadcast doesn't handle spaces
	#Palworld why Q.Q
	message.replace(" ", "\x1F")
	with Client(SERVER_IP, RCON_PORT, passwd=RCON_PASSWORD) as client:
		response = client.run("broadcast", message, enforce_id=False)
	
	

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
	
timePrintedPlayersLast = datetime.min

firstRun = True

def main():
	global timePrintedPlayersLast
	global PlayersList
	global firstRun
	
	
	NewPlayersList = parsePlayersList(rconSendCommand('ShowPlayers'))
	logging.debug(NewPlayersList)
	
	# If join/leave notifications is turned on, and it's NOT the first run... otherwise the script
	# prints out all players as "Joined" when it first runs
	if (JOIN_LEAVE_NOTIFICATIONS & (not firstRun)):
		PlayersList = sendJoinedOrLeftPlayers(NewPlayersList, PlayersList)
	else:
		PlayersList = NewPlayersList
	
	timePrintedPlayersLast = printAllPlayersToconsole(timePrintedPlayersLast, PlayersList)

	firstRun = False
	logging.debug(NewPlayersList)
	logging.debug(list(NewPlayersList))
	logging.debug('Main loop ran. Waiting ' + str(LOOP_INTERVAL) + 's to run again')

if __name__ == "__main__":
	failedConnections = 0
	while True:
		try:
			main()
			sleep(LOOP_INTERVAL)
		except KeyboardInterrupt:
			print('CTRL+C hit. Exiting...')
			sys.exit(0)
		except ConnectionRefusedError:
			failedConnections +=1
			if (failedConnections >= 4):
				print('SERVER DOWN AFTER 5 TRIES, RESTARTING')
				os.system('SCHTASKS /RUN /TN "Restart Palserver NOW MANUAL-ONLY"')
				failedConnections = 0
				sleep(45)
			logging.warning('Connection failed! Maybe palworld server is down? Trying again in 15 seconds...')
			print('Times Failed: ' + str(failedConnections))
			sleep(15)
			
		except Exception as e:
			logging.warning('Got this error, trying again in 15 seconds:')
			logging.warning(str(e))
			sleep(15)
			pass
