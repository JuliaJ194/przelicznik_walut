
import requests
import xmltodict
from tkinter import *
import tkinter.ttk as ttk

respond = requests.get("https://www.nbp.pl/kursy/xml/LastA.xml") #pobieramy dane z NBP

if respond.status_code != 200:    #w przypadku błędu przy pobieraniu ze strony
    f = open('kursy_walut.txt', 'r') #pobieramy dane z zapisanego wcześniej pliku tekstowego
    r = f.read()
    f.close()
    kursy_słownik = xmltodict.parse(r) #tworzymy słownik

else: 
    kursy_xml = respond.content   
    with open('kursy_walut.txt', 'wb') as f: #tworzymy nowy plik z nowymi danymi
        f.write(kursy_xml)
        f.close()
    kursy_słownik = xmltodict.parse(kursy_xml) #zamieniamy na słownik    

lista = dict(dict(kursy_słownik)['tabela_kursow'])['pozycja'] #pomijamy wcześniejsze dane i jako listę definiujemy wszystkie słowniki gdzie mamy zapisaną nazwę waluty, kod, przelicznik i kurs średni

słowniki = [{'nazwa_waluty': 'złoty', #dodajemy PLN żeby później było łatwiej
              'przelicznik': '1',
              'kod_waluty': 'PLN',
              'kurs_sredni': '1,0000'}]
for i in range(len(lista)): 
    słowniki.append(dict(lista[i])) #zamieniamy OrderedDict na zwykły dict i tworzymy listę słowników

przeliczniki = []
for i in range(len(słowniki)):
    przeliczniki.append(słowniki[i]['przelicznik'])

kody = []
for i in range(len(słowniki)):
    kody.append(słowniki[i]['kod_waluty'])

kursy = []
for i in range(len(słowniki)):
    kursy.append(słowniki[i]['kurs_sredni'].replace(",", ".")) #zmieniamy przecinek na kropkę, żeby później zamienić stringa na floata



def wymiana_waluty():    
    """
    Program przeliczający kursy walut.
    """  
    try:
        
        kwota = float(entry.get()) #kwotę wpisujemy ręcznie
        kod1 = combobox1.get() #kody walut wybieramy z listy rozwijanej
        kod2 = combobox2.get()

        if kod1 == kod2:
            label4.config(text = kwota) #jeśli wybierzemy tą samą walutę

        else:
            for i in range(len(kody)):
                if kody[i] == kod1:
                    indeks1 = i       #pętlą wyszukujemy jaki indeks w listach mają wybrane przez nas waluty    
            kurs1 = float(kursy[indeks1]) #wyszukujemy jaki jest kurs średni i przelicznik waluty
            przelicznik1 = float(przeliczniki[indeks1])

            for n in range(len(kody)):
                if kody[n] == kod2:
                    indeks2 = n           
            kurs2 = float(kursy[indeks2])
            przelicznik2 = float(przeliczniki[indeks2])

            pln = (kwota * kurs1) / przelicznik1    #najpierw przeliczamy na pln
            wynik1 = (przelicznik2 * pln) / kurs2   #następnie z pln na docelową walutę
            wynik2 = round(wynik1, 2)
            label4.config(text = wynik2)
            
    except:
        label4.config(text = "Podana kwota nie jest liczbą!!!")
            

def zamknij():
    """Funkcja zamykająca okno."""
    okno.quit()
    okno.destroy()

okno = Tk()
okno.geometry('500x300')
topFrame = Frame(okno)
topFrame.pack()
bottomFrame = Frame(okno)
bottomFrame.pack(side=BOTTOM)
tytuł = "Program przeliczający kursy walut"
okno.title(tytuł)

przycisk1 = Button(okno, text = "OBLICZ", font = ("Calibri", 14),
                   fg = "green", bg = "white", command = wymiana_waluty) #definiujemy przycisk przeliczający kursy wybranych walut
przycisk1.pack(side=BOTTOM, expand=YES)
przycisk1.place(x=320, y=200)

przycisk2 = Button(bottomFrame, text = "ZAMKNIJ", font = ("Calibri", 10),
                   fg = "white", bg = "red", command = zamknij) #definiujemy przycisk zamykający okno 
przycisk2.pack(side=BOTTOM, expand=YES) 

label1 = Label(okno, text = "Wpisz kwotę, którą chcesz wymienić.", font = ("Calibri", 10))
label1.pack()
label1.place(x=10, y=30)

entry = Entry(okno) #do wpisywania kwoty
entry.pack()
entry.place(x=50, y=70)

label2 = Label(okno, text = "Wybierz walutę, którą chcesz wymienić.", font = ("Calibri", 10))
label2.pack()
label2.place(x=240, y=30)

combobox1 = ttk.Combobox(okno)
combobox1['values'] = kody
combobox1.current(0)
combobox1.pack()
combobox1.place(x=280, y=70)

label3 = Label(okno, text = "Wybierz walutę, na którą chcesz wymienić.", font = ("Calibri", 10))
label3.pack()
label3.place(x=240, y=110)

combobox2 = ttk.Combobox(okno)
combobox2['values'] = kody
combobox2.current(0)
combobox2.pack()
combobox2.place(x=280, y=150)

label4 = Label(okno, text = " ", font = ("Calibri", 14))
label4.pack()
label4.place(x=80, y=180)

label5 = Label(okno, text = "Wynik", font = ("Calibri", 14))
label5.pack()
label5.place(x=80, y=140)

okno.mainloop()
