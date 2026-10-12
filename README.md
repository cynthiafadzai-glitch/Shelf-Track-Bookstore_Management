
# Shelf Track — Bookstore Inventory Management System

## Project Overview

Shelf Track is a Python-based bookstore inventory management application developed using SQLite.

The system allows bookstore clerks to manage books, track inventory quantities, search for records, and maintain author information.

This project demonstrates practical knowledge of Python programming, relational database design, SQL queries, and data management.

## Features

- Add new books to the database
- Update book titles, quantities, and author IDs
- Delete books from the database
- Search books by ID or title
- View books with author names and countries
- Update author information
- Validate user inputs
- Handle database errors
- Maintain data integrity using foreign keys

## Technologies Used

- Python 3
- SQLite3
- SQL
- Visual Studio Code
- Git and GitHub

## Database Structure

The application contains two main tables:

**Book Table**
- id (Primary Key)
- title
- authorID (Foreign Key)
- qty

**Author Table**
- id (Primary Key)
- name
- country

The tables are linked using book.authorID and author.id.

## SQL Concepts Demonstrated

- CREATE TABLE
- INSERT INTO
- SELECT
- UPDATE
- DELETE
- INNER JOIN
- PRIMARY KEY
- FOREIGN KEY
- Parameterised queries

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Run:

   python shelf_track.py

5. Follow the interactive menu.

The SQLite database is created automatically when the program runs.

## Skills Demonstrated

- Python programming
- Relational database management
- CRUD operations
- SQL querying
- Data validation
- Error handling
- Code modularity
- Debugging and testing

## Project Background

Developed as part of a Python and Database Management learning project, with a focus on practical inventory management and relational database concepts.
