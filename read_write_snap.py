"""
Script To Send & Receive Data From PLC SIEMENS
PUT / GET Communication
"""
# Import Modules
import os
import random

# Import snap7 Or Install If Not Exists
try:
    import snap7
except Exception as e:
    # Install The Package python-snap7
    import pip
    pip.main(['install', 'python-snap7'])
    import snap7

finally:
    print('python-snap7 Successful Installed')

# Change Current Directory Working
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create Instance plc
plc = snap7.client.Client()

# Connect To PLC
plc.connect('192.168.0.1', 0, 1)  # IP Address, Rack, Slot


def read_data_from_PLC(db_number: int, start_offset: int, data_size: int):
    """ 
    - Function To Read Data From Data Block
    - Stock Data In List
    Args :
        db_number    : Data block Number To Read
        start_offset : Start Offset To Read from DB
        data_size    : Length Of Data To Read

    Return :
        List 
    """

    receive_data = []
    reading_data = plc.db_read(db_number, start_offset, data_size)
    for mot in range(0, data_size, 2):
        value_int = snap7.util.get_int(reading_data, mot)
        receive_data.append(value_int)

    return receive_data


def write_data_in_PLC(db_number: int, start_offset: int, data_size: int, data_to_write: list):
    """ 
    Function To Write Data In To Data Block
    Args :
        db_number    : Data block Number To Write
        start_offset : Start Offset To Write
        data_size    : Lenght Of Data To Write
        data_to_write: Data To Write In Data Bolck
    """
    reading_data = plc.db_read(db_number, start_offset, data_size)
    for mot in range(0, data_size, 2):
        snap7.util.set_int(reading_data, mot, data_to_write[int(mot/2)])
        plc.db_write(db_number, start_offset, reading_data)


if __name__ == "__main__":
    """
    This Will No Be Running In Case Of Import Module
    """
    db_number = 10
    start_offset = 0
    data_size = 20
    data_to_write = [random.randrange(1, 1000) for i in range(10)]

    # Call read_data_from_PLC Fuction
    data_receive = read_data_from_PLC(db_number, start_offset, data_size)

    # Make Txt File Before Changing Values
    with open("plc_data.txt", 'w') as data_file:
        data_file.write("------Data Before Changing------\n")
        for mot in data_receive:
            data_file.write("--- " + str(mot)+" ---\n")

    print(f"Result Before: {data_receive}")

    # Call write_data_in_PLC Fuction
    write_data_in_PLC(db_number, start_offset, data_size, data_to_write)
    data_receive = read_data_from_PLC(db_number, start_offset, data_size)

    # Get Values After Changing Values
    with open("plc_data.txt", 'a') as data_file:
        data_file.write("------ Data After Changing ------\n")
        for mot in data_receive:
            data_file.write("--- " + str(mot)+" ---\n")

    print(f"Result After: {data_receive}")
