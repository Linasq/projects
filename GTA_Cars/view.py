from tkinter import *
from tkinter import ttk
import sqlite3

#tworzenie okna, tytul, wymiary
root=Tk()
root.title('Baza danych')
root.geometry("500x400")

#tworzenie zakladek
tab=ttk.Notebook(root)
tab1=ttk.Frame(tab)
tab2=ttk.Frame(tab)
tab3=ttk.Frame(tab)
tab.add(tab1, text="Add")
tab.add(tab2, text="Show")
tab.add(tab3, text="Query")

#tworzenie bazy danych
conn=sqlite3.connect('Cars_GTA.sqlite')
c = conn.cursor()

#tworzenie tabeli, jesli nie istnieje
c.execute("""Create table if not exists cars (
id integer primary key autoincrement not null,
marka text not null,
model text not null,
rodzaj text not null,
cena integer not null,
garaz text not null,
sklep text not null
)
""")

#wprowadzenie samochodu do bazy tab1
def submit():
    #polaczenie z baza danych
    conn = sqlite3.connect('Cars_GTA.sqlite')
    c = conn.cursor()

    #insert table
    c.execute("Insert into cars values (null, :marka, :model, :rodzaj, :cena, :garaz, :sklep)",
              {
                  'marka':marka.get(),
                  'model':model.get(),
                  'rodzaj':rodzaj.get(),
                  'cena':cena.get(),
                  'garaz':garaz.get(),
                  'sklep':sklep.get(),
              })

    conn.commit()
    conn.close()

    #clear text boxes
    marka.delete(0, END)
    model.delete(0, END)
    rodzaj.delete(0, END)
    cena.delete(0, END)
    garaz.delete(0, END)
    sklep.delete(0, END)

#wyswietlanie wszystkich samochodow tab2
def query():
    conn = sqlite3.connect('Cars_GTA.sqlite')
    c = conn.cursor()
    c.execute("select marka, model, rodzaj, cena, garaz, sklep from cars")
    records=c.fetchall()

    # create scrollbar tab2
    scr = Scrollbar(tab2)
    scr.grid(sticky=NS, column=2)

    #width
    max=0
    for record in records:
        strange=''
        strange+=str(record[0]) + " | " + str(record[1]) + " | " + str(record[2])+ " | " + str(record[3])+ " | " + str(record[4])+ " | " + str(record[5])
        if len(strange)>max:
            max=len(strange)

    myListBox=Listbox(tab2, width=max, height=20)
    for record in records:
        myListBox.insert(END,str(record[0]) + " | " + str(record[1]) + " | " + str(record[2])+ " | " + str(record[3])+ " | " + str(record[4])+ " | " + str(record[5])+ "\n")
        myListBox.insert(END, '-'*len(str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + "\n"))
    myListBox.grid(row=1, columnspan=2, rowspan=10)
    scr.config(command=myListBox.yview)

    conn.commit()
    conn.close()

#wyswietlanie customowych danych
def custom():
    conn = sqlite3.connect('Cars_GTA.sqlite')
    c = conn.cursor()
    c.execute(input3.get())
    records=c.fetchall()
    length = len(records[0])

    input3.delete(0, END)

    #by try zadzialal to sobie tak zapisze
    global scr, myListBox

    # czyszczenie listboxa (kontrowersyjne, ale dziala)
    try:
        myListBox.destroy()
        scr.destroy()
    except Exception:
        pass

    # width
    maxw = 0
    for record in records:
        strange = ''
        for i in range(length):
            strange += str(record[i]) + " | "
        if len(strange) > maxw:
            maxw = len(strange)

    #height
    minh=20
    if len(records) < minh:
        minh=len(records)
    else:
        # create scrollbar tab2
        scr = Scrollbar(tab3)
        scr.grid(sticky=NS, column=2)

    #create listbox and add items to it
    myListBox = Listbox(tab3, width=maxw, height=minh)
    for record in records:
        print_r = ''
        for i in range(length):
            print_r+= str(record[i]) + " | "
        print_r+="\n"
        myListBox.insert(END,print_r)
        myListBox.insert(END, "-"*len(print_r))
    myListBox.grid(row=2, columnspan=2, rowspan=10)
    if minh==20:
        scr.config(command=myListBox.yview)
    conn.commit()
    conn.close()

# ustawienie inputow w tab1
marka=Entry(tab1, width=30)
marka.grid(row=0, column=1, padx=20)
model=Entry(tab1, width=30)
model.grid(row=1, column=1, padx=20)
rodzaj=Entry(tab1, width=30)
rodzaj.grid(row=2, column=1, padx=20)
cena=Entry(tab1, width=30)
cena.grid(row=3, column=1, padx=20)
garaz=Entry(tab1, width=30)
garaz.grid(row=4, column=1, padx=20)
sklep=Entry(tab1, width=30)
sklep.grid(row=5, column=1, padx=20)

# zwykly string tab1
tmarka=Label(tab1, text="Marka: ")
tmarka.grid(row=0, column=0)
tmodel=Label(tab1, text="Model: ")
tmodel.grid(row=1, column=0)
trodzaj=Label(tab1, text="Rodzaj: ")
trodzaj.grid(row=2, column=0)
tcena=Label(tab1, text="Cena: ")
tcena.grid(row=3, column=0)
tgaraz=Label(tab1, text="Garaż: ")
tgaraz.grid(row=4, column=0)
tsklep=Label(tab1, text="Sklep: ")
tsklep.grid(row=5, column=0)

#create submit button tab1
submit_btn = Button(tab1, text="Add record", command=submit)
submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#create query btn tab2
query_btn = Button(tab2, text="Show cars", command=query)
query_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#create input and btn for custom query tab3
text3 = Label(tab3, text="Your query (SQL)")
text3.grid(row=0, column=0)

input3 = Entry(tab3, width=30)
input3.grid(row=0, column=1, padx=20)

ur_btn=Button(tab3, text="Submit", command=custom)
ur_btn.grid(row=1, columnspan=2, pady=10, padx=10, ipadx=100)

conn.commit()
conn.close()
tab.pack(expand=1, fill="both")
root.mainloop()