""" test area for using construct lib to decode a jk serial packet """
try:
    import construct as cs
    import serial
    import sys
    import argparse
    import codecs
    import time

except ImportError:
    print("You are missing dependencies")
    print("To install use:")
    print("    python -m pip install 'construct'")

def process_text(text):
    index = text.find("1016") 
    index2 = text.find("ce00d5009")
    index3 = text.find("cf00d6009")
    index4 = text.find("00000000000000000000000000000000000005")

    index5 = text.find("c700c8008d03efb72")
    index6 = text.find("c700c8008d031ab82")
    index7 = text.find("00000000000000000000000000000100000005")
    index8 = text.find("c800c8008d03")
    index9 = text.find("d000d6009a03")
    index10= text.find("c900c8008d03")
    index11= text.find("d000d7009a03")
    index12= text.find("d100d7009a03")
    index13= text.find("c900c9008d03")
    index14= text.find("d200d7009a03")
    index15= text.find("ca00c9008d03")
    index16= text.find("d300d7009a03")
    index17= text.find("d300d8009a03")
    index18= text.find("cb00c9008d03")
    if index != 2 and index2!=0 and index3!=0 and index4!=0 and index5!=0 and index6!=0 and index7!=0 and index8!=0 and index9!=0 and index10!=0 and index11!=0 and index12!=0 and index13!=0 and index14!=0 and index15!=0 and index16!=0 and index17!=0 and index18!=0:
        result = jk02_32_definition.parse(bytes.fromhex(text))
#        print('uptime:' + str(result['uptime']))
#        print('discard1:' + str(result['discard1']))
#        print('discard3:' + str(result['discard3']))
#        print('discard8:' + str(result['discard8']))
#        print('discard9:' + str(result['discard9']))
#        print('rest:    ' + str(result['rest']))
        print('Record Type:' + str(result['Record_Type']))
        print('Cell Voltage Array:' + str(result['cell_voltage_array']))

#        print(result)

def read_serial_port(serial_port, baud_rate):
    with serial.Serial(serial_port, baud_rate, timeout=0) as ser:
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file = codecs.open(timestr+".log", "w", "utf-8")
        while True:
            # Read all available bytes from the serial port
            data = ser.read_all()

            # If there is data, process and display in hexadecimal format
            if data:
                hex_data = data.hex()
                print(hex_data, end='\n')
                file.write(hex_data)
                file.write('\n')
                sys.stdout.flush()
                process_text(hex_data)

        # If there is no more data, exit the loop
        sys.stdout.flush()


# print(len(response))
cell_details = cs.Struct("no" / cs.Byte, "voltage_mV" / cs.Int16ub)
definition = cs.Struct(
    "stx" / cs.Const(b"NW"),
    "length" / cs.Int16ub,
    "terminal-no" / cs.Bytes(4),
    "command_word" / cs.Byte,
    "frame_source" / cs.Enum(cs.Byte, BMS=0, Bluetooth=1, GPS=2, PC=3),
    "transport_type" / cs.Enum(cs.Byte, Response_Frame=1, BMS_Active_Upload=2),
    "_id" / cs.Const(b"\x79"),
    "data_length" / cs.Byte,
    "cell_count" / cs.Computed(cs.this.data_length // 3),
    "cell_array" / cs.Array(cs.this.cell_count, cell_details),
    "_id" / cs.Const(b"\x80"),
    "power_tube_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x81"),
    "battery_box_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x82"),
    "battery_temperature" / cs.Int16ub,
    "_id" / cs.Const(b"\x83"),
    "battery_voltage_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x84"),
    "battery_current" / cs.BitStruct("direction" / cs.Enum(cs.Bit, discharge=0, charge=1), "current" / cs.BitsInteger(15)),  # possible 10000 - cs.Int16ub (if \xc0 = 00)
    "_id" / cs.Const(b"\x85"),
    "battery_soc" / cs.Byte,
    "_id" / cs.Const(b"\x86"),
    "number_of_temp_sensors" / cs.Byte,
    "_id" / cs.Const(b"\x87"),
    "cycle_count" / cs.Int16ub,
    "_id" / cs.Const(b"\x89"),
    "total_cycle_capacity" / cs.Int32ub,
    "_id" / cs.Const(b"\x8a"),
    "battery_strings" / cs.Int16ub,
    "_id" / cs.Const(b"\x8b"),
    "warning_messages" / cs.Bytes(2),
    "_id" / cs.Const(b"\x8c"),
    "status_info" / cs.BitStruct(cs.Padding(12),
        'Battery is down' / cs.Flag,
        'Equalization Switching State' / cs.Flag,
        'Discharge MOS tube is on' / cs.Flag,
        'Charge MOS tube is on' / cs.Flag,),
    "_id" / cs.Const(b"\x8e"),
    "battery_overvoltage_protection_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x8f"),
    "battery_undervoltage_protection_10mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x90"),
    "cell_overvoltage_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x91"),
    "cell_overvoltage_protection_recovery_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x92"),
    "cell_overvoltage_protection_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x93"),
    "cell_undervoltage_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x94"),
    "cell_undervoltage_protection_recovery_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x95"),
    "cell_undervoltage_protection_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x96"),
    "cell_differential_protection_mV" / cs.Int16ub,
    "_id" / cs.Const(b"\x97"),
    "discharge_protection_current_A" / cs.Int16ub,
    "_id" / cs.Const(b"\x98"),
    "discharge_protection_current_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x99"),
    "charge_protection_current_A" / cs.Int16ub,
    "_id" / cs.Const(b"\x9a"),
    "charge_protection_current_delay_secs" / cs.Int16ub,
    "_id" / cs.Const(b"\x9b"),
    "equalization_starting_voltage_mV" / cs.Int16ub,

    "rest" / cs.Bytes(93),

    "_id" / cs.Const(b"\xb7"),
    "software_id" / cs.Bytes(15),
    "_id" / cs.Const(b"\xb8"),
    "start_calibration" / cs.Byte,
    "_id" / cs.Const(b"\xb9"),
    "battery_capacity_Ah" / cs.Int32ub,
    "_id" / cs.Const(b"\xba"),
    "manufacturer_name" / cs.Bytes(24),
    "_id" / cs.Const(b"\xc0"),
    "agreement_no" / cs.Bytes(1),
    "record_number" / cs.Bytes(4),
    "end_of_identity" / cs.Const(b"h"),
    "checksum" / cs.Bytes(4)
)
jk02_32_definition = cs.Struct(
    "header" / cs.Bytes(4),
    "Record_Type" / cs.Byte,
    "Record_Counter" / cs.Byte,
    "cell_voltage_array" / cs.Array(32, cs.Int16ul),
    "discard1" / cs.Bytes(4),
    "Average_Cell_Voltage" / cs.Int16ul,
    "Delta_Cell_Voltage" / cs.Int16ul,
    "Current_Balancer" / cs.Int16ul,
    "cell_resistance_array" / cs.Array(32, cs.Int16ul),
    "mos_temp" / cs.Int16ul,
    "discard3" / cs.Bytes(4),
    "battery_voltage" / cs.Int32ul,
    # "battery_voltage_c" / cs.Computed(cs.this.bv / 1000),
    #"discard4" / cs.Bytes(2),
    "battery_power" / cs.Int32ul,
    # "battery_power_c" / cs.Computed(cs.this.bp / 1000),
    # "Balance_Current" / cs.Bytes(2),
    #"Balance_Current_part2" / cs.Bytes(1),
    "battery_current" / cs.Int32sl,
    # "battery_current_c" / cs.Computed(cs.this.bc / 1000),
    "T2" / cs.Int16ul,
    "T3" / cs.Int16ul,
    "balance_current" / cs.Int32sl,
    "discard9" /  cs.Bytes(3),
    "Percent_Remain" / cs.Int8ul,
    "Capacity_Remain" / cs.Int32ul,
    "Nominal_Capacity" / cs.Int32ul,
    "Cycle_Count" / cs.Int32ul,
    "Cycle_Capacity" / cs.Int32ul,
    "discard7" / cs.Bytes(4),
    "uptime" / cs.Int24ul,
    "discard8" / cs.Bytes(24),
    # "Current_Charge" / cs.Int16ul,
    # "Current_Discharge" / cs.Int16ul,
 
    "rest" / cs.GreedyBytes
)






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Just an example",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-a", "--archive", action="store_true", help="archive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("-B", "--block-size", help="checksum blocksize")
    parser.add_argument("--ignore-existing", action="store_true", help="skip files that exist")
    parser.add_argument("--exclude", help="files to exclude")
    parser.add_argument("--input-file", help="Source location")
    parser.add_argument("--dest", help="Destination location")
    args = parser.parse_args()
    config = vars(args)
    print(config)
    if (config['input_file']==None):
       # Serial port configuration (adjust the port and baud rate based on your setup)
       serial_port = '/dev/ttyUSB0'  # Change this to the serial port you are using
       baud_rate = 115200  # Change this to the baud rate of your device
       read_serial_port(serial_port, baud_rate)
    else:
       # Using readlines()
       file1 = open(config['input_file'], 'r')
       Lines = file1.readlines()
       count = 0
       # Strips the newline character
       for line in Lines:
           count += 1
           text=line.strip()
           ##print("Line{}: {}".format(count, text))
           process_text(text)
