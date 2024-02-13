""" test area for using construct lib to decode a jk serial packet """
try:
    import construct as cs
except ImportError:
    print("You are missing dependencies")
    print("To install use:")
    print("    python -m pip install 'construct'")

response14 = b'NW\x01\x1b\x00\x00\x00\x00\x03\x00\x01y*\x01\x0f\x90\x02\x0f\x91\x03\x0f\x94\x04\x0f\x8e\x05\x0f\x92\x06\x0f\x91\x07\x0f\x91\x08\x0f\x91\t\x0f\x93\n\x0f\x8e\x0b\x0f\x91\x0c\x0f\x90\r\x0f\x90\x0e\x0f\x8d\x80\x00!\x81\x00\x1c\x82\x00\x1e\x83\x15\xca\x84\x81\xc5\x85d\x86\x02\x87\x00\x19\x89\x00\x00\x16\xda\x8a\x00\x0e\x8b\x00\x00\x8c\x00\x03\x8e\x16\xb2\x8f\x10\xf4\x90\x106\x91\x10\x04\x92\x00\x05\x93\x0c\x1c\x94\x0c\x80\x95\x00\x05\x96\x01,\x97\x00n\x98\x01,\x99\x00U\x9a\x00\x1e\x9b\x0b\xb8\x9c\x002\x9d\x01\x9e\x00Z\x9f\x00F\xa0\x00d\xa1\x00d\xa2\x00\x14\xa3\x00<\xa4\x00<\xa5\x00\x01\xa6\x00\x03\xa7\xff\xec\xa8\xff\xf6\xa9\x0e\xaa\x00\x00\x00\xea\xab\x01\xac\x01\xad\x047\xae\x01\xaf\x01\xb0\x00\n\xb1\x14\xb2123456\x00\x00\x00\x00\xb3\x00\xb4Input Us\xb52306\xb6\x00\x01\x82\xe3\xb711.XW_S11.261__\xb8\x00\xb9\x00\x00\x00\xea\xbaInput UserdaJK_B1A20S15P\xc0\x01\x00\x00\x00\x00h\x00\x00Q\xd6'
response4 = bytes.fromhex("4e 57 00 fd 00 00 00 00 06 00 01 79 0c 01 0d 06 02 0d 06 03 0d 07 04 0d 07 80 00 10 81 00 0e 82 00 0d 83 05 35 84 00 00 85 62 86 02 87 00 00 89 00 00 00 05 8a 00 04 8b 00 00 8c 00 03 8e 05 a0 8f 04 10 90 0e 10 91 0d de 92 00 05 93 0a 28 94 0a 5a 95 00 05 96 01 2c 97 00 78 98 00 1e 99 00 3c 9a 00 1e 9b 0d 48 9c 00 05 9d 01 9e 00 50 9f 00 41 a0 00 64 a1 00 64 a2 00 14 a3 00 32 a4 00 37 a5 00 03 a6 00 08 a7 ff ec a8 ff f6 a9 04 aa 00 00 01 31 ab 01 ac 01 ad 03 7e ae 01 af 00 b0 00 0a b1 14 b2 35 33 31 34 00 00 00 00 00 00 b3 00 b4 49 6e 70 75 74 20 55 73 b5 32 33 31 32 b6 00 00 36 a6 b7 31 31 2e 58 57 5f 53 31 31 2e 32 31 48 5f 5f b8 00 b9 00 00 01 31 ba 49 6e 70 75 74 20 55 73 65 72 64 61 45 64 64 69 65 42 6c 75 65 42 4d 53 c0 01 00 00 00 00 68 00 00 44 6f")

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

result = definition.parse(response4)
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
