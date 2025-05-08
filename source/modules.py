from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Padding
from io import BytesIO
import struct
import zlib
import argparse
import hashlib