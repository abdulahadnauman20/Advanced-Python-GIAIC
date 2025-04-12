import streamlit as st
import json
import os

def load_library(filename='library.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            library = json.load(file)
    else:
        library = []
    return library

def save_library(library, filename='library.json'):
    with open(filename, 'w') as file:
        json.dump(library, file, indent=4)

def add_book(library):
    st.subheader("Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.selectbox("Have you read it?", ["Yes", "No"])

    if st.button("Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": True if read == "Yes" else False
        }
        library.append(book)
        save_library(library)
        st.success("Book added successfully!")

def remove_book(library):
    st.subheader("Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library[:] = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success("Book removed successfully.")
    else:
        st.info("No books available to remove.")

def search_books(library):
    st.subheader("Search for a Book")
    option = st.radio("Search by", ["Title", "Author"])
    query = st.text_input("Enter your search query")
    if st.button("Search"):
        results = []
        if option == "Title":
            results = [book for book in library if query.lower() in book["title"].lower()]
        else:
            results = [book for book in library if query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(book)
        else:
            st.warning("No matching books found.")

def display_books(library):
    st.subheader("All Books in Library")
    if library:
        for i, book in enumerate(library, start=1):
            st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("Library is empty.")

def display_stats(library):
    st.subheader("Library Statistics")
    total = len(library)
    read = len([b for b in library if b["read"]])
    unread = total - read
    if total > 0:
        percent_read = (read / total) * 100
    else:
        percent_read = 0
    st.write(f"Total Books: {total}")
    st.write(f"Read Books: {read}")
    st.write(f"Unread Books: {unread}")
    st.write(f"Percentage Read: {percent_read:.2f}%")

def main():
    st.title("📚 Personal Library Manager")
    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "View Stats"]
    choice = st.sidebar.selectbox("Menu", menu)
    library = load_library()

    if choice == "Add Book":
        add_book(library)
    elif choice == "Remove Book":
        remove_book(library)
    elif choice == "Search Book":
        search_books(library)
    elif choice == "Display All Books":
        display_books(library)
    elif choice == "View Stats":
        display_stats(library)

if __name__ == "__main__":
    main()
