#!/usr/bin/env python
__author__ = 'frederikjuutilainen, modified by jonasfehr'

import sys
sys.path.append('/usr/local/lib/python3.5/site-packages/')

import keen, argparse, time, urllib.request,json

from pythonosc import dispatcher
from pythonosc import osc_server

class KeenLog:

    trappeV = 0
    bevaegelse = 0
    trappeH = 0
    sojleV = 0
    sojleH = 0
    week_day = 0
    gehl_day = 0

    def __init__(self):
        keen.project_id = "57ff83d98db53dfda8a7360f"
        keen.write_key = "CFF4875F16541E6451BC503DD99B2BB0C49C44FCB62C2FBA5F5B37282A67BCED14CCC6A443C65A66A58D78A2D64BC03F27D96DB5DE047A7A9095F5A08565CCA851001282251B3ED6E615DD35B4C298DB93CA668142D1717BAF0CF2CB22CBD256"
        keen.read_key = "2A17BDAEC05E7637A7E67580C077024FB53900773CD3597667994AF6EC955E6E1E42AE9842B3F535F60195BA8C53960A5737764CFD7B027207C0D3C9A44C2F11D5F300C8224372248F154471FF3BE7B254C766B007364D4EA61C86F6FADAE396"
        keen.master_key = "53C114F0E2EA4CA1734E126B12ECB77946A9202DD1D368E918A9E5FE899D996D"

    def send_to_server(self, unused_addr):
        keen.add_event("vardeDataLog", {
            "trappeV": self.trappeV,
            "bevaegelse": self.bevaegelse,
            "trappeH": self.trappeH,
            "sojleV": self.sojleV,
            "sojleH": self.sojleH,
            "week_day": self.week_day,
            "gehl_day": self.gehl_day
        })
        print("Log seent to Keen.io at: ", time.strftime('%X %x'))

    def print_log(self, unused_addr):
        print("vardeDataLog", {
            "trappeV": self.trappeV,
            "bevaegelse": self.bevaegelse,
            "trappeH": self.trappeH,
            "sojleV": self.sojleV,
            "sojleH": self.sojleH,
            "week_day": self.week_day,
            "gehl_day": self.gehl_day
        })

    def set_trappeV(self,unused_addr,input):
        self.trappeV = input

    def set_bevaegelse(self,unused_addr,input):
        self.bevaegelse = input

    def set_trappeH(self,unused_addr,input):
        self.trappeH = input

    def set_sojleV(self,unused_addr,input):
        self.sojleV = input

    def set_sojleH(self,unused_addr,input):
        self.sojleH = input

    def set_week_day(self,unused_addr,input):
        self.week_day = input

    def set_gehl_day(self,unused_addr,input):
        self.gehl_day = input

# Main loop / OSC Listener
port = 7281
ip = "127.0.0.1"
log = KeenLog()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=ip, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=port, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    # Assigning methods for incoming OSC messages
    dispatcher.map("/trappeV", log.set_trappeV)
    dispatcher.map("/bevaegelse", log.set_bevaegelse)
    dispatcher.map("/trappeH", log.set_trappeH)
    dispatcher.map("/sojleV", log.set_sojleV)
    dispatcher.map("/sojleH", log.set_sojleH)
    dispatcher.map("/week_day",log.set_week_day)
    dispatcher.map("/gehl_day",log.set_gehl_day)

# Logging!
    dispatcher.map("/go", log.send_to_server) # vent til tr er sat op. Max 50,000 logs per mned
    dispatcher.map("/go", log.print_log)  # Temporary

server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
