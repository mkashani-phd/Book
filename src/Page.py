import numpy as np
import time
from src import Packet

# it considers that the packet added to the page must have SN as the first element
# the rest is optional
import time

class Page:
    def __init__(self, page_size: int = 10):
        self.page_size = page_size
        self.packets = [None] * self.page_size  # Initialize a list to hold Packet instances
        self.last_update_time = time.time()
        self.min_SN = None
        self.max_SN = None
        self.occupancy = 0  # Track the number of packets in the page

    def add_packet(self, packet: Packet) -> bool:
        """Check if the SN is in the range of the page_size and add the packet."""
        SN = packet.SN

        if self.min_SN is None:
            self.min_SN = SN - SN % self.page_size
            self.max_SN = self.min_SN + self.page_size
        elif SN < self.min_SN or SN >= self.max_SN:
            return False
        elif self.packets[SN % self.page_size] is not None:
            return False

        self.packets[SN % self.page_size] = packet
        self.last_update_time = time.time()
        self.occupancy += 1
        return True

    def is_full(self) -> bool:
        """Check if the page is full."""
        return self.occupancy == self.page_size

    def clear(self) -> None:
        """Clear the page by deleting all Packet instances."""
        del self.packets[:]  # Deletes all elements in the list
        self.packets = [None] * self.page_size  # Reinitialize the list
        self.last_update_time = time.time()
        self.min_SN = None
        self.max_SN = None
        self.occupancy = 0

    def __repr__(self):
        return f"Page(size={self.page_size}, packets={self.packets}, occupancy={self.occupancy})"


