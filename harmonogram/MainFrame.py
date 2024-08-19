import customtkinter

# frame that is placed at the top
class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)

        self.entryName = customtkinter.CTkEntry(self, placeholder_text='Imię i nazwisko', height=40, width=400, font=customtkinter.CTkFont(size=15))
        self.entryName.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        self.optionMonth = customtkinter.CTkOptionMenu(self, values=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'], font=customtkinter.CTkFont(size=15))
        self.optionMonth.grid(row=0, column=1, pady=20)

        self.optionYear = customtkinter.CTkOptionMenu(self, values=[str(i) for i in range(2020, 2051)], font=customtkinter.CTkFont(size=15))
        self.optionYear.grid(row=0, column=2, padx=20, pady=20)


    def getMonth(self):
        return self.optionMonth.get()


    def getYear(self):
        return self.optionYear.get()


    def isLeapYear(self):
        try:
            year = int(self.getYear())
        except ValueError:
            exit('Could not convert str to int')

        if year % 4 != 0: return 0
        if year % 100 == 0 and year % 400 != 0: return 0

        return 1


