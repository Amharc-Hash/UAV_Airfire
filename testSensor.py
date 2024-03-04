import serial
from pymodbus.client.sync import ModbusSerialClient

# RS485 USB Configuration
port = '/dev/ttyUSB0'  # Replace if your USB adapter uses a different port
baudrate = 9600        # Adjust if your device uses a different baud rate
parity = 'N'
stopbits = 1
bytesize = 8

# Modbus Slave Configuration
client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate,
                            parity=parity, stopbits=stopbits, bytesize=bytesize,
                            timeout=2000)   # Adjust timeout if needed

slave_id = 0x02           # ID of your Modbus slave device
register_address_list = [0x1F4, 0x1F6, 0x1F8, 0x1F9]    # [WindSpeed, WindDir, Hum, Temp]
count = 1               # Number of registers to read

data_list = []

# Connect to the device
client.connect()

# Read data
for register_address in register_address_list:
	result = client.read_holding_registers(register_address, count, unit=slave_id)
	if not result.isError():
		data_list.append(result.registers[0])
		#print(len(result.registers))
	else:
		data_list.append('error')
		print(f'Error reading registers : {register_address}: {result}')

# Process the result
print('Data:', data_list)

# Close the connection
client.close()

