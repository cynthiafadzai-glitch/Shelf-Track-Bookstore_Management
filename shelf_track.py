import sqlite3
from pathlib import Path

# Get the folder where this Python file is saved
folder = Path(__file__).resolve().parent

# Create the database in the same folder
db = sqlite3.connect(folder / "ebookstore.db")

# Enable foreign key constraints
db.execute("PRAGMA foreign_keys = ON")

# Create a cursor to execute SQL commands
cursor = db.cursor()

# Create the book table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        authorID INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        FOREIGN KEY (authorID) REFERENCES author (id)
    )
""")
# Create the author table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL
    )
""")
# List of authors
authors = [
    (1290, "Charles Dickens", "England"),
    (8937, "J.K. Rowling", "England"),
    (2356, "C.S. Lewis", "Ireland"),
    (6380, "J.R.R. Tolkien", "England"),
    (5620, "Lewis Carroll", "England")
]

# Insert authors into the author table
cursor.executemany("""
    INSERT OR IGNORE INTO author (id, name, country)
    VALUES (?, ?, ?)
""", authors)

# Save changes
db.commit()

# List of books to add to the database
books = [
    (3001, "A Tale of Two Cities", 1290, 30),
    (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
    (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
    (3004, "The Lord of the Rings", 6380, 37),
    (3005, "Alice's Adventures in Wonderland", 5620, 12)
]

# Add sample books only when the database is first created
cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_setup (
        name TEXT PRIMARY KEY
    )
""")

cursor.execute(
    "SELECT name FROM app_setup WHERE name = ?",
    ("initial_books",)
)
if cursor.fetchone() is None:
    cursor.executemany("""
        INSERT OR IGNORE INTO book (id, title, authorID, qty)
        VALUES (?, ?, ?, ?)
    """, books)

    cursor.execute(
        "INSERT INTO app_setup (name) VALUES (?)",
        ("initial_books",)
    )
# Function to add a new book
def add_book():
    try:
        # Ask the user for book details
        book_id = int(input("Enter book ID: "))
        title = input("Enter book title: ").strip()
        author_id = int(input("Enter author ID: "))
        quantity = int(input("Enter quantity: "))

        # Validate the information
        if book_id <= 0 or author_id <= 0:
            print("Error: IDs must be positive numbers.")
            return

        if not title:
            print("Error: Book title cannot be empty.")
            return

        if quantity < 0:
            print("Error: Quantity cannot be negative.")
            return

        # Insert the book into the database
        cursor.execute("""
            INSERT INTO book (id, title, authorID, qty)
            VALUES (?, ?, ?, ?)
        """, (book_id, title, author_id, quantity))

        # Save the changes
        db.commit()

        print("\nBook added successfully!")

    except ValueError:
        print("\nError: Book ID, Author ID and quantity must be numbers.")

    except sqlite3.IntegrityError as error:
        db.rollback()

        if "FOREIGN KEY constraint failed" in str(error):
            print("\nError: Author ID does not exist.")
            print("Please use an existing Author ID.")

        elif "UNIQUE constraint failed" in str(error):
            print("\nError: This Book ID already exists.")

        else:
            print(f"\nDatabase error: {error}")

# Function to update an existing book
def update_book():
    try:
        # Ask for the book ID
        book_id = int(input("Enter the book ID to update: "))

        # Check if the book exists
        cursor.execute(
            "SELECT * FROM book WHERE id = ?", (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            print("\nBook not found.")
            return

        # Display current book information
        print("\nCurrent book details:")
        print(f"Title: {book[1]}")
        print(f"Author ID: {book[2]}")
        print(f"Quantity: {book[3]}")

        # Ask what the user wants to update
        print("\nWhat would you like to update?")
        print("1. Quantity")
        print("2. Title")
        print("3. Author ID")

        option = input("Select an option: ")
        if option == "1":
            new_quantity = int(input("Enter new quantity: "))

            if new_quantity < 0:
                print("Quantity cannot be negative.")
                return

            cursor.execute(
                "UPDATE book SET qty = ? WHERE id = ?",
                (new_quantity, book_id)
            )

        elif option == "2":
            new_title = input("Enter new title: ").strip()

            if not new_title:
                print("Title cannot be empty.")
                return

            cursor.execute(
                "UPDATE book SET title = ? WHERE id = ?",
                (new_title, book_id)
            )

        elif option == "3":
            new_author = int(input("Enter new author ID: "))

            if new_author <= 0:
                print("Author ID must be positive.")
                return

            cursor.execute(
                "UPDATE book SET authorID = ? WHERE id = ?",
                (new_author, book_id)
            )

        else:
            print("Invalid update option.")
            return

        # Save the changes
        db.commit()

        print("\nBook updated successfully!")

    except sqlite3.IntegrityError as error:
        db.rollback()

        if "FOREIGN KEY constraint failed" in str(error):
            print("\nError: Author ID does not exist.")

        else:
            print(f"\nDatabase error: {error}")

    except sqlite3.Error as error:
        db.rollback()
        print(f"\nDatabase error: {error}")


# Function to delete a book
def delete_book():
    try:
        # Ask the user for the book ID
        book_id = int(input("Enter the book ID to delete: "))

        # Check if the book exists
        cursor.execute(
            "SELECT * FROM book WHERE id = ?", (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            print("\nBook not found.")
            return

        # Display the book details
        print("\nBook found:")
        print(f"ID: {book[0]}")
        print(f"Title: {book[1]}")
        print(f"Author ID: {book[2]}")
        print(f"Quantity: {book[3]}")

        # Ask for confirmation before deleting
        confirm = input(
            "\nAre you sure you want to delete this book? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            # Delete the selected book
            cursor.execute(
                "DELETE FROM book WHERE id = ?", (book_id,)
            )

            # Save the changes
            db.commit()

            print("\nBook deleted successfully!")

        else:
            print("\nDeletion cancelled.")

    except ValueError:
        print("\nError: Please enter a valid book ID.")

    except sqlite3.IntegrityError as error:
        db.rollback()
        print(f"\nDatabase error: {error}")
# Function to display book information
def display_book(book):
    print(f"\nBook ID: {book[0]}")
    print(f"Title: {book[1]}")
    print(f"Author ID: {book[2]}")
    print(f"Quantity: {book[3]}")
    print("---------------------------")


# Function to search for books
def search_book():
    try:
        print("\n===== SEARCH BOOKS =====")
        print("1. Search by Book ID")
        print("2. Search by Title")

        option = input("Select an option: ")

        if option == "1":
            # Search using the book ID
            book_id = int(input("Enter Book ID: "))

            cursor.execute(
                "SELECT * FROM book WHERE id = ?",
                (book_id,)
            )

            books = cursor.fetchall()

        elif option == "2":
            # Search using the book title
            title = input("Enter book title: ").strip()

            if not title:
                print("Error: Please enter a book title.")
                return

            cursor.execute(
                "SELECT * FROM book WHERE title LIKE ?",
                (f"%{title}%",)
            )

            books = cursor.fetchall()

        else:
            print("Invalid search option.")
            return

        # Display search results
        if books:
            print("\n===== SEARCH RESULTS =====")

            for book in books:
                display_book(book)

        else:
            print("\nNo matching books found.")

    except ValueError:
        print("\nError: Please enter a valid Book ID.")

    except sqlite3.Error as error:
        print(f"\nDatabase error: {error}")

# Test the author table
cursor.execute("SELECT * FROM author")

print("\n===== AUTHORS =====")

for author in cursor.fetchall():
    print(author)
        
# Function to view all books and their authors
def view_all_books():
    try:
        cursor.execute("""
            SELECT book.id, book.title, author.name,
                   author.country, book.qty
            FROM book
            INNER JOIN author
            ON book.authorID = author.id
            ORDER BY book.id
        """)

        books = cursor.fetchall()

        if books:
            print("\n===== ALL BOOK DETAILS =====")

            for book in books:
                print(f"\nBook ID: {book[0]}")
                print(f"Title: {book[1]}")
                print(f"Author: {book[2]}")
                print(f"Country: {book[3]}")
                print(f"Quantity: {book[4]}")
                print("---------------------------")
        else:
            print("\nNo matching books found.")

    except sqlite3.Error as error:
        print(f"\nDatabase error: {error}")

# Function to update author details
def update_author():
    try:
        # Ask for the author ID
        author_id = int(input("Enter the Author ID to update: "))

        # Check if the author exists
        cursor.execute(
            "SELECT * FROM author WHERE id = ?",
            (author_id,)
        )

        author = cursor.fetchone()

        if author is None:
            print("\nAuthor not found.")
            return

        # Display current author details
        print("\nCurrent author details:")
        print(f"Name: {author[1]}")
        print(f"Country: {author[2]}")

        # Ask what the user wants to update
        print("\nWhat would you like to update?")
        print("1. Author Name")
        print("2. Country")

        option = input("Select an option: ")

        if option == "1":
            new_name = input("Enter new author name: ").strip()

            if not new_name:
                print("Author name cannot be empty.")
                return

            cursor.execute(
                "UPDATE author SET name = ? WHERE id = ?",
                (new_name, author_id)
            )

        elif option == "2":
            new_country = input("Enter new country: ").strip()

            if not new_country:
                print("Country cannot be empty.")
                return

            cursor.execute(
                "UPDATE author SET country = ? WHERE id = ?",
                (new_country, author_id)
            )

        else:
            print("Invalid update option.")
            return

        # Save the changes
        db.commit()

        print("\nAuthor updated successfully!")

    except ValueError:
        print("\nError: Please enter a valid Author ID.")

    except sqlite3.Error as error:
        db.rollback()
        print(f"\nDatabase error: {error}")

# Check for books without matching authors
cursor.execute("""
    SELECT book.id, book.title, book.authorID
    FROM book
    LEFT JOIN author
    ON book.authorID = author.id
    WHERE author.id IS NULL
""")

missing_authors = cursor.fetchall()

print("\n===== BOOKS WITH MISSING AUTHORS =====")

if missing_authors:
    for book in missing_authors:
        print(book)
else:
    print("All books have matching authors.")

# Bookstore menu
while True:
    print("\n===== SHELF TRACK BOOKSTORE =====")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("5. View all books")
    print("6. Update author")
    print("0. Exit")

    choice = input("\nPlease select an option: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        update_book()

    elif choice == "3":
        delete_book()

    elif choice == "4":
        search_book()

    elif choice == "5":
        view_all_books()

    elif choice == "6":
        update_author()

    elif choice == "0":
        print("Thank you for using Shelf Track!")
        break

    else:
        print("Invalid option. Please try again.")

# Close the database when the user exits
db.close()




