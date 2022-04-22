import msgpack
from io import BytesIO


## stream io
def test1():
    buf = BytesIO()
    for i in range(100):
        buf.write(msgpack.packb(i, use_bin_type=True))
    buf.seek(0)

    unpacker = msgpack.Unpacker(buf, raw=False)
    for unpacked in unpacker:
        print(unpacked)


### custom datatype
import datetime
import msgpack

useful_dict = {
        "id": 1,
        "created": datetime.datetime.now(),
    }

def decode_datetime(obj):
    if '__datetime__' in obj:
        obj = datetime.datetime.strptime(obj["as_str"], "%Y%m%dT%H:%M:%S.%f")
    return obj

def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    return obj

packed_dict = msgpack.packb(useful_dict, default=encode_datetime, use_bin_type=True)
this_dict_again = msgpack.unpackb(packed_dict, object_hook=decode_datetime, raw=False)

print(this_dict_again)


