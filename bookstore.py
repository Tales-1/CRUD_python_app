import sqlite3

# Select query abstracted as it is used multiple times
select_query = "SELECT * from books"

# Function to retrieve rows from the database
def retrieve_rows(query):
    try:
        db = sqlite3.connect("library.db")
        cursor = db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if db:
            db.close()

# Function to populate table with default values
def populate_table():
    try:
        db = sqlite3.connect("library.db")
        cursor = db.cursor()
        current_books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                        (3002,"Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                        (3003,"The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                        (3004,"The Lord of the Rings", "J.R.R Tolkien", 37),
                        (3005,"Alice in Wonderland", "Lewis Caroll", 12)]
        
        cursor.executemany('''INSERT INTO books VALUES(?,?,?,?)''', current_books)
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if db:
            db.close()

while True:
    # Open a connection with the library.db, if it doesn't exist then create one
    db = sqlite3.connect("library.db")
    cursor = db.cursor()
    ## Check if table exists by searching sqlite master and looking for table name
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = 'books'")
    table_exists = cursor.fetchone()
    # If table doesn't exist then create one
    if not table_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
        id INTEGER,
        Title TEXT,
        Author TEXT,
        Qty INTEGER,
        CONSTRAINT pk_id PRIMARY KEY(id)
    ''')
        db.commit()
        # Populate new table with data
        populate_table()
        db.commit()
    else:
        # if table exists check if it has data
        rows = retrieve_rows(select_query)
        if not rows:
            # If not then populate the table with default data
            populate_table()
    
    # Options presented to clerk
    option = input('''Select an option:
    1 - Add book
    2 - Update book
    3 - Delete book
    4 - Search book by Id
    5- View all books
    0 - Exit 
    ''')

    if option == "1":
        id = input("Enter the id of the book: ")
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        qty = input("Enter the qty of this book: ")
        cursor.execute("INSERT INTO books VALUES(?,?,?,?)",(id,title,author,qty))
        db.commit()
    
    elif option == "2":
        target_book_id = int(input("Enter the id of the book you would like to update: "))
        exists = False
        # Check if the id exists
        records = retrieve_rows(select_query)
        for row in records:
            if row[0] == target_book_id:
                exists = True

        if exists is True:
            target_col = input('''Enter the column you would like to update: 
                id
                Title
                Author
                Qty
                ''')
            check_col = cursor.execute(select_query)
            for column in check_col.description:
                if column[0].lower() == target_col.lower():
                    new_value = input(f"Change {target_col} to: ")
                    cursor.execute(f'''UPDATE books 
                    SET {target_col} = ?
                    WHERE id = ?
                    ''', (new_value, target_book_id))
                    db.commit()
            else:
                print("Wrong column entered \n")
            # make input match col name if first letter is lower case
        else:
            print("Book doesn't exist")

            
    elif option == "3":
        target_book_id = int(input("Enter the Id of the book you would like to remove: "))
        cursor.execute('''DELETE FROM books
        WHERE id = ?
        ''',(target_book_id,))
        db.commit()

    elif option == "4":
        target_book_id = int(input("Enter the Id of the book you would like to search: \n"))
        cursor.execute("SELECT * FROM books WHERE id = ?", (target_book_id,))
        record = cursor.fetchone()
        print("Id: ", record[0])
        print("Title: ", record[1])
        print("Author: ", record[2])
        print("Qty: ", record[3], "\n")

    elif option == "5":
          records = retrieve_rows(select_query)
          for row in records:
              print("Id: ", row[0])
              print("Title: ", row[1])
              print("Author: ", row[2])
              print("Qty: ", row[3], "\n")

    elif option == "0":
        db.close()
        exit()
