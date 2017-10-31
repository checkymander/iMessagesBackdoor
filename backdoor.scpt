using terms from application "Messages"
	
	on received text invitation theText from theBuddy for theChat
	end received text invitation
	
	on received audio invitation theText from theBuddy for theChat
	end received audio invitation
	
	on received video invitation theText from theBuddy for theChat
	end received video invitation
	
	on received file transfer invitation theFileTransfer
	end received file transfer invitation
	
	on buddy authorization requested theRequest
	end buddy authorization requested
	
	# The following are unused but need to be defined to avoid an error
	
	on message sent theMessage for theChat
		
	end message sent
	
	on message received theMessage from theBuddy for theChat
		if theMessage contains "helloworld" then
			do shell script "sqlite3 ~/Library/Messages/chat.db 'DELETE FROM message WHERE text=\"helloworld\";' && killall -9 \"Messages\" && open /Applications/Messages.app"
		end if
	end message received
	
	on chat room message received theMessage from theBuddy for theChat
		
	end chat room message received
	
	on active chat message received
	end active chat message received
	
	on addressed chat room message received theMessage from theBuddy for theChat
		
	end addressed chat room message received
	
	on addressed message received theMessage from theBuddy for theChat
		
	end addressed message received
	
	on av chat started
		
	end av chat started
	
	on av chat ended
		
	end av chat ended
	
	on login finished for theService
		
	end login finished
	
	on logout finished for theService
		
	end logout finished
	
	on buddy became available theBuddy
		
	end buddy became available
	
	on buddy became unavailable theBuddy
		
	end buddy became unavailable
	
	on completed file transfer
		
	end completed file transfer
end using terms from
