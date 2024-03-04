import pymodbus
from pymodbus.client.sync import ModbusSerialClient

# **Important:** Replace these placeholders with your specific values
# - Replace 'your_device_id' with the actual ID of your Modbus device
# - Replace '/dev/ttyUSB*' with the correct serial port for your USB-RS485 adapter
# - Adjust 'baudrate', 'parity', 'stopbits', and 'timeout' as needed based on your device's settings
device_id = 0x2
port = '/dev/ttyUSB0'  # Check with `ls /dev/ttyUSB*` to identify the correct port
baudrate = 9600
parity = 'O'
stopbits = 1
timeout = 1  # Adjust as needed

# Create a Modbus serial client, handling potential errors gracefully
try:
    client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, timeout=timeout)
    client.connect()
except Exception as e:
    print(f"Error connecting to Modbus device: {e}")
    exit()

# Read specific Modbus register(s)
try:
    # Replace these placeholders with the function code and register addresses you need to read
    function_code = pymodbus.constants.READ_HOLDING_REGISTERS
    register_address = 0x1F4  # Replace with the starting register address
    register_count = 1  # Replace with the number of registers to read

    # Execute the Modbus read request
    read_result = client.read_holding_registers(register_address, register_count)

    # Check for successful read operation
    if read_result.is_exception():
        print(f"Error reading Modbus registers: {read_result}")
    else:
        # Process the read register values (e.g., print, store in variables)
        print(f"Read values: {read_result.registers}")

except Exception as e:
    print(f"Error during Modbus read operation: {e}")

finally:
    # Always close the Modbus connection
    client.close()
    print("Modbus connection closed.")

