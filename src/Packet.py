import struct
import time
import unittest

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



class TestPacket(unittest.TestCase):

    def test_packet_creation(self):
        # Test packet creation with minimum payload size
        packet = Packet(SN=1, message=b'', mac=b'')
        self.assertEqual(packet.SN, 1)
        self.assertEqual(packet.payload_size, 0)
        self.assertEqual(packet.message, b'')
        self.assertEqual(packet.mac, b'')

    def test_packet_to_bytes(self):
        # Test conversion to bytes
        packet = Packet(SN=1, message=b'Hello, World!', mac=b'0123456789ABCDEF')
        packet_bytes = packet.to_bytes()
        
        # Check the length of the resulting bytes
        expected_length = 8 + 8 + packet.payload_size + len(packet.mac)  # 8 bytes SN+size, 8 bytes timestamp
        self.assertEqual(len(packet_bytes), expected_length)

        # Check if the SN and payload size are correctly packed
        SN_and_size, timestamp = struct.unpack('!Qd', packet_bytes[:16])
        self.assertEqual(SN_and_size >> 32, packet.SN)
        self.assertEqual(SN_and_size & 0xFFFFFFFF, packet.payload_size)

    def test_packet_from_bytes(self):
        # Create a packet and convert it to bytes
        packet = Packet(SN=1, message=b'Hello, World!', mac=b'0123456789ABCDEF')
        packet_bytes = packet.to_bytes()

        # Reconstruct the packet from bytes
        reconstructed_packet = Packet.from_bytes(packet_bytes)

        # Validate that the original and reconstructed packets are the same
        self.assertEqual(packet.SN, reconstructed_packet.SN)
        self.assertEqual(packet.payload_size, reconstructed_packet.payload_size)
        self.assertEqual(packet.message, reconstructed_packet.message)
        self.assertEqual(packet.mac, reconstructed_packet.mac)
        self.assertAlmostEqual(packet.timestamp, reconstructed_packet.timestamp, places=6)

    def test_packet_with_max_payload_size(self):
        # Test packet creation with maximum payload size
        message = b'a' * 1024  # 1024 bytes message
        packet = Packet(SN=1, message=message, mac=b'0123456789ABCDEF')
        packet_bytes = packet.to_bytes()

        # Reconstruct the packet from bytes
        reconstructed_packet = Packet.from_bytes(packet_bytes)

        # Validate that the original and reconstructed packets are the same
        self.assertEqual(packet.SN, reconstructed_packet.SN)
        self.assertEqual(packet.payload_size, reconstructed_packet.payload_size)
        self.assertEqual(packet.message, reconstructed_packet.message)
        self.assertEqual(packet.mac, reconstructed_packet.mac)
        self.assertAlmostEqual(packet.timestamp, reconstructed_packet.timestamp, places=6)

    def test_invalid_payload_size(self):
        # Test packet creation with an invalid payload size
        with self.assertRaises(ValueError):
            Packet(SN=1, message=b'a' * 1025)  # Message exceeding the maximum allowed size

    def test_packet_without_mac(self):
        # Test packet creation without a MAC
        packet = Packet(SN=2, message=b'Just a message')
        packet_bytes = packet.to_bytes()

        # Reconstruct the packet from bytes
        reconstructed_packet = Packet.from_bytes(packet_bytes)

        # Validate that the original and reconstructed packets are the same
        self.assertEqual(packet.SN, reconstructed_packet.SN)
        self.assertEqual(packet.payload_size, reconstructed_packet.payload_size)
        self.assertEqual(packet.message, reconstructed_packet.message)
        self.assertEqual(packet.mac, reconstructed_packet.mac)
        self.assertAlmostEqual(packet.timestamp, reconstructed_packet.timestamp, places=6)

if __name__ == '__main__':
    unittest.main()

