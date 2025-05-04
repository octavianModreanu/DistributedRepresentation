import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile 
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import network as DR
import os
"""
0.1
-the text field scrolls on its own -> NOT DONE    3
-the text field should clear after a few messages -> NOT DONE    3
-Clear all button -> NOT DONE     3
-A way to add multiple connections and nodes at once -> NOT DONE    3
-Activation of nodes -> IN PROGRESS     1
-Weights -> DONE
-Person nodes -> IN PROGRESS   1 
-Bind return to save button on popsave window -> NOT DONE     3
-If you just press the save button when you're in the popsave window, it should save under the current name -> NOT DONE   3
-Nodes with the same attribute should cluster together -> IN PROGRESS     2
    -> See chatgpt, but essentially we can give each category a cluster center to draw around

0.2 
-Embedding of novel data -> NOT DONE        4
"""
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.net = DR.network()

        # Window properties
        self.title("Node visualiser")
        self.geometry("800x600")
        
        # Top frame that holds two sub-frames side by side
        top_frame = tk.Frame(self)
        top_frame.pack(pady=10)

        add_frame = tk.Frame(top_frame)
        add_frame.pack(side="left",padx= 20)

        remove_frame = tk.Frame(top_frame)
        remove_frame.pack(side= "left", padx= 20)

        # Label, Entry, Text
        self.lbl = tk.Label(add_frame, text="ADD NODE")
        self.ent = tk.Entry(add_frame)
        self.lblr = tk.Label(remove_frame, text="REMOVE NODE")
        self.entr = tk.Entry(remove_frame)
        self.txt = tk.Text(self, height=5)
        
        # Bind <Return> in the Entry to add_line
        self.ent.bind("<Return>", self.add_line)
        self.entr.bind("<Return>", self.remove_line)

        # Dropdown button
        options = [
            "Name",
            "Age",
            "Education",
            "Occupation",
            "Gang",
            "Marital Status"
        ]
        self.category = tk.StringVar()
        self.category.set(options[0])
        self.drop= tk.OptionMenu(self, self.category, *options)

        # Button to open GraphML files
        self.load_button = tk.Button(self, text="Load GraphML", command=self.open_file)
        # Save button
        self.save_button = tk.Button(self, text= "Save", command= self.save_file)

        # Layout widgets
        self.lbl.pack()
        self.lblr.pack()
        self.ent.pack()
        self.entr.pack()
        self.txt.pack()
        self.load_button.pack()
        self.drop.pack()
        self.save_button.pack()

        # A reference to the current FigureCanvas so I can remove/replace it on new loads
        self.current_canvas = None

    def add_line(self, event):
        # Insert text from the Entry into the Text widget
        input = self.ent.get()
        category_in = self.category.get()

        for _ in input:
            # Add new connection
            if _ == "-":
                self.txt.insert(tk.END, f"New Connection: {self.ent.get()}\n")
                split_input = list(input.strip().split("-"))
                node1 = split_input[0]
                node2 = split_input[1]
                self.net.add_conn(node1,node2)
                break

            if _ == " ":
                self.txt.insert(tk.END, f"A dash (-) is used to add a new connection\n")
                break
        else:
            # Add a one word node
            self.txt.insert(tk.END, f"New Node: {self.ent.get()}\n")
            self.net.add_node(input, category_in)
        
        # Clear entry
        self.ent.delete(0, tk.END)

        # Draw current graph
        self.draw_current_graph()

    def remove_line(self, event):
        node_remove=self.entr.get().strip()

        for _ in node_remove:
            if _ == "-":
                self.txt.insert(tk.END, f"Connection {node_remove} has been removed.\n")
                split_node_remove = list(node_remove.strip().split("-"))
                node1 = split_node_remove[0]
                node2 = split_node_remove[1]
                self.net.remove_edge(node1, node2)
                break

            if _ == " ":
                self.txt.insert(tk.END, f"A dash (-) is used to remove a new connection\n")
                break
        else:
            if node_remove in self.net.graph.nodes:
                self.net.graph.remove_node(node_remove)
                self.txt.insert(tk.END, f"Node '{node_remove}' has been removed.\n")
            else:
                self.txt.insert(tk.END, f"Node '{node_remove}' not found in graph.\n")
        
        self.entr.delete(0,tk.END)

        self.draw_current_graph()
        

    def draw_current_graph(self):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().pack_forget()
        # Create a new Matplotlib figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Draw the current graph
        edge_labels = nx.get_edge_attributes(self.net.graph, "weight")
        pos = nx.spring_layout(self.net.graph)

        nx.draw(self.net.graph, ax=ax, with_labels=True, pos= pos)
        nx.draw_networkx_edge_labels(self.net.graph,pos= pos, edge_labels=edge_labels, ax=ax)

        #Embed the figure in this Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Keep track of this new canvas so we can remove it if we load another file
        self.current_canvas = canvas

# These things might be better to have them in a separate util file just for the sake of organisation 

    def save_file(self):
        popsave = tk.Toplevel(self)
        popsave.title("Save Graph")
        popsave.geometry("250x250")

        # Entry widget for the popup
        filename_entry = tk.Entry(popsave)

        save_button= tk.Button(popsave, text= "Save", command= lambda: self.confirm_save(filename_entry,popsave))
        
        # Widgetssss
        filename_entry.pack()
        save_button.pack()

    def confirm_save(self, filename_entry, popsave):
        filename= filename_entry.get().strip()
        if not filename:
            return

        saves_folder = "local_saves"
        if not os.path.exists(saves_folder):
            os.makedirs(saves_folder)

        if os.path.exists(filename):
            #I should put a warning message that it overwrites the save file but eh its late
            os.remove(file_path)
        file_path = os.path.join(saves_folder,filename)
        nx.write_graphml(self.net.graph, file_path)
        self.txt.insert(tk.END, f"Graph saved to {file_path}\n")

        popsave.destroy()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            #filetypes=[("GraphML Files", "*.graphml"), ("All files", "*.*")]
        )
        if file_path:
            self.net.graph = nx.read_graphml(file_path)
            self.draw_current_graph()


if __name__ == "__main__":
    App().mainloop()