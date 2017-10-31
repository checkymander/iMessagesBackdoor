# iMessagesBackdoor
A script to help set up an event handler in order to install a persistent backdoor that can be activated by sending a message.

# Explanation
Just as <a href="https://www.n00py.io/2016/10/using-email-for-persistence-on-os-x/">Mail.app</a> and <a href="https://github.com/sensepost/ruler">Outlook</a> can be used to create a persistent backdoor on a victim, iMessages can also be used in order to keep access to a victim machine.

iMessages supports an AppleScript handler that can be set to execute a shell commands on the firing of a specific trigger. A few examples of these triggers:

- Received Text Invitation

- Message Sent

- Message Received

- Login Finished

- Logout Finished

By modifying the Preferences in the GUI you can set an AppleScript handler that defines what happens when each of these events triggers.

However, on a Red Team engagement we'd likely want to do this exclusively from the command line. Luckily, we're able to manually modify  the plist file in order to force the application to accept our AppleScript handler.

iMessages stores its preferences file in two locations:

> \~/Library/Preferences/com.apple.iChat.plist

and

> \~/Library/Containers/com.apple.soagent/Data/Library/Preferences/com.apple.messageshelper.AlertsController.plist

The second plist seems to takes precedence over the first during my own testing.

<strong>Note:</strong> If someone can explain to me why this is, I'd love to know.

If you were to try and open the files in a text editor such as vim you would get a binary blob, that's because by default MacOSX stores these plist files in a binary format, however they provide a neat little tool that can be used to convert it into a human readable XML format.

>plutil -convert xml1 \~/Library/Containers/com.apple.soagent/Data/Library/Preferences/com.apple.messageshelper.AlertsController.plist

Now we can open the file in our text editor and see the list of keys available in this preference files. The key we're going to be looking for is named <strong>AppleScriptNameKey</strong>, this is the key that controls which AppleScript file defines the handlers and the script we'd like to modify in order to execute our shell commands.

The best part is that you can modify already existing scripts in order to remain under the radar, and as far as security products are concerned it's legitimate functionality!

After modifying this file, you'll want to convert the plist file back to binary and the Messages.app will need to be restarted for the application to pick up these new preferences. This can be done from the command line using the following commands:

> plutil -convert binary1 ~/Library/Containers/com.apple.soagent/Data/Library/Preferences/com.apple.messageshelper.AlertsController.plist

> killall Messages

> killall soagent

<strong>Warning: </strong>This will cause the application to bounce and the user may notice that the application restarted, although you could also potentially just be patient and wait for the user to restart their computer.

Now anytime your victim receives a message containing your keyword, a shell command will be executed containing your payload!

# Usage
python iMessagesBackdoor.py [-h] [-handler HANDLERNAME] [--force] [--delete] [--verbose]

-handler HANDLERNAME : The name of the applescript file that will be stored in the iMessages configuration (Does not require .scpt extension)

--force : &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Force overwriting of the users currenct applescript event handler

--delete :&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Removes the current script handler.

--verbose :&nbsp;&nbsp; Displays debugging messages.

ex. python iMessagesBackdoor.py -handler backdoor --force

# Usage with Empire:
In order to install an Empire backdoor on your target using iMessages generate an empire stager in accordance with the instructions <a href="https://www.powershellempire.com/?page_id=104">here</a>

Copy the output into the event handler you want to control your backdoor. 
Place this file into 

> ~/Library/Application Scripts/Com.Apple.iChat 

or 

> ~/Library/Scripts/Messages (Messages 7.x.x - Mountain Lion)

Run the iMessagesBackdoor.py command in order to set the user preferences to run the backdoor.


# Example run command on message received:
1.) Copy the output into the "On message received" event handler within backdoor.scpt.

2.) Replace "helloworld" with the keyword that you want to use to execute your backdoor.

3.) Place the file in ~/Library/Application Scripts/com.apple.iChat/

4.) Terminal: python iMessagesBackdoor.py -handler backdoor --force.

5.) Send a message to your target containing the phrase and you should get a connection to your empire server.

# TODO:
1.) Take the contents of the username from this file and display it for the user to easier see what account to send the message to.

2.) Better fix the script in order to delete all traces of the message from the user.

3.) Implement into an Empire Module

