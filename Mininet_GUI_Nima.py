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
import customtopology
import os


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
    g = nx.DiGraph()
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
    nx.draw_networkx(g, pos, node_color='r', with_labels=True, node_size=400, font_size=10)
    plt.ylabel('Topology')
    plt.title('Topology graph based on "Links" dictionary in JSON file')
    plt.show()


def pdf():
#    tkinter.messagebox.showinfo("Generate pdf", "Results has been stored in a PDF file.")
#    status.config(text="Pdf has been generated")
    reader = open('./stdout.txt', 'r')
    rep = reader.readlines()
    return rep


def generate_pdf(lines, output="report.pdf"):
    now = datetime.datetime.today()
    date = now.strftime("%h %d %Y %H:%M:%S")
    c = canvas.Canvas(output)
    text_object = c.beginText()
#    c.setPageSize(landscape(letter))
    text_object.setTextOrigin(inch, 10*inch)
    text_object.textLines('''Result from Mininet: %s ''' % date + '\n')

    for line in lines:
        text_object.textLine(line.rstrip())
    c.drawText(text_object)
    c.showPage()
    c.save()


report = pdf()
generate_pdf(report)


def clear_canvas():
    status.config(text="Canvas has been cleared")
    textBox_mininet_deploy.delete('1.0', END)


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
toolbar = Frame(root, bg="steelblue1")

PlotBtn = Button(toolbar, text="Topology preview as a plot", bg='azure', command=plot_preview)
PathBtn = Button(toolbar, text="Path preview as a plot", bg='azure', command=path_preview)
Co_checkBtn = Button(toolbar, text="Connection check preview as a plot", bg='azure', command=co_check)
DeployBtn = Button(toolbar, text="Deploy topology to mininet from the JSON file", bg='DeepSkyBlue2', command=customtopology.testtopology)
ModifyJsonBtn = Button(toolbar, text="Preview the JSON File", bg='azure',  command=json)
PdfReportBtn = Button(toolbar, text="Generate a PDF report",  bg='azure', command=pdf)
ClearCanvasBtn = Button(toolbar, text="Clear canvas",  bg='azure', command=clear_canvas)

PlotBtn.pack(side=LEFT, padx=3, pady=3)
PathBtn.pack(side=LEFT, padx=3, pady=3)
Co_checkBtn.pack(side=LEFT, padx=3, pady=3)
DeployBtn.pack(side=LEFT, padx=3, pady=3)
ModifyJsonBtn.pack(side=LEFT, padx=3, pady=3)
PdfReportBtn.pack(side=LEFT, padx=3, pady=3)
ClearCanvasBtn.pack(side=LEFT, padx=3, pady=3)
toolbar.pack(side=TOP, fill=X)

# Textbox
textBox_mininet_deploy = Text(root, height=40, width=200, bg='lavender')
textBox_mininet_deploy.pack(side=TOP, padx=20, pady=20)
customtopology.mnOutput = textBox_mininet_deploy


# StatusBar
status = Label(root, text="Mininet Project designed and developed by Nima Eivazzadeh",
                     bd=2, bg="light blue", relief=SUNKEN, anchor=W)
status.pack(side=TOP, padx=5, pady=5)


# Mainloop
root.mainloop()
