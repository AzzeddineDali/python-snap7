# Import snap7 Or Install If Not Exist
try:
    import snap7

except Exception as e:

    # Install The Package python-snap7
    import pip
    pip.main(['install', 'python-snap7'])

    import snap7

finally:
    print('python-snap7 has installed')


plc = snap7.client.Client()
plc.connect('192.168.0.1', 0, 1)  # IP Address, Rack, Slot


def read_data(db_number, start_offset, data_size):

    # Function To Read Data From Data Block
    reading_data = plc.db_read(db_number, start_offset, data_size)
