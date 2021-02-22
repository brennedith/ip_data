# Pre-requisites

1. Enable required Raspberry Pi interfaces:
- SPI
- I2C

2. Install required dependencies

```sh
sudo apt-get update
sudo apt-get install python3-pip python3-pil python3-numpy
sudo pip3 install RPi.GPIO spidev
```

3. Run the script

```sh
# Run script manually
python3 ip_data.py

# Schedule a cron job every 30th min from 7am to 10pm
echo "*/30 7-22 * * * $PWD/ip_data.py >> ~/cron.log 2>&1"

crontab -e # Paste result here
```
