import customtkinter

# frame used for displaying days and hours
class DayFrame(customtkinter.CTkFrame):
    def __init__(self, master, startDate: int, endDate: int):
        super().__init__(master)
        self.startDate = startDate
        self.endDate = endDate
        self.columnconfigure(0, weight=1)

        # to store objects
        self.tabStartHour: list[customtkinter.CTkEntry] = []
        self.tabEndHour: list[customtkinter.CTkEntry] = []
        self.tabTotalHour: list[customtkinter.CTkLabel] = []


    # update look of frame when user changes month or year
    def updateFrame(self, month):
        # clearing lists
        self.tabEndHour = []
        self.tabStartHour = []
        self.tabTotalHour = []

         # clearing frame
        for widget in self.winfo_children():
            widget.destroy()

        self.data = customtkinter.CTkLabel(self, text='Data', font=customtkinter.CTkFont(size=15))
        self.data.grid(row=0, column=0, pady=20, padx=10)
        self.starting = customtkinter.CTkLabel(self, text='Godzina rozpoczęcia', font=customtkinter.CTkFont(size=15))
        self.starting.grid(row=0, column=1, pady=20, padx=10)

        self.ending = customtkinter.CTkLabel(self, text='Godzina zakończenia', font=customtkinter.CTkFont(size=15))
        self.ending.grid(row=0, column=2, pady=20, padx=10)

        self.totalHours = customtkinter.CTkLabel(self, text='Suma godzin', font=customtkinter.CTkFont(size=15))
        self.totalHours.grid(row=0, column=3, pady=20, padx=10)


        for i in range(self.startDate, self.endDate+1):
            self.label = customtkinter.CTkLabel(self, text=f'{i} {month}')
            self.label.grid(row=i, column=0, padx=10, pady=5)

            self.startHour = customtkinter.CTkEntry(self, placeholder_text='Godzina rozpoczęcia')
            self.startHour.grid(row=i, column=1, padx=10, pady=5)
            self.tabStartHour.append(self.startHour)

            self.endHour = customtkinter.CTkEntry(self, placeholder_text='Godzina zakończenia')
            self.endHour.grid(row=i, column=2, padx=10, pady=5)
            self.tabEndHour.append(self.endHour)

            self.totalHour = customtkinter.CTkLabel(self, text='0:00')
            self.totalHour.grid(row=i, column=3, padx=10, pady=5)
            self.tabTotalHour.append(self.totalHour)

