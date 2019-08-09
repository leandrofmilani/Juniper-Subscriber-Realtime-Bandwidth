from ncclient import manager
import time
import json

class ServerSentEvent:
    def __init__(self, username, ip):
        self.username = username
        self.ip = ip

    def generate(self):
        try:
            conn = manager.connect(
                    host=self.ip,
                    port='22',
                    username='teste',
                    password='BUDWjhpgJ8sl',
                    timeout=10,
                    device_params={'name':'junos'},
                    hostkey_verify=False)

            def getInterface(command):
                interface = command.xpath('//subscribers-information/subscriber/interface')[0].text.strip()
                #ipaddress = command.xpath('//subscribers-information/subscriber/ip-address')[0].text.strip()
                return interface
            
            try:
                print('Conecting...')
                print(self.username)
                interface = getInterface(conn.command(f'show subscriber user-name {self.username}'))
            except:
                message = (f"Error, username '{self.username}' not found!")
                print(message)
                conn.close_session()
                print("Closed connection!")
                error = json.dumps({'error':message})
                yield "data: " + error + "\n\n"
                return False

            def realSpeed(value,direction):
                value_kbps = ((int(value)*8)/1024)
                kbps = int(value_kbps)
                if (kbps >= 1024):
                    value_mbps = (kbps / 1024)
                    mbps = round(value_mbps,2)
                    data = {direction:mbps,'speed'+direction:'Mbps'}
                    return data
                else:
                    data = {direction:kbps,'speed'+direction:'Kbps'}
                    return data

            def getSpeed(command):
                inputBW = command.xpath('//transit-traffic-statistics/input-bps')[0].text.strip()
                outputBW = command.xpath('//transit-traffic-statistics/output-bps')[0].text.strip()
                up = (int(inputBW)*8/1024)
                down = (int(outputBW)*8/1024)
                #up = realSpeed(inputBW,'UP')
                #down = realSpeed(outputBW,'Down')
                infilter = command.xpath('//filter-information/filter-input')[0].text.strip()
                filterIN = "IN-" + infilter.split('-')[1]
                outfilter = command.xpath('//filter-information/filter-output')[0].text.strip()
                filterOUT = "OUT-" + outfilter.split('-')[1]
                values = {'up':int(up),'down':int(down),'filterin':filterIN,'filterout':filterOUT}
                #filters = {'filterin':filterIN,'filterout':filterOUT}
                #values = {**up,**down,**filters}
                return values

            while True:
                try:
                    data = getSpeed(conn.command(f'show interfaces {interface} statistics detail'))
                    data['username'] = self.username
                    print(data)
                    values = json.dumps(data)
                    yield "data: " + values + "\n\n"
                    time.sleep(2)
                except Exception as e:
                    message = "Conection lost!"
                    print(message)
                    conn.close_session()
                    print("Closed connection!")
                    error = json.dumps({'error':message})
                    yield "data: " + error + "\n\n"
                    break

        except GeneratorExit:
            conn.close_session()
            print("Closed connection!")

        except Exception as e:
            message = "Problem found! " + str(e)
            print(message)
            error = json.dumps({'error':message})
            yield "data: " + error + "\n\n"
            return False
