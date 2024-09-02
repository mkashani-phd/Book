import numpy as np
import time
from .Packet import Packet 
from .Page import Page


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
    
    def remove_page(self, page_index:int) -> Page:
        if page_index in self.pages:
            page = self.pages.pop(page_index)
            
            # If the page is the first page, update the global min and max SN
            if page_index == self.get_min_page_index():
                self.global_min_SN += self.page_size
                self.global_max_SN += self.page_size
            
            return page  # Return the detached packets
        return None

    def add_packet(self, packet:Packet) -> Page:
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
    
    def __repr__(self):
        return f"SlidingBook(num_pages={self.num_pages}, page_size={self.page_size}, pages={self.pages}, global_min_SN={self.global_min_SN}, global_max_SN={self.global_max_SN})"
 