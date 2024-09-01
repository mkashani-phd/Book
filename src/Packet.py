import struct
import time

class Packet:
    ALLOWED_PAYLOAD_SIZES = [0, 128, 256, 512, 1024]

    def __init__(self, SN: int, message: bytes, mac: bytes = b'', timestamp: float = None):
        self.SN = SN
        self.timestamp = timestamp if timestamp is not None else time.time()
        self.message = message
        self.mac = mac
        self.payload_size = self._determine_payload_size(len(message))  # Determine the payload size based on the message length

    def _determine_payload_size(self, message_length: int) -> int:
        """Determine the payload size based on the message length."""
        for size in self.ALLOWED_PAYLOAD_SIZES:
            if message_length <= size:
                return size
        raise ValueError(f"Message length {message_length} exceeds the maximum allowed size of 1024 bytes.")

    def to_bytes(self) -> bytes:
        """Convert the packet to bytes for transmission."""
        # Combine SN and payload size into a single 8-byte value
        SN_and_size = (self.SN << 32) | self.payload_size
        # Using struct.pack to efficiently serialize the packet
        return struct.pack(f'!Qd{self.payload_size}s{len(self.mac)}s', 
                           SN_and_size, self.timestamp, self.message.ljust(self.payload_size, b'\0'), self.mac)

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create a Packet instance from a bytes object."""
        # Unpack the combined SN and payload size (first 8 bytes)
        SN_and_size = struct.unpack('!Q', data[:8])[0]
        SN = SN_and_size >> 32  # Extract SN (upper 4 bytes)
        payload_size = SN_and_size & 0xFFFFFFFF  # Extract payload size (lower 4 bytes)
        
        # Validate payload size
        if payload_size not in cls.ALLOWED_PAYLOAD_SIZES:
            raise ValueError(f"Invalid payload size {payload_size}.")

        # Extract the timestamp (next 8 bytes)
        timestamp = struct.unpack('!d', data[8:16])[0]
        
        # Extract message and MAC
        message = data[16:16 + payload_size].rstrip(b'\0')  # Extract message and strip padding
        mac_start = 16 + payload_size
        mac = data[mac_start:] if mac_start < len(data) else b''

        return cls(SN=SN, message=message, mac=mac, timestamp=timestamp)

    def __repr__(self):
        return f"Packet(SN={self.SN}, message={self.message}, mac={self.mac}, timestamp={self.timestamp}, payload_size={self.payload_size})"


