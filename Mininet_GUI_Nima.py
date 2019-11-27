from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter, A4, landscape
import subprocess
from os import listdir
from os import getcwd
from os import walk
from os.path import exists
from os import access
from os import F_OK, R_OK, W_OK, X_OK
from os import stat
import customtopology
import os


# Show directory
def directory():

    # list_report = listdir('.')
    #
    # for list_dir in list_report:
    #     print(list_dir)

    # tree = walk('.')
    #
    # print(tree)

    # exists('./report.txt')

    # z = access('./report.txt', os.W_OK)
    # print(z)
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
#         data_json = Text(root, height=35, width=35, bg='lightblue')
#         data_json.pack(side=TOP, fill=X, padx=2, pady=2)


# About software version and the developer
def about():
    tkinter.messagebox.showinfo("GUI Mininet application",
                                "\n Version - 1" +
                                ' ' + "\n CopyRight@Nima Eivazzadeh" +
                                "\n Developed by Python 3+ for the \n"
                                " course problems solving \n "
                                "with scripting language")


# create a path from JSON file
def path_preview():
    status.config(text="Path Preview")
    g = nx.DiGraph()
    for path in customtopology.data['Path']:
        for p in path:
            src = p
            dst = path[p]

            sr_link = src
            ds_link = dst

# create graph from the JSON file to show Path
            g.add_node(sr_link)
            g.add_node(ds_link)
            g.add_edge(sr_link, ds_link)
    nx.draw_networkx(g, node_color='g', with_labels=True, node_size=400, font_size=10)
    plt.ylabel('Path Preview')
    plt.title('Path graph based on "path" dictionary in JSON file')
    plt.show()


# Connection check
def co_check():
    status.config(text="Connection check Preview")
    g = nx.DiGraph()
    for co in customtopology.data['Con-check']:
        for check in co:
            src_node = check
            des_node = co[check]

            src_node_name = src_node
            des_node_name = des_node

            # create graph from the JSON file to show Co_Check
            g.add_node(src_node_name)
            g.add_node(des_node_name)
            g.add_edge(src_node_name, des_node_name)
    nx.draw_networkx(g, node_color='y',  with_labels=True, node_size=400, font_size=10)
    plt.ylabel('Connection check')
    plt.title('Co check graph based on connection dictionary in JSON file')
    plt.show()


# Plot preview
def plot_preview():
    status.config(text="Plot Preview form Links dictionary in JSON file")
    g = nx.Graph()
    for link in customtopology.data['Links']:
        for x in link:
            source_node = x
            destination_node = link[x]

            source_node_name = source_node.split('-')[0]
            destination_node_name = destination_node.split('-')[0]

            # create graph from JSON file made for the project
            g.add_node(source_node_name)
            g.add_node(destination_node_name)
            g.add_edge(source_node_name, destination_node_name)

    pos = nx.spring_layout(g)
    nx.draw_networkx(g, pos, node_color='orange', with_labels=True, node_size=400, font_size=10)
    plt.ylabel('Topology')
    plt.title('Topology graph based on "Links" dictionary in JSON file')
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
PathBtn = Button(toolbar, text="Path preview as a plot", bg='lightblue', command=path_preview)
Co_checkBtn = Button(toolbar, text="Connection check preview as a plot", bg='lightblue', command=co_check)
DeployBtn = Button(toolbar, text="Deploy topology to mininet from the JSON file", bg='DeepSkyBlue2', command=customtopology.testtopology)
ModifyJsonBtn = Button(toolbar, text="Preview the JSON File", bg='lightblue',  command=json)
PdfReportBtn = Button(toolbar, text="Generate a report",  bg='lightblue', command=report)
DirectoryBtn = Button(toolbar, text="Show the report",  bg='lightblue', command=directory)
ClearCanvasBtn = Button(toolbar, text="Clear canvas",  bg='lightblue', command=clear_canvas)

PlotBtn.pack(side=LEFT, padx=1, pady=1)
PathBtn.pack(side=LEFT, padx=1, pady=1)
Co_checkBtn.pack(side=LEFT, padx=1, pady=1)
DeployBtn.pack(side=LEFT, padx=1, pady=1)
ModifyJsonBtn.pack(side=LEFT, padx=1, pady=1)
PdfReportBtn.pack(side=LEFT, padx=1, pady=1)
DirectoryBtn.pack(side=LEFT, padx=1, pady=1)
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
