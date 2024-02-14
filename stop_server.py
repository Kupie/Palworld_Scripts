#### CONFIG READER ####
import configparser, pathlib
config = configparser.ConfigParser()
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
SERVER_IP = str(config['default']['SERVER_IP'])
RCON_PORT = int(config['default']['RCON_PORT'])
RCON_PASSWORD = str(config['default']['RCON_PASSWORD'])

#### BEGIN REAL SCRIPT SHIT ####

from time import sleep
import sys
from datetime import datetime
import os
import logging

try:
	from importlib.metadata import version
except:
	logging.error('Missing module importlib_metadata. Install with: pip install importlib_metadata')
	sys.exit(1)
try:
	import psutil    
except:
	logging.error('Missing module psutil. Install with: pip install psutil')
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

def rconSendCommand(command: str, args: str = ''):
	with Client(SERVER_IP, RCON_PORT, passwd=RCON_PASSWORD) as client:
		#palworld broadcast doesn't handle spaces
		#Palworld why Q.Q
		#Also yoinked this from: https://github.com/gavinnn101/palworld_dedi_helper/blob/main/src/palworld_rcon/source_rcon.py
		if command.lower() == "broadcast":
			command = command + " " + args.replace(" ", "\x1F")
		else:
			command = command + " " + " ".join(args)

		logging.warning('Sending command: ' + command)
		return client.run(command, enforce_id=False)


def isServerRunning():
	serverRunning = "PalServer-Win64-Test-Cmd.exe" in (p.name() for p in psutil.process_iter())
	serverRunning2 = "PalServer.exe" in (p.name() for p in psutil.process_iter())
	return (serverRunning and serverRunning2)


def stopServerNicely():
	rconSendCommand('shutdown 60')
	rconSendCommand('broadcast', 'SERVER SHUTTING DOWN IN 60 SECONDS')
	rconSendCommand('Save')
	print('Broadcasted server 1 minute shutdown warning...')
	sleep(30)
	print('Broadcasted server half minute shutdown warning...')
	rconSendCommand('broadcast', 'SERVER SHUTTING DOWN IN 30 SECONDS')
	sleep(19)
	rconSendCommand('broadcast', 'SERVER SHUTTING DOWN IN 10...')
	print('Broadcasted server 10 second shutdown warning and doing countdown...')

	sleep(1)
	for i in range(9, 0, -1):
		rconSendCommand('broadcast', str(i) + '...')
		sleep(1)
	print('Shutting Down Server...')
	
	
def stopServerRudely():
	os.system("taskkill /IM PalServer-Win64-Test-Cmd.exe")
	os.system("taskkill /IM PalServer.exe")

def fuckingMurderTheServer():
	os.system("taskkill /IM PalServer-Win64-Test-Cmd.exe /F")
	os.system("taskkill /IM PalServer.exe /F")


def main():
	if isServerRunning():
		try:
			stopServerNicely()
		except ConnectionRefusedError:
			logging.warning('Connection failed! Maybe palworld server is down?')
			sys.exit(1)
		except rcon.exceptions.WrongPassword:
			print('Wrong rcon password bruh')
			sys.exit(1)
		except Exception as e:
			logging.warning('Got this error trying to stop server nicely')
			logging.warning(str(e))
			sys.exit(1)
			pass
	else:
		print('Server not running bruh')
		sys.exit(0)
	
	#Check again after running stopServerNicely and waiting 30 seconds, checking every 5 seconds if it stopped yet
	for i in range(1,30):
		if isServerRunning():
			sleep(1)
			print('Server still running: ' + str(i))
		else:
			print('Server exited')
			sys.exit(0)
	if isServerRunning():
		print('Server still running. Stopping rudely...')
		stopServerRudely()
	else:
		sys.exit(0)
	sleep(5)
	if isServerRunning():
		print('Server STILL RUNNING. Killing server...')
		fuckingMurderTheServer()

	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('CTRL+C hit. Exiting...')
		sys.exit(0)


