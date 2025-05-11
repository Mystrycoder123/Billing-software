import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("One Stop Store - Billing Software")
        self.root.geometry("900x600")
        
        # Variables
        self.items = []
        self.item_vars = {
            "name": tk.StringVar(),
            "price": tk.DoubleVar(),
            "quantity": tk.IntVar(value=1),
            "search": tk.StringVar()
        }
        self.total_var = tk.StringVar(value="Total: $0.00")
        self.tax_rate = 0.08  # 8% tax
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Header Frame
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10)
        
        ttk.Label(header_frame, text="ONE STOP STORE", font=('Helvetica', 16, 'bold')).grid(row=0, column=0)
        ttk.Label(header_frame, text="Billing Software", font=('Helvetica', 12)).grid(row=1, column=0)
        
        # Search Frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=5, fill='x', padx=10)
        
        ttk.Label(search_frame, text="Search Item:").pack(side='left')
        ttk.Entry(search_frame, textvariable=self.item_vars["search"], width=30).pack(side='left', padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_item).pack(side='left')
        
        # Item Entry Frame
        entry_frame = ttk.LabelFrame(self.root, text="Add New Item")
        entry_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(entry_frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        ttk.Entry(entry_frame, textvariable=self.item_vars["name"], width=30).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(entry_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        ttk.Entry(entry_frame, textvariable=self.item_vars["price"], width=10).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(entry_frame, text="Quantity:").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        ttk.Entry(entry_frame, textvariable=self.item_vars["quantity"], width=5).grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(entry_frame, text="Add Item", command=self.add_item).grid(row=0, column=6, padx=10)
        
        # Items Table Frame
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Treeview for items
        self.tree = ttk.Treeview(table_frame, columns=('name', 'price', 'quantity', 'total'), show='headings')
        self.tree.heading('name', text='Item Name')
        self.tree.heading('price', text='Price')
        self.tree.heading('quantity', text='Qty')
        self.tree.heading('total', text='Total')
        
        self.tree.column('name', width=300)
        self.tree.column('price', width=100, anchor='e')
        self.tree.column('quantity', width=50, anchor='center')
        self.tree.column('total', width=100, anchor='e')
        
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Action Buttons
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Button(action_frame, text="Remove Selected", command=self.remove_item).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Clear All", command=self.clear_items).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Print Bill", command=self.print_bill).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Save to CSV", command=self.save_to_csv).pack(side='left', padx=5)
        
        # Total Label
        ttk.Label(self.root, textvariable=self.total_var, font=('Helvetica', 12, 'bold')).pack(pady=10)
        
    def add_item(self):
        name = self.item_vars["name"].get().strip()
        price = self.item_vars["price"].get()
        quantity = self.item_vars["quantity"].get()
        
        if not name:
            messagebox.showerror("Error", "Please enter item name")
            return
        if price <= 0:
            messagebox.showerror("Error", "Price must be greater than 0")
            return
        if quantity <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
            
        total = price * quantity
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": total
        })
        
        self.update_treeview()
        self.calculate_total()
        
        # Clear entry fields
        self.item_vars["name"].set("")
        self.item_vars["price"].set(0.0)
        self.item_vars["quantity"].set(1)
        
    def update_treeview(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add items from list
        for item in self.items:
            self.tree.insert('', 'end', values=(
                item["name"],
                f"${item['price']:.2f}",
                item["quantity"],
                f"${item['total']:.2f}"
            ))
    
    def remove_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
            
        # Get index of selected item
        index = self.tree.index(selected_item[0])
        del self.items[index]
        
        self.update_treeview()
        self.calculate_total()
    
    def clear_items(self):
        if not self.items:
            return
            
        if messagebox.askyesno("Confirm", "Clear all items?"):
            self.items = []
            self.update_treeview()
            self.calculate_total()
    
    def calculate_total(self):
        subtotal = sum(item["total"] for item in self.items)
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax
        
        self.total_var.set(
            f"Subtotal: ${subtotal:.2f} | "
            f"Tax ({self.tax_rate*100:.0f}%): ${tax:.2f} | "
            f"Grand Total: ${grand_total:.2f}"
        )
    
    def print_bill(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items to print")
            return
            
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Print Bill")
        bill_window.geometry("400x600")
        
        # Bill header
        ttk.Label(bill_window, text="ONE STOP STORE", font=('Helvetica', 14, 'bold')).pack(pady=10)
        ttk.Label(bill_window, text="123 Main Street, City", font=('Helvetica', 10)).pack()
        ttk.Label(bill_window, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").pack(pady=5)
        
        # Bill items
        bill_text = tk.Text(bill_window, font=('Courier', 10))
        bill_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Format bill
        bill_text.insert('end', f"{'Item':<30}{'Qty':>5}{'Price':>10}{'Total':>10}\n")
        bill_text.insert('end', "-"*55 + "\n")
        
        subtotal = 0
        for item in self.items:
            bill_text.insert('end', 
                f"{item['name'][:30]:<30}"
                f"{item['quantity']:>5}"
                f"{item['price']:>10.2f}"
                f"{item['total']:>10.2f}\n"
            )
            subtotal += item['total']
        
        tax = subtotal * self.tax_rate
        grand_total = subtotal + tax
        
        bill_text.insert('end', "-"*55 + "\n")
        bill_text.insert('end', f"{'Subtotal:':<40}${subtotal:>10.2f}\n")
        bill_text.insert('end', f"{'Tax:':<40}${tax:>10.2f}\n")
        bill_text.insert('end', f"{'Grand Total:':<40}${grand_total:>10.2f}\n")
        
        # Disable editing
        bill_text.config(state='disabled')
        
        # Print button
        ttk.Button(bill_window, text="Print", command=lambda: self.print_bill_action(bill_window)).pack(pady=10)
    
    def print_bill_action(self, window):
        # In a real app, this would send to printer
        messagebox.showinfo("Print", "Bill sent to printer")
        window.destroy()
    
    def save_to_csv(self):
        if not self.items:
            messagebox.showwarning("Warning", "No items to save")
            return
            
        filename = f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                # Write header
                writer.writerow(['Item Name', 'Price', 'Quantity', 'Total', 'Date'])
                
                # Write items
                for item in self.items:
                    writer.writerow([
                        item['name'],
                        item['price'],
                        item['quantity'],
                        item['total'],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ])
                
                # Calculate totals
                subtotal = sum(item["total"] for item in self.items)
                tax = subtotal * self.tax_rate
                grand_total = subtotal + tax
                
                # Write totals
                writer.writerow([])
                writer.writerow(['Subtotal', '', '', subtotal])
                writer.writerow([f'Tax ({self.tax_rate*100:.0f}%)', '', '', tax])
                writer.writerow(['Grand Total', '', '', grand_total])
                
            messagebox.showinfo("Success", f"Bill saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def search_item(self):
        search_term = self.item_vars["search"].get().lower().strip()
        if not search_term:
            self.update_treeview()
            return
            
        filtered_items = [item for item in self.items if search_term in item["name"].lower()]
        
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add filtered items
        for item in filtered_items:
            self.tree.insert('', 'end', values=(
                item["name"],
                f"${item['price']:.2f}",
                item["quantity"],
                f"${item['total']:.2f}"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()