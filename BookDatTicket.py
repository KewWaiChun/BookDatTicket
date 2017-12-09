import Tkinter as tk
import MySQLdb
import smtplib, sys, getpass
import tkMessageBox
import random
from datetime import datetime,date
import time
from PIL import Image, ImageTk

def planeRate(Company):
    if Company=="MAS":
        rate=30
    elif Company=="FLY AHEAD":
        rate=25
    elif Company=="AIRASIA":
        rate=21
    elif Company=="PLANE IS GUD":
        rate=18
    elif Company=="HAPPY RIDE(P)":
        rate=15
    return rate

def planeCompany(planeCompanyCounter):
    planeCompanylist=["MAS", "FLY AHEAD","AIRASIA", "PLANE IS GUD", "HAPPY RIDE(P)"]
    company=planeCompanylist[planeCompanyCounter]
    return company

def trainRate(Company):
    if Company=="RAIL EXPRESS":
        rate=18
    elif Company=="DOKODEMO":
        rate=15
    elif Company=="KTMB":
        rate=11
    elif Company=="TRAIN IS GUD":
        rate=7
    elif Company=="HAPPY RIDE(T)":
        rate=4
    return rate

def trainCompany(trainCompanyCounter):
        trainCompanylist=["RAIL EXPRESS", "DOKODEMO", "KTMB", "TRAIN IS GUD", "HAPPY RIDE(T)"]
        company=trainCompanylist[trainCompanyCounter]
        return company

def busRate(Company):
    if Company=="NICE":
        rate=20
    elif Company=="KKKL":
        rate=16
    elif Company=="AEROLINE":
        rate=12
    elif Company=="BUS IS GUD":
        rate=8
    elif Company=="HAPPY RIDE(B)":
        rate=5
    return rate

def busCompany(busCompanyCounter):
    busCompanylist=["NICE", "KKKL", "AEROLINE", "BUS IS GUD", "HAPPY RIDE(B)"]
    company=busCompanylist[busCompanyCounter]
    return company

def Position(place):
    position_dictionary={"Terengganu" : 0,
                         "Kelantan" : 1.0,
                         "Pahang" : 1.1,
                         "Perak" : 2.0,
                         "Selangor" : 2.1,
                         "Negeri Sembilan" : 2.2,
                         "Melaka" : 2.3,
                         "Perlis" : 3.0,
                         "Kedah" : 3.1,
                         "Penang" : 3.2,
                         "Johor" : 3.3,
                         "Singapore" : 3.4,
                         "Sarawak" : 4.0,
                         "Sabah" : 5.0}
    position=position_dictionary.get(place)
    return position

def Conversion(place):
    if place == 4.0 :
        place = -1.0
    if place == 5.0 :
        place = -1.1
    return place
    
def calcPrice(position,rate):
    if position >= 0 and position < 1.6 :
        price = 1*rate
    elif position >= 1.6 and position < 2.6 :
        price = 2*rate
    elif position >= 2.6 and position < 3.6 :
        price = 3*rate
    elif position >= 3.6 and position < 4.6 :
        price = 4*rate
    elif position >= 4.6 and position < 5.6 :
        price = 5*rate
    return price
       
StandardFont=("Verdana", 20)
allLocation=['Terengganu', 'Kelantan','Pahang','Perak','Selangor','Negeri Sembilan','Melaka','Perlis','Kedah','Penang','Johor','Singapore','Sarawak','Sabah']
global CapacityIndex
CapacityIndex=[[] for b in range (6)]
db=MySQLdb.connect("localhost","root","","newtest")

class BookDatTicket(tk.Tk):    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "BookDatTicket")
        tk.Tk.iconbitmap(self,"TicketIcon.ico")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames={}

        for F in (LoginPage, BookTypeSelection, Register, ManualPage, AutoPage):
            cont=F.__name__

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)

        global username, password

        backImage=tk.PhotoImage(file="Transportation.gif")
        background=tk.Label(self, image=backImage)
        background.img=backImage
        background.place(x=0,y=0)

        def checkAccount():
            global gmail
            cursor=db.cursor()
            try:
                cursor.execute("SELECT * FROM account2 WHERE username = %s AND password = %s" , (username.get(), password.get()))
                cursor.fetchall()
                if (cursor.rowcount!=1):
                    tkMessageBox.showinfo("Invalid", "Invalid Username or Password!")
                    username.delete(0,'end')
                    password.delete(0,'end')
                else:
                    tkMessageBox.showinfo("Success", "Welcome %s" % username.get())
                    for row in cursor:
                        gmail=row[4]
                    username.delete(0,'end')
                    password.delete(0,'end')
                    controller.show_frame(BookTypeSelection)
            except MySQLdb.Error as error:
                print error()

        Logo=tk.PhotoImage(file="Ticket.gif")
        LogoLabel=tk.Label(self, image=Logo)
        LogoLabel.img=Logo
        LogoLabel.place(relx=0.5,rely=0.2,anchor='center')

        UsernameLabel=tk.Label(self, text="Username: ")
        UsernameLabel.place(relx=0.4,rely=0.5,anchor='center')

        username=tk.Entry(self)
        username.place(relx=0.55,rely=0.5,anchor='center')

        PasswordLabel=tk.Label(self, text="Password: ")
        PasswordLabel.place(relx=0.4,rely=0.6,anchor='center')

        password=tk.Entry(self, show="*")
        password.place(relx=0.55,rely=0.6,anchor='center')

        LoginButton=tk.Button(self, text="Login",bg="blue",fg='white',
                          command=checkAccount)
        LoginButton.place(relx=0.55,rely=0.7,anchor='center')
        RegisterButton=tk.Button(self, text="Register",bg='red',fg='white',
                           command=lambda: controller.show_frame(Register))
        RegisterButton.place(relx=0.4,rely=0.7,anchor='center')

        NewLabel=tk.Label(self, text="New User?")
        NewLabel.place(relx=0.32, rely=0.7, anchor='center')

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        backImage=tk.PhotoImage(file="Transportation.gif")
        background=tk.Label(self, image=backImage)
        background.img=backImage
        background.place(x=0,y=0)
        self.controller=controller
        default_gmail='testslave97@gmail.com'
        default_password='testing1997'
        
        label=tk.Label(self, text="REGISTRATION PAGE", font=StandardFont)
        label.place(relx=0.5,rely=0.2,anchor='center')

        def createAccount():
            try:
                smtpserver=smtplib.SMTP("smtp.gmail.com", 587)
                smtpserver.ehlo()
                smtpserver.starttls()
                smtpserver.ehlo()
                try:
                    smtpserver.login(default_gmail, default_password)      
                except smtplib.SMTPException:
                    print "Authentication failed"
                    smtpserver.close()
            except smtplib.SMTPException:
                print "Connection to Gmail failed..."
                sys.exit(1)
            UsedUsername="False"
            cursor=db.cursor()
            if (len(username.get())>0 and len(password.get())>0 and len(name.get())>0 and len(gmail.get())>0):
                try:
                    cursor.execute("select username from account2")
                    data=cursor.fetchall()
                    for row in data:
                        if username.get()==row[0]:
                            UsedUsername="True"
                            break
                except MySQLdb.Error as error:
                    print (error)
                if UsedUsername=="False":
                    Subject="Welcome to BookDatTicket!\n"
                    body="Account created successfully!\n Thank you for signing up for BookDatTicket! We sincerely hope that you will enjoy our service!"
                    msg='\r\n'.join(['To: %s' % gmail,
                                     'From: %s' % default_gmail,
                                     'Subject: %s' % Subject,
                                     '',body])
                    try:
                        smtpserver.sendmail(default_gmail, gmail.get(), msg)
                    except smtplib.SMTPException:
                        tkMessageBox.showinfo("Invalid", "Gmail does not exist!")
                        smtpserver.close()
                        controller.show_frame(Register)
                    else:
                        sql="INSERT INTO account2 (username, password, name, gmail) \
                        VALUES('%s','%s','%s', '%s')" % \
                        (username.get(),password.get(),name.get(), gmail.get())
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            db.rollback()
                        Login=tkMessageBox.askquestion("Success!", "Would you like to log in now?")
                        if Login=="yes":
                            controller.show_frame(LoginPage)
                        else:
                            controller.show_frame(Register)
                else:
                    tkMessageBox.showinfo("Invalid!","The username has already existed!\n Please register with a new username!")
            else:
                tkMessageBox.showinfo("Invalid", "Please enter your information!")
            username.delete(0,'end')
            password.delete(0,'end')
            name.delete(0,'end')
            gmail.delete(0,'end')

        UsernameLabel=tk.Label(self, text="Enter Username:")
        UsernameLabel.place(relx=0.4,rely=0.4,anchor='center')
        username=tk.Entry(self)
        username.place(relx=0.58,rely=0.4,anchor='center')
        PasswordLabel=tk.Label(self, text="Enter Password: ")
        PasswordLabel.place(relx=0.4,rely=0.5,anchor='center')
        password=tk.Entry(self)
        password.place(relx=0.58,rely=0.5,anchor='center')
        NameLabel=tk.Label(self, text="Enter your name: ")
        NameLabel.place(relx=0.4,rely=0.6,anchor='center')
        name=tk.Entry(self)
        name.place(relx=0.58,rely=0.6,anchor='center')
        EmailLabel=tk.Label(self, text="Please enter your email address : ")
        EmailLabel.place(relx=0.4,rely=0.7,anchor='center')
        gmail=tk.Entry(self)
        gmail.place(relx=0.58,rely=0.7,anchor='center')

        CreateAccButton=tk.Button(self, text="Create Account",fg='blue',
                          command=createAccount)
        CreateAccButton.place(relx=0.55,rely=0.8,anchor='center')
        BackButton=tk.Button(self, text="Back",fg='red',
                          command=lambda: controller.show_frame(LoginPage))
        BackButton.place(relx=0.4,rely=0.8,anchor='center')

class BookTypeSelection(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        backImage=tk.PhotoImage(file="Transportation.gif")
        background=tk.Label(self, image=backImage)
        background.img=backImage
        background.place(x=0,y=0)
        
        SelectionLabel=tk.Label(self, text="SELECT YOUR BOOKING MODE", font=StandardFont)
        SelectionLabel.place(relx=0.5,rely=0.1 ,anchor='center')
        ManualButton=tk.Button(self, height=10, width=32,text="Manual",bg='black',fg='white',
                          command=lambda: controller.show_frame(ManualPage),bd=4)
        ManualButton.place(relx=0.3, rely=0.5, anchor='center')
        AutoButton=tk.Button(self, height=10, width=32,text="Automatic",bg='white',
                          command=lambda: controller.show_frame(AutoPage),bd=4)
        AutoButton.place(relx=0.7, rely=0.5, anchor='center')

        def Back():
            QuitPage=tkMessageBox.askquestion("Quit", "Do you want to exit to the login page?")
            if QuitPage=='yes':
                controller.show_frame(LoginPage)
        
        backButton=tk.Button(self, text="Back",bg='red', command=Back,bd=4)
        backButton.place(relx=0.5,rely=0.7,anchor='center')

class ManualPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        backImage=tk.PhotoImage(file="Transportation.gif")
        background=tk.Label(self, image=backImage)
        background.img=backImage
        background.place(x=0,y=0) 

        ManualLabel=tk.Label(self,text="Manual Booking", font=StandardFont)
        ManualLabel.grid(row=0,column=2,columnspan=12,sticky='wens')
        default_gmail='testslave97@gmail.com'
        default_password='testing1997'

        Timelist=list(time.localtime())
        Year=Timelist[0]
        Yearlist=[Year,Year+1]
        
        try:
            smtpserver=smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            try:
                smtpserver.login(default_gmail, default_password)      
            except smtplib.SMTPException:
                print "Authentication failed"
                smtpserver.close()
        except smtplib.SMTPException:
            print "Connection to Gmail failed..."
            sys.exit(1)
        
        Company_dictionary= {"Plane" : ["MAS", "FLY AHEAD","AIRASIA", "PLANE IS GUD", "HAPPY RIDE(P)"],
                     "Train": ["RAIL EXPRESS", "DOKODEMO", "KTMB", "TRAIN IS GUD", "HAPPY RIDE(T)"],
                     "Bus": ["NICE", "KKKL", "AEROLINE", "BUS IS GUD", "HAPPY RIDE(B)"]}

        Time_dictionary= {"Plane" : ["7am", "10am", "3pm"],
                         "Train": ["9am", "12pm", "4pm"],
                         "Bus": ["10am", "1pm", "5pm"]}

        Location_dictionary={"EAST" : ["Sarawak","Sabah"],
                             "WEST" : ["Terengganu", "Kelantan","Pahang","Perak","Selangor","Negeri Sembilan","Melaka","Perlis","Kedah","Penang","Johor","Singapore"],
                             "Both sides (Plane only)" : ["Terengganu", "Kelantan","Pahang","Perak","Selangor","Negeri Sembilan","Melaka","Perlis","Kedah","Penang","Johor","Singapore","Sarawak","Sabah"]}

        def updateOptions(self, *args):
            companies=Company_dictionary[TransVar.get()]
            CompanyVar.set(companies[0])

            menu=CompanyChoice["menu"]
            menu.delete(0,'end')

            for company in companies:
                menu.add_command(label=company, command=lambda comp=company: CompanyVar.set(comp))

        def updateOptions2(self, *args):
            
            time=Time_dictionary[TransVar.get()]
            TimeVar.set(time[0])

            menu2=TimeChoice["menu"]
            menu2.delete(0,'end')

            for timing in time:
                menu2.add_command(label=timing, command=lambda time2=timing: TimeVar.set(time2))

        def updateOptions3(self, *args):

            board=Location_dictionary[SideVar.get()]
            LocationVar.set(board[0])

            menu3=LocationOption["menu"]
            menu3.delete(0,'end')

            for boarding in board:
                menu3.add_command(label=boarding, command=lambda board2=boarding: LocationVar.set(board2))

        def updateOptions4(self, *args):
            
            reach=Location_dictionary[SideVar.get()]
            DestinationVar.set(reach[0])

            menu4=DestinationOption["menu"]
            menu4.delete(0,'end')

            for reaching in reach:
                menu4.add_command(label=reaching, command=lambda reach2=reaching: DestinationVar.set(reach2))
        
        TransportLabel=tk.Label(self, text="Transport Type")
        TransportLabel.grid(row=5,column=0,sticky='wens')
        TransVar=tk.StringVar(self)
        TransOption=tk.OptionMenu(self, TransVar, *Company_dictionary.keys())
        TransOption.grid(row=5,column=1,sticky='wens')

        SideLabel=tk.Label(self, text="Which side?")
        SideLabel.grid(row=6,column=0,sticky='wens')
        SideVar=tk.StringVar(self)
        Side=tk.OptionMenu(self, SideVar, *Location_dictionary.keys())
        Side.grid(row=6,column=1,sticky='wens')
        
        CompanyLabel=tk.Label(self, text="Select a company")
        CompanyLabel.grid(row=7,column=0,sticky='wens')
        TransVar.trace("w", updateOptions)
        CompanyVar=tk.StringVar(self)
        CompanyChoice=tk.OptionMenu(self, CompanyVar, *allLocation)
        CompanyChoice.grid(row=7,column=1,sticky='wens')
        
        TimeLabel=tk.Label(self, text="Choose your time")
        TimeLabel.grid(row=8,column=0,sticky='wens')
        TransVar.trace("w", updateOptions2)
        TimeVar=tk.StringVar(self)
        TimeChoice=tk.OptionMenu(self, TimeVar, '')
        TimeChoice.grid(row=8,column=1,sticky='wens')
        
        LocationLabel=tk.Label(self, text="Choose a location to board")
        LocationLabel.grid(row=9,column=0,sticky='wens')
        SideVar.trace("w", updateOptions3)
        LocationVar=tk.StringVar(self)
        LocationOption=tk.OptionMenu(self, LocationVar, *allLocation)
        LocationOption.grid(row=9,column=1,sticky='wens')
        
        DestinationLabel=tk.Label(self, text="Choose your destination")
        DestinationLabel.grid(row=10,column=0,sticky='wens')
        SideVar.trace("w", updateOptions4)
        DestinationVar=tk.StringVar(self)
        DestinationOption=tk.OptionMenu(self, DestinationVar, *allLocation)
        DestinationOption.grid(row=10,column=1,sticky='wens')
        
        QuantityLabel=tk.Label(self, text="Please enter your quantity")
        QuantityLabel.grid(row=11,column=0,sticky='wens')
        slider=tk.Scale(self, from_=1, to=40, orient='horizontal')
        slider.grid(row=11,column=1,sticky='wens')

        DayLabel=tk.Label(self, text="Please enter your day:\n (dd)")
        DayLabel.grid(row=12,column=0,sticky='wens')
        dayOption=tk.Entry(self)
        dayOption.grid(row=12,column=1,sticky='wens')
        
        MonthLabel=tk.Label(self, text="Please enter your month:\n (mm)")
        MonthLabel.grid(row=13,column=0,sticky='wens')
        monthOption=tk.Entry(self)
        monthOption.grid(row=13,column=1,sticky='wens')

        YearLabel=tk.Label(self,text="Select the year:")
        YearLabel.grid(row=14,column=0,sticky='wens')
        YearVar=tk.StringVar(self)
        yearOption=tk.OptionMenu(self, YearVar, *Yearlist)
        yearOption.grid(row=14,column=1,sticky='wens')

        def checkInfo():
            output.config(state='normal')
            output.delete("1.0", tk.END)
            if (len(TransVar.get()))>0 and (len(LocationVar.get()))>0 and (len(DestinationVar.get()))>0 and (len(CompanyVar.get()))>0 and (len(TimeVar.get()))>0 and (len(SideVar.get()))>0:
                if TransVar.get()=="Train" or TransVar.get()=="Bus":
                    if SideVar.get()=="Both sides (Plane only)":
                        errorState="True"
                    else:
                        errorState="False"
                else:
                    errorState="False"
            else:
                errorState="Pass"
                tkMessageBox.showinfo("Invalid", "Please fill in the requirements correctly!")
            if errorState=="False":
                if (DestinationVar.get() != LocationVar.get()):
                    global Location,Destination,Type,Quantity,Time,Price,EstimatedTime,Company,SinglePrice,DateFormat
                    Type=TransVar.get()
                    Location=LocationVar.get()
                    Destination=DestinationVar.get()
                    Quantity=slider.get()
                    Company=CompanyVar.get()
                    Time=TimeVar.get()
                    place1=Position(Location)
                    place2=Position(Destination)
                    distance=Conversion(place2)-Conversion(place1)
                    if distance<0:
                        distance=distance*(-1)
                    if Type=="Bus":
                        rate=busRate(Company)
                        EstimatedTime=distance*120
                    elif Type=="Train":
                        rate=trainRate(Company)
                        EstimatedTime=distance*60
                    else:
                        rate=planeRate(Company)
                        EstimatedTime=distance*30
                    SinglePrice=calcPrice(distance,rate)
                    Price=SinglePrice*Quantity
                    try:
                        Year=int(YearVar.get())
                        Month=int(monthOption.get())
                        Day=int(dayOption.get())
                        DateFormat=date(Year, Month, Day)
                    except:
                        tkMessageBox.showinfo("Invalid!","Please enter a valid date!")
                    else:
                        tempoDate="%s/%s/%s" % (Day, Month, Year)
                        DefaultDateFormat="%d/%m/%Y"
                        BookingDate=datetime.strptime(tempoDate, DefaultDateFormat)
                        DateNow=datetime.now()
                        if BookingDate<=DateNow:
                            tkMessageBox.showinfo("Invalid", "Please enter a date that starts from tomorrow!")
                        else:
                            output.config(state='normal')
                            output.insert(tk.END, '\r\n'.join([
                                'a. Company: %s' % Company,
                                'b. Transport: %s' % Type,
                                'c. Date: %s' % DateFormat,
                                'd. Time: %s' % Time,
                                'e. Location: %s' % Location,
                                'f. Destination: %s' % Destination,
                                'g. Price: RM%s X %s = RM%s' % (SinglePrice, Quantity, Price),
                                'h. Estimated Time for arrival: %s minutes\n' % EstimatedTime,
                                '',
                                ]) )
                            output.config(state='disable')
                            output.see(tk.END)
                            ConfirmButton.config(state='normal')
                else:
                    tkMessageBox.showinfo("Invalid", "Please fill in the requirements correctly!")
            elif errorState=="True":
                tkMessageBox.showinfo("Invalid", "Please note that 'Both Sides' is only available for 'Plane' services'")

        def Back():
            QuitPage=tkMessageBox.askquestion("Quit", "Are you sure you want to quit this page?")
            if QuitPage=='yes':
                output.config(state="normal")
                output.delete('1.0',tk.END)
                output.config(state='disable')
                monthOption.delete(0,'end')
                ConfirmButton.config(state="disabled")
                dayOption.delete(0,'end')
                controller.show_frame(BookTypeSelection)

        def ConfirmBooking():
            global gmail,Company,Type,DateFormat,Time,Location,Destination,SinglePrice,Quantity,Price,EstimatedTime
            confirming=tkMessageBox.askquestion("Confirmation", "Would you like to confirm your purchase?\nPlease NOTE that the system will purchase according to the information gathered in the description box.")
            if confirming=='yes':
                try:
                    CapacityIndex[0].index(Company)
                    CapacityIndex[1].index(DateFormat)
                    CapacityIndex[2].index(Location)
                    CapacityIndex[3].index(Destination)
                    CapacityIndex[4].index(Time)
                except:
                    CapacityIndex[0].append(Company)
                    CapacityIndex[1].append(DateFormat)
                    CapacityIndex[2].append(Location)
                    CapacityIndex[3].append(Destination)
                    CapacityIndex[4].append(Time)
                    CapacityIndex[5].append(Quantity)
                    fullSeat="False"
                else:
                    length=len(CapacityIndex[0])
                    for counting in range (0,length):
                        if CapacityIndex[0][counting]==Company:
                            if CapacityIndex[1][counting]==DateFormat:
                                if CapacityIndex[2][counting]==Location:
                                    if CapacityIndex[3][counting]==Destination:
                                        if CapacityIndex[4][counting]==Time:
                                            if Type=="Plane":
                                                if (CapacityIndex[5][counting]+Quantity)>180:
                                                    tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                    fullSeat="True"
                                                else:
                                                    CapacityIndex[5][counting]=CapacityIndex[5][counting]+Quantity
                                                    fullSeat="False"
                                            elif Type=="Train":
                                                if (CapacityIndex[5][counting]+Quantity)>328:
                                                    tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                    fullSeat="True"
                                                else:
                                                    CapacityIndex[5][counting]=CapacityIndex[5][counting]+Quantity
                                                    fullSeat="False"
                                            else:
                                                if (CapacityIndex[5][counting]+Quantity)>40:
                                                    tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                    fullSeat="True"
                                                else:
                                                    CapacityIndex[5][counting]=CapacityIndex[5][counting]+Quantity
                                                    fullSeat="False"
                if fullSeat=="False":
                    Subject="Thank You for using BookDatTicket!"
                    randomstring="Your verification code is: %s-%s-%s" % (random.randint(1000,9999),random.randint(1000,9999),random.randint(1000,9999))
                    body1='a. Company: %s' % Company
                    body2='b. Transport: %s' % Type
                    body3='c. Date: %s' % DateFormat
                    body4='d. Time: %s' % Time
                    body5='e. Location: %s' % Location
                    body6='f. Destination: %s' % Destination
                    body7='g. Price: RM%s X %s = RM%s' % (SinglePrice, Quantity, Price)
                    body8='h. Estimated Time for arrival: %s minutes\n' % EstimatedTime
                    Body='\r\n'.join(['To: %s' % gmail,
                                      'From: %s' % default_gmail,
                                      'Subject: %s' % Subject,
                                      '',body1,body2,body3,body4,body5,body6,body7,body8,randomstring])
                    try:
                        smtpserver.sendmail(default_gmail, gmail, Body)
                    except smtplib.SMTPException:
                        print "Email could not be sent"
                        smtpserver.close()
                        sys.exit(1)
                    tkMessageBox.showinfo("Thank You", "Thank you for your purchase!\nThe receipt and the verification code will be sent to your E-mail address!\n")
                    Continue=tkMessageBox.askquestion("Another Purchase?", "Would you like to proceed with another purchase?")
                    if Continue=='yes':
                        output.config(state="normal")
                        output.delete('1.0',tk.END)
                        output.config(state='disable')
                        ConfirmButton.config(state="disabled")
                        monthOption.delete(0,'end')
                        dayOption.delete(0,'end')
                        controller.show_frame(BookTypeSelection)
                    else:
                        app.destroy()
                        app.quit()
                else:
                    controller.show_frame(ManualPage)
                
        CheckButton=tk.Button(self, text="Check",fg='brown',command=checkInfo,height=5,width=20)
        CheckButton.grid(row=15,column=1,sticky='wens')
        ConfirmButton=tk.Button(self, text="Confirm",fg='blue',command=ConfirmBooking,height=5,width=20,state='disabled')
        ConfirmButton.grid(row=15,column=2,sticky='wens')
        BackButton=tk.Button(self, text="Back",fg='red',command=Back,height=5,width=20)
        BackButton.grid(row=15,column=0,sticky='wens')

        output = tk.Text(self,state='disabled',height=20,width=50,bd=5)
        output.grid(row=5,column=10,rowspan=10,columnspan=10)

class AutoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        backImage=tk.PhotoImage(file="Transportation.gif")
        background=tk.Label(self, image=backImage)
        background.img=backImage
        background.place(x=0,y=0)

        State="False"
        State2="False"

        default_gmail='testslave97@gmail.com'
        default_password='testing1997'
        
        global Yearlist
        Timelist=list(time.localtime())
        Year=Timelist[0]
        Yearlist=[Year,Year+1]
         
        try:
            smtpserver=smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            try:
                smtpserver.login(default_gmail, default_password)      
            except smtplib.SMTPException:
                print "Authentication failed"
                smtpserver.close()
        except smtplib.SMTPException:
            print "Connection to Gmail failed..."
            sys.exit(1)

        Location_dictionary={"EAST" : ["Sarawak","Sabah"],
                             "WEST" : ["Terengganu", "Kelantan","Pahang","Perak","Selangor","Negeri Sembilan","Melaka","Perlis","Kedah","Penang","Johor","Singapore"],
                             "Both sides (Plane only)" : ["Terengganu", "Kelantan","Pahang","Perak","Selangor","Negeri Sembilan","Melaka","Perlis","Kedah","Penang","Johor","Singapore","Sarawak","Sabah"]}
        Time_dictionary= {"Plane" : ["7am", "10am", "3pm"],
                         "Train": ["9am", "12pm", "4pm"],
                         "Bus": ["10am", "1pm", "5pm"]}
        
        AutoResultIndex=[[]for a in range(7)]
        AutoLabel=tk.Label(self,text="Automatic Booking", font=StandardFont)
        AutoLabel.grid(row=0,column=2,columnspan=12,sticky='wens')   

        def updateOptions(self, *args):
            Location=Location_dictionary[SideVar.get()]
            LocationVar.set(Location[0])

            menu=LocationOption["menu"]
            menu.delete(0,'end')

            for locations in Location:
                menu.add_command(label=locations, command=lambda tempoLoc=locations: LocationVar.set(tempoLoc))

        def updateOptions2(self, *args):
            Destination=Location_dictionary[SideVar.get()]
            DestinationVar.set(Destination[0])

            menu=DestinationOption["menu"]
            menu.delete(0,'end')

            for destinations in Destination:
                menu.add_command(label=destinations, command=lambda tempoDesti=destinations: DestinationVar.set(tempoDesti))

        def searchResult():
            global State2
            global State
            global AutoResultIndex
            global Yearlist
            State2="False"
            State="False"
            output.config(state="normal")
            output.delete("1.0", tk.END)
            output.config(state="disable")
            AutoResultIndex=[[],[],[],[],[],[],[]]
            if (len(SideVar.get()))>0 and (len(LocationVar.get()))>0 and (len(DestinationVar.get()))>0:
                if (LocationVar.get() != DestinationVar.get()):
                    Location=LocationVar.get()
                    Destination=DestinationVar.get()
                    maxbudget=slider.get()
                    Quantity=slider2.get()
                    if SideVar.get()=="Both sides (Plane only)":
                        for planeCompCounter in range (0,5):
                            tempoCompany=planeCompany(planeCompCounter)
                            place1=Position(Location)
                            place2=Position(Destination)
                            distance=Conversion(place2)-Conversion(place1)
                            if distance<0:
                                distance=distance*(-1)
                            rate=planeRate(tempoCompany)
                            tempoPrice=calcPrice(distance,rate)
                            EstimatedTime=distance*30
                            if (tempoPrice<=maxbudget):
                                AutoResultIndex[0].append(tempoCompany)
                                AutoResultIndex[1].append(tempoPrice)
                                AutoResultIndex[2].append("Plane")
                                AutoResultIndex[3].append(Location)
                                AutoResultIndex[4].append(Destination)
                                AutoResultIndex[5].append(Quantity)
                                AutoResultIndex[6].append(EstimatedTime)
                    else:
                        for planeCompCounter in range (0,5):
                            tempoCompany=planeCompany(planeCompCounter)
                            place1=Position(Location)
                            place2=Position(Destination)
                            distance=Conversion(place2)-Conversion(place1)
                            if distance<0:
                                distance=distance*(-1)
                            rate=planeRate(tempoCompany)
                            tempoPrice=calcPrice(distance,rate)
                            EstimatedTime=distance*30
                            if (tempoPrice<=maxbudget):
                                AutoResultIndex[0].append(tempoCompany)
                                AutoResultIndex[1].append(tempoPrice)
                                AutoResultIndex[2].append("Plane")
                                AutoResultIndex[3].append(Location)
                                AutoResultIndex[4].append(Destination)
                                AutoResultIndex[5].append(Quantity)
                                AutoResultIndex[6].append(EstimatedTime)
                                
                        for trainCompCounter in range (0,5):
                            tempoCompany=trainCompany(trainCompCounter)
                            place1=Position(Location)
                            place2=Position(Destination)
                            distance=Conversion(place2)-Conversion(place1)
                            if distance<0:
                                distance=distance*(-1)
                            rate=trainRate(tempoCompany)
                            tempoPrice=calcPrice(distance,rate)
                            EstimatedTime=distance*60
                            if (tempoPrice<=maxbudget):
                                AutoResultIndex[0].append(tempoCompany)
                                AutoResultIndex[1].append(tempoPrice)
                                AutoResultIndex[2].append("Train")
                                AutoResultIndex[3].append(Location)
                                AutoResultIndex[4].append(Destination)
                                AutoResultIndex[5].append(Quantity)
                                AutoResultIndex[6].append(EstimatedTime)
                                
                        for busCompCounter in range (0,5):
                            tempoCompany=busCompany(busCompCounter)
                            place1=Position(Location)
                            place2=Position(Destination)
                            distance=Conversion(place2)-Conversion(place1)
                            if distance<0:
                                distance=distance*(-1)
                            rate=busRate(tempoCompany)
                            tempoPrice=calcPrice(distance,rate)
                            EstimatedTime=distance*120
                            if (tempoPrice<=maxbudget):
                                AutoResultIndex[0].append(tempoCompany)
                                AutoResultIndex[1].append(tempoPrice)
                                AutoResultIndex[2].append("Bus")
                                AutoResultIndex[3].append(Location)
                                AutoResultIndex[4].append(Destination)
                                AutoResultIndex[5].append(Quantity)
                                AutoResultIndex[6].append(EstimatedTime)
                                
                    IndexLength=len(AutoResultIndex[0])
                    if IndexLength<=0:
                        output.config(state='normal')
                        output.insert(tk.END, "0 Results found!\n")
                        output.config(state='disable')
                        output.see(tk.END)
                    else:
                        output.config(state='normal')
                        output.insert(tk.END, "%s results found!\n" % IndexLength)
                        output.see(tk.END)
                        for ResultCounter in range (0,IndexLength):
                            output.config(state='normal')
                            output.insert(tk.END, '\r\n'.join([
                                '\n%s.' % (ResultCounter+1),
                                'a. Company: %s' % AutoResultIndex[0][ResultCounter],
                                'b. Transport: %s' % AutoResultIndex[2][ResultCounter],
                                'c. Location: %s' % AutoResultIndex[3][ResultCounter],
                                'd. Destination: %s' % AutoResultIndex[4][ResultCounter],
                                'e. Price: RM%s' % AutoResultIndex[1][ResultCounter],
                                'f. Estimated Time for arrival: %s minutes\n' % AutoResultIndex[6][ResultCounter],
                                '',
                                ]) )
                            output.config(state='disable')
                            output.see(tk.END)
                    if IndexLength>0:
                        codeOption.config(state='normal')
                        CheckButton1.config(state='normal')
                else:
                   tkMessageBox.showinfo("Invalid", "Please enter a valid selection!") 
            else:
                tkMessageBox.showinfo("Invalid", "Please enter the required information before checking!")

        SideLabel=tk.Label(self, text="Please select which side")
        SideLabel.grid(row=5,column=0,sticky='wens')
        SideVar=tk.StringVar(self)
        Side=tk.OptionMenu(self, SideVar, *Location_dictionary.keys())
        Side.grid(row=5,column=1,sticky='wens')

        LocationLabel=tk.Label(self, text="Please select where you would like to board")
        LocationLabel.grid(row=6,column=0,sticky='wens')
        LocationVar=tk.StringVar(self)
        SideVar.trace("w", updateOptions2)
        LocationOption=tk.OptionMenu(self, LocationVar, '')
        LocationOption.grid(row=6,column=1,sticky='wens')

        DestinationLabel=tk.Label(self, text="Please select your destination")
        DestinationLabel.grid(row=7,column=0,sticky='wens')
        DestinationVar=tk.StringVar(self)
        SideVar.trace("w", updateOptions)
        DestinationOption=tk.OptionMenu(self, DestinationVar, '')
        DestinationOption.grid(row=7,column=1,sticky='wens')

        BudgetLabel=tk.Label(self,text="Please select your maximum budget")
        BudgetLabel.grid(row=8,column=0,sticky='wens')
        slider=tk.Scale(self, from_=1, to=200, orient='horizontal')
        slider.grid(row=8,column=1,sticky='wens')

        QuantityLabel=tk.Label(self, text="How many tickets would you like to book?")
        QuantityLabel.grid(row=9,column=0,sticky='wens')
        slider2=tk.Scale(self, from_=1, to=40, orient="horizontal")
        slider2.grid(row=9,column=1,sticky='wens')

        OptionLabel=tk.Label(self, text="Please enter your option:")
        OptionLabel.grid(row=10,column=0,sticky='wens')
        codeOption=tk.Entry(self, state='disable')
        codeOption.grid(row=10,column=1,sticky='wens')

        TimeLabel=tk.Label(self, text="Please select your time:")
        TimeLabel.grid(row=11,column=0,sticky='wens')
        timeOption=tk.Entry(self,state='disable')
        timeOption.grid(row=11,column=1,sticky='wens')

        DayLabel=tk.Label(self, text="Please enter your day:\n (dd)")
        DayLabel.grid(row=12,column=0,sticky='wens')
        dayOption=tk.Entry(self,state='disable')
        dayOption.grid(row=12,column=1,sticky='wens')
        
        MonthLabel=tk.Label(self, text="Please enter your month:\n (mm)")
        MonthLabel.grid(row=13,column=0,sticky='wens')
        monthOption=tk.Entry(self,state='disable')
        monthOption.grid(row=13,column=1,sticky='wens')

        YearLabel=tk.Label(self,text="Select the year:")
        YearLabel.grid(row=14,column=0,sticky='wens')
        YearVar=tk.StringVar(self)
        yearOption=tk.OptionMenu(self, YearVar, *Yearlist)
        yearOption.grid(row=14,column=1,sticky='wens')

        def Back():
            confirming=tkMessageBox.askquestion("Quit", "Are you sure you want to quit this page?")
            if confirming=='yes':
                timeOption.delete(0,'end')
                dayOption.delete(0,'end')
                monthOption.delete(0,'end')
                CheckButton1.config(state="disabled")
                CheckButton2.config(state="disabled")
                ConfirmButton.config(state="disabled")
                codeOption.delete(0,'end')
                output.config(state='normal')
                output.delete(0.0,'end')
                output.see(tk.END)
                controller.show_frame(BookTypeSelection)

        def CheckResult():
            global State2
            global State
            global AutoResultIndex
            global Code
            global timeAvailable
            global Yearlist
            State2="False"
            State="False"
            Code=codeOption.get()
            try:
                Code=int(Code)
            except:
                tkMessageBox.showinfo("Invalid!", "Please enter the correct code!")
            else:
                output.config(state='normal')
                output.delete("1.0", tk.END)
                try:
                    if Code>0:
                        if AutoResultIndex[2][Code-1]=="Bus":
                            timeAvailable=["10am", "1pm", "5pm"]
                        elif AutoResultIndex[2][Code-1]=="Train":
                            timeAvailable=["9am", "12pm", "4pm"]
                        else:
                            timeAvailable=["7am", "10am", "3pm"]
                        output.insert(tk.END, '\r\n'.join([
                                'Your choice is : %s.' % (Code),
                                'a. Company: %s' % AutoResultIndex[0][Code-1],
                                'b. Transport: %s' % AutoResultIndex[2][Code-1],
                                'c. Location: %s' % AutoResultIndex[3][Code-1],
                                'd. Destination: %s' % AutoResultIndex[4][Code-1],
                                'e. Price: RM%s' % AutoResultIndex[1][Code-1],
                                'f. Estimated Time for arrival: %s minutes\n' % AutoResultIndex[6][Code-1],
                                "\n Time available:\n 1.%s\n 2.%s\n 3.%s\n" % (timeAvailable[0],timeAvailable[1],timeAvailable[2]),
                                '',
                                ]) )
                        output.config(state='disabled')
                        output.see(tk.END)
                        timeOption.config(state='normal')
                        dayOption.config(state='normal')
                        monthOption.config(state='normal')
                        yearOption.config(state='normal')
                        State2="True"
                        CheckButton2.config(state='normal')
                    else:
                        tkMessageBox.showinfo("Invalid","Please enter the correct code1!")
                except:
                    tkMessageBox.showinfo("Invalid","Please enter the correct code!")

        def CheckResult2():
            global State2
            global State
            global Code
            global timeAvailable
            global dateindex
            global AutoResultIndex
            global DateFormat,Time,Total
            State="False"
            if State2=="True":
                Time=timeOption.get()
                SinglePrice=int(AutoResultIndex[1][Code-1])
                Total=SinglePrice*slider2.get()
                try:
                    Time=int(Time)
                    Year=int(YearVar.get())
                    Month=int(monthOption.get())
                    Day=int(dayOption.get())
                    DateFormat=date(Year, Month, Day)
                except:
                    tkMessageBox.showinfo("Invalid!","Please enter a valid date!")
                else:
                    tempoDate="%s/%s/%s" % (Day, Month, Year)
                    DefaultDateFormat="%d/%m/%Y"
                    BookingDate=datetime.strptime(tempoDate, DefaultDateFormat)
                    DateNow=datetime.now()
                    if BookingDate<=DateNow:
                        tkMessageBox.showinfo("Invalid", "Please enter a date that starts from tomorrow!")
                    else:
                        output.config(state="normal")
                        output.delete("1.0",tk.END)
                        try:
                            if Time>0:
                               output.insert(tk.END, '\r\n'.join([
                                    'Your choice is : %s.' % (Code),
                                    'a. Company: %s' % AutoResultIndex[0][Code-1],
                                    'b. Transport: %s' % AutoResultIndex[2][Code-1],
                                    'c. Location: %s' % AutoResultIndex[3][Code-1],
                                    'd. Destination: %s' % AutoResultIndex[4][Code-1],
                                    'e. Price: RM%s X %s = RM%s' % (AutoResultIndex[1][Code-1], slider2.get(), Total),
                                    'f. Estimated Time for arrival: %s minutes' % AutoResultIndex[6][Code-1],
                                    'g. Time: %s' % timeAvailable[Time-1],
                                    'h. Date: %s' % DateFormat,
                                    '',
                                    ]) )
                               output.config(state='disabled')
                               output.see(tk.END)
                               ConfirmButton.config(state='normal')
                               State="True"
                            else:
                                tkMessageBox.showinfo("Invalid!","Please enter the correct code!")
                        except:
                            tkMessageBox.showinfo("Invalid","Please enter the correct code!")
                            CheckButton2.config(state='disabled')
            else:
                tkMessageBox.showinfo("Invalid","Please check with your code first!")

        def ConfirmBooking():
            global State
            global gmail
            global CapacityIndex
            global AutoResultIndex
            global Code
            if State=="True":
                confirming=tkMessageBox.askquestion("Confirmation", "Would you like to confirm your purchase?\nPlease NOTE that the system will purchase according to the information gathered in the description box.")
                if confirming=='yes':
                    try:
                        CapacityIndex[0].index(AutoResultIndex[0][Code-1])
                        CapacityIndex[1].index(DateFormat)
                        CapacityIndex[2].index(AutoResultIndex[3][Code-1])
                        CapacityIndex[3].index(AutoResultIndex[4][Code-1])
                        CapacityIndex[4].index(timeAvailable[Time-1])
                    except:
                        CapacityIndex[0].append(AutoResultIndex[0][Code-1])
                        CapacityIndex[1].append(DateFormat)
                        CapacityIndex[2].append(AutoResultIndex[3][Code-1])
                        CapacityIndex[3].append(AutoResultIndex[4][Code-1])
                        CapacityIndex[4].append(timeAvailable[Time-1])
                        CapacityIndex[5].append(slider2.get())
                        fullSeat="False"
                    else:
                        length=len(CapacityIndex[0])
                        for counting in range (0,length):
                            if CapacityIndex[0][counting]==AutoResultIndex[0][Code-1]:
                                if CapacityIndex[1][counting]==DateFormat:
                                    if CapacityIndex[2][counting]==AutoResultIndex[3][Code-1]:
                                        if CapacityIndex[3][counting]==AutoResultIndex[4][Code-1]:
                                            if CapacityIndex[4][counting]==timeAvailable[Time-1]:
                                                if AutoResultIndex[2][Code-1]=="Plane":
                                                    if (CapacityIndex[5][counting]+slider2.get())>180:
                                                        tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                        fullSeat="True"
                                                    else:
                                                        CapacityIndex[5][counting]=CapacityIndex[5][counting]+slider2.get()
                                                        fullSeat="False"
                                                elif AutoResultIndex[2][Code-1]=="Train":
                                                    if (CapacityIndex[5][counting]+slider2.get())>328:
                                                        tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                        fullSeat="True"
                                                    else:
                                                        CapacityIndex[5][counting]=CapacityIndex[5][counting]+slider2.get()
                                                        fullSeat="False"
                                                else:
                                                    if (CapacityIndex[5][counting]+slider2.get())>40:
                                                        tkMessageBox.showinfo("Invalid!", "Sorry that particular shift is full!")
                                                        fullSeat="True"
                                                    else:
                                                        CapacityIndex[5][counting]=CapacityIndex[5][counting]+slider2.get()
                                                        fullSeat="False"
                    if fullSeat=="False":
                        Subject="Thank You for using BookDatTicket!"
                        randomstring="Your verification code is: %s-%s-%s" % (random.randint(1000,9999),random.randint(1000,9999),random.randint(1000,9999))
                        body='\r\n'.join([
                            'a. Company: %s' % AutoResultIndex[0][Code-1],
                            'b. Transport: %s' % AutoResultIndex[2][Code-1],
                            'c. Location: %s' % AutoResultIndex[3][Code-1],
                            'd. Destination: %s' % AutoResultIndex[4][Code-1],
                            'e. Price: RM%s X %s = RM%s' % (AutoResultIndex[1][Code-1], slider2.get(), Total),
                            'f. Estimated Time for arrival: %s minutes' % AutoResultIndex[6][Code-1],
                            'g. Time: %s' % timeAvailable[Time-1],
                            'h. Date: %s' % DateFormat,
                            '',
                            ])
                        msg='\r\n'.join(['To: %s' % gmail,
                                         'From: %s' % default_gmail,
                                         'Subject: %s' % Subject,
                                         '',body,randomstring])
                        try:
                            smtpserver.sendmail(default_gmail, gmail, msg)
                        except smtplib.SMTPException:
                            print "Email could not be sent"
                            smtpserver.close()
                            sys.exit(1)
                        else:
                            tkMessageBox.showinfo("Thank You", "Thank you for your purchase!\nThe receipt and the verification code will be send to your E-mail address!\n")
                            Continue=tkMessageBox.askquestion("Another Purchase?", "Would you like to proceed with another purchase?")
                            if Continue=='yes':
                                timeOption.delete(0,'end')
                                dayOption.delete(0,'end')
                                monthOption.delete(0,'end')
                                codeOption.delete(0,'end')
                                CheckButton1.config(state="disabled")
                                CheckButton2.config(state="disabled")
                                ConfirmButton.config(state="disabled")
                                output.config(state='normal')
                                output.delete(0.0,'end')
                                output.see(tk.END)
                                controller.show_frame(BookTypeSelection)
                            else:
                                app.destroy()
                                app.quit()
                    else:
                        controller.show_frame(AutoPage)
            else:
                tkMessageBox.showinfo("Invalid","Please Check before confirming!")

        SearchButton=tk.Button(self, text="Search Result",fg='blue', command=searchResult,bd=5)
        SearchButton.grid(row=9,column=2,sticky='wens')
        BackButton=tk.Button(self, text="Back",fg='red', command=Back,height=5,width=20)
        BackButton.grid(row=16,column=0,sticky='wens')
        ConfirmButton=tk.Button(self, text="Confirm",fg='blue',command=ConfirmBooking, height=5, width=20)
        ConfirmButton.config(state='disable')
        ConfirmButton.grid(row=16,column=2,sticky='wens')

        CheckButton1=tk.Button(self, text="Check",fg='brown', command=CheckResult,bd=5,state='disabled')
        CheckButton1.grid(row=10,column=2,sticky='wens')
        CheckButton2=tk.Button(self, text="Check",fg='brown', command=CheckResult2, bd=5,state='disabled')
        CheckButton2.grid(row=15,column=2,sticky='wens')

        output=tk.Text(self, state='disable',height=20,width=50,bd=5)
        output.grid(row=5,column=10,rowspan=10,columnspan=10)
        
if __name__ == "__main__":
    app = BookDatTicket()
    app.mainloop()
