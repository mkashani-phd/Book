import numpy as np
import time
from .Packet import Packet

class Page:
    def __init__(self, page_size: int = 10):
        self.page_size = page_size
        self.packets = np.full(page_size, None, dtype=object)  # Use a NumPy array to hold Packet instances
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
        self.packets.fill(None)  # Use NumPy's fill method to reset the array
        self.last_update_time = time.time()
        self.min_SN = None
        self.max_SN = None
        self.occupancy = 0

    def fill_missing_packets(self) -> None:
        """Fill missing packets with the appropriate SN and an empty message (b'')."""
        if self.min_SN is None or self.max_SN is None:
            return  # If the page has no packets yet, there's nothing to fill

        # Find the indices where packets are missing
        missing_indices = np.where(self.packets == None)[0]
        
        if len(missing_indices) > 0:
            # Create the sequence numbers for the missing packets
            missing_SNs = self.min_SN + missing_indices
            
            # Vectorized creation of Packet instances
            new_packets = np.array([Packet(SN=sn, message=b'') for sn in missing_SNs], dtype=object)
            
            # Assign the new packets to the missing indices
            self.packets[missing_indices] = new_packets
            self.occupancy += len(missing_indices)

    def __repr__(self):
        return f"Page(size={self.page_size}, packets={self.packets}, occupancy={self.occupancy})"



