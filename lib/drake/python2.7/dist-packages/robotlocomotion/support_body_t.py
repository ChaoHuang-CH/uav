"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class support_body_t(object):
    __slots__ = ["utime", "body_id", "use_support_surface", "override_contact_pts", "num_contact_pts", "contact_pts", "support_surface"]

    def __init__(self):
        self.utime = 0
        self.body_id = 0
        self.use_support_surface = False
        self.override_contact_pts = False
        self.num_contact_pts = 0
        self.contact_pts = [ [] for dim0 in range(3) ]
        self.support_surface = [ 0.0 for dim0 in range(4) ]

    def encode(self):
        buf = BytesIO()
        buf.write(support_body_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        buf.write(struct.pack(">qibbi", self.utime, self.body_id, self.use_support_surface, self.override_contact_pts, self.num_contact_pts))
        for i0 in range(3):
            buf.write(struct.pack('>%dd' % self.num_contact_pts, *self.contact_pts[i0][:self.num_contact_pts]))
        buf.write(struct.pack('>4d', *self.support_surface[:4]))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != support_body_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return support_body_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = support_body_t()
        self.utime, self.body_id = struct.unpack(">qi", buf.read(12))
        self.use_support_surface = bool(struct.unpack('b', buf.read(1))[0])
        self.override_contact_pts = bool(struct.unpack('b', buf.read(1))[0])
        self.num_contact_pts = struct.unpack(">i", buf.read(4))[0]
        self.contact_pts = []
        for i0 in range(3):
            self.contact_pts.append(struct.unpack('>%dd' % self.num_contact_pts, buf.read(self.num_contact_pts * 8)))
        self.support_surface = struct.unpack('>4d', buf.read(32))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if support_body_t in parents: return 0
        tmphash = (0x728fbe08984041a7) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if support_body_t._packed_fingerprint is None:
            support_body_t._packed_fingerprint = struct.pack(">Q", support_body_t._get_hash_recursive([]))
        return support_body_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)
