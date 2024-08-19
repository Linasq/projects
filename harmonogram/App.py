from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import customtkinter
from DayFrame import DayFrame
from MainFrame import MainFrame
import threading as t
                  
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # startup parameters
        self.height = self.winfo_screenheight()
        self.width = self.winfo_screenwidth()
        self.title('Harmonogramy')
        self.geometry(f'{self.width}x{self.height}')
        self.month=''
        self.year=''
        self.darkmode = True

        self.grid_columnconfigure((0,1,2,3), weight=1)

        # frame with name, surname, month and year
        self.mainFrame = MainFrame(self)
        self.mainFrame.grid(row=0, column=0, padx=15, pady=20, sticky='ew', columnspan=2)

        # toggle theme button
        self.buttonTheme = customtkinter.CTkButton(self, text='Motyw', command=self.changeTheme, font=customtkinter.CTkFont(size=15))
        self.buttonTheme.grid(row=0, column=2, pady=20, padx=10)

        # frame with days, etc
        self.dayFrame = DayFrame(self, 1, 15)
        self.dayFrame.grid(row=1, column=0, padx=15, pady=20, sticky='ewns', columnspan=2)

        self.dayFrame1 = DayFrame(self, 16, self.lastDay())
        self.dayFrame1.grid(row=1, column=2, pady=20, padx=15, sticky='ewns', columnspan=2)

        # total hours labels
        self.sumTotalHoursText = customtkinter.CTkLabel(self, text='Łączna liczba przepracowanych godzin: ', font=customtkinter.CTkFont(size=17))
        self.sumTotalHoursText.grid(row=2, column=0, padx=15, pady=10, sticky='ew', columnspan=2)

        self.sumTotalHours = customtkinter.CTkLabel(self, text='0:00', font=customtkinter.CTkFont(size=17))
        self.sumTotalHours.grid(row=2, column=2, padx=15, pady=10, sticky='ew', columnspan=2)

        # when pressed we save file as pdf
        self.button = customtkinter.CTkButton(self, text='Zapisz', command=self.button_callback, font=customtkinter.CTkFont(size=15))
        self.button.grid(row=0, column=3, padx=20, pady=20, sticky='ew', columnspan=4)

        self.check_update()


    def check_update(self):
        year = self.mainFrame.getYear()
        month = self.mainFrame.getMonth() 

        if self.month != month or (self.year != year and month == 'Luty'):
            self.month = month
            self.year = year

            self.dayFrame.updateFrame(self.month)
            self.dayFrame1.endDate = self.lastDay()
            self.dayFrame1.updateFrame(self.month)
            self.sumTotalHours.configure(text='0:00')

        else:
            # threads boosts perf by 0.0001s
            t1 = t.Thread(target=self.updateTotalHour, args=(self.dayFrame,)) 
            t2 = t.Thread(target=self.updateTotalHour, args=(self.dayFrame1,))

            t1.run()
            t2.run()

            # self.updateTotalHour(self.dayFrame)
            # self.updateTotalHour(self.dayFrame1)
            self.updateSumHours()

        # updating function, 60fps
        self.after(16, self.check_update)

    
    # updating hours of each day
    def updateTotalHour(self, frame: DayFrame):
        for i, totalHour in enumerate(frame.tabTotalHour):
            startHour = frame.tabStartHour[i]
            endHour = frame.tabEndHour[i]
            try:
                if ':' in startHour.get() and ':' in endHour.get():
                    # get hours and minutes from user input
                    sH, sM = startHour.get().split(':')
                    eH, eM = endHour.get().split(':')

                    try:
                        sH, sM, eH, eM = int(sH), int(sM), int(eH), int(eM)
                        # kind of validation
                        if 0 <= sM < 60 and 0 <= eM < 60 and 0 <= sH < 24 and 0 <= eH < 24:
                            # arithmetics on hours and minutes 
                            if eM < sM: 
                                eH -= 1
                                eM += 60
                            m = str(eM-sM) if len(str(eM-sM)) == 2 else f'0{eM-sM}'
                            totalSum = f'{eH-sH}:{m}'
                            totalHour.configure(text=totalSum)
                    except ValueError:
                        pass
            except:
                pass


    # additional function to sum up how many hours person was warking per month
    def hoursMinutes(self, frame: DayFrame):
        sumHour = 0
        sumMinute = 0
        for i in frame.tabTotalHour:

            text = i.cget('text')

            if ':' in text:
                h,m = text.split(':')
                sumHour += int(h)
                sumMinute += int(m)

        return sumHour, sumMinute



    # sum up hours
    def updateSumHours(self):
        sumHour = 0
        sumMinute = 0

        frames = [self.dayFrame, self.dayFrame1]
        
        for i in frames:
            h,m = self.hoursMinutes(i)
            sumHour += h
            sumMinute += m
        
        sumHour += sumMinute // 60
        sumMinute = sumMinute % 60
        sumMinute = str(sumMinute) if len(str(sumMinute)) == 2 else f'0{sumMinute}'

        self.sumTotalHours.configure(text=f'{sumHour}:{sumMinute}')


    # creating pdf file and saving it where user specifies
    def button_callback(self):
        name = self.mainFrame.entryName.get()

        if name:
            f = customtkinter.filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=(('PDF document', '.pdf'), ('All files', '*.*')))

            # if dialog closed
            if f is None: return

            # creating pdf document

            # uncomment this line if you want to create exe file with auto-py-to-exe
            # pdfmetrics.registerFont(TTFont('JetBrains Mono', '_internal/JetBrainsMonoNerdFontMono-Regular.ttf'))
            pdfmetrics.registerFont(TTFont('JetBrains Mono', 'JetBrainsMonoNerdFontMono-Regular.ttf'))
            canvas = Canvas(filename=f, pagesize=A4)
            canvas.setFont(psfontname='JetBrains Mono', size=11)
            
            # header
            canvas.drawString(2 * cm,27.9 * cm,'PRACODAWCA:')
            canvas.drawString(2 * cm, 26.5 * cm, '.'*20)
            canvas.drawRightString(19 * cm, 28 * cm, f'ROK:  {self.year}')
            canvas.drawRightString(19 * cm, 26.5 * cm, f'MIESIĄC:  {self.month}')

            canvas.setFontSize(size=13)
            canvas.drawCentredString(10.5 * cm, 28.2 * cm, 'Harmonogram')
            canvas.drawCentredString(10.5 * cm, 27.2 * cm, 'Ewidencja czasu pracy')

            #name and surname
            canvas.drawString(1.2 * cm, 24.6 * cm, 'Imię i Nazwisko')
            canvas.setFontSize(size=18)
            canvas.drawString(7 * cm, 24.55 * cm, f'{name}')

            x1 = [1, 1, 5.5, 1, 20, 1, 2.3, 4.6, 7.5, 9.8, 12.7, 15.1, 17.2, 18.5, 20, 1, 1, 2.3, 7.5, 12.7, 15.1, 17.2]
            y1 = [25.3, 24.2, 25.3, 25.3, 25.3, 23.8, 23.8, 23.8, 23.8, 23.8, 23.8, 23.5, 23, 22.2, 23.8, 23.8, 21.8, 23.5, 23.5, 23.5, 23, 22.2]
            x2 = [20, 20, 5.5, 1, 20, 1, 2.3, 4.6, 7.5, 9.8, 12.7, 15.1, 17.2, 18.5, 20, 20, 20, 4.6, 9.8, 20, 20, 20]
            y2 = [25.3, 24.2, 24.2, 24.2, 24.2, 21.2, 21.2, 21.2, 21.2, 21.2, 21.2, 21.2, 21.2, 21.2, 21.2, 23.8, 21.8, 23.5, 23.5, 23.5, 23, 22.2]
            for i in range(len(x1)):
                canvas.line(x1[i] * cm,y1[i] * cm,x2[i] * cm,y2[i] * cm)

            #description
            canvas.setFontSize(size=6)
            x =  [1.65, 3.5, 3.45, 3.45, 8.6, 8.65, 8.6, 16.3, 14, 14, 17.5, 16.2, 18.62, 18.6, 17.8, 19.2]
            y =  [22.6, 23.55, 22.7, 22.5, 23.55, 22.7, 22.5, 23.55, 22.7, 22.5, 23.2, 22.4, 22.6, 22.4, 21.9, 21.9]
            text = ['LP', '1', 'godz. rozpoczęcia', 'pracy', '2', 'godz. zakończenia', 'pracy', '3', 'liczba godz.', 'przepracowanych', 'w tym:', 'w porze nocnej', 'w godzinach', 'nadliczbowych', '50,00%', '100,00%']
            for i in range(len(text)):
                canvas.drawCentredString(x[i] * cm, y[i] * cm, text[i])

            canvas.setFontSize(size=7)
            canvas.drawCentredString(6 * cm, 22.55 * cm, 'PODPIS PRACOWNIKA')
            canvas.drawCentredString(11.3 * cm, 22.55 * cm, 'PODPIS PRACOWNIKA')

            # dayframes
            tabStart = self.dayFrame.tabStartHour + self.dayFrame1.tabStartHour
            tabEnd = self.dayFrame.tabEndHour + self.dayFrame1.tabEndHour
            tabTotal = self.dayFrame.tabTotalHour + self.dayFrame1.tabTotalHour

            yTemp = 0
            yyyTemp = 0
            for i in range(len(tabTotal)):
                yTemp = 21.5 * cm - 0.6 * cm * i     # used for strings
                yyTemp = 21.2 * cm - i * 0.6 * cm    # used for lines above
                yyyTemp = yyTemp - 0.6 * cm          # and below
                canvas.line(1 * cm, yyTemp, 20 * cm, 21.2 * cm - i * 0.6 * cm)
                canvas.line(1 * cm, yyTemp, 1 * cm, yyyTemp)

                for x in [2.3, 4.6, 7.5, 9.8, 12.7, 15.1, 17.2, 18.5, 20]:
                    canvas.line(x * cm, yyTemp, x * cm, yyyTemp)

                canvas.drawCentredString(1.7 * cm, yTemp, f'{i+1}')
                canvas.drawCentredString(3.5 * cm, yTemp, f'{tabStart[i].get()}')
                canvas.drawCentredString(8.6 * cm, yTemp, f'{tabEnd[i].get()}')
                canvas.drawCentredString(14 * cm,yTemp,f'{"" if tabTotal[i].cget("text")=="0:00" else tabTotal[i].cget("text")}')

            yTemp -= 0.6 * cm
            canvas.drawCentredString(1.7 * cm, yTemp, 'RAZEM') 
            canvas.drawCentredString(14 * cm, yTemp, f'{self.sumTotalHours.cget("text")}') 
            canvas.line(1 * cm, yyyTemp, 20 * cm, yyyTemp)

            canvas.save()


    # toggle theme
    def changeTheme(self):
        # check if theme is light or dark
        theme = 'light' if self.darkmode else 'dark'
        self.darkmode = not self.darkmode

        self._set_appearance_mode(theme)
        self.dayFrame._set_appearance_mode(theme)
        self.dayFrame1._set_appearance_mode(theme)
        self.mainFrame._set_appearance_mode(theme)

        for widget in self.dayFrame.winfo_children():
            widget._set_appearance_mode(theme)

        for widget in self.dayFrame1.winfo_children():
            widget._set_appearance_mode(theme)

        for widget in self.mainFrame.winfo_children():
            widget._set_appearance_mode(theme)

        self.sumTotalHours._set_appearance_mode(theme)
        self.sumTotalHoursText._set_appearance_mode(theme)


    # last day of month
    def lastDay(self):
        month = self.mainFrame.getMonth()
        if month in ['Styczeń', 'Marzec', 'Maj', 'Lipiec', 'Sierpień', 'Październik', 'Grudzień']:
            return 31
        elif month == 'Luty' and self.mainFrame.isLeapYear():
            return 29
        elif month == 'Luty':
            return 28
        else: 
            return 30
