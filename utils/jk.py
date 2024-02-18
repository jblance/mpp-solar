""" test area for using construct lib to decode a jk serial packet """
try:
    import construct as cs
except ImportError:
    print("You are missing dependencies")
    print("To install use:")
    print("    python -m pip install 'construct'")

response = b'U\xaa\xeb\x90\x02a6\x0c8\x0c)\x0c:\x0c5\x0c:\x0c8\x0c:\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x009\x0c\x1c\x00\x03\x028\x009\x008\x008\x008\x008\x007\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\xc5a\x00\x00\xb2E\x03\x00\x88\xde\xff\xff\xd4\x00\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0E\x04\x00\x0b\x00\x00\x00\xf2\xe00\x00d\x00\x00\x00\xae\x170\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\xfc\x03#\x00*\x00\xca\xfa@@\x00\x00\x00\x00\xc6\t\xa1\x1b\x00\x01\x00\x01\xbb\x05\x00\x00\x8a\xd4O\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc\x0f\x01\x00\x00\x00\x00\x00\x00Q'
response2 = b'U\xaa\xeb\x90\x02\xc1\xac\x0c\xad\x0c\xae\x0c\xb1\x0c\xb1\x0c\xb2\x0c\xae\x0c\xae\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xb0\x0c\x07\x00\x03\x008\x009\x008\x008\x008\x008\x007\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe2\x00\x00\x00\x00\x00\x81e\x00\x00\x8fx\x06\x00\xc0?\x00\x00\xc0\x00\xbe\x00\x00\x00\x00\x00\x00\x00\x00\t\xbfb\x00\x00\xc0E\x04\x00\x0b\x00\x00\x00\x94\r2\x00d\x00\x00\x00\xee\xbc0\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\xfc\x03P\x00\x00\x00\xca\xfa@@\x00\x00\x00\x00&\n\x85\x1b\x00\x01\x00\x01\xbc\x05\x00\x00\x07IV\x00\x00\x00\x00\x00\xe2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc\x0f\x01\x00\x00\x00\x00\x00\x00R'
response3 = bytes.fromhex('55aaeb900200120d120d110d110d110d110d110d110d120d110d110d110d110d110d110d110d0000000000000000000000000000000000000000000000000000000000000000ffff0000110d01000003530050004f004a004d004b004d004d0053004e004d004a004c004d00520051000000000000000000000000000000000000000000000000000000000000000000dd000000000017d100000000000000000000c700cd000000000000000064aa9e040080a3040000000000b30c00006400000056a3290001010000000000000000000000000000ff00010000009a030000000060543f4000000000e8140000000101010006000082775c0000000000dd00c700ce009a03533f09007f0000008051010000000000000000000000000000feff7fdd2f0101b0070000003e001016200001059a')
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

# result = jk02_32_definition.parse(response)
# print(result)
result = jk02_32_definition.parse(response3)
print(result)

# for x in result:
#     match type(result[x]):
#         # case cs.ListContainer:
#         #     print(f"{x}:listcontainer")
#         case cs.Container:
#             print(f"{x}:")
#             for y in result[x]:
#                 if y != "_io":
#                     print(f"\t{y}: {result[x][y]}")    
#         case _:
#             if x != "_io":
#                 print(f"{x}: {result[x]}")