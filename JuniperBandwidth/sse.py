from ncclient import manager
import time
import json

class ServerSentEvent:
    def __init__(self, username, ip):
        self.username = username
        self.ip = ip

    def generate(self):
        try:
            with open("./JuniperBandwidth/login_juniper.json", "r") as handler:
                login_pass = json.load(handler)

            print(f"Connecting to '{self.ip}'")
            conn = manager.connect(
                    host=self.ip,
                    port='22',
                    username=login_pass["login"],
                    password=login_pass["password"],
                    timeout=10,
                    device_params={'name':'junos'},
                    hostkey_verify=False)

            def getInterfaceIpaddress(command):
                interface = command.xpath('//subscribers-information/subscriber/interface')[0].text.strip()
                ipaddress = command.xpath('//subscribers-information/subscriber/ip-address')[0].text.strip()
                return (interface,ipaddress)
            
            try:
                print(f"Getting info from PPPoE: '{self.username}'")
                interfaceIP = getInterfaceIpaddress(conn.command(f'show subscriber user-name {self.username}'))
                interface = interfaceIP[0]
                ipaddress = interfaceIP[1]
            except:
                message = (f"Error, username '{self.username}' not found!")
                print(message)
                conn.close_session()
                print(f"Connection closed! Host: '{self.ip}'")
                error = json.dumps({'error':message})
                yield "data: " + error + "\n\n"
                return False

            def getSpeed(command):
                inputBW = command.xpath('//transit-traffic-statistics/input-bps')[0].text.strip()
                outputBW = command.xpath('//transit-traffic-statistics/output-bps')[0].text.strip()
                up = (int(inputBW)/1000)
                down = (int(outputBW)/1000)
                infilter = command.xpath('//filter-information/filter-input')[0].text.strip()
                filterIN = "IN-" + infilter.split('-')[1]
                outfilter = command.xpath('//filter-information/filter-output')[0].text.strip()
                filterOUT = "OUT-" + outfilter.split('-')[1]
                values = {'up':int(up),'down':int(down),'filterin':filterIN,'filterout':filterOUT}
                return values

            while True:
                try:
                    data = getSpeed(conn.command(f'show interfaces {interface} statistics detail'))
                    data['username'] = self.username
                    data['ipaddress'] = ipaddress
                    values = json.dumps(data)
                    yield "data: " + values + "\n\n"
                    time.sleep(2)
                except Exception as e:
                    message = "Conection lost!"
                    print(message)
                    conn.close_session()
                    print(f"Connection closed! Host: '{self.ip}'")
                    error = json.dumps({'error':message})
                    yield "data: " + error + "\n\n"
                    break

        except GeneratorExit:
            conn.close_session()
            print(f"Connection closed! Host: '{self.ip}'")

        except Exception as e:
            message = "Problem found! " + str(e)
            print(message)
            error = json.dumps({'error':message})
            yield "data: " + error + "\n\n"
            return False
