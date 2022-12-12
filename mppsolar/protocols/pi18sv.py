import logging

from .abstractprotocol import AbstractProtocol

from .protocol_helpers import crcPI as crc

# from .pi30 import COMMANDS

log = logging.getLogger("18sv")

COMMANDS = {
    "PI": {
        "name": "PI",
        "prefix": "^P005",
        "crc": False,
        "description": "Device Protocol Version inquiry",
        "help": " -- queries the device protocol version",
        "type": "QUERY",
        "response": [["string", "Protocol Version", ""]],
        "test_responses": [
            b"^D00518;\x03\r",
        ],
    },
    "T": {
        "name": "T",
        "prefix": "^P004",
        "crc": False,        
        "description": "Query current time",
        "help": " -- queries current time from the Inverter",
        "type": "QUERY",
        "response": [
            ["string", "DateTime", "YYYYMMDDHHMMSS"],
        ],
        "test_responses": [
            b"^D01720210521234743\x0eR\r",
        ],
    },
    "ET": {
        "name": "ET",
        "prefix": "^P005",
        "crc": False,        
        "description": "Query total generated energy",
        "help": " -- queries total generated energy from the Inverter",
        "type": "QUERY",
        "response": [
            ["int", "Generated energy", "kWh"],
        ],
        "test_responses": [
            b"^D01100006591\xba\x10\r",
        ],
    },
    "EY": {
        "name": "EY",
        "prefix": "^P009",
        "crc": False,
        "description": "Query generated energy of year",
        "help": " -- queries generated energy for the year YYYY from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated energy", "Wh"],
        ],
        "test_responses": [
            b"^D01100006591\xba\x10\r",
        ],
        "regex": "EY(\\d\\d\\d\\d)$",
    },
    "EM": {
        "name": "EM",
        "prefix": "^P011",
        "crc": False,
        "description": "Query generated energy of month",
        "help": " -- queries generated energy for the month YYYYMM from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated energy", "Wh"],
        ],
        "test_responses": [
            b"^D01000006591\xba\x10\r",
        ],
        "regex": "EM(\\d\\d\\d\\d\\d\\d)$",
    },
    "ED": {
        "name": "ED",
        "prefix": "^P013",
        "crc": True,
        "description": "Query generated energy of day",
        "help": " -- queries generated energy for the day YYYYMMDD from the Inverter",
        "type": "QUERYEN",
        "response": [
            ["int", "Generated energy", "Wh"],
        ],
        "test_responses": [
            b"^D01100003537\x89X\r",
        ],
        "regex": "ED(\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },    
    "ID": {
        "name": "ID",
        "prefix": "^P005",
        "crc": False,
        "description": "Device Serial Number inquiry",
        "help": " -- queries the device serial number",
        "type": "QUERY",
        "response": [["string", "Serial Number", ""]],
        "test_responses": [
            b"^D0251496161704100242000000le\r",
        ],
    },
    "VFW": {
        "name": "VFW",
        "prefix": "^P006",
        "crc": True,
        "description": "Device CPU version inquiry",
        "help": " -- queries the CPU version",
        "type": "QUERY",
        "response": [["int", "Main CPU Version", ""],
                     ["int", "Slave 1 CPU version",""],
                     ["int", "Slave 2 CPU version",""]],
        "test_responses": [
            b"^D02005402,08025,00000)\xc3\x9d\r",
        ],
    },
    "MCHGCR": { # On my SV IV, this commands returns 12 values, from 10 to 120 amps
        "name": "MCHGCR",
        "prefix": "^P009",
        "crc": True,
        "description": "Query Max. charging current selectable values",
        "help": " -- queries the Max. charging current selectable values",
        "type": "QUERY",
        "response": [["int", "Max. charging current selectable value 1", "A"],
                     ["int", "Max. charging current selectable value 2", "A"],
                     ["int", "Max. charging current selectable value 3", "A"],
                     ["int", "Max. charging current selectable value 4", "A"],
                     ["int", "Max. charging current selectable value 5", "A"],
                     ["int", "Max. charging current selectable value 6", "A"],
                     ["int", "Max. charging current selectable value 7", "A"]],
#                     ["int", "Max. charging current selectable value 8", "A"]],
#                     ["int", "Max. charging current selectable value 9", "A"]],
#                     ["int", "Max. charging current selectable value 10", "A"]],
#                     ["int", "Max. charging current selectable value 11", "A"]],
#                     ["int", "Max. charging current selectable value 12", "A"]],                         
        "test_responses": [
            b"^D030010,020,030,040,050,060,070\n",
        ],
    },
    "MUCHGCR": { # On my SV IV, this commands returns 13 values, from 2 to 120 amps
        "name": "MUCHGCR",
        "prefix": "^P010",
        "crc": True,
        "description": "Query Max. AC charging current selectable values",
        "help": " -- queries the Max. AC charging current selectable values",
        "type": "QUERY",
        "response": [["int", "Max. charging current selectable value 1", "A"],
                     ["int", "Max. charging current selectable value 2", "A"],
                     ["int", "Max. charging current selectable value 3", "A"],
                     ["int", "Max. charging current selectable value 4", "A"],
                     ["int", "Max. charging current selectable value 5", "A"],
                     ["int", "Max. charging current selectable value 6", "A"],
                     ["int", "Max. charging current selectable value 7", "A"]],
#                     ["int", "Max. charging current selectable value 8", "A"]],
#                     ["int", "Max. charging current selectable value 9", "A"]],
#                     ["int", "Max. charging current selectable value 10", "A"]],
#                     ["int", "Max. charging current selectable value 11", "A"]],
#                     ["int", "Max. charging current selectable value 12", "A"]],
#                     ["int", "Max. charging current selectable value 12", "A"]],                                 
        "test_responses": [
            b"^D030010,020,030,040,050,060,070\n",
        ],
    },
    "PRI": {
        "name": "PRI",
        "prefix": "^P007",
        "crc": True,
        "description": "Query different rated information of parallel system",
        "help": " -- queries different rated information of parallel system",
        "type": "QUERYEN",
        "response": [
            ["option", "Parallel ID connection status", ["Not existent","Existent"]],
            ["int", "Serial Number valid length", ""],
            ["string", "Serial Number", ""],
            ["option", "Charging source priority", ["Solar first","Solar and Utility","Only Solar"]],
            ["int", "Max. charging current", "A"],
            ["int", "Max. AC charging current", "A"],
            ["option", "Output mode setting", ["Single mode", "parallel output", "Phase 1 of 3 phases", "Phase 2 of 3 phases", "Phase 3 of 3 phases"]],
        ],
        "test_responses": [
            b"^D0401,14,96132206100410000000,2,060,050,1Jl\r",
        ],
        "regex": "PRI(\\d)$",
    },
    "PGS": {
        "name": "PGS",
        "prefix": "^P007",
        "crc": True,
        "description": "Query general status of parallel system",
        "help": " -- queries  general status of parallel system",
        "type": "QUERYEN",
        "response": [
            ["option", "Parallel ID connection status", ["Not existent","Existent"]],
            ["int", "Work mode", ""],
            ["int", "Fault code", ""],
            ["int", "Grid voltage", "0.1V"],
            ["int", "Grid frequency", "0.1HZ"],
            ["int", "AC output voltage", "0.1V"],                        
            ["int", "AC output frequency", "0.1Hz"],
            ["int", "AC output apparent power", "VA"],
            ["int", "AC output active power", "W"],
            ["int", "Total AC output apparent power", "VA"],
            ["int", "Total AC output active power", "W"],
            ["int", "Output load percent", "%"],
            ["int", "Total output load percent", "%"],
            ["int", "Battery voltage", "0.1V"],
            ["int", "Battery discharge current", "A"],
            ["int", "Battery charging current", "A"],
            ["int", "Total battery charging current", "A"],
            ["int", "Battery capacity", "%"],
            ["int", "PV1 Input power", "W"],
            ["int", "PV2 Input power", "W"],
            ["int", "PV1 Input voltage", "0.1V"],
            ["int", "PV2 Input voltage", "0.1V"],
            ["option", "MPPT1 charger status", ["abnormal", "normal but not charging", "charging"]],
            ["option", "MPPT2 charger status", ["abnormal", "normal but not charging", "charging"]],
            ["option", "Load connection", ["disconnect","connect"]],
            ["option", "Battery power direction", ["donothing","charge","discharge"]],
            ["option", "DC/AC power direction", ["donothing","AC-DC","DC-AC"]],
            ["option", "Line power direction", ["donothing", "input", "output"]],
            ["int", "Max Temperature", "°C"],            
        ],
        "test_responses": [
            b"^D1131,5,00,2387,499,2387,499,0716,0165,01232,00505,012,004,518,000,015,031,036,1137,0000,2088,0000,2,0,1,1,2,1,037\x8a$\r",
        ],
        "regex": "PGS(\\d)$",
    },        
    "FWS": {
        "name": "FWS",
        "prefix": "^P005",
        "crc": True,
        "description": "Query fault and warning status",
        "help": " -- queries the fault and warning status",
        "type": "QUERY",
        "response": [
            ["int", "Fault code", ""],
            ["int", "Line fail", ""],            
            ["int", "Output circuit short", ""],
            ["int", "Inverter over temperature", ""],
            ["int", "Fan lock", ""],
            ["int", "Battery voltage high", ""],
            ["int", "Battery low", ""],
            ["int", "Battery under", ""],
            ["int", "Over load", ""],
            ["int", "EEProm fail", ""],
            ["int", "Power limit", ""],
            ["int", "PV1 voltage high", ""],
            ["int", "PV2 voltage high", ""],
            ["int", "MPPT1 overload warning", ""],
            ["int", "MPPT2 overload warning", ""],
            ["int", "Battery too low to charge for SCC1", ""],
            ["int", "Battery too low to charge for SCC2", ""],                                                
        ],
        "test_responses": [
            b"^D03900,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\xc2\xb6\x9e\r",
        ],
    },    
    "DI": {
        "name": "DI",
        "prefix": "^P005",
        "crc": False,
        "description": "Query default value of changeable parameters",
        "help": "",
        "type": "QUERY",
        "response": [
            ["int", "AC output voltage", "0.1V"],
            ["int", "AC output frequency", "0.1Hz"],
            ["option", "AC input voltage range", ["Appliance", "UPS"]],
            ["int", "Battery Under voltage", "0.1V"],
            ["int", "Charging float voltage", "0.1V"],
            ["int", "Charging bulk voltage", "0.1V"],
            ["int", "Battery default re-charge voltage", "0.1V"],
            ["int", "Battery re-discharge voltage", "0.1V"],
            ["int", "Max charging current", "A"],
            ["int", "Max AC charging current", "A"],
            ["option", "Battery type", ["AGM","Flooded","User"]],
            ["option", "Output source priority", ["Solar-Utility-Battery","Solar-Battery-Utility"]],
            ["option", "Charger source priority", ["Solar first", "Solar and Utility", "Only solar"]],
            ["option", "Solar power priority", ["Battery-Load-Utility","Load-Battery-Utility"]],
            ["option", "Machine type", ["Off-Grid","Grid-Tie"]],
            ["option", "Output mode setting", ["Single mode", "parallel output", "Phase 1 of 3 phases", "Phase 2 of 3 phases", "Phase 3 of 3 phases"]],
            ["option", "Silence buzzer or open buzzer", ["disable","enable"]],
            ["option", "Overload restart", ["disable","enable"]],
            ["option", "Over temperature restart", ["disable","enable"]],
            ["option", "LCD backlight on", ["disable","enable"]],
            ["option", "Alarm when primary source interrupted", ["disable","enable"]],
            ["option", "Fault code record", ["disable","enable"]],
            ["option", "Overload bypass", ["disable","enable"]],
            ["option", "LCD display escape to default page after timeout", ["disable","enable"]],                                             
        ],
        "test_responses": ['^D0682300,500,0,408,540,564,460,540,060,30,0,0,1,0,0,0,1,0,0,1,1,0,1,1Q\xc3\xa6\r']
    },
    "PIRI": {
        "name": "PIRI",
        "prefix": "^P007",
        "crc": True,
        "description": "Device rated information",
        "help": " -- queries rated information",
        "type": "QUERY",
        "response": [
            ["int", "AC input rated voltage", "0.1V"],
            ["int", "AC input rated current", "0.1A"],
            ["int", "AC output rated voltage", "0.1V"],
            ['int', "AC output rated frequency", "0.1HZ"],            
            ["int", "AC output rated current", "0.1A"],
            ["int", "AC output rated apparent power", "1VA"],
            ["int", "AC output rated active power", "W"],
            ["int", "Battery rated voltage", "0.1V"],
            ["int", "Battery recharge voltage", "0.1V"],
            ["int", "Battery redischarge voltage", "0.1V"],
            ["int", "Battery under voltage", "0.1V"],
            ["int", "Battery bulk voltage", "0.1V"],
            ["int", "Battery float voltage", "0.1V"],
            ["option", "Battery Type", ["AGM", "Flooded", "User"]],
            ["int", "Max AC charging current", "A"],
            ["int", "Max charging current", "A"],            
            ["option", "Input voltage range", ["Appliance","UPS"]],
            ["option", "Output source priority", ["Solar-Utility-Battery","Solar and Utility"]],
            ["option", "Charger source priority", ["Solar first","Solar and Utility","Only Solar"]],
            ["int", "Parallel max num", ""],
            ["option", "Machine type", ["Off-grid","Grid-tie"]],
            ["option", "Topology", ["transformerless", "transformer"]],
            ["option", "Output model setting", ["Single module","Parallel output","Phase 1 of 3 output","Phase 2 of 3 output","Phase 3 of 3 output"]],
            ["option", "Solar power priority", ["Battery-Load-Utility", "Load-Battery-Utility"]],
            ["int", "MPPT string", ""]
        ],
        "test_responses": [
            b'^D0892300,243,2300,500,243,5600,5600,480,500,530,480,570,544,2,050,060,0,1,2,9,0,0,1,1,1,00\x8e~\r'
        ],
    },
    "GS": {
        "name": "GS",
        "prefix": "^P005",
        "crc": False, # For some strange reason, crc makes this query return only partial infos ?!
        "description": "Query general status",
        "help": " -- queries general status",
        "type": "QUERY",
        "response": [
            ["int", "AC Input Voltage", "0.1V"],
            ["int", "AC Input Frequency", "0.1Hz"],
            ["int", "AC Output Voltage", "0.1V"],
            ["int", "AC Output Frequency", "0.1Hz"],
            ["int", "AC Output Apparent Power", "VA"],
            ["int", "AC Output Active Power", "W"],
            ["int", "AC Output Load", "%"],
            ["int", "Battery Voltage", "0.1V"],
            ["int", "Battery Voltage from SCC", "0.1V"],
            ["int", "Battery Voltage from SCC2", "0.1V"],                        
            ["int", "Battery Discharge Current", "A"],
            ["int", "Battery Charge Current", "A"],            
            ["int", "Battery Capacity", "%"],
            ["int", "Inverter Temperature", "°C"],
            ["int", "MPPT1 Charger Temperature", "°C"],
            ["int", "MPPT2 Charger Temperature", "°C"],
            ["int", "PV1 Input Power","W"],
            ["int", "PV2 Input Power","W"],
            ["int", "PV1 Input Voltage","0.1V"],
            ["int", "PV2 Input Voltage","0.1V"],
            ["option", "Setting value configuration state", ["Nothing changed","Something changed"]],
            ["option", "MPPT1 charger status", ["abnormal","normal but not charged","normal"]],
            ["option", "MPPT2 charger status", ["abnormal","normal but not charged","normal"]],
            ["option", "Load connection", ["disconnect","connect"]],
            ["option", "Battery power direction", ["donothing","charge","discharge"]],
            ["option", "DC/AC power direction", ["donothing","AC-DC","DC-AC"]],
            ["option", "Line power direction", ["donothing","input","output"]],
            ["int", "Local parallel ID", ""]     
        ],        
        "test_responses": [
            b'^D1062336,499,2336,499,0443,0255,007,524,000,000,000,017,042,039,000,000,1326,0000,1907,0000,0,2,0,1,1,2,1,1`\xc3\xaa\r'
        ],
    },
    "MOD": {
        "name": "MOD",
        "prefix": "^P006",
        "crc": True,
        "description": "Device working mode inquiry",
        "help": " -- queries the device working mode",
        "type": "QUERY",
        "response": [
            [
                "keyed",
                "Working mode",
                {
                    "00": "Power on mode",
                    "01": "Standby mode",
                    "02": "Bypass mode",
                    "03": "Battery mode",
                    "04": "Fault mode",
                    "05": "Hybrid mode (Line mode, Grid mode)",
                },
            ],
        ],
        "test_responses": [
            b"^D00505\xc3\x99\x9f\r",
        ],
    },
    "FLAG": {
        "name": "FLAG",
        "prefix": "^P007",
        "crc": True,
        "description": "Query enable/disable flag status",
        "help": " -- queries enable/disable flag status from the Inverter",
        "type": "QUERY",
        "response": [
            ["option", "Mute buzzer beep", ["Disabled", "Enabled"]],
            ["option", "Overload bypass function", ["Disabled", "Enabled"]],
            ["option", "LCD Display escape to default page after timeout", ["Disabled", "Enabled"]],
            ["option", "Overload restart", ["Disabled", "Enabled"]],
            ["option", "Over temperature restart", ["Disabled", "Enabled"]],
            ["option", "Backlight on", ["Disabled", "Enabled"]],
            ["option", "Alarm on when primary source interrupted", ["Disabled", "Enabled"]],
            ["option", "Fault code record", ["Disabled", "Enabled"]],
            ["option", "Reserved", ["Disabled", "Enabled"]],                                                                        
        ],
        "test_responses": [
            b"'^D0201,0,1,0,0,1,1,0,0\xc3\x85\xa0\r'",
        ],
    },
    "ACCT": {
        "name": "ACCT",
        "prefix": "^P005",
        "crc": True,
        "description": "Query AC charge time bucket",
        "help": " -- queries AC charge time bucket",
        "type": "QUERY",
        "response": [
            ["string", "Start time for enable AC charger working", "HH:MM"],
            ["string", "Ending time for enable AC charger working", "HH:MM"],                                                        
        ],
        "test_responses": [
            b"^D0201,0,1,0,0,1,1,0,0\xc3\x85\xa0\r",
        ],
    },
    "ACCT": {
        "name": "ACCT",
        "prefix": "^P005",
        "crc": True,
        "description": "Query AC charge time bucket",
        "help": " -- queries AC charge time bucket",
        "type": "QUERY",
        "response": [
            ["string", "Start time for enable AC charger working", "HH:MM"],
            ["string", "Ending time for enable AC charger working", "HH:MM"],                                                        
        ],
        "test_responses": [
            b"^D0120000,0000\xc3\x82\x1c\r",
        ],
    },
    "ACLT": {
        "name": "ACLT",
        "prefix": "^P005",
        "crc": True,
        "description": "Query AC supply load time bucket",
        "help": " -- queries AC supply load time bucket",
        "type": "QUERY",
        "response": [
            ["string", "Start time for enable AC supply the load", "HH:MM"],
            ["string", "Ending time for enable AC supply the load", "HH:MM"],                                                        
        ],
        "test_responses": [
            b"^D0120000,0000\xc3\x82\x1c\r",
        ],
    },
    
    # Now the setters
    "LON": {
        "name": "LON",
        "prefix": "S007",
        "crc": True,
        "description": "Set enable/disable machine supply power to the loads",
        "help": " -- examples: LON1 (0: disable, 1: enable)",
        "type": "SETTER",        
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "LON([01])$",
    },
    "PEA": {
        "name": "PEA",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Silence buzzer or open buzzer",
        "help": " -- Enable Silence buzzer or open buzzer",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDA": {
        "name": "PDA",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Silence buzzer or open buzzer",
        "help": " -- Disable Silence buzzer or open buzzer",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },    
    "PEB": {
        "name": "PEB",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Overload bypass function",
        "help": " -- Enable Overload bypass function",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDB": {
        "name": "PDB",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Overload bypass function",
        "help": " -- Disable Overload bypass function",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEC": {
        "name": "PEC",
        "prefix": "S006",
        "crc": True,
        "description": "Enable LCD display escape to default page after 1min timeout",
        "help": " -- Enable LCD display escape to default page after 1min timeout",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDC": {
        "name": "PDC",
        "prefix": "S006",
        "crc": True,
        "description": "Disable LCD display escape to default page after 1min timeout",
        "help": " -- Disable LCD display escape to default page after 1min timeout",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PED": {
        "name": "PED",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Overload restart",
        "help": " -- Enable Overload restart",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDD": {
        "name": "PDD",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Overload restart",
        "help": " -- Disable Overload restart",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEE": {
        "name": "PEE",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Over temperature restart",
        "help": " -- Enable Over temperature restart",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDE": {
        "name": "PDE",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Over temperature restart",
        "help": " -- Disable Over temperature restart",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEF": {
        "name": "PEF",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Backlight on",
        "help": " -- Enable Backlight on",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDF": {
        "name": "PDF",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Backlight on",
        "help": " -- Disable Backlight on",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEG": {
        "name": "PEG",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Alarm on when primary source interrupt",
        "help": " -- Enable Alarm on when primary source interrupt",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDG": {
        "name": "PDG",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Alarm on when primary source interrupt",
        "help": " -- Disable Alarm on when primary source interrupt",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEH": {
        "name": "PEH",
        "prefix": "S006",
        "crc": True,
        "description": "Enable Fault code record",
        "help": " -- Enable Fault code record",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDH": {
        "name": "PDH",
        "prefix": "S006",
        "crc": True,
        "description": "Disable Fault code record",
        "help": " -- Disable Fault code record",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PEI": {
        "name": "PEI",
        "prefix": "S006",
        "crc": True,
        "description": "Set Machine type Grid-Tie",
        "help": " --Set Machine type Grid-Tie",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PDI": {
        "name": "PDI",
        "prefix": "S006",
        "crc": True,
        "description": "Set Machine type Off-Grid",
        "help": " -- Set Machine type Off-Grid",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "PF": {
        "name": "PF",
        "prefix": "S005",
        "crc": True,
        "description": "Set changeable parameter restore to default value",
        "help": " -- Set changeable parameter restore to default value",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
    },
    "MCHGC": {
        "name": "MCHGC",
        "prefix": "S013",
        "crc": False,
        "description": "Set battery maximum charge current",
        "help": " -- MCHGCRm,nnn with m : 0~Parallel number, if single model, it should be 0 ; n : current. Must choose a seable value returned by MCHGCR ; Ex: MCHGC0,050",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MCHGC(\\d,\\d\\d\\d)$",
    },
    "MUCHGC": { # Not working
        "name": "MUCHGC",
        "prefix": "S014",
        "crc": False,
        "description": "Set battery maximum AC charge current",
        "help": " -- MUCHGCm,nnn with m : 0~Parallel number, if single model, it should be 0 ; n : current. Must choose a seable value returned by MUCHGCR ; Ex: MUCHGC0,050",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MUCHGC(\\d,\\d\\d\\d)$",
    },
    "MCHGV": {
        "name": "MCHGV",
        "prefix": "S015",
        "crc": True,
        "description": "Set battery maximum charge voltage",
        "help": " -- MCHGVmmm,nnn with mmm battery constant charge voltage and nnn battery float voltage. Unit 0.1V",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "MCHGV(\\d\\d\\d,\\d\\d\\d)$",
    },                
    "DAT": {
        "name": "DAT",
        "prefix": "S018",
        "crc": True,
        "description": "Set date time",
        "help": " -- examples: DAT190518224530(YYMMDDHHMMSS-12digits)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "DAT(\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d)$",
    },
    "POP": {
        "name": "POP",
        "prefix": "S007",
        "crc": True,
        "description": "Set output source priority",
        "help": " -- POP0 : Solar-Utility-Battery ; POP1 : Solar-Battery-Utility",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "POP(\\d)$",
    },
    "BUCD": {
        "name": "BUCD",
        "prefix": "S014",
        "crc": True,
        "description": "Battery re-charged and re-discharged voltage when utility is available",
        "help": " -- BUCDmmm,nnn with mmm battery recharge voltage when utility available (44 to 51V) and nnn Battery re-discharged voltage when utility is available (0,48-58)",
        "type": "SETTER",
        "response": [
            ["ack", "Command execution", {"NAK": "Failed", "ACK": "Successful"}],
        ],
        "test_responses": [
            b"^1\x0b\xc2\r",
            b"^0\x1b\xe3\r",
        ],
        "regex": "BUCD(\\d\\d\\d,\\d\\d\\d)$",
    },
    
}


class pi18sv(AbstractProtocol):
    def __str__(self):
        return "PI18-SV protocol handler"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self._protocol_id = b"PI18SV"
        self.COMMANDS = COMMANDS
        self.STATUS_COMMANDS = ["PI","T","ET","EY","EM","ED","ID","VFW","PIRI","GS","MOD","FWS","FLAG","DI","CHGCR","MUCHGCR","PRI","PGS","ACCT","ACLT"]
        self.SETTINGS_COMMANDS = [
            "LON",
            "PEA","PDA","PEB","PDB","PEC","PDC","PED","PDD","PEE","PDE","PEF","PDF","PEG","PDG","PEH","PDH",
            "PF",
            "MUCHGC",
            "MUCHGV",
            "MCHGV",
            "BUCD",
            "DAT"
        ]
        self.DEFAULT_COMMAND = "GS"

    def get_full_command(self, command) -> bytes:
        """
        Override the default get_full_command as its different
        """
        log.info(f"Using protocol {self._protocol_id} with {len(self.COMMANDS)} commands")
        # These need to be set to allow other functions to work`
        self._command = command
        self._command_defn = self.get_command_defn(command)
        # End of required variables setting
        if self._command_defn is None:
            return None

        _cmd = bytes(self._command, "utf-8")
        _type = self._command_defn["type"]
        # No CRC in PI17 commands?
        data_length = len(_cmd) + 1
        if _type == "QUERY":
#            _prefix = f"^P{data_length:03}"
            _prefix = self._command_defn["prefix"]
            _pre_cmd = bytes(_prefix, "utf-8") + _cmd
            log.debug(f"_pre_cmd: {_pre_cmd}")
            log.debug(f"_prefix: {_prefix}")
            # calculate the CRC
            crc_high, crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            # PI18 full command "^P005GS\x..\x..\r"
            _crc = bytes([crc_high, crc_low, 13])
            if self._command_defn["crc"] == False :            
                full_command = _pre_cmd + bytes([13]) 
            else :
                full_command = _pre_cmd  + _crc
            log.debug(f"full command: {full_command}")
            return full_command
        elif _type == "QUERYD":
            _prefix = self._command_defn["prefix"]
            _pre_cmd = bytes(_prefix, "utf-8") + _cmd
            log.debug(f"_pre_cmd: {_pre_cmd}")
            log.debug(f"_prefix: {_prefix}")
            # calculate the CRC
            # crc_high; crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            # PI18 full command "^P005GS\x..\x..\r"
            # _crc = bytes([crc_high, crc_low, 13])
            full_command = _pre_cmd + bytes([13])  # + _crc
            log.debug(f"full command: {full_command}")
            return full_command
        elif _type == "QUERYEN":
            data_length1 = len(_cmd) + 4
            # _prefix = f"^P{data_length1:03}" # Woot ?
            _prefix = self._command_defn["prefix"]
            log.debug(f"_prefix: {_prefix}")
            intermedstr = _prefix + self._command
            #_numb0 = sum(bytearray(intermedstr, "utf-8")) & 255
            #_numb = f"{_numb0:03d}"
            #log.debug(f"_numb: {_numb}")
            _pre_cmd = bytes(intermedstr, "utf-8")
            log.debug(f"_pre_cmd: {_pre_cmd}")
            crc_high, crc_low = crc(_pre_cmd)
            _crc = bytes([crc_high, crc_low, 13])            
#            full_command = bytes(_pre_cmd, "utf-8") + bytes([13])
            if self._command_defn["crc"] == False :            
                full_command = _pre_cmd + bytes([13])
            else :
                full_command = _pre_cmd + bytes([13])  + _crc            
            log.debug(f"full command: {full_command}")
            return full_command
        elif _type == "SETTER":
            data_length1 = len(_cmd) + 4
            _prefix = '^'+self._command_defn["prefix"]
            log.debug(f"_prefix: {_prefix}")
            #intermedstr = _prefix + "T" #+ self._command
            intermedstr = _prefix + self._command
            _pre_cmd = bytes(intermedstr, "utf-8")
            log.debug(f"_pre_cmd: {_pre_cmd}")
            crc_high, crc_low = crc(_pre_cmd)
            _crc = bytes([crc_high, crc_low, 13])
            if self._command_defn["crc"] == False:
                full_command = _pre_cmd + bytes([13])
            else :
                full_command = _pre_cmd + _crc
            return full_command
        else:
            _prefix = f"^S{data_length:03}"
            _pre_cmd = bytes(_prefix, "utf-8") + _cmd
            log.debug(f"_pre_cmd: {_pre_cmd}")
            # calculate the CRC
            # crc_high; crc_low = crc(_pre_cmd)
            # combine byte_cmd, CRC , return
            # PI18 full command "^P005GS\x..\x..\r"
            # _crc = bytes([crc_high, crc_low, 13])
            full_command = _pre_cmd + bytes([13])  # + _crc
            log.debug(f"full command: {full_command}")
            return full_command

    def get_responses(self, response):
        """
        Override the default get_responses as its different
        """
        responses = response.split(b",")
        if responses[0] == b"^0\x1b\xe3\r":
            # is a reject response
            return ["NAK"]
        elif responses[0] == b"^1\x0b\xc2\r":
            # is a successful acknowledgement response
            return ["ACK"]

        # Drop ^Dxxx from first response
        responses[0] = responses[0][5:]
        # Remove CRC of last response
        responses[-1] = responses[-1][:-3]
        return responses


# Bugs / Not working
# EMYYYYDD returns an error
