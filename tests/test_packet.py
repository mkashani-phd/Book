import unittest
import struct
from src import Packet 

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
