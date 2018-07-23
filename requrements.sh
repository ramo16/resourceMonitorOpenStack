
echo "Install Grafana Server"
sudo apt-get -y install curl
sudo apt-get install -y apt-transport-https
sudo apt install curl
wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.2.0_amd64.deb
sudo apt-get install -y adduser libfontconfig
sudo dpkg -i grafana_4.2.0_amd64.deb
echo "deb https://packagecloud.io/grafana/stable/debian/ jessie main"| sudo tee -a /etc/apt/sources.list
curl https://packagecloud.io/gpg.key | sudo apt-key add -
sudo apt-get update
sudo apt-get -qq --assume-yes install grafana 
sudo service grafana-server start
sleep 5
echo "Install Influx db"
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
sleep 5
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt-get update && sudo apt-get -y install influxdb
sudo service influxdb start
sudo grafana-cli plugins install grafana-piechart-panel
sudo grafana-cli plugins install briangann-datatable-panel
sudo service grafana-server restart
