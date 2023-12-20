import base64
import struct

import libscrc


def raw_to_userfriendly(address: str, is_bounceable: bool = False) -> str:
    """
    Converts a raw address string to a user-friendly format.

    :param address: The raw address string in the format "workchain_id:key".
    :param is_bounceable: The flag indicating if the address is bounceable. Defaults to False.
    :return: The user-friendly address string, encoded in base64 and URL-safe.
    """
    tag = 0x11 if is_bounceable else 0x51
    workchain_id, key = address.split(':')
    workchain_id = int(workchain_id)
    key = bytearray.fromhex(key)

    short_ints = [j * 256 + i for i, j in zip(*[iter(key)] * 2)]
    payload = struct.pack(f'Bb{"H" * 16}', tag, workchain_id, *short_ints)
    crc = libscrc.xmodem(payload)
    encoded_key = payload + struct.pack('>H', crc)
    return base64.urlsafe_b64encode(encoded_key).decode("utf-8")
