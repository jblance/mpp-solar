""" test area for using construct lib to decode a jk serial packet """
try:
    import construct as cs
except ImportError:
    print("You are missing dependencies")
    print("To install use:")
    print("    python -m pip install 'construct'")

response1 = b'U\xaa\xeb\x90\x02a6\x0c8\x0c)\x0c:\x0c5\x0c:\x0c8\x0c:\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x009\x0c\x1c\x00\x03\x028\x009\x008\x008\x008\x008\x007\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\xc5a\x00\x00\xb2E\x03\x00\x88\xde\xff\xff\xd4\x00\xca\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0E\x04\x00\x0b\x00\x00\x00\xf2\xe00\x00d\x00\x00\x00\xae\x170\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\xfc\x03#\x00*\x00\xca\xfa@@\x00\x00\x00\x00\xc6\t\xa1\x1b\x00\x01\x00\x01\xbb\x05\x00\x00\x8a\xd4O\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc\x0f\x01\x00\x00\x00\x00\x00\x00Q'
response2 = b'U\xaa\xeb\x90\x02\xc1\xac\x0c\xad\x0c\xae\x0c\xb1\x0c\xb1\x0c\xb2\x0c\xae\x0c\xae\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xb0\x0c\x07\x00\x03\x008\x009\x008\x008\x008\x008\x007\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe2\x00\x00\x00\x00\x00\x81e\x00\x00\x8fx\x06\x00\xc0?\x00\x00\xc0\x00\xbe\x00\x00\x00\x00\x00\x00\x00\x00\t\xbfb\x00\x00\xc0E\x04\x00\x0b\x00\x00\x00\x94\r2\x00d\x00\x00\x00\xee\xbc0\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\xfc\x03P\x00\x00\x00\xca\xfa@@\x00\x00\x00\x00&\n\x85\x1b\x00\x01\x00\x01\xbc\x05\x00\x00\x07IV\x00\x00\x00\x00\x00\xe2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc\x0f\x01\x00\x00\x00\x00\x00\x00R'
response3 = bytes.fromhex('55aaeb900200120d120d110d110d110d110d110d110d120d110d110d110d110d110d110d110d0000000000000000000000000000000000000000000000000000000000000000ffff0000110d01000003530050004f004a004d004b004d004d0053004e004d004a004c004d00520051000000000000000000000000000000000000000000000000000000000000000000dd000000000017d100000000000000000000c700cd000000000000000064aa9e040080a3040000000000b30c00006400000056a3290001010000000000000000000000000000ff00010000009a030000000060543f4000000000e8140000000101010006000082775c0000000000dd00c700ce009a03533f09007f0000008051010000000000000000000000000000feff7fdd2f0101b0070000003e001016200001059a')
response4 = b'U\xaa\xeb\x90\x02&\xf5\x0c\xfa\x0c\xf9\x0c\x01\r\xf9\x0c\xff\x0c\xf9\x0c\xf9\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xfa\x0c\x0b\x00\x03\x008\x009\x008\x008\x008\x008\x007\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe5\x00\x00\x00\x00\x00\xd3g\x00\x00K7\x10\x00\xfc\x9c\x00\x00\xbd\x00\xb7\x00\x00\x00\x00\x00m\xf8\x02\rX\x89\x00\x00\xc0E\x04\x00\x0e\x00\x00\x00\x8e\xce?\x00d\x00\x00\x00\xc1\x016\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x01\x00\x00\x00\xfc\x03\xc5\x00\x00\x00\xca\xfa@@\xd3\x00\x00\x00a\n\x94\x1b\x00\x01\x00\x01\xbd\x05\x00\x00F\xf9\x8a\x00\x00\x00\x00\x00\xe5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xfe\xff\x7f\xdc\x0f\x01\x00\x00\x00\x00\x00\x00\x9a'
response5 = bytes.fromhex('55aaeb900200130d120d120d120d120d120d120d110d110d120d110d110d110d120d120d110d0000000000000000000000000000000000000000000000000000000000000000ffff0000120d02000008530050004f004a004d004b004d004d0053004e004d004a004c004d00520051000000000000000000000000000000000000000000000000000000000000000000ea00000000001dd100000000000000000000d100d80000000000000000632d92040080a30400000000003019000064000000a022410001010000000000000000000000000000ff00010000009a030000000060543f4000000000e914000000010101000600006570470100000000ea00d200d7009a030fbf20007f0000008051010000000000000000000000000000feff7fdd2f0101b00700000093001016200001059a')
response6 = bytes.fromhex('55aaeb900200130d120d120d120d120d120d120d120d110d110d110d120d120d110d110d110d0000000000000000000000000000000000000000000000000000000000000000ffff0000120d02000007530050004f004a004d004b004d004d0053004e004d004a004c004d00520051000000000000000000000000000000000000000000000000000000000000000000ea00000000001fd100000000000000000000d000d80000000000000000632d92040080a30400000000003019000064000000a722410001010000000000000000000000000000ff00010000009a030000000060543f4000000000e91400000001010100060000ad70470100000000ea00d200d7009a0316bf20007f0000008051010000000000000000000000000000feff7fdd2f0101b007000000e9001016200001059a')
response_type01 = bytes.fromhex('55aaeb900100ac0d0000280a00005a0a0000240e0000780d000005000000790d0000500a00007a0d0000160d0000c409000050c30000030000003c000000102700002c0100003c00000005000000d0070000bc02000058020000bc0200005802000038ffffff9cffffffe8030000200300001000000001000000010000000100000080a30400dc0500007a0d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000500000060e3160010023c3218feffffffbfe9010200000000f50010161e00016456')
response = response1
print(len(response))

record_01 = cs.Struct(
    "Record_Counter" / cs.Byte,
    "voltage_smart_sleep" / cs.Int32ul,
    "cell_under_voltage_protection" / cs.Int32ul,
    "cell_under_voltage_protection_recovery" / cs.Int32ul,
    "cell_over_voltage_protection" / cs.Int32ul,
    "cell_over_voltage_protection_recovery" / cs.Int32ul,
    "balance_trigger_voltage" / cs.Int32ul,
    "soc_100%_voltage" / cs.Int32ul,
    "soc_0%_voltage" / cs.Int32ul,
    "cell_request_charge_voltage" / cs.Int32ul,
    "cell_request_float_voltage" / cs.Int32ul,
    "power_off_cell_voltage" / cs.Int32ul,
    "continued_charge_current" / cs.Int32ul,
    "charge_ocp_delay_sec" / cs.Int32ul,
    "charge_ocpr_time_sec" / cs.Int32ul,
    "unknown2" / cs.Int32ul,
    "discharge_ocp_delay_sec" / cs.Int32ul,
    "discharge_ocpr_time_sec" / cs.Int32ul,
    "scpr_time_sec" / cs.Int32ul,
    "max_balance_current" / cs.Int32ul,
    "charge_otp_c" / cs.Int32ul,
    "charge_otpr_c" / cs.Int32ul,
    "discharge_otp_c" / cs.Int32ul,
    "discharge_otpr_c" / cs.Int32ul,
    "charge_utp_c" / cs.Int32sl,
    "charge_utpr_c" / cs.Int32sl,
    "mos_otp_c" / cs.Int32ul,
    "mos_otpr_c" / cs.Int32ul,
    "cell_count" / cs.Int32ul,
    "unknown7" / cs.Bytes(4),
    "unknown8" / cs.Bytes(4),
    "unknown9" / cs.Bytes(4),
    "nominal_battery_capacity" / cs.Int32ul,
    "scp_delay_us" / cs.Int32ul,
    "start_balance_voltage" / cs.Int32ul,
    "unknown11" / cs.Bytes(8),
    "unknown12" / cs.Bytes(8),
    "unknown13" / cs.Bytes(8),
    "unknown14" / cs.Bytes(8),
    "unknown15" / cs.Bytes(8),

    "rest" / cs.GreedyBytes,
)

record_02 = cs.Struct(
    "Record_Counter" / cs.Byte,
    "cell_voltage_array" / cs.Array(32, cs.Int16ul),
    "cell_presence" / cs.BitStruct("cells" / cs.Array(32, cs.Enum(cs.Bit, not_present=0, present=1))),
    "Average_Cell_Voltage" / cs.Int16ul,
    "Delta_Cell_Voltage" / cs.Int16ul,
    "cell_highest_voltage" / cs.Byte,
    "cell_lowest_voltage" / cs.Byte,
    "cell_resistance_array" / cs.Array(32, cs.Int16ul),
    "mos_temp" / cs.Int16ul,
    "discard3" / cs.Bytes(4),
    "battery_voltage" / cs.Int32ul,
    "battery_power" / cs.Int32ul,
    "battery_current" / cs.Int32sl,
    "T1" / cs.Int16ul,
    "T2" / cs.Int16ul,
    "discard4" / cs.Bytes(4),
    "balance_current" / cs.Int16sl,
    "discard5" /  cs.Bytes(1),
    "Percent_Remain" / cs.Int8ul,
    "Capacity_Remain" / cs.Int32ul,
    "Nominal_Capacity" / cs.Int32ul,
    "Cycle_Count" / cs.Int32ul,
    "Cycle_Capacity" / cs.Int32ul,
    "discard6" / cs.Bytes(4),
    "uptime" / cs.Int24ul,
    "discard8" / cs.Bytes(8),
    "discard9" / cs.Bytes(8),
    "discard10" / cs.Bytes(8),
    "discard11" / cs.Bytes(8),
    "discard12" / cs.Bytes(8),
    "discard13" / cs.Bytes(8),
    "discard14" / cs.Bytes(8),
    "discard15" / cs.Bytes(8),
    "discard16" / cs.Bytes(8),
    "discard17" / cs.Bytes(8),
    "discard18" / cs.Bytes(8),
    "discard19" / cs.Bytes(8),
    "discard20" / cs.Optional(cs.Bytes(8)),
    "discard21" / cs.Optional(cs.GreedyBytes)
)
jk02_32_definition = cs.Struct(
    "header" / cs.Bytes(4),
    "record_type" / cs.Byte,
    "record_decode" / cs.Switch(cs.this.record_type, {1: record_01, 2: record_02, 3: cs.GreedyBytes}),
)

# result = jk02_32_definition.parse(response)
# print(result)
result = jk02_32_definition.parse(response)
print(result)
#print(bin(result[0].discard1))
# result = jk02_32_definition.parse(response5)
# result2 = jk02_32_definition.parse(response6)
exit()
for x in result:
    match type(result[x]):
        # case cs.ListContainer:
        #     print(f"{x}:listcontainer")
        case cs.Container:
            pass
            print(f"{x}:")
            for y in result[x]:
                if y.startswith("discard1"):
                    print(f"\t{y}: {bin(result[x][y])}")    
        case _:
            if x == "discard1":
                #if result[x] == result2[x]:
                #    print(f"{x}: {result[x]} matches")
                print(f"{x}bin: {bin(result[x])}")
            else:
                print(f"{x}: {result[x]}")
