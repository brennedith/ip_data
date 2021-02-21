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

# To schedule a cron job for the script, paste the result on crontab
echo "5 * * * * $PWD/ip_data.py >> ~/cron.log 2>&1"

crontab -e
```
