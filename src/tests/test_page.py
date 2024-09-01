import unittest
import time
from src import Page, Packet

class TestPage(unittest.TestCase):

    def test_page_initialization(self):
        # Test that a page initializes correctly
        page = Page(page_size=5)
        self.assertEqual(page.page_size, 5)
        self.assertEqual(len(page.packets), 5)
        self.assertTrue(all(p is None for p in page.packets))
        self.assertIsNone(page.min_SN)
        self.assertIsNone(page.max_SN)
        self.assertEqual(page.occupancy, 0)

    def test_add_packet(self):
        # Test adding a packet to the page
        page = Page(page_size=5)
        packet1 = Packet(SN=1, message=b'message1', mac=b'mac1')
        result = page.add_packet(packet1)

        self.assertTrue(result)
        self.assertEqual(page.packets[1 % 5], packet1)
        self.assertEqual(page.occupancy, 1)
        self.assertEqual(page.min_SN, 0)
        self.assertEqual(page.max_SN, 5)

    def test_add_packet_out_of_range(self):
        # Test adding a packet with SN out of range
        page = Page(page_size=5)
        packet1 = Packet(SN=1, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=6, message=b'message2', mac=b'mac2')

        result = page.add_packet(packet1)
        self.assertTrue(result)

        result = page.add_packet(packet2)
        self.assertFalse(result)
        self.assertEqual(page.occupancy, 1)
        self.assertEqual(page.packets[1 % 5], packet1)


    def test_is_full(self):
        # Test checking if the page is full
        page = Page(page_size=2)
        packet1 = Packet(SN=0, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=1, message=b'message2', mac=b'mac2')

        page.add_packet(packet1)
        page.add_packet(packet2)

        self.assertTrue(page.is_full())
        
    def test_aviod_repetetive_SN(self):
        # Test checking if the page is full
        page = Page(page_size=2)
        packet1 = Packet(SN=0, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=1, message=b'message2', mac=b'mac2')

        page.add_packet(packet1)
        page.add_packet(packet2)

        self.assertTrue(page.is_full())

        packet3 = Packet(SN=0, message=b'message3', mac=b'mac3')
        result  = page.add_packet(packet3)
        self.assertFalse(result)

    def test_clear_page(self):
        # Test clearing the page
        page = Page(page_size=5)
        packet1 = Packet(SN=0, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=1, message=b'message2', mac=b'mac2')

        page.add_packet(packet1)
        page.add_packet(packet2)
        page.clear()

        self.assertTrue(all(p is None for p in page.packets))
        self.assertEqual(page.occupancy, 0)
        self.assertIsNone(page.min_SN)
        self.assertIsNone(page.max_SN)

    def test_last_update_time(self):
        # Test that the last update time changes when adding a packet and clearing the page
        page = Page(page_size=5)
        packet1 = Packet(SN=0, message=b'message1', mac=b'mac1')
        
        # Capture the last update time before adding a packet
        last_update_time_before = page.last_update_time
        time.sleep(0.01)  # Ensure some time passes
        page.add_packet(packet1)

        self.assertGreater(page.last_update_time, last_update_time_before)

        # Capture the last update time before clearing the page
        last_update_time_before_clear = page.last_update_time
        time.sleep(0.01)  # Ensure some time passes
        page.clear()

        self.assertGreater(page.last_update_time, last_update_time_before_clear)

if __name__ == '__main__':
    unittest.main()




