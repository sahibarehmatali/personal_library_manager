import streamlit as st
import sqlite3

# Database connection
def create_connection():
    conn = sqlite3.connect("library.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        year INTEGER,
                        genre TEXT,
                        read_status BOOLEAN)''')
    conn.commit()
    conn.close()

create_table()

# Add a book
def add_book(title, author, year, genre, read_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, read_status))
    conn.commit()
    conn.close()
    st.rerun()

# Remove a book
def remove_book(title):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    st.rerun()

# Search for a book
def search_books(search_query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
    results = cursor.fetchall()
    conn.close()
    return results

# Display all books
def get_all_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Display statistics
def get_statistics():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    conn.close()
    return total_books, percentage_read

# Streamlit UI
st.title("📚 Personal Library Manager")

menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics", "Exit"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(title, author, year, genre, read_status)
        st.success(f"'{title}' has been added!")

elif choice == "Remove Book":
    st.subheader("❌ Remove a Book")
    title = st.text_input("Enter book title to remove")
    if st.button("Remove Book"):
        remove_book(title)
        st.success(f"'{title}' has been removed!")

elif choice == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter title or author")
    if st.button("Search"):
        results = search_books(search_query)
        if results:
            for book in results:
                st.write(f"📖 {book[1]} by {book[2]} ({book[3]}), Genre: {book[4]}, Read: {'Yes' if book[5] else 'No'}")
        else:
            st.warning("No books found!")

elif choice == "Display All Books":
    st.subheader("📚 All Books in Library")
    books = get_all_books()
    for book in books:
        st.write(f"📖 {book[1]} by {book[2]} ({book[3]}), Genre: {book[4]}, Read: {'Yes' if book[5] else 'No'}")

elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books, percentage_read = get_statistics()
    st.write(f"📚 Total Books: {total_books}")
    st.write(f"✅ Percentage Read: {percentage_read:.2f}%")

elif choice == "Exit":
    st.subheader("🚪 Exit Application")
    st.warning("You can close this tab to exit the application.")
