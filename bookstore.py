import sqlite3


while True:
    db = sqlite3.connect("library.db")
    cursor = db.cursor()
    check_id = 3001
    ## check if table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS books(
        id INTEGER,
        Title TEXT,
        Author TEXT,
        Qty INTEGER,
        CONSTRAINT pk_id PRIMARY KEY(id))
    ''')

    db.commit()

    cursor.execute("SELECT * FROM books WHERE id=?", (check_id,))
    row = cursor.fetchone()
    if row is None:
        current_books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                        (3002,"Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                        (3003,"The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
                        (3004,"The Lord of the Rings", "J.R.R Tolkien", 37),
                        (3005,"Alice in Wonderland", "Lewis Caroll", 12)]
        
        cursor.executemany('''INSERT INTO books VALUES(?,?,?,?)''', current_books)
        db.commit()
        cursor.execute("SELECT * FROM books")
        result = cursor.fetchall()
        print(result)
    
    option = input('''Select an option:
    1 - Enter book
    2 - Update book
    3 - Delete book
    4 - Search books
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
        target_book = input("Enter the id of the book you would like to update")
        target_col = input('''Enter the column you would like to update: 
        id
        Title
        Author
        Qty
        ''')
        # make input match col name if first letter is lower case
        target_col

    elif option == "0":
        db.close()
        exit()
