# amadanBot
 ---
A small bot made for a small Discord. Most things are hardcoded and will not work on other Discord servers.
___

## Current State:

### On Join
When  a new member joins they will be assigned the 'New' role.  
The bot will then DM them asking for in game name.  
If the IGN matches a member of the PS2 outfit they are automaticaly assigned  the 'Amadan' role and their nickname is changed to their provided IGN.

### Commands (>)
###### ping
>Answers "Pong".
###### listNewMembers
>Displays all members with 'New' role still assigned
## ToDo: (Client)
- [x] Assign 'New' role for new members
- [x] Ask for name and check against DBG database, assign role base off answer
- [x] Command to list 'New' members
- [x] Send ping on continent lock alerts
- [ ] Send ping on continent unlock
- [ ] Command to check TeamSpeak Users
- [ ] Command to check Planetside status (continent, pop, alerts)
- [ ] Automatically move Teamspeak users to AFK channel after given idle time
## ToDo: (Server)
- [x] Thread Discord and DBG client to run at same time
- [x] Get Discord server object from non-Discord function
- [ ] Implement encrypted secrets (tokens, Discord IDs)