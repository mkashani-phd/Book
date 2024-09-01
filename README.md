# Book Package

## Overview

The **Book** package is a Python module designed to manage a collection of network packets. It includes classes for handling individual packets (`Packet`), organizing these packets into pages (`Page`), and managing multiple pages in a sliding window fashion (`SlidingBook`). Each class is thoroughly tested with corresponding unit tests.

## Project Structure

The `Book` package is organized as follows:

- **`__init__.py`**: Initializes the `Book` package, allowing it to be imported as a module.
- **`Book.py`**: Contains the `SlidingBook` class, which manages multiple pages of packets in a sliding window fashion.
- **`Page.py`**: Contains the `Page` class, which organizes multiple `Packet` instances into a page.
- **`Packet.py`**: Contains the `Packet` class, representing an individual network packet.
- **`tests/`**: A directory containing unit tests for each class in the `Book` package:
  - **`__init__.py`**: Initializes the `tests` package.
  - **`test_book.py`**: Unit tests for the `SlidingBook` class.
  - **`test_page.py`**: Unit tests for the `Page` class.
  - **`test_packet.py`**: Unit tests for the `Packet` class.

## Classes

### 1. `Packet` (Located in `Packet.py`)

The `Packet` class represents an individual network packet. It includes:

- **Attributes**:
  - `SN`: Sequence Number of the packet.
  - `message`: The message contained in the packet, in bytes.
  - `mac`: Optional MAC (Message Authentication Code) of the packet, in bytes.
  - `timestamp`: The timestamp indicating when the packet was created.
  - `payload_size`: The size of the message in bytes.

- **Methods**:
  - `to_bytes()`: Converts the packet instance to bytes for transmission.
  - `from_bytes(data: bytes)`: Creates a `Packet` instance from a byte sequence.
  - `__repr__()`: Provides a string representation of the `Packet`.

### 2. `Page` (Located in `Page.py`)

The `Page` class organizes multiple `Packet` instances into a page. It includes:

- **Attributes**:
  - `page_size`: The maximum number of packets a page can hold.
  - `packets`: A list to hold `Packet` instances.
  - `last_update_time`: The last time a packet was added to the page.
  - `min_SN`, `max_SN`: Track the minimum and maximum sequence numbers within the page.
  - `occupancy`: The current number of packets in the page.

- **Methods**:
  - `add_packet(packet: Packet)`: Adds a packet to the page if it falls within the allowed sequence number range.
  - `is_full()`: Checks if the page is full.
  - `clear()`: Clears the page, deleting all `Packet` instances it holds.
  - `__repr__()`: Provides a string representation of the `Page`.

### 3. `SlidingBook` (Located in `Book.py`)

The `SlidingBook` class manages multiple pages in a sliding window fashion. It includes:

- **Attributes**:
  - `pages`: A dictionary to hold `Page` instances, indexed by page number.
  - `num_pages`: The maximum number of pages.
  - `page_size`: The number of packets each page can hold.
  - `global_min_SN`, `global_max_SN`: Track the global range of sequence numbers across all pages.
  - `timeout`: Time after which a page is considered stale and removed.

- **Methods**:
  - `get_min_page_index()`: Returns the index of the minimum page.
  - `remove_page(page_index: int)`: Removes a page and returns it.
  - `add_packet(packet: Packet)`: Adds a packet to the appropriate page, removing a stale page if necessary.
  - `get_page_index()`: Returns the indices of the current pages.
  - `clear_all()`: Clears all pages.
  - `__repr__()`: Provides a string representation of the `SlidingBook`.

## Unit Tests

Each class has a corresponding unit test file located in the `tests/` directory. The tests ensure the correctness of the class implementations.

### Running Tests

To run the unit tests, navigate to the `Book/` directory and execute:

```bash
python3 -m unittest discover -s src/tests
```

This command will automatically discover and run all unit tests in the tests/ directory.

## Usage

Here is a basic example of how to use the Book package:

```python
from Book import SlidingBook, Packet

# Create a SlidingBook instance
book = SlidingBook(num_pages=10, page_size=5)

# Create a Packet instance
packet = Packet(SN=1, message=b"Hello, World!", mac=b"0123456789ABCDEF")

# Add the packet to the SlidingBook
book.add_packet(packet)

# Retrieve current page indices
print(book.get_page_index())

# Clear all pages
book.clear_all()
```

# Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue on GitHub.

# Licence

This project is licensed under the MIT License - see the LICENSE file for details.


### Key Sections:

1. **Overview**: Provides a brief introduction to the package.
2. **Project Structure**: Outlines the directory structure of the package.
3. **Classes**: Describes the key classes (`Packet`, `Page`, `SlidingBook`) and their functionalities.
4. **Unit Tests**: Explains where the unit tests are located and how to run them.
5. **Usage**: Provides a basic example of how to use the package.
6. **Contributing**: Invites contributions from the community.
7. **License**: Mentions the license under which the package is distributed.



