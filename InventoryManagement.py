import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

# Database setup
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      quantity INTEGER NOT NULL,
                      price REAL NOT NULL)''')
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL)''')
    
    # Insert default admin user (only if not exists)
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    
    conn.commit()
    conn.close()

# Authentication
def login():
    username = simpledialog.askstring("Login", "Enter Username:")
    password = simpledialog.askstring("Login", "Enter Password:", show='*')
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Login Successful", f"Welcome, {username}")
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Add product
def add_product():
    name = name_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    
    if name and quantity.isdigit() and price.replace('.', '', 1).isdigit():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)", (name, int(quantity), float(price)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product added successfully!")
        display_products()
    else:
        messagebox.showerror("Error", "Invalid input. Ensure quantity and price are numbers.")

# Edit product
def edit_product():
    selected = listbox.selection()
    if selected:
        product_id = listbox.item(selected[0], 'values')[0]
        new_quantity = simpledialog.askinteger("Edit Quantity", "Enter new quantity:")
        new_price = simpledialog.askfloat("Edit Price", "Enter new price:")
        
        if new_quantity is not None and new_price is not None:
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET quantity=?, price=? WHERE id=?", (new_quantity, new_price, product_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product updated successfully!")
            display_products()
    else:
        messagebox.showerror("Error", "Select a product to edit")

# Delete product
def delete_product():
    selected = listbox.selection()
    if selected:
        product_id = listbox.item(selected[0], 'values')[0]
        
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        
        display_products()
        messagebox.showinfo("Success", "Product deleted successfully!")
    else:
        messagebox.showerror("Error", "Select a product to delete")

# Display products
def display_products():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    
    listbox.delete(*listbox.get_children())
    for row in rows:
        listbox.insert("", tk.END, values=row)

# Generate reports
def generate_report():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < 5")
    low_stock = cursor.fetchall()
    conn.close()
    
    if low_stock:
        report = "Low Stock Products:\n" + "\n".join([f"{p[1]} - {p[2]} left" for p in low_stock])
        messagebox.showwarning("Low Stock Alert", report)
    else:
        messagebox.showinfo("Stock Report", "All products have sufficient stock.")

# Main Application
def main_app():
    global name_entry, quantity_entry, price_entry, listbox
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("500x500")

    # Input fields
    tk.Label(root, text="Product Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Quantity:").pack()
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    tk.Label(root, text="Price:").pack()
    price_entry = tk.Entry(root)
    price_entry.pack()

    # Buttons
    tk.Button(root, text="Add Product", command=add_product).pack()
    tk.Button(root, text="Edit Product", command=edit_product).pack()
    tk.Button(root, text="Delete Product", command=delete_product).pack()
    tk.Button(root, text="Generate Report", command=generate_report).pack()

    # Product Listbox
    columns = ("ID", "Name", "Quantity", "Price")
    listbox = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        listbox.heading(col, text=col)
    listbox.pack(fill=tk.BOTH, expand=True)

    display_products()
    root.mainloop()

# Initialize database and start login
init_db()
login()
