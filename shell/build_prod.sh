# Config Variables: PATHS
BOT="./Discord-Bot/"
SERVER="./Web-Server/"
GIT_BOT="./LotusBot/"
GIT_SERVER="./ServerSys/"

# Actions: Kill App
pkill python

# Actions: Remove Previous
rm -r -f $BOT
rm -r -f $SERVER
rm -r -f $GIT_BOT
rm -r -f $GIT_SERVER


# Actions: Make Directories
mkdir $BOT
mkdir $SERVER


# Actions: Clone Code
git clone https://github.com/Deadtrix21/LotusBot.git
#git clone https://github.com/Deadtrix21/LotusBot.git


# Actions: Move Code
cp $GIT_BOT* $BOT -r


# Actions: Remove Git Directories
rm -r -f $GIT_BOT
rm -r -f $GIT_SERVER