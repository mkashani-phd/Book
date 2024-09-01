
import unittest
import numpy as np
import time
from Page import Page
from Packet import Packet   


class SlidingBook:
    def __init__(self, num_pages:int = 15, page_size:int = 18, timeout:float = 0.001):
        self.pages = {}
        self.num_pages = num_pages
        self.page_size = page_size
        self.global_min_SN = 0
        self.global_max_SN = num_pages * page_size
        self.timeout = timeout


    def get_min_page_index(self) -> int:
        return self.global_min_SN // self.page_size
    
    def remove_page(self, page_index:int) -> Page | None:
        if page_index in self.pages:
            page = self.pages.pop(page_index)
            
            # If the page is the first page, update the global min and max SN
            if page_index == self.get_min_page_index():
                self.global_min_SN += self.page_size
                self.global_max_SN += self.page_size
            
            return page  # Return the detached packets
        return None

    def add_packet(self, packet:Packet) -> Page | None:
        SN = packet.SN
        page_index = SN // self.page_size

        if SN < self.global_min_SN or SN >= self.global_max_SN:
            min_page_index = self.get_min_page_index()
            page = self.pages.get(min_page_index)
            if page and page.last_update_time + self.timeout < time.time(): 
                return self.remove_page(min_page_index)
            return None

        page = self.pages.get(page_index)
        
        if page is None:
            page = Page(page_size=self.page_size)
            self.pages[page_index] = page

        if page.add_packet(packet):
            if page.is_full():
                return self.remove_page(page_index)
        return None
    
    def get_page_index(self) -> np.ndarray:
        return np.array(list(self.pages.keys()))

    def clear_all(self) -> None:
        self.pages = {}
        self.global_min_SN = 0
        self.global_max_SN = self.num_pages * self.page_size
    
class TestSlidingBook(unittest.TestCase):

    def test_sliding_book_initialization(self):
        # Test that a SlidingBook initializes correctly
        book = SlidingBook(num_pages=10, page_size=5)
        self.assertEqual(book.num_pages, 10)
        self.assertEqual(book.page_size, 5)
        self.assertEqual(book.global_min_SN, 0)
        self.assertEqual(book.global_max_SN, 50)  # 10 pages * 5 page_size
        self.assertEqual(len(book.pages), 0)

    def test_add_packet_within_range(self):
        # Test adding a packet within the global SN range
        book = SlidingBook(num_pages=10, page_size=5)
        packet = Packet(SN=3, message=b'message', mac=b'mac')
        returned_page = book.add_packet(packet)
        
        self.assertIsNone(returned_page)  # No page should be removed
        self.assertIn(0, book.pages)  # Page 0 should exist
        self.assertEqual(book.pages[0].packets[3 % 5], packet)  # Packet should be in the correct place

    def test_add_packet_out_of_range(self):
        # Test adding a packet outside the global SN range
        book = SlidingBook(num_pages=10, page_size=5)
        packet = Packet(SN=55, message=b'message', mac=b'mac')
        returned_page = book.add_packet(packet)
        
        self.assertIsNone(returned_page)  # No page should be removed
        self.assertEqual(len(book.pages), 0)  # No pages should be added

    def test_remove_page(self):
        # Test removing a page
        book = SlidingBook(num_pages=10, page_size=5)
        packet1 = Packet(SN=3, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=4, message=b'message2', mac=b'mac2')
        
        book.add_packet(packet1)
        book.add_packet(packet2)
        removed_page = book.remove_page(0)

        self.assertIsNotNone(removed_page)
        self.assertEqual(len(book.pages), 0)  # Page 0 should be removed
        self.assertEqual(removed_page.packets[3 % 5], packet1)
        self.assertEqual(removed_page.packets[4 % 5], packet2)
        self.assertEqual(book.global_min_SN, 5)
        self.assertEqual(book.global_max_SN, 55)

    def test_add_packet_and_remove_page(self):
        # Test adding packets and then triggering page removal
        book = SlidingBook(num_pages=2, page_size=2)
        packet1 = Packet(SN=0, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=1, message=b'message2', mac=b'mac2')
        packet3 = Packet(SN=2, message=b'message3', mac=b'mac3')
        packet4 = Packet(SN=3, message=b'message4', mac=b'mac4')

        book.add_packet(packet1)
        book.add_packet(packet2)
        book.add_packet(packet3)
        returned_page = book.add_packet(packet4)

        self.assertIsNotNone(returned_page)
        self.assertEqual(len(book.pages), 0)
        self.assertEqual(book.global_min_SN, 4)
        self.assertEqual(book.global_max_SN, 8)

    def test_get_page_index(self):
        # Test getting the current page indices
        book = SlidingBook(num_pages=10, page_size=5)
        packet1 = Packet(SN=3, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=15, message=b'message2', mac=b'mac2')

        book.add_packet(packet1)
        book.add_packet(packet2)

        page_indices = book.get_page_index()
        self.assertTrue((page_indices == [0, 3]).all())

    def test_clear_all(self):
        # Test clearing all pages
        book = SlidingBook(num_pages=10, page_size=5)
        packet1 = Packet(SN=3, message=b'message1', mac=b'mac1')
        packet2 = Packet(SN=15, message=b'message2', mac=b'mac2')

        book.add_packet(packet1)
        book.add_packet(packet2)
        book.clear_all()

        self.assertEqual(len(book.pages), 0)
        self.assertEqual(book.global_min_SN, 0)
        self.assertEqual(book.global_max_SN, 50)

if __name__ == '__main__':
    unittest.main()
