
from tkinter import *
import urllib.request
from tkinter import messagebox
import pymysql

class RoomReservation:

    def __init__(self, win):

        self.win = win
        self.win.title("Login")

        pic = "http://www.cc.gatech.edu/classes/AY2015/cs2316_fall/codesamples/techlogo.gif"
        response = urllib.request.urlopen(pic)
        myPicture = response.read()

        
        import base64
        data = base64.encodebytes(myPicture)

        self.photo = PhotoImage(data = data)

        Label(self.win, image = self.photo).grid(row=0,column=1, sticky=EW)

        self.sv = StringVar()
        self.sv2 = StringVar()

        Label(self.win, text = "Username").grid(row=1,column=0,sticky=E)
        Label(self.win, text = "Password").grid(row=2,column=0,sticky=E)

        self.e1 = Entry(self.win, textvariable = self.sv, width = 30)
        self.e1.grid(row=1,column=1,sticky=E)

        self.e2 = Entry(self.win, textvariable = self.sv2, width = 30)
        self.e2.grid(row=2,column=1,sticky=E)

        f1 = Frame(self.win)

        Button(f1, text = "Register",command=self.Register).grid(row=0,column=0,sticky=E)
        Button(f1, text = "Login", command=self.LoginCheck).grid(row=0,column=1,sticky=E)

        f1.grid(row=3,column=1,sticky=E)

        Button(self.win, text = "Exit", command=self.Exit).grid(row=3,column=2,sticky=E)


    def Register(self):

        self.win.withdraw()

        self.win2 = Toplevel()

        self.win2.title("Room Reservation New User Registration")

        Label(self.win2, image = self.photo).grid(row=0,column=1, sticky=EW)

        self.sv3 = StringVar()
        self.sv4 = StringVar()
        self.sv5 = StringVar()
        self.sv6 = StringVar()

        Label(self.win2, text = "Last Name").grid(row=1,column=0,sticky=W)
        Label(self.win2, text = "Username").grid(row=2,column=0,sticky=W)
        Label(self.win2, text = "Password").grid(row=3,column=0,sticky=W)
        Label(self.win2, text = "Confirm Password").grid(row=4,column=0,sticky=W)
        

        self.e1 = Entry(self.win2, textvariable = self.sv3, width = 30)
        self.e1.grid(row=1,column=1,sticky=E)

        self.e2 = Entry(self.win2, textvariable = self.sv4, width = 30)
        self.e2.grid(row=2,column=1,sticky=E)

        self.e3 = Entry(self.win2, textvariable = self.sv5, width = 30)
        self.e3.grid(row=3,column=1,sticky=E)

        self.e4 = Entry(self.win2, textvariable = self.sv6, width = 30)
        self.e4.grid(row=4,column=1,sticky=E)

        Button(self.win2, text = "Cancel", command=self.Cancel).grid(row=5,column=1,sticky=E)
        Button(self.win2, text = "Register", command=self.RegisterNew).grid(row=5,column=2,sticky=E)


    def Connect(self):
        
        try:
            database = pymysql.connect(host = 'academic-mysql.cc.gatech.edu', user = 'lbeall3', passwd = 'CbN0QnRX', db = 'cs2316db')
            return database
        
        except:
            messagebox.showwarning("Error", "Please check your Internet connection!")

    def RegisterNew(self):

        pw1 = self.sv6.get()
        un2 = self.sv4.get()
        pw2 = self.sv5.get()
        lastname = self.sv3.get()

        if pw1 != pw2:
            messagebox.showwarning("Error", "Please type in the same password twice")
            return None

        if un2 == "" or pw2 == "":
            messagebox.showwarning("Error", "Please type in username and password!")
            return None

        nList = []
        uList = []
        
        for item in pw1:
            a = ord(item)
            if a >= 65 and a <= 90:
                uList.append(a)
            if a >= 48 and a <= 57:
                nList.append(a)

        if uList == [] or nList == []:
            messagebox.showwarning("Error", "Incorrect Password")
            return None

        db = self.Connect()
        cursor = db.cursor()

        cursor.execute("SELECT Username FROM ReservationUser")
        UNList = []
        for u in cursor:
            u = u[0].upper()
            UNList.append(u)

        for item in UNList:
            new = un2.upper()
            if item == new:
                messagebox.showwarning("Error" , "Sorry that username already exists")
                db.close()
                return None

        if lastname != "":

            cursor.execute("INSERT INTO ReservationUser (Username, Password, LastName) VALUES (%s, %s, %s)", (un2, pw1, lastname))

            db.commit()
            db.close()
        else:

            cursor.execute("INSERT INTO ReservationUser (Username, Password) VALUES (%s, %s)", (un2, pw1))

            db.commit()
            db.close()

        messagebox.showwarning("Registration Successful", "You are now registered")

        self.win2.withdraw()
        self.win.deiconify()

    def LoginCheck(self):

        db = self.Connect()
        cursor = db.cursor()

        un1 = self.sv.get()
        pw1 = self.sv2.get()

        upper = un1.upper()

        cursor.execute("SELECT Password FROM ReservationUser WHERE UPPER(Username) LIKE %s", upper)
                       
        pwList = []

        for pw in cursor:
            pwList.append(pw)

        for item in pwList:

            if item[0] == pw1:
                messagebox.showwarning("Successful", "Login was a success!")
                self.win.withdraw()
                self.Homepage()
                return None

        messagebox.showwarning("Error", "Sorry the username/password is unrecognizable")


    def Exit(self):

        self.win.withdraw()

    def Cancel(self):

        self.win2.withdraw()
        self.win.deiconify()


    def Homepage(self):

        self.hpwin = Toplevel()
        self.hpwin.title("Room Reservation Homepage")

        Label(self.hpwin, text = "Welcome to GT Room Reservation System!", relief = "raised").grid(row=0,column=1,columnspan = 3,sticky = EW)

        self.username = self.sv.get()
        self.string = StringVar()
        self.string2 = StringVar()
        db = self.Connect()
        cursor = db.cursor()

        self.res = Frame(self.hpwin)

        cursor.execute("SELECT * FROM RoomReservations WHERE ReservedBy LIKE %s", self.username)
        Label(self.res, text = "Current Reservations").grid(row=0,column=0,sticky=W)

        resList = []

        for r in cursor:
            resList.append(r)

        z = len(resList)

        stringList = []


        if z == 2:

            building = resList[0][0]
            floor = resList[0][1]
            number = resList[0][2]
            day = resList[0][3]
            time = resList[0][4]

            aStr = "Room {0} on {1} floor {2} is reserved for {3} at {4} hours.".format(number, building, floor, day, time)
            self.one = Entry(self.res, textvariable = self.string,width=50)
            self.one.grid(row=0,column=1)
            self.string.set(aStr)

            building2 = resList[1][0]
            floor2 = resList[1][1]
            number2 = resList[1][2]
            day2 = resList[1][3]
            time2 = resList[1][4]

            bStr = "Room {0} on {1} floor {2} is reserved for {3} at {4} hours.".format(number2, building2, floor2, day2, time2)
            self.one = Entry(self.res, textvariable = self.string2,width=50)
            self.one.grid(row=1,column=1)
            self.string2.set(bStr)

        if z == 1:

            building = resList[0][0]
            floor = resList[0][1]
            number = resList[0][2]
            day = resList[0][3]
            time = resList[0][4]

            aStr = "Room {0} on {1} floor {2} is reserved for {3} at {4} hours.".format(number, building, floor, day, time)
            self.one = Entry(self.res, textvariable = self.string,width=50)
            self.one.grid(row=0,column=1)
            self.string.set(aStr)

        if z == 0:

            self.room = Entry(self.res, textvariable = self.string, width=50)
            self.string.set("No Reservations")
            self.room.grid(row=0,column=1,sticky=W)

        self.res.grid(row=1, column=0, columnspan=5,sticky=W)

        Label(self.hpwin, text = "Make New Reservations:").grid(row=2,column=0,sticky=W)

        self.v = StringVar()
        self.v.set(" ")
        self.v2 = StringVar()
        self.v2.set(" ")
        self.v3 = StringVar()
        self.v3.set(" ")
        self.v4 = IntVar()
        self.v5 = IntVar()


        self.f1 = Frame(self.hpwin, relief = "sunken", borderwidth = 2)
        self.f2 = Frame(self.hpwin, relief = "sunken", borderwidth = 2)
        self.f3 = Frame(self.hpwin, relief = "sunken", borderwidth = 2)
        self.f4 = Frame(self.hpwin, relief = "sunken", borderwidth = 2)
        self.f5 = Frame(self.hpwin, relief = "sunken", borderwidth = 2)
        
        #First set of radiobuttons
        f1L = Label(self.f1, text = "Day Choices")
        
        rb1 = Radiobutton(self.f1, text="Monday", variable=self.v, value="Monday")
        rb2 = Radiobutton(self.f1, text="Tuesday", variable=self.v, value="Tuesday")
        rb3 = Radiobutton(self.f1, text="Wednesday", variable=self.v, value="Wednesday")
        rb4 = Radiobutton(self.f1, text="Thursday", variable=self.v, value="Thursday")
        rb5 = Radiobutton(self.f1, text="Friday", variable=self.v, value="Friday")

        rb1.grid(row=1,column=0,sticky=W)
        rb2.grid(row=2,column=0,sticky=W)
        rb3.grid(row=3,column=0,sticky=W)
        rb4.grid(row=4,column=0,sticky=W)
        rb5.grid(row=5,column=0,sticky=W)

        f1L.grid(row=0,column=0)

        self.f1.grid(row=3,column=0)
        
        #Second set of radiobuttons
        f2L = Label(self.f2, text = "Time Choices")
        f2L.grid(row=0,column=0)
        
        rb1a = Radiobutton(self.f2, text="Morning", variable=self.v2, value="Morning")
        rb2a = Radiobutton(self.f2, text="Afternoon", variable=self.v2, value="Afternoon")
        rb3a = Radiobutton(self.f2, text="Evening", variable=self.v2, value="Evening")
        rb4a = Radiobutton(self.f2, text="Night", variable=self.v2, value="Night")

        rb1a.grid(row=1,column=0,sticky=W)
        rb2a.grid(row=2,column=0,sticky=W)
        rb3a.grid(row=3,column=0,sticky=W)
        rb4a.grid(row=4,column=0,sticky=W)

        self.f2.grid(row=3,column=1,sticky=EW)

        #Third set of radionbuttons
        f3L = Label(self.f3, text = "Building Choices")
        f3L.grid(row=0,column=0)

        rb1b = Radiobutton(self.f3, text="CULC", variable=self.v3, value="CULC")
        rb2b = Radiobutton(self.f3, text="Klaus", variable=self.v3, value="Klaus")

        rb1b.grid(row=1,column=0,sticky=W)
        rb2b.grid(row=2,column=0,sticky=W)

        self.f3.grid(row=3,column=2,sticky=EW)


        #Fourth set of radiobuttons
        f4L = Label(self.f4, text = "Floor Choices")
        f4L.grid(row=0,column=0)

        rb1c = Radiobutton(self.f4, text="1", variable=self.v4, value=1)
        rb2c = Radiobutton(self.f4, text="2", variable=self.v4, value=2)
        rb3c = Radiobutton(self.f4, text="3", variable=self.v4, value=3)
        rb4c = Radiobutton(self.f4, text="4", variable=self.v4, value=4)

        rb1c.grid(row=1,column=0,sticky=W)
        rb2c.grid(row=2,column=0,sticky=W)
        rb3c.grid(row=3,column=0,sticky=W)
        rb4c.grid(row=4,column=0,sticky=W)

        self.f4.grid(row=3,column=3,sticky=EW)

        #Fifth set of radiobuttons
        f5L = Label(self.f5, text = "Room Choices")
        f5L.grid(row=0,column=0)

        rb1d = Radiobutton(self.f5, text="1", variable=self.v5, value=1)
        rb2d = Radiobutton(self.f5, text="2", variable=self.v5, value=2)
        rb3d = Radiobutton(self.f5, text="3", variable=self.v5, value=3)
        rb4d = Radiobutton(self.f5, text="4", variable=self.v5, value=4)
        rb5d = Radiobutton(self.f5, text="5", variable=self.v5, value=5)
        rb6d = Radiobutton(self.f5, text="6", variable=self.v5, value=6)
        rb7d = Radiobutton(self.f5, text="7", variable=self.v5, value=7)
        rb8d = Radiobutton(self.f5, text="8", variable=self.v5, value=8)
        rb9d = Radiobutton(self.f5, text="9", variable=self.v5, value=9)
        rb10d = Radiobutton(self.f5, text="10", variable=self.v5, value=10)

        rb1d.grid(row=1,column=0,sticky=W)
        rb2d.grid(row=2,column=0,sticky=W)
        rb3d.grid(row=3,column=0,sticky=W)
        rb4d.grid(row=4,column=0,sticky=W)
        rb5d.grid(row=5,column=0,sticky=W)
        rb6d.grid(row=1,column=1,sticky=W)
        rb7d.grid(row=2,column=1,sticky=W)
        rb8d.grid(row=3,column=1,sticky=W)
        rb9d.grid(row=4,column=1,sticky=W)
        rb10d.grid(row=5,column=1,sticky=W)

        self.f5.grid(row=3,column=4,sticky=EW)

        self.b1 = Button(self.hpwin, text = "Cancel All Reservations", command = self.cancelReservation)
        self.b1.grid(row=4,column=0,sticky=EW)

        self.b2 = Button(self.hpwin, text = "Check Avaliable Options", command = self.availableReservations)
        self.b2.grid(row=4,column=1,columnspan = 2,sticky=EW)

        self.b3 = Button(self.hpwin, text = "Stats", command = self.stats)
        self.b3.grid(row=4,column=3,sticky=EW)

        self.b4 = Button(self.hpwin, text = "Logout",command = self.Logout)
        self.b4.grid(row=4,column=4,sticky=EW)

    def availableReservations(self):
        

        if self.v.get() == 0 or self.v2.get() == 0 or self.v3.get() == 0 or self.v4.get() == 0 or self.v5.get() == 0:
            messagebox.showwarning("Search Failure", "Please choose a valid option from each category")
            return None

        
        db = self.Connect()
        cursor = db.cursor()

        day = self.v.get()
        time = self.v2.get()
        building = self.v3.get()
        floor = self.v4.get()
        room = self.v5.get()
        
        if time == "Morning":
            timeList = ["08:00", "09:00", "10:00", "11:00"]
        if time == "Afternoon":
            timeList = ["12:00", "01:00", "02:00", "03:00"]
        if time == "Evening":
            timeList = ["16:00", "17:00", "18:00", "19:00"]
        if time == "Night":
            timeList = ["20:00", "21:00", "22:00", "23:00"]

        
        #checking for reserved rooms during the time slot    
        sql = "SELECT Time FROM RoomReservations WHERE (RoomNo, Building, Floor, Day) = (%s, %s, %s, %s)"
        cursor.execute(sql, (room, building, floor, day))

        tList = []

        for i in cursor:
            tList.append(i[0])


        x = 0

        for i in tList:
            for t in timeList:
                if i == t:

                    x = x + 1
                
        if x ==4:
            
            messagebox.showwarning("Search Failure", "Sorry! But this room is unavailable for the selected day and time.")
            return None

        cursor.execute("SELECT * FROM RoomReservations WHERE ReservedBy LIKE %s", self.username)

        aList = []

        for i in cursor:
            aList.append(i)
            

        if len(aList) == 2:

            messagebox.showwarning("Error", "You can only make 2 reservations per week. Try again next week")
            return None

        self.hpwin.withdraw()

        self.arooms = Toplevel()
        self.arooms.title("Available Rooms")

        Label(self.arooms, text = "Building", relief = "raised").grid(row=0,column=0,sticky=EW)
        Label(self.arooms, text = "Floor", relief = "raised").grid(row=0,column=1,sticky=EW)
        Label(self.arooms, text = "Room", relief = "raised").grid(row=0,column=2,sticky=EW)
        Label(self.arooms, text = "Day", relief = "raised").grid(row=0,column=3,sticky=EW)
        Label(self.arooms, text = "Time", relief = "raised").grid(row=0,column=4,sticky=EW)
        Label(self.arooms, text = "Select", relief = "raised").grid(row=0,column=5,sticky=EW)

        finalList = []

        for item in timeList:
            if item not in tList:
                finalList.append(item)


        x = 1
        self.t = IntVar()


        for i in range(len(finalList)):

            l = Label(self.arooms, text = building)
            l.grid(row=x,column=0)

            l2 = Label(self.arooms, text = floor)
            l2.grid(row=x,column=1)

            l3 = Label(self.arooms, text = room)
            l3.grid(row=x,column=2)

            l4 = Label(self.arooms, text = day)
            l4.grid(row=x,column=3)

            l5 = Label(self.arooms, text = finalList[i])
            l5.grid(row=x,column=4)

            rb = Radiobutton(self.arooms, variable = self.t, value=x)
            rb.grid(row=x,column=5)

            x = x + 1

        Button(self.arooms, text = "Submit Reservation",command= self.makeReservation).grid(row=x+1,column=3,columnspan=2)
        Button(self.arooms, text = "Cancel", command=self.CancelRes).grid(row=x+1,column=5)

        self.finalList = finalList

    def CancelRes(self):

        self.arooms.withdraw()
        self.hpwin.deiconify()

    def makeReservation(self):

        db = self.Connect()
        cursor = db.cursor()

        value = self.t.get()
        v = value - 1

        day = self.v.get()
        b = self.v3.get()
        floor = self.v4.get()
        room = self.v5.get()
        time = self.finalList[v]

        if self.t.get() == 0:

            messagebox.showwarning("Error", "Please select one of the available times or press cancel to return to the homepage.")
            return None

        else:

            sql = "INSERT INTO RoomReservations (Building, Floor, RoomNo, Day, Time, ReservedBy) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (b, floor, room, day, time, self.username))
            db.commit()

            sql2 = "SELECT NumberOfReservations FROM ReservationUser WHERE Username = %s"
            cursor.execute(sql2, self.username)

            nList = []
            for num in cursor:
                nList.append(num[0])

            new = int(nList[0]) + 1


            cursor.execute("UPDATE ReservationUser SET NumberOfReservations = %s WHERE Username = %s", (new, self.username))

            db.commit()
            db.close()

            messagebox.showwarning("Reservation Completion", "You have reserved your room. Click OK to go back to Homepage.")

            self.arooms.withdraw()
            self.Homepage()

    def cancelReservation(self):

        db = self.Connect()
        cursor = db.cursor()

        select = "SELECT NumberOfReservations FROM ReservationUser WHERE Username = %s"
        cursor.execute(select, self.username)

        sList = []

        for s in cursor:
            sList.append(s[0])


        if sList[0] != 0:

            sql = "DELETE FROM RoomReservations WHERE ReservedBy = %s"

            cursor.execute(sql, self.username)

            db.commit()

            sql2 = "UPDATE ReservationUser SET NumberOfReservations = %s WHERE Username = %s"
            cursor.execute(sql2, (0,self.username))

            db.commit()
            db.close()

            messagebox.showwarning("Cancellation Completion", "Congratulations! You have cancelled your previous reservations.")
            self.hpwin.withdraw()
            self.Homepage()
            return None
        else:
            
            messagebox.showwarning("Error", "You already have zero reservations scheduled.")
            return None

    def stats(self):

        db = self.Connect()
        cursor = db.cursor()

        self.hpwin.withdraw()

        self.stat = Toplevel()
        self.stat.title("Statistics")

        Label(self.stat, text = "The average number of reservations per person is:").grid(row=0,column=0)
        Label(self.stat, text = "The busiest building:").grid(row=1,column=0, sticky=E)

        self.stat1 = StringVar()
        self.stat2 = StringVar()

        self.se1 = Entry(self.stat, textvariable = self.stat1, width=50)
        self.se1.grid(row=0,column=1,sticky=EW)
        self.se1.config(state = "readonly")

        self.se2 = Entry(self.stat, textvariable = self.stat2,width=50)
        self.se2.grid(row=1,column=1,sticky=EW)
        self.se2.config(state = "readonly")

        Button(self.stat, text = "Back", command = self.backstat).grid(row=3,column=1,sticky=EW)
        

        sql = "SELECT * FROM RoomReservations"
        cursor.execute(sql)

        cList = []

        for item in cursor:
            cList.append(item)

        totalres = len(cList)

        sql2 = "SELECT * FROM ReservationUser"
        cursor.execute(sql2)

        uList = []

        for item in cursor:
            uList.append(item)

        totalpeople = len(uList)

        avg = totalres / totalpeople
        self.stat1.set(avg)

        sql2 = "SELECT * FROM RoomReservations WHERE Building LIKE 'CULC'"
        cursor.execute(sql2)

        CULCList = []
        kList = []
        
        for b in cursor:
            CULCList.append(b)
            

        sql3 = "SELECT * FROM RoomReservations WHERE Building LIKE 'Klaus'"
        cursor.execute(sql3)

        for k in cursor:
            kList.append(k)


        if len(kList) > len(CULCList):

            diff = len(kList) - len(CULCList)
            self.stat2.set("Klaus is more busy with {0} reservations so far.".format(diff))

        if len(kList) < len(CULCList):

            diff = len(CULCList) - len(kList)
            self.stat2.set("CULC is more busy with {0} reservations so far.".format(diff))

        if len(kList) == len(CULCList):

            r = len(kList)
            self.stat2.set("Both are busy with {0} reservations so far.".format(r))
            
    def backstat(self):

        self.stat.withdraw()
        self.hpwin.deiconify()

    def Logout(self):

        self.hpwin.withdraw()
        self.win.deiconify()
        
        
        
win = Tk()
app = HW9b(win)
win.mainloop()      
