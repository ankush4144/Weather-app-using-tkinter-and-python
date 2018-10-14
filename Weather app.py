from tkinter import *
from tkinter import messagebox
import urllib.request
import json


class weatherData():                                                            #class with all the functions

    def __init__(self):
        self.root = Tk()
        self.root.title('Weather')
        self.root.resizable(False, False)
        self.root.geometry('400x100+100+100')

        self.canvas = Canvas(self.root, bg='#3F2B2C',height=400,width=400)
        self.canvas.grid()

        self.label=Entry(self.root,width=40)
        self.label.place(x=80,y=10)

        self.dataList=[]
        self.index=0      

        
    def show(self):                                                             #function to show first window on closing second window
        self.second.destroy()
        self.root.update()
        self.root.deiconify()

        
    def secondWindow(self):                                                     #function for opening second window
        self.second = Tk()
        self.second.protocol("WM_DELETE_WINDOW", self.show)
        self.sun = PhotoImage(file="sun.png", master = self.second).subsample(5)
        self.cloudy = PhotoImage(file="cloudy.png", master = self.second).subsample(5)

        
        self.second.title('RESULTS')
        self.second.resizable(False, False)
        self.second.geometry('400x400+100+100')
        self.canvas1 = Canvas(self.second, bg='#EF9121',height=400,width=400)
        self.canvas1.grid()
        NextDay = Button(self.second, text='Next Day',command=self.nextDay,bg='#561210',fg='#EF9121')
        self.canvas1.create_window(100, 370,height=25, width=90, window=NextDay)
        PreviousDay = Button(self.second, text='Previous Day',command=self.previousDay,bg='#561210',fg='#EF9121')
        self.canvas1.create_window(300, 370,height=25, width=90, window=PreviousDay)
        self.initialData()
    

    def tempToCelsius(self,temp):                                               #function to convert temperature from kelvin to celsius
        return str(round((temp-273.15),2))



    def getData(self):                                                          #function to get data from api
        url=self.label.get()
        URL = "https://api.openweathermap.org/data/2.5/forecast?q="+url+",in&appid=5fa70590378b2cf06fca2de89f8c616f"
        try:
            response=urllib.request.urlopen(URL)
        except:
            messagebox.showinfo("ERROR","Please Enter A Valid City")
        else:
            
            data = json.loads(response.read())
            self.dataList=data['list']
            self.openingSecondWindow()


    def hide(self):                                                             #function to hide first window
        self.root.withdraw()


    def openingSecondWindow(self):                                          
        self.hide()
        self.secondWindow()
        

    def nextDay(self):                                                          #function for next day button
        try:
            if(self.index>=32):
                raise ValueError
        except ValueError:
            messagebox.showinfo("ERROR ","Data Not Available For More Than 4 Days")
        else:
            self.second.destroy()
            self.index+=8
            self.secondWindow()



    def previousDay(self):                                                      #function for previous day button
        try:
            if(self.index<=0):
                raise ValueError
        except ValueError:
            messagebox.showinfo("ERROR ","Historical Data Not Available")
        else:
            self.second.destroy()
            self.index-=8
            self.secondWindow()
        


    def mainData(self):                                                         #function to display final data
        if(self.dataList[self.index]['clouds']['all']==0):  
            self.canvas1.create_image(10,20,image=self.sun,anchor=NW)
        else:
            self.canvas1.create_image(0,0,image=self.cloudy,anchor=NW)
            
        self.canvas1.create_text(210,90,text=self.dataList[self.index]['dt_txt'].split()[0],font="Times 13 bold",fill='snow')
        self.canvas1.create_text(72,170,text=self.tempToCelsius(self.dataList[self.index]['main']['temp'])+u' \u2103',font="Times 15 bold",fill='#F6EB1F')    
        self.canvas1.create_text(340,150,text=self.tempToCelsius(self.dataList[self.index]['main']['temp_max'])+u' \u2103',font="Times 10",anchor=W,fill='#F6EB1F')
        self.canvas1.create_text(340,170,text=self.tempToCelsius(self.dataList[self.index]['main']['temp_min'])+u' \u2103',font="Times 10",anchor=W,fill='#F6EB1F')    
        self.canvas1.create_text(280,220,text=str(self.dataList[self.index]['main']['pressure'])+" hPa",font="Times 10",anchor=W,fill='#F6EB1F')
        self.canvas1.create_text(280,240,text=str(self.dataList[self.index]['main']['humidity'])+"%",font="Times 10",anchor=W,fill='#F6EB1F')
        self.canvas1.create_text(280,260,text=str(self.dataList[self.index]['wind']['speed'])+' m/s',font="Times 10",anchor=W,fill='#F6EB1F')
        self.canvas1.create_text(280,280,text=str(self.dataList[self.index]['wind']['deg'])+' degrees',font="Times 10",anchor=W,fill='#F6EB1F')
        self.canvas1.create_text(280,300,text=str(self.dataList[self.index]['clouds']['all'])+'%',font="Times 10",anchor=W,fill='#F6EB1F')
        if('rain' not in self.dataList[self.index].keys() or '3h' not in self.dataList[self.index]['rain']):
            self.canvas1.create_text(280,320,text="0 mm",font="Times 10",anchor=W,fill='#F6EB1F')
        else:
            self.canvas1.create_text(280,320,text=str(round(self.dataList[self.index]['rain']['3h'],2))+' mm',font="Times 10",anchor=W,fill='#F6EB1F')
    


            
    def initialData(self):                                                      #function to display initial headings
        self.canvas1.create_text(210,55,text=self.label.get().upper(),font="ComicSansMS 25 bold",fill='#561210')
        self.canvas1.create_text(90,150,text="TEMPERATURE:",font="ComicSansMS 15 bold",fill='#561210')
        self.canvas1.create_text(40,220,text="Pressure:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(40,240,text="Humidity:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(40,260,text="Wind Speed:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(40,280,text="Wind Direction:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(40,300,text="Cloudiness:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(40,320,text="Rain:",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(280,150,text="Maximum :",font="Times 10",anchor=W,fill='#561210')
        self.canvas1.create_text(280,170,text="Minimum :",font="Times 10",anchor=W,fill='#561210')
        self.mainData()
        

weather=weatherData()                                                           #object to call functions from weatherData class

showWeather = Button(weather.root,fg='#3F2B2C',text='SHOW WEATHER',font='ComicSansMS 15 bold',bg='#EC3047',command=weather.getData)
weather.canvas.create_window(200,60,height=40, width=180, window=showWeather)
weather.root.mainloop()
