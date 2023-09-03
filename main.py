#import library
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors

#import CSV file
df = pd.read_csv("./birthdead.csv")

#making GUI window and window setting
root = Tk()
root.geometry("1200x1000")
root.title("Birth and Death in BKK")

#import png file
startpic = (PhotoImage(file = r"./image/start_icon.png")).subsample(12,12)
endpic = (PhotoImage(file = r"./image/end_icon.png")).subsample(12,12)
arrowpic = (PhotoImage(file = r"./image/arrow.png")).subsample(12,12)
bkk = (PhotoImage(file = r"./image/bkkpic.png")).subsample(1,1)
addpic = (PhotoImage(file = r"./image/add.png")).subsample(24,24)
clearpic = (PhotoImage(file = r"./image/clear.png")).subsample(95,95)
setpic = (PhotoImage(file = r"./image/setting.png")).subsample(20,20)
howto = (PhotoImage(file = r"./image/howto.png")).subsample(1,1)
barpic = (PhotoImage(file = r"./image/bar.png")).subsample(12,12)
piepic = (PhotoImage(file = r"./image/pie.png")).subsample(12,12)
bpic = (PhotoImage(file = r"./image/birth_icon.png")).subsample(6,6)
dpic = (PhotoImage(file = r"./image/death_icon.png")).subsample(6,6)
bdpic = (PhotoImage(file = r"./image/compare.png")).subsample(6,6)

#background image
Label(root,image=bkk,bg="white" ).place(relx=0.5, rely=0.9, anchor=CENTER)

#making combobox for select first year
Label(root,image=startpic,bg="white" ).place(relx=0.5, rely=0.17, anchor=CENTER)
start_value = IntVar()
start_value.set(52)
startt = ttk.Combobox(root,textvariable = start_value,width=2)
startt["value"] = [i for i in range(52,62)]
startt.place(relx=0.52, rely=0.17, anchor= W)

#making combobox for select end year
Label(root,image=endpic,bg="white").place(relx=0.617, rely=0.17, anchor=CENTER)
end_value = IntVar()
end_value.set(52)
endd = ttk.Combobox(textvariable = end_value,width=2)
endd["value"] = [x for x in range(52,62)]
endd.place(relx=0.56, rely=0.17, anchor=W)

# HOE TO USE image section
def setting():
    how = Toplevel(root)
    how.geometry("1200x1000")
    how.title("How to use")
    how['bg'] = 'white'
    Label(how,image=howto,bg="black" ).place(relx=0.5, rely=0.5, anchor=CENTER)

how_to = Button(root,image=setpic,bg = "white",command=setting).place(relx = 0.1,rely=0.2,anchor=CENTER)


#for select specific year
data = IntVar()
en1 = Entry(width=2,textvariable=data,font=30)
en1.place(relx=0.517, rely=0.22, anchor=W)

graph_list = []
def add_graph():
    year_add = data.get()
    if year_add in range(52,62) and year_add not in graph_list:
        graph_list.append(year_add)
    en1.delete(0,END)
    show_list()

def clear_graph():
    print(graph_list)
    graph_list.clear()
    en1.delete(0,END)
    show_list()

def show_list():
    Label(root,text=graph_list,bg="pink",font= 30).place(relx=0.56,rely=0.27,anchor=CENTER)

btn = Button(root,image=addpic,command=add_graph).place(relx=0.547, rely=0.22, anchor=W)
btn1 = Button(root,image=clearpic,command=clear_graph).place(relx=0.577, rely=0.22, anchor=W)

#graph selection
choice_bar = StringVar()
Checkbutton(root,image=barpic,variable=choice_bar,bg="white").place(relx=0.7, rely=0.2, anchor=W)
choice_pie = StringVar()
Checkbutton(root,image=piepic,variable=choice_pie,bg="white").place(relx=0.8, rely=0.2, anchor=W)

def clear():
    canvas = Canvas(root, width = 850, height = 500,bg="white",bd=0)
    canvas.place(relx=0.16,rely=0.3,anchor=NW)
    canvas.create_rectangle(0, 0, 0,0)


def birth_selected():
    S,E = start_value.get(),end_value.get()
    choice1,choice2 = choice_bar.get(),choice_pie.get()
    clear()
    if(graph_list != []):
        graph_list.sort()
        year = graph_list
        birth = [df.iloc[:,x-51].sum() for x in year]
        year_np = np.arange(len(year))
    else:
        year = [x for x in range(S,E+1)]
        birth = [df.iloc[:,x-51].sum() for x in range(S,E+1)]
        year_np = np.arange(len(year))

    colors = [x[4:] for x in mcolors.TABLEAU_COLORS]

    bx,by = 0.5,0.65
    px,py = 0.52,0.61
    if choice1 == '1' and choice2 != '1':
        fig = plt.figure(figsize=(5, 5), dpi=90)
        plt.bar(year_np,birth,align='center', alpha=1.0,color = colors)
        plt.xticks(year_np, year)
        plt.ylabel('Volume')
        plt.xlabel('Year')
        plt.tight_layout(pad=2.2, w_pad=0.5, h_pad=0.1)
        plt.title('Volumes of Birth in BKK')
        plt.xticks(rotation=30, horizontalalignment="center")
        for index, datapoints in enumerate(birth):
            plt.text(x=index, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        canvasbar = FigureCanvasTkAgg(fig, master=root)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(relx=bx, rely=by, anchor=CENTER)

    elif choice1 != '1' and choice2 == '1':
        fig = plt.figure(figsize=(5, 5), dpi=95)
        fig.set_size_inches(5, 5)
        plt.title('Volumes of Birth in BKK')
        explodep = [0 for x in range(len(year))]
        plt.pie(birth, explode=explodep, labels=year, colors=colors, autopct='%1.1f%%', shadow=True, startangle=120)
        plt.axis('equal') # creates the pie chart like a circle
        canvaspie = FigureCanvasTkAgg(fig, master=root)
        canvaspie.draw()
        canvaspie.get_tk_widget().place(relx=px, rely=py, anchor=CENTER)

    elif choice1 == '1' and choice2 == '1':
        fig = plt.figure(figsize=(4, 4), dpi=100)
        bx,by = 0.18,0.4
        plt.bar(year_np,birth,align='center', alpha=1.0,color = colors)
        plt.xticks(year_np, year)
        plt.ylabel('Volume')
        plt.xlabel('Year')
        plt.tight_layout(pad=2.2, w_pad=0.5, h_pad=0.1)
        plt.title('Volumes of Birth in BKK')
        plt.xticks(rotation=30, horizontalalignment="center")
        for index, datapoints in enumerate(birth):
            plt.text(x=index, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        canvasbar = FigureCanvasTkAgg(fig, master=root)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(relx=bx, rely=by, anchor=NW)

        fig = plt.figure(figsize=(4, 4), dpi=100)
        fig.set_size_inches(4, 4)
        px,py = 0.52,0.37
        explodep = [0 for x in range(len(year))]
        plt.pie(birth, explode=explodep, labels=year, colors=colors, autopct='%1.1f%%', shadow=True, startangle=120)
        plt.axis('equal') # creates the pie chart like a circle
        canvaspie = FigureCanvasTkAgg(fig, master=root)
        canvaspie.draw()
        canvaspie.get_tk_widget().place(relx=px, rely=py, anchor=NW)

def death_selected():
    S,E = start_value.get(),end_value.get()
    choice1,choice2 = choice_bar.get(),choice_pie.get()
    clear()
    if(graph_list != []):
        graph_list.sort()
        year = graph_list
        death = [df.iloc[:,x-41].sum() for x in year]
        year_np = np.arange(len(year))
    else:
        year = [x for x in range(S,E+1)]
        death = [df.iloc[:,x-41].sum() for x in range(S,E+1)]
        year_np = np.arange(len(year))
    
    colors = [x[4:] for x in mcolors.TABLEAU_COLORS]

    bx,by = 0.5,0.65
    px,py = 0.52,0.61
    if choice1 == '1' and choice2 != '1':
        fig = plt.figure(figsize=(5, 5), dpi=90)
        plt.bar(year_np,death,align='center', alpha=1.0,color = colors)
        plt.xticks(year_np, year)
        plt.ylabel('Volume')
        plt.xlabel('Year')
        plt.tight_layout(pad=2.2, w_pad=0.5, h_pad=0.1)
        plt.title('Volumes of Death in BKK')
        plt.xticks(rotation=30, horizontalalignment="center")
        for index, datapoints in enumerate(death):
            plt.text(x=index, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        canvasbar = FigureCanvasTkAgg(fig, master=root)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(relx=bx, rely=by, anchor=CENTER)

    elif choice1 != '1' and choice2 == '1':
        fig = plt.figure(figsize=(5, 5), dpi=95)
        fig.set_size_inches(5, 5)
        explodep = [0 for x in range(len(year))]
        plt.pie(death, explode=explodep, labels=year, colors=colors, autopct='%1.1f%%', shadow=True, startangle=120)
        plt.axis('equal') # creates the pie chart like a circle
        plt.title('Volumes of Death in BKK')
        canvaspie = FigureCanvasTkAgg(fig, master=root)
        canvaspie.draw()
        canvaspie.get_tk_widget().place(relx=px, rely=py, anchor=CENTER)

    elif choice1 == '1' and choice2 == '1':
        fig = plt.figure(figsize=(4, 4), dpi=100)
        bx,by = 0.18,0.4
        plt.bar(year_np,death,align='center', alpha=1.0,color = colors)
        plt.xticks(year_np, year)
        plt.ylabel('Volume')
        plt.xlabel('Year')
        plt.tight_layout(pad=2.2, w_pad=0.5, h_pad=0.1)
        plt.title('Volumes of Death in BKK')
        plt.xticks(rotation=30, horizontalalignment="center")
        for index, datapoints in enumerate(death):
            plt.text(x=index, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        canvasbar = FigureCanvasTkAgg(fig, master=root)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(relx=bx, rely=by, anchor=NW)

        fig = plt.figure(figsize=(4, 4), dpi=100)
        fig.set_size_inches(4, 4)
        px,py = 0.52,0.37
        explodep = [0 for x in range(len(year))]
        plt.pie(death, explode=explodep, labels=year, colors=colors, autopct='%1.1f%%', shadow=True, startangle=120)
        plt.axis('equal') # creates the pie chart like a circle
        canvaspie = FigureCanvasTkAgg(fig, master=root)
        canvaspie.draw()
        canvaspie.get_tk_widget().place(relx=px, rely=py, anchor=NW)

def compare_selected():
    S,E = start_value.get(),end_value.get()
    choice1,choice2 = choice_bar.get(),choice_pie.get()
    clear()
    if(graph_list != []):
        graph_list.sort()
        year = graph_list
        birth = [df.iloc[:,x-51].sum() for x in year]
        death = [df.iloc[:,x-41].sum() for x in year]
        year_np = np.arange(len(year))
    else:
        year = [x for x in range(S,E+1)]
        birth = [df.iloc[:,x-51].sum() for x in range(S,E+1)]
        death = [df.iloc[:,x-41].sum() for x in range(S,E+1)]
        year_np = np.arange(len(year))
    colors = [x[4:] for x in mcolors.TABLEAU_COLORS]
    if choice1 == '1' :
        bx,by = 0.5,0.65
        fig = plt.figure(figsize=(5, 5), dpi=90)
        plt.bar(year_np - 0.2, birth, 0.4, label = 'Birth',color = colors)
        plt.bar(year_np + 0.2, death, 0.4, label = 'Death')
        plt.xticks(year_np, year)
        plt.ylabel('Volume')
        plt.xlabel('Year')
        plt.tight_layout(pad=2.2, w_pad=0.5, h_pad=0.1)
        plt.title('Volumes of Birth/Death in BKK')
        plt.xticks(rotation=30, horizontalalignment="center")
        for index, datapoints in enumerate(birth):
            plt.text(x=index-0.2, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        for index, datapoints in enumerate(death):
            plt.text(x=index+0.2, y=datapoints + 0.3, s=f"{datapoints}", fontdict=dict(fontsize=10-(0.5*(E-S))), ha='center', va='bottom')
        
        ## This section draws a canvas to allow the barchart to appear in it
        canvasbar = FigureCanvasTkAgg(fig, master=root)
        canvasbar.draw()
        canvasbar.get_tk_widget().place(relx=bx, rely=by, anchor=CENTER)  # show the barchart on the ouput window




birth_button = Button(root,image=bpic,command=birth_selected).place(relx = 0.2,rely=0.2,anchor=CENTER)
death_button = Button(root,image=dpic,command=death_selected).place(relx = 0.3,rely=0.2,anchor=CENTER)
bd_button = Button(root,image=bdpic,command=compare_selected).place(relx = 0.4,rely=0.2,anchor=CENTER)


root.mainloop()