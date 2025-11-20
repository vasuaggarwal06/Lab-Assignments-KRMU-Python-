import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(filename='library.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"


class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()

    def load_books(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        self.books.append(Book(**item))
            else:
                logging.info("Catalog file not found. Creating new one.")
        except Exception as e:
            logging.error(f"Error loading file: {e}")

    def save_books(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        for b in self.books:
            print(b)


def main():
    inventory = LibraryInventory()

    while True:
        print("\n---- Library Inventory Manager ----")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                title = input("Enter title: ")
                author = input("Enter author: ")
                isbn = input("Enter ISBN: ")
                inventory.add_book(Book(title, author, isbn))
                print("Book added.")

            elif choice == '2':
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_books()
                    print("Book issued.")
                else:
                    print("Book unavailable or not found.")

            elif choice == '3':
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_books()
                    print("Book returned.")
                else:
                    print("Book not found or already available.")

            elif choice == '4':
                inventory.display_all()

            elif choice == '5':
                title = input("Enter title to search: ")
                results = inventory.search_by_title(title)
                if results:
                    for b in results:4
                    print(b)
                else:
                    print("No match found.")

            elif choice == '6':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            logging.error(f"Error in operation: {e}")
            print("An error occurred.")


if __name__ == "__main__":
    main()
