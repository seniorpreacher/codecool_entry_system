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
                try:
                    _device.open(d['vendor_id'], d['product_id'], d['serial_number'])

                    if _device is not None:
                        print("Connected to device!")
                        print("    Manufacturer: %s" % _device.get_manufacturer_string())
                        print("    Product: %s" % _device.get_product_string())
                        print("    Serial No: %s" % _device.get_serial_number_string())

                        return _device
                    else:
                        print("-- Unable to open device")

                except OSError as e:
                    print("-- Failed to open device")

    if device is not None:
        raise Exception('Could not find any mathing device for the following name: ' + device_product_name)

def read_device_data(device, callback=None):
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
            if len(card) >= 10:
                card_id = "".join(card)

                record_card_touch(card_id)

                if callback is not None:
                    print("-- Calling callback function")
                    callback(card_id)

                del card[:]
        except KeyboardInterrupt as e:
            print("\n\nSo long and thanks for all the cards!")
            exit()
    print("-- VÉGE")


def record_card_touch(card_id):
    try:
        print("Finding owner of this Card (" + card_id + ")")
        student = Student.get(Student.rfid_id == card_id)
        student.last_seen = datetime.datetime.now()
        student.save()

    except DoesNotExist:
        student = Student.get(Student.name == "Unknown RFID ID")

    finally:
        read = Reads.create(time=datetime.datetime.now(), student=student)
        print("Card of " + student.name + " read at " + read.time.strftime("%Y-%m-%d %H:%M:%S"))

def read_data_of_available_device(callback=None):
    device = find_device()
    if device is not None:
        read_device_data(device, callback)
    else:
        print("-- Could not connect to device")
