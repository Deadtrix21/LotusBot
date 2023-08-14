apt update && sudo apt upgrade -y
add-apt-repository ppa:linuxuprising/java -y
apt update
apt-get install -y oracle-java17-installer oracle-java17-set-default

echo java -version

sudo apt-get -y install python3-pip git


mkdir "discord-bot"
cd "./discord-bot"

git clone "https://github.com/Deadtrix21/LotusBot.git"
cp ./LotusBot/* ./ -r
rm -r -f "./LotusBot"

python3 -m pip install -r ./requirements.txt