on run argv
    set targetBuddy to item 1 of argv
    tell application "Messages"
        set iMessageService to 1st service whose service type = iMessage
        try
            set targetBuddy to buddy targetBuddy of iMessageService
            return "true"
        on error
            return "false"
        end try
    end tell
end run