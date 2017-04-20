import hid
import datetime
from app.mod_rfid.models import Student, Reads
from peewee import DoesNotExist

device_product_name = 'SYC ID&IC USB Reader'
device = None

def find_device():
    for d in hid.enumerate():
        keys = list(d.keys())
        keys.sort()
        for key in keys:
            #print("%s : %s" % (key, d[key]))
            if key == 'product_string' and d[key] == device_product_name:
                print('Opening ' + device_product_name + '...')

                _device = hid.device()
                _device.open(d['vendor_id'], d['product_id'], d['serial_number'])
                return _device
    if device is not None:
        return None

def read_device_data(device):
    # enable non-blocking mode
    device.set_nonblocking(1)

    print("Reading the data...")
    card = []
    while True:
        try:
            d = device.read(4)
            if d:
                if type(d) is list:
                    char = d[2]
                    if char > 0:
                        if char < 39:
                            card.append(str(char - 29))
                        elif char == 39:
                            card.append(str(0))
            if len(card) == 10:
                card_id = "".join(card)

                student_name = input("Enter name: ")
                record_card_student(card_id, student_name)

                exit()
        except KeyboardInterrupt as e:
            print("\n\nSo long and thanks for all the cards!")
            exit()


def record_card_student(card_id, student_name):
    #student = None
    student = Student.create(rfid_id=card_id, name=student_name, last_seen = datetime.datetime.now())

    print("Student recorded: " + student.name)


reader_device = find_device()

if reader_device is None:
    raise Exception('Could not find any mathing device for the following name: ' + device_product_name)
else:
    print("Connected to device!")
    print("    Manufacturer: %s" % reader_device.get_manufacturer_string())
    print("    Product: %s" % reader_device.get_product_string())
    print("    Serial No: %s" % reader_device.get_serial_number_string())

    read_device_data(reader_device)
