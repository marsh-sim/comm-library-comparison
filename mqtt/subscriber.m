brokerAddress = "tcp://localhost";
mqClient = mqttclient(brokerAddress);
subscribe(mqClient, "area/data")

pause(10)

dataTT = read(mqClient);

clear mqClient