from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from os import stat
import customtopology


# Show directory
def directory():


    info = stat('./report.txt')
    print("========================> Size of the report file is:", info.st_size)
    print("========================> The most recent modification is:", info.st_mtime)


# Open a file
def openfile():
    root.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                 filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    print(root.filename)


# Open the JSON file
def json():

    status.config(text="JSON file")
    with open('Topology', 'r+') as f:
        data = f.read()
        tkinter.messagebox.showinfo("The JSON file", data)

        data_json = Text(root, height=35, width=35, bg='lightblue')
        data_json.pack(side=TOP, fill=X, padx=2, pady=2)


# About software version and the developer
def about():
    tkinter.messagebox.showinfo("GUI Mininet application",
                                "\n Version - 1" +
                                ' ' + "\n CopyRight@Nima Eivazzadeh" +
                                "\n Developed by Python 3+ for the \n"
                                " course problems solving \n "
                                "with scripting language")
# Plot preview
def plot_preview():

    nodes = customtopology.data['Switches'] + customtopology.data['Hosts']
    path = customtopology.data['Path']
    labels = {}
    edges_all = []
    edges_path = []
    G = nx.DiGraph()

    for link in customtopology.data['Links']:
        for A, B in link.items():
            A_name = A.split('-')[0]
            A_if = A.split('-')[1]
            B_name = B.split('-')[0]
            B_if = B.split('-')[1]
            edges_all.append([A_name, B_name])
            labels[(A_name, B_name)] = A_if
            labels[(B_name, A_name)] = B_if

    for i in range(0, len(path) - 1):
        edges_path.append([path[i], path[i + 1]])

    G.add_nodes_from(nodes)
    G.add_edges_from(edges_all)

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color='orange')
    nx.draw_networkx_labels(G, pos, node_size=800, font_size=10, with_labels=True)
    nx.draw_networkx_edges(G, pos, arrows=False)
    nx.draw_networkx_edges(G, pos, edges_path, edge_color='#00FF00', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, labels, 0.8)
    plt.ylabel('Topology')
    plt.title('Topology graph based on "Links" dictionary in JSON file')
    plt.axis('off')
    plt.show()


# Generate a report when deployment has been completed
def report():
    tkinter.messagebox.showinfo("Generate report", "Report has been generated")
    status.config(text="Report has been published")

    reader = open('./stdout.txt', 'r')
    rep = reader.readlines()

    f = open('report.txt', 'w')
    for item in rep:
        f.write(str(item))
    f.close()


# clear canvas
def clear_canvas():
    status.config(text="Canvas has been cleared")
    textBox_mininet_deploy.delete('1.0', END)


# callback function for drop down
def callback(*args):
    customtopology.node_1 = node_1.get()
    customtopology.node_2 = node_2.get()


root = Tk()

root.geometry("1960x960")
root.title('This is the Mininet project designed and developed by Nima Eivazzadeh')
root.option_add("*Dialog.msg.wrapLength", "10i")

# Menu_bar
menu_bar = Menu(root)
root.config(menu=menu_bar, width=1680, height=768, bg="SkyBlue1")

subMenu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=openfile)
subMenu.add_separator()
subMenu.add_command(label="Exit ", command=root.destroy)

EditMenu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=EditMenu)
EditMenu.add_command(label="About", command=about)

# Toolbar
toolbar = Frame(root, bg="lightblue")

PlotBtn = Button(toolbar, text="Topology preview as a plot", bg='lightblue', command=plot_preview)
DeployBtn = Button(toolbar, text="Deploy topology to mininet from the JSON file", bg='DeepSkyBlue2', command=customtopology.testtopology)
ModifyJsonBtn = Button(toolbar, text="Preview the JSON File", bg='lightblue',  command=json)
PdfReportBtn = Button(toolbar, text="Generate a report",  bg='lightblue', command=report)
ClearCanvasBtn = Button(toolbar, text="Clear canvas",  bg='lightblue', command=clear_canvas)

PlotBtn.pack(side=LEFT, padx=1, pady=1)
DeployBtn.pack(side=LEFT, padx=1, pady=1)
ModifyJsonBtn.pack(side=LEFT, padx=1, pady=1)
PdfReportBtn.pack(side=LEFT, padx=1, pady=1)
ClearCanvasBtn.pack(side=LEFT, padx=1, pady=1)
toolbar.pack(side=TOP, fill=X)


# Drop down lists
choices = list()

for host in customtopology.data['Hosts']:  # a loop in Hosts list from JSON file to test iPerf.
    choices.append(host)

node_1 = StringVar(root)  # makes a variable for drop down
node_2 = StringVar(root)

node_1.set(choices[0])    # makes a default value for drop down
node_2.set(choices[1])
callback()

drop_down_1 = OptionMenu(root, node_1, *choices)
drop_down_2 = OptionMenu(root, node_2,  *choices)

drop_down_1.pack(side=TOP,  padx=3, pady=3, anchor=CENTER)
drop_down_2.pack(side=TOP,  padx=3, pady=3, anchor=CENTER)

node_1.trace('w', callback)
node_2.trace('w', callback)


# iPerf label
w = Label(root, text="Choose hosts from drop down list and press deploy button to test IPerf for any specific nodes and see the result in the canvas",
                bg='deepskyblue', bd=2, relief=GROOVE)
w.pack(side=TOP)


# Textbox
textBox_mininet_deploy = Text(root, height=35, width=200, bg='lightblue')
textBox_mininet_deploy.pack(side=TOP,  fill=X, padx=2, pady=2)
customtopology.mnOutput = textBox_mininet_deploy


# StatusBar
status = Label(root, text="Mininet Project designed and developed by Nima Eivazzadeh",
                     bd=2, bg="deepskyblue", relief=GROOVE, )
status.pack(side=BOTTOM, fill=X, padx=20, pady=20)

# Mainloop
root.mainloop()
