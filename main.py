from Tkinter import *
import tkMessageBox
from ttk import Combobox
from PIL import Image, ImageDraw
from OCR import odczyt_img, tworzenie_sieci, uczenie_sieci, zapsi_model, wczytaj_model, test_mnist

import time

class oknoGUI(object):
    def __init__(self):
        self.oknoGlowne = Tk()
	self.okno = None
        self.okno_szer = 250
        self.okno_wys = 250
        self.siec=tworzenie_sieci();
        self.img = None
        self.rysowanie = None
        self.inicjacja()

    def inicjacja(self):
        self.oknoGlowne.title( "OCR CYFR" )
	self.oknoGlowne.geometry('252x500')
        self.okno = Canvas(self.oknoGlowne, width=self.okno_szer, height=self.okno_wys, bg='black')
	self.okno.place(x=0, y=0)
        self.okno.bind( "<B1-Motion>", self.maluj )

        self.img = Image.new('RGB', (self.okno_szer, self.okno_wys), 'black')
        self.rysowanie = ImageDraw.Draw(self.img)

	label3=Label(self.oknoGlowne,text="wynik ",fg="black")
	label3.place(x=10, y=251)
	
	self.wynik=Entry(self.oknoGlowne)
	self.wynik.place(x=75, y=251)

        self.odczytButton = Button(self.oknoGlowne, text='Odczytaj', command=self.odczytaj, anchor = SW)
        self.odczytButton.place(x=10, y=281)

        self.wyczyscButton = Button(self.oknoGlowne, text='Wyczysc', command=self.wyczysc, anchor = NW)
        self.wyczyscButton.place(x=100, y=281)
	
	self.testButton = Button(self.oknoGlowne, text='Test', command=self.test, anchor = SW)
        self.testButton.place(x=190, y=281)
	
	label1=Label(self.oknoGlowne,text="liczba iteracji treningu",fg="black")
	label1.place(x=0, y=311)

	data=(1,2,3,4,5,6,7,8,9,10)
	self.liczba_iteracji=Combobox(self.oknoGlowne,values=data,width=5)
	self.liczba_iteracji.current(0)
	self.liczba_iteracji.place(x=150, y=311)	

        self.uczenieButton= Button(self.oknoGlowne, text='uczenie', command=self.ucz, anchor = S)
	self.uczenieButton.place(x=100, y=331)
 	
	label3=Label(self.oknoGlowne,text="nazwa pliku",fg="black")
	label3.place(x=1, y=371)

	self.nazwa_pliku_1=Entry(self.oknoGlowne,width=15)
	self.nazwa_pliku_1.insert(END,'siec.h5')
	self.nazwa_pliku_1.place(x=100, y=371)

	self.ladujButton= Button(self.oknoGlowne, text='ladowanie', command=self.laduj, anchor = S)
	self.ladujButton.place(x=100, y=391)
	
	label2=Label(self.oknoGlowne,text="nazwa pliku",fg="black")
	label2.place(x=1, y=431)
	
	self.nazwa_pliku=Entry(self.oknoGlowne,text='siec.h5',width=15)
	self.nazwa_pliku.insert(END,'siec.h5')
	self.nazwa_pliku.place(x=100, y=431)

	self.zapiszButton = Button(self.oknoGlowne, text='zapisz', command=self.zapisz, anchor = S)
	self.zapiszButton.place(x=100, y=451)	
		
        mainloop()
        self.img.close()

        img = Image.open('img/temp.jpg')
        img = img.resize((28,28))
        img.save('img/temp.jpg')
        img.close()

    def wyczysc(self):
        self.okno.delete("all")
        self.img = Image.new('RGB', (self.okno_szer, self.okno_wys), 'black')
        self.rysowanie = ImageDraw.Draw(self.img)
	self.wynik.delete(0,END)

    def odczytaj(self):
        plik="img/temp.jpg"
        self.img.save(plik)
	wynik_img=odczyt_img(plik,self.siec)
	print('\nwynik: ')
	print(wynik_img)
	self.wynik.insert(END,wynik_img)
	
 	self.okno.delete("all")
	self.img = Image.new('RGB', (self.okno_szer, self.okno_wys), 'black')
        self.rysowanie = ImageDraw.Draw(self.img)

    def ucz(self):
	self.odczytButton.config(state="disable")
	self.wyczyscButton.config(state="disable")
	self.uczenieButton.config(state="disable")
	self.zapiszButton.config(state="disable")
	self.ladujButton.config(state="disable")
	self.testButton.config(state="disable")
	self.okno.config(state="disable")
	self.oknoGlowne.update()

	iteracja=int(self.liczba_iteracji.get())

	if iteracja > 0 and iteracja < 11:
       		try:
			self.siec=uczenie_sieci(self.siec,iteracja)
			tkMessageBox.showinfo('sykces', 'Uczenie Zakonczone!')
		except:
			tkMessageBox.showerror('Error', 'nieznany blad uczenia sie!')
		
	else:
		tkMessageBox.showerror('Error', 'bledna liczba iteracji!')

        self.okno.config(state="normal")
        self.odczytButton.config(state="normal")
	self.wyczyscButton.config(state="normal")
	self.uczenieButton.config(state="normal")
	self.zapiszButton.config(state="normal")
	self.ladujButton.config(state="normal")
	self.testButton.config(state="normal")
	self.oknoGlowne.update()
  
    def zapisz(self):
	nazwa=self.nazwa_pliku.get()

	if len(nazwa) != 0 :
		zapsi_model(self.siec, nazwa)
		tkMessageBox.showinfo("sykces", "Zapisano pomyslnie!")
	else:
		tkMessageBox.showerror('Error', 'brak nazwy pliku!')

	
    def laduj(self):
	self.odczytButton.config(state="disable")
	self.wyczyscButton.config(state="disable")
	self.uczenieButton.config(state="disable")
	self.zapiszButton.config(state="disable")
	self.ladujButton.config(state="disable")
	self.testButton.config(state="disable")
	self.okno.config(state="disable")
	self.oknoGlowne.update()
		
	nazwa=self.nazwa_pliku_1.get()

	if len(nazwa)!=0:
        	self.siec=wczytaj_model(nazwa)
		tkMessageBox.showinfo('sykces', 'Zaladowano pomylnie!')
	else:
		tkMessageBox.showerror('Error', 'brak nazwy pliku!')

	self.okno.config(state="normal")
        self.odczytButton.config(state="normal")
	self.wyczyscButton.config(state="normal")
	self.uczenieButton.config(state="normal")
	self.zapiszButton.config(state="normal")
	self.ladujButton.config(state="normal")
	self.testButton.config(state="normal")
	self.oknoGlowne.update()
	
    def test(self):
	self.odczytButton.config(state="disable")
	self.wyczyscButton.config(state="disable")
	self.uczenieButton.config(state="disable")
	self.zapiszButton.config(state="disable")
	self.ladujButton.config(state="disable")
	self.testButton.config(state="disable")
	self.okno.config(state="disable")
	self.oknoGlowne.update()

	self.wynik.delete(0,END)
	self.wynik.insert(END,test_mnist(self.siec)) 
	
	self.okno.config(state="normal")
        self.odczytButton.config(state="normal")
	self.wyczyscButton.config(state="normal")
	self.uczenieButton.config(state="normal")
	self.zapiszButton.config(state="normal")
	self.ladujButton.config(state="normal")
	self.testButton.config(state="normal")
	self.oknoGlowne.update()

    def maluj(self, clik):
        x1, y1 = clik.x, clik.y
        x2, y2 = ( clik.x + 10), ( clik.y + 10 )
        self.okno.create_oval( x1, y1, x2, y2, fill = "#FFFFFF", width=0 )
        self.rysowanie.ellipse([x1,y1,x2,y2], fill='white')

    

oknoGUI()

