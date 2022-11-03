# Import snap7 Or Install If Not Exist
try:
    import snap7
except Exception as e:
    # Install The Package python-snap7
    import pip
    pip.main(['install', 'python-snap7'])
    import snap7

finally:
    print('python-snap7 Successful Installed')

# Create Instance plc
plc = snap7.client.Client()

# Connect To PLC
plc.connect('192.168.0.1', 0, 1)  # IP Address, Rack, Slot


def read_data(db_number: int, start_offset: int, data_size: int):
    """ 
    Function To Read Data From Data Block
    Args :
        db_number    : Data block Number To Read
        start_offset : Start Offset To Read from DB
        data_size    : Lenght Of Data To Read
    """
    receive_data = []
    reading_data = plc.db_read(db_number, start_offset, data_size)
    for mot in range(0, data_size, 2):
        value_int = snap7.util.get_int(reading_data, mot)
        receive_data.append(value_int)

    return receive_data


def write_data(db_number: int, start_offset: int, data_size: int):
    """ 
    Function To Write Data In To Data Block
    Args :
        db_number    : Data block Number To Write
        start_offset : Start Offset To Write
        data_size    : Lenght Of Data To Read
        value        : Value To Write
    """
    my_list = [1090, 0, 91, 568, 65, 0, 935, 751, 982, 5]
    reading_data = plc.db_read(db_number, start_offset, data_size)
    for mot in range(0, data_size, 2):
        snap7.util.set_int(reading_data, mot, my_list[int(mot/2)])
        plc.db_write(db_number, start_offset, reading_data)


result = read_data(10, 0, 20)
print(f"Resuslt avant: {result}")
write_data(10, 0, 20)
result = read_data(10, 0, 20)
print(f"Resuslt apres: {result}")
