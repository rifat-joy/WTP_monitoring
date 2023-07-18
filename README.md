# Developer Muanual  

## Library Information and Installation guide 
    install python -> 3.10 and pip
    pymodbus 3.0.2 -> pip install pymodbus
    paho-mqtt 1.6.1 -> pip install paho-mqtt
    RPi.GPIO 0.7.1 -> pip install RPi.GPIO

## Error Code -> Error Status
    101 -> Flowmeter in Is not connected or not working
    102 -> Flowmeter out Is not connected or not working
    103 -> C4E - Conductivity sensor reading error
    104 -> pH sensor reading error
    105 -> Turbidity sensor reading error
    106 -> Sensor measurements not started


## Remote response:
**Copy and paste this below commands to the Broker terminal ig. mosquitto**
 
    Error code : mosquitto_sub -h "waterplant.vertical-innovations.com" -t Error_code -p 8883 --cafile newvision_root.cer -u "newqttvm" -P "newqttvm"
    Current Status : mosquitto_sub -h "waterplant.vertical-innovations.com" -t current_status -p 8883 --cafile newvision_root.cer -u "newqttvm" -P "newqttvm"
    
**Or These status can be seen from MQTT Explorer using below credentials**
    
    Protocol : mqtt://
    Host     : waterplant.vertical-innovations.com
    Port     : 8883
    Username : newqttvm
    Password : newqttvm
    
 **Check Encryption (tls) then go to Advanced -> Certificates -> Server Certificate (CA) seclect **newvision_root.cer** and hit connect**

## To make a file run on startup

 **Two services running on systemd which makes those executable files run on startup.**

    newVision.service -> Services for sensors and gpio control
    Flowmeter.service -> Services for flowmeter control

    Script Directory : /bin/python /home/pi/Desktop/NewVision/main.py
    Making the script executable “chmod +x filename”
    Then creating a service in “cd /lib/systemd/system”
    Creating a service “sudo touch dummy.service”

    Type “sudo nano newVision.service”

    [Unit]
    Description= Sensors service
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python3 /home/pi/Desktop/NewVision/main.py
    User=pi

    [Install]
    WantedBy=multi-user.target


    Type “sudo nano Flowmeter.service”

    [Unit]
    Description= Flowmeter service
    After=multi-user.target

    [Service]
    ExecStart=/usr/bin/python3 /home/pi/Desktop/NewVision/Flowmeter.py
    User=pi

    [Install]
    WantedBy=multi-user.target

## For Example:

    To start the service type command:
    “sudo systemctl enable newVision.service”

    To stop service:
    “sudo systemctl disable newVision.service”

    To Confirm enable status
    “sudo systemctl is-enabled newVision.service”

    To  Start a service
    “sudo systemctl start newVision.service”

    To stop a service
    “sudo systemctl stop newVision.service”

    Need to reload the daemon whenever changes made in services file:
    “sudo systemctl daemon-reload”

 ## To remote access to raspberry pi

    Remote access is done via dataplicity, a simple way to access raspberry pi terminal via the internet.
    Go to this link - https://www.dataplicity.com/devices/

    Sign in there using provided credentials
    Email : rifat.islam@vertical-innovations.com
    Password : vilnewvisionru

    Then go to the device to access the pi terminal
    Type "su pi" at the terminal to make the user pi as super user then conventional terminal will appear

    Real VNC credentials:
    Email : rifat.islam@vertical-innovations.com
    Password : newvisionrnd
