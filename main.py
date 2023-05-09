import os
from collections import OrderedDict
from functools import partial #Lambda
import sqlite3 as sql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# from tkinter import dnd Not in 3.4.2?
from datetime import datetime
# import pickle
import csv
import re

#module for encryption
import binascii

# import filedialog module
from tkinter import filedialog

class FileHandler():
    """Handles the file operations"""
    def __init__(self, file) -> None:
        """Initialises the file handler"""
        global conn
        self.file = file

        self.key = "Your dad loves you! Get in the robot Shinji!"
        
        #Open file if exists, else create new shcema in memory (file will be created on save)
        if os.path.isfile(file):
            self.openFile()
        else:
            conn = sql.connect(":memory:")
            self.createTables()
            conn.commit()
    
    def openFile(self):
        """Opens and decrypts the file. Creates a database in memory"""
        global conn
        #Read and decrypt encrypted File to memory sql
        f = open(self.file, "r", encoding="utf-8")
        fContents = f.read()

        #Decrypt file into sql statement
        decryptedFile = self.decrypt(fContents)

        splash.destroy()
        # Create a database in memory and import from decryptedFile
        conn = sql.connect(":memory:")
        conn.cursor().executescript(decryptedFile)
        conn.commit()
        
    def closeFile(self):
        """Saves database into encrypted file and creates a backup for the current day"""        
        os.makedirs("backups", exist_ok=True)
        
        # Create a backup of the current database
        print("Backup created: " + "backups/" + datetime.now().strftime("%d-%m-%Y") + ".lzl")
        self.saveFile("backups/" + datetime.now().strftime("%d-%m-%Y") + ".lzl")
        
        # Save the current database to the file
        self.saveFile(self.file)
        conn.close()
        
        
    def saveFile(self, file = "savedata.lzl"):
        """Saves the database in memory into an encrypted file"""
        #Transforms the sql in memory into an sql statement to be encoded
        sqlStatement = ""
        for line in conn.iterdump():
            sqlStatement += line

        #Encrypt the sql statement
        encryptedSql = self.encrypt(sqlStatement)

        #Serialise the encrypted statement in a file
        encryptedFile = open(file, "w" , encoding="utf-8")
        encryptedFile.write(encryptedSql)
        encryptedFile.close()
        print("Saved Encrypted File as: " + file)
    
    def encrypt(self, message):
        # Convert message and key to byte arrays
        message_bytes = message.encode('utf-8')
        key_bytes = self.key.encode('utf-8')

        # # XOR each byte of the message with the corresponding byte of the key
        # encrypted_bytes = bytes([message_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(message_bytes))])

        # # Convert encrypted bytes to a string
        # encrypted_message = encrypted_bytes.hex()

        # Convert message and key to bytes objects
        message_bytes = message.encode('utf-8')
        key_bytes = self.key.encode('utf-8')

        # XOR each byte of the message with the corresponding byte of the key
        encrypted_bytes = bytearray()
        for i in range(len(message_bytes)):
            encrypted_byte = message_bytes[i] ^ key_bytes[i % len(key_bytes)]
            encrypted_bytes.append(encrypted_byte)

        # Convert encrypted bytes to a string
        encrypted_message = binascii.hexlify(encrypted_bytes).decode('utf-8')
        
        return encrypted_message

    def decrypt(self, encrypted_message):
        # Convert encrypted message and key to byte arrays
        encrypted_bytes = bytes.fromhex(encrypted_message)
        key_bytes = self.key.encode('utf-8')

        # XOR each byte of the encrypted message with the corresponding byte of the key
        decrypted_bytes = bytes([encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])

        # Convert decrypted bytes to a string
        decrypted_message = decrypted_bytes.decode('utf-8')
        return decrypted_message

    def createTables(self):
        """Creates the tables in the database"""
        c = conn.cursor()
        c.execute("""
                CREATE TABLE IF NOT EXISTS EMPLOYEE (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT(24),
                    password TEXT(24),
                    forename TEXT(24),
                    surname TEXT(24),
                    sex INTEGER,
                    title TEXT(4),
                    birthdate TEXT(10),
                    hire_date TEXT(10),
                    job_description TEXT(20),
                    town TEXT(30),
                    county TEXT(15),
                    postcode TEXT,
                    phone_num TEXT(11),
                    email TEXT(40)
            );""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS TEACHER (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT(24),
                    password TEXT(24),
                    forename TEXT(24),
                    surname TEXT(24),
                    sex INTEGER,
                    title TEXT(4),
                    birthdate TEXT(10),
                    hire_date TEXT(10),
                    town TEXT(30),
                    county TEXT(15),
                    postcode TEXT,
                    phone_num TEXT(11),
                    email TEXT(40)
            );""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS CUSTOMER (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    forename TEXT(24),
                    surname TEXT(24),
                    sex INTEGER,
                    title TEXT(4),
                    birthdate TEXT(10),
                    town TEXT(30),
                    county TEXT(15),
                    postcode TEXT,
                    phone_number TEXT(11),
                    email TEXT(40)
                );
                """)
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS STUDENT (
                    ID INTEGER,
                    username TEXT(24),
                    password TEXT(24),
                    forename TEXT(24),
                    surname TEXT(24),
                    sex INTEGER,
                    title TEXT(4),
                    birthdate TEXT(10),
                    town TEXT(30),
                    county TEXT(15),
                    postcode TEXT,
                    phone_number TEXT(11),
                    guardian_phone_num TEXT(11),
                    email TEXT(40)
                );
                """)
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS STUDENT_BOOKING (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    StudentID INTEGER(8),
                    TeacherID INTEGER(8),
                    location TEXT(12),
                    lesson_frequency INTEGER,
                    lesson_day TEXT(12),
                    lesson_time TEXT(5),
                    lesson_length INTEGER(8),
                    lesson_cost NUMERIC(1),
                    booking_date TEXT(10),
                    last_update TEXT(10),
                    cancelled INTEGER,
                    FOREIGN KEY(StudentID) REFERENCES STUDENT(ID),
                    FOREIGN KEY(TeacherID) REFERENCES TEACHER(ID)
                );
                """)
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS LESSON_REPORT (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LessonPlansID INTEGER(8),
                    StudentID INTEGER(8),
                    TeacherID INTEGER(8),
                    attended INTEGER(1),
                    student_behaviour INTEGER(2),
                    notes TEXT(50000),
                    date TEXT(10),
                    FOREIGN KEY(StudentID) REFERENCES STUDENT(ID),
                    FOREIGN KEY(TeacherID) REFERENCES TEACHER(ID)
                );
                """)
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS LESSON_PLAN (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_title TEXT(50),
                    lesson_objective TEXT(50),
                    materials TEXT(50),
                    procedure TEXT(50000)
                )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS MUSIC_ITEM (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT(50),
                    type TEXT(50),
                    model TEXT(50),
                    price NUMERIC(5),
                    serial_num TEXT(20)
                    )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS CAFE_ITEM (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT(50),
                    description TEXT(50),
                    price NUMERIC(5),
                    expiry_date TEXT(10)
                    )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS CAFE_INVENTORY (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CafeItemID INTEGER(8),
                    count INTEGER(8),
                    date TEXT(10),
                    FOREIGN KEY(CafeItemID) REFERENCES CAFE_ITEM(ID)
                    )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS MUSIC_INVENTORY (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MusicItemID INTEGER(8),
                    count INTEGER(8),
                    date TEXT(10),
                    FOREIGN KEY(MusicItemID) REFERENCES MUSIC_ITEM(ID)
                    )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS CAFE_SALES (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    CafeItemID INTEGER(8),
                    CustomerID INTEGER(8),
                    count INTEGER(8),
                    date TEXT(10),
                    FOREIGN KEY(CafeItemID) REFERENCES CAFE_ITEM(ID),
                    FOREIGN KEY(CustomerID) REFERENCES CUSTOMER(ID)
                    )""")
        
        c.execute("""
                CREATE TABLE IF NOT EXISTS MUSIC_SALES (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    MusicItemID INTEGER(8),
                    CustomerID INTEGER(8),
                    count INTEGER(8),
                    date TEXT(10),
                    FOREIGN KEY(MusicItemID) REFERENCES MUSIC_ITEM(ID),
                    FOREIGN KEY(CustomerID) REFERENCES CUSTOMER(ID)
                    )""")

        c.close()

class App(Tk):
    """Class for handling tkinter window"""
    def __init__(self, minwidth = 800, minheight = 500):
        super().__init__()
        
        self.title('Lizzy Lee\'s All-Purpose Handler')
        self.iconbitmap("Lizzy Lees Logo.ico")
        self.minsize(width=minwidth, height=minheight)

        #Place in middle
        self.update()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        geometry = "+" + str(x) + "+" + str(y)
        self.geometry(geometry).format(x,y)

class Splash(App):
    """Creates a splash screen"""
    def __init__(self, width, height, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.overrideredirect(True) # Removes title bar
        self.wm_attributes('-topmost', True)
        
        self.width = width
        self.height = height
        x = (self.winfo_screenwidth() - self.width)/2
        y = (self.winfo_screenheight() - self.height)/2
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.update()


class Login(App):
    """Class for handling the login screen"""
    ###Class for handling the application###
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        
        # Create a label for the user name
        user_label = Label(self, text='Username:')
        user_label.pack()

        # Create an entry field for the user name
        self.user_entry = Entry(self)
        self.user_entry.bind("<Return>", lambda e: self.checkCredentials())
        self.user_entry.pack()

        # Create a label for the password
        pass_label = Label(self, text='Password:')
        pass_label.pack()

        # Create an entry field for the password
        self.pass_entry = Entry(self, show='*')
        self.pass_entry.bind("<Return>", lambda e: self.checkCredentials())
        self.pass_entry.pack()

        # Create a button to check the user credentials
        check_button = Button(self, text='Login', command=self.checkCredentials)
        check_button.pack()
        
        # Create a button to skip login
        check_button = Button(self, text='Just get me in there', command=self.skip)
        check_button.pack()

        # Run the window
        self.mainloop()
    
    ### Temporary function to skip login for debuggig
    def skip(self):
        """Dev function to skip login with manager access for debugging"""
        # Open the main window
        self.destroy()
        global userRole
        userRole = "manager"
        PrimaryApp(1400, 700)
        return
        
    def checkCredentials(self):
        """Function to check the user credentials"""
        #Get the username and password from the entry fields
        username = self.user_entry.get().lower()
        password = self.pass_entry.get()

        #Define array to contain all table names
        tables = []
        
        #Get all table names
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        for queryResult in c.fetchall():
            if queryResult[0] != "sqlite_sequence":
                tables.append(queryResult[0])
                
        #For each table
        for table in tables:
            #Get all data from table
            sqlStatement = "SELECT * FROM " + table
        
            c= conn.cursor()
            queryResults = c.execute(sqlStatement)
            
            #Get Table Columns
            for col in queryResults.description:
                #If there is a 'username' column
                if col[0] == "username":
                    #Get username and password details from table
                    sqlStatement = "SELECT id, username, password FROM " + table
                    queryResults = c.execute(sqlStatement).fetchall()
                    #Search through stored records for match
                    for records in queryResults:
                        #If credentials MATCH data
                        if (username == records[1].lower()) and (password == records[2]):
                            #Get table name
                            #Check if table_name is equal to 'employees'
                            if table == 'EMPLOYEE':
                                #Get job description
                                permission = c.execute(str("SELECT job_description FROM EMPLOYEE WHERE id = '" + str(records[0]) + "'")).fetchone()[0]
                            else:
                                permission = table

                            global loggedInUserID, loggedInUserTable, userRole
                            loggedInUserID = c.execute(str("SELECT ID FROM " + table + " WHERE password = '" + password + "'")).fetchone()[0]
                            loggedInUserTable = table
                            userRole = permission.lower()
                            print(loggedInUserID)

                            self.destroy()

                            #Grant user access to employee dashboard
                            print(permission)
                            PrimaryApp(1400, 700)
                            return #Exit method
                        
        # Display an error message if no match found
        messagebox.showerror('Error', 'Invalid credentials')                            
        c.close() #Close cursor
                    
    
class PrimaryApp(App):
    """Subclass for handling the main window"""
    ###Class for handling the application###
    def __init__(self, *args, **kwargs):
        super(PrimaryApp, self).__init__(*args, **kwargs)

        self.title("Lizzy Lee's - " + titleCase(userRole) + " Dashboard")
        #Hide window until it is ready to show
        self.withdraw()

        #Define array to contain all table names
        self.tables = []
        
        #Get all table names for use thoroughout program
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        for queryResult in c.fetchall():
            if queryResult[0] != "sqlite_sequence":
                self.tables.append(queryResult[0])
        print("Tables: " + str(self.tables))
        c.close()

        #Define Menubar
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        
        #Set Grid to expand with window resizes
        # self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1) #Expand vertically
        self.grid_columnconfigure(1, weight=1)
        
        ### MENUBAR ###
        fileMenu = Menu(self)
        
        fileMenu.add_command(label="Save", command=self.save, underline=0)
        fileMenu.add_command(label="Logout", command=self.logOut)
        fileMenu.add_command(label="Exit", command=self.onExit)
        self.menubar.add_cascade(label = 'File', menu=fileMenu, underline=0)

        if userRole == "manager" or userRole == "employee":
            editMenu = Menu(self)
            editMenu.add_command(label = "Import", command = self.importWin)
            editMenu.add_command(label = "Export", command = self.exportWin)
            self.menubar.add_cascade(label = 'Edit', menu=editMenu, underline=0)
            
        #Set callback for window close button        
        self.protocol("WM_DELETE_WINDOW", self.onExit)
        
        ##### !!! SIDEBAR !!! #####
        sidebarFrame = Frame(self, width = 120)
        sidebarFrame.grid(row = 0, column=0, sticky="ns")

        #Records
        recordsButton = Button(sidebarFrame, text = "Records", command=selectRecords)
        recordsButton.place(width = 80, height = 30, relx = 0.1616, rely = 0.2)
        
        #Only the employees can't access the lessons
        if userRole != "employee":
            #Lessons
            lessonsButton = Button(sidebarFrame, text = "Lessons", command=selectLessons)
            lessonsButton.place(width = 80, height = 30, relx = 0.1616, rely = 0.4)
        
        #Managers and employees can access stock
        if userRole == "manager" or userRole == "employee":
            #Stock
            stockButton = Button(sidebarFrame, text = "Stock", command=selectStock)
            stockButton.place(width = 80, height = 30, relx = 0.1616, rely = 0.6)
        
        #Managers and employees can access sales
        if userRole == "manager" or userRole == "employee":
            #Sales
            salesButton = Button(sidebarFrame, text = "Sales", command=selectSales)
            salesButton.place(width = 80, height = 30, relx = 0.1616, rely = 0.8)
            
        ### !!! MENU SELECTION FRAME !!! ###
        menuSelectionFrame = Frame(self)
        menuSelectionFrame.grid(row = 0, column=1, sticky="nesw")

        menuSelectionFrame.grid_columnconfigure(0, weight=1)
        menuSelectionFrame.grid_rowconfigure(0, weight=1)

        ### !!! RECORDS FRAME !!! ###
        global recordFrame
        recordFrame = Frame(menuSelectionFrame)
        recordFrame.pack(fill = "both", expand = 1)
        
        recordTabs = ttk.Notebook(recordFrame)
        recordTabs.pack(fill = "both", expand = 1)        
        
        ### --- EMPLOYEE TAB --- ###
        #Only managers and employees can access the employee tab
        if userRole == "manager" or userRole == "employee":
            employeeTab = PrimaryTab(self, recordTabs, "Employees")
            employeeRecord = Record(employeeTab, "EMPLOYEE")
            employeeRecord.grid(row = 0, column=0, sticky="nesw")
    
        ### --- TEACHER TAB --- ###
        #Only managers and teachers can access the teacher tab
        if userRole == "manager" or userRole == "teacher":
            teacherTab = PrimaryTab(self, recordTabs, "Teacher")
            teacherRecord = Record(teacherTab, table="TEACHER")
            teacherRecord.grid(row = 0, column = 0, sticky="nesw")

        ### --- STUDENT TAB --- ###validate
        #Only employees can't access the student tab
        if userRole != "employee":
            studentTab = PrimaryTab(self, recordTabs, "Student")
            studentRecord = Record(studentTab, table="STUDENT")
            studentRecord.grid(row = 0, column = 0, sticky="nesw")
            
        ### --- CUSTOMER TAB --- ###
        if userRole == "manager" or userRole == "employee":
            customerTab = PrimaryTab(self, recordTabs, "Customer")
            customerRecord = Record(customerTab, table="CUSTOMER")
            customerRecord.grid(row = 0, column = 0, sticky="nesw")
    
    
        #Only employees can't access the Lessons section
        if userRole != "employee":
        
            ### !!! LESSONS FRAME !!! ###
            global lessonFrame
            lessonFrame = Frame(menuSelectionFrame, width = 400, height = 400)
            
            #Create notebook for lesson tabs
            lessonTabs = ttk.Notebook(lessonFrame)
            lessonTabs.pack(fill = "both", expand = 1)


            bookingTab = PrimaryTab(self, lessonTabs, "Student Bookings")
            bookingFrame = Booking(bookingTab, "STUDENT_BOOKING")
            bookingFrame.grid(row = 0, column = 0, sticky = "nesw")
        
            #Only managers and teachers can access the lesson report and lesson plan tabs
            if userRole != "student":
                lessonReportTab = PrimaryTab(self, lessonTabs, "Lesson Report")
                lessonReportFrame = Report(lessonReportTab, "LESSON_REPORT")
                lessonReportFrame.grid(row = 0, column = 0, sticky = "nesw")
            
                lessonPlanTab = PrimaryTab(self, lessonTabs, "Lesson Plan")
                lessonPlanFrame = Plan(lessonPlanTab, "LESSON_PLAN")
                lessonPlanFrame.grid(row = 0, column = 0, sticky = "nesw")
    
    
        # only managers and employees can access stock and sales
        if userRole == "manager" or userRole == "employee":
        
            ### !!! STOCK FRAME !!! ###
            global stockFrame
            stockFrame = Frame(menuSelectionFrame, width = 400, height = 400)
            
            #Create notebook for stock tabs
            stockTabs = ttk.Notebook(stockFrame)
            stockTabs.pack(fill = "both", expand = 1)
            
            ### Create Primary Tabs for Stock
            musicItemTab = PrimaryTab(self, stockTabs, "Music Item")
            cafeItemTab = PrimaryTab(self, stockTabs, "Cafe Item")
            musicInventoryTab = PrimaryTab(self, stockTabs, "Music Inventory")
            cafeInventoryTab = PrimaryTab(self, stockTabs, "Cafe Inventory")
            
            musicItemFrame = Record(musicItemTab, "MUSIC_ITEM")
            musicItemFrame.grid(row = 0, column = 0, sticky = "nesw")
            
            cafeItemFrame = Record(cafeItemTab, "CAFE_ITEM")
            cafeItemFrame.grid(row = 0, column = 0, sticky = "nesw")
            
            musicInventoryFrame = Inventory(musicInventoryTab, "MUSIC_INVENTORY")
            musicInventoryFrame.grid(row = 0, column = 0, sticky = "nesw")
            
            cafeInventoryFrame = Inventory(cafeInventoryTab, "CAFE_INVENTORY")
            cafeInventoryFrame.grid(row = 0, column = 0, sticky = "nesw")
            
            
            ### !!! SALES FRAME !!! ###
            global salesFrame
            salesFrame = Frame(menuSelectionFrame, width = 400, height = 400, bg = "blue")
            
            salesTabs = ttk.Notebook(salesFrame)
            salesTabs.pack(fill = "both", expand = 1)
            
            ### Create Primary Tabs for Sales
            musicSalesTab = PrimaryTab(self, salesTabs, "Music Sales")
            cafeSalesTab = PrimaryTab(self, salesTabs, "Cafe Sales")
            
            musicSalesFrame = Sale(musicSalesTab, "MUSIC_SALES")
            musicSalesFrame.grid(row = 0, column = 0, sticky = "nesw")
            
            cafeSalesFrame = Sale(cafeSalesTab, "CAFE_SALES")
            cafeSalesFrame.grid(row = 0, column = 0, sticky = "nesw")
                      
    
        #Place window in middle of screen
        self.update()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2) - 40
        geometry = "+" + str(x) + "+" + str(y)
        self.geometry(geometry).format(x,y)
        
        #Show the window
        self.deiconify()
    
        #Run the mainloop
        self.mainloop()
    
    
    def onExit(self):
        """Function to run when the application is closed"""
        handler.closeFile()
        print("App Closing")  
        self.destroy()
        
    def logOut(self):
        """Function to log out of the current user account"""
        self.save()
        self.destroy()
        print("Logged out")
        Login()
        
    def save(self):
        """Function to save the current database"""
        handler.saveFile()
        
    def importWin(self):
        """Window for importing a CSV file into a table"""
        self.importWin = App(500, 300)
        self.importWin.title("Export table data")
        
        importText = Label(self.importWin, text = "Select '.csv' file and table to import data to", anchor = "center")
        importText.pack(side="top", fill="x")
        
        #Create listbox to display tables
        listbox = Listbox(self.importWin, selectmode = "single")
               
        # Add fancified table names to the listbox
        for table in self.tables:
            listbox.insert(END, titleCase(table))
        listbox.pack(fill="x")
        
        importButton = Button(self.importWin, text = "Import", command = lambda table=table: self.importCSV(self.tables[listbox.curselection()[0]]))
        importButton.pack(fill="x")

        self.importWin.mainloop()

    #Check if filename and tables are valid and then attempt to import file
    def importCSV(self, table):
        """Prompt user for '.csv' file to import into the specified table"""
        
        filename = filedialog.askopenfilename(
                                          title ="Select a File",
                                          filetypes = (("Comma Seperated Values files",
                                                       "*.csv*"),
                                                       ("all files",
                                                       "*.*")))
        
        if filename:
            f = open(filename, 'r', encoding='utf-8')
            
            #If table is not None:
            if (table != "None"):
                c = conn.cursor()
                
                sql = "SELECT MAX(id) FROM " + table
                c.execute(sql)
                last_id = c.fetchone()[0]
                c.close() 
                
                #If last_id is not an integer (therefore probably blank), set it to 0
                if type(last_id) is not int:
                    idValue = 0
                else:   
                    idValue = int(last_id)
                
                            
                #Pass the file object to reader() to get the reader object
                reader = csv.reader(f)

                #Convert the csv.reader object to a list
                rows = list(reader)

                #Get the headers from the first row of the CSV file
                headers = rows[0]
                
                # Iterate through each row of the CSV file after the first line
                for row in rows[1:]:
                    idValue += 1
                    
                    # Insert only the values from the headers with data into the sql table
                    sql = "INSERT INTO " + table +" (ID, "
                    
                    for column in headers:
                        sql += column + ", "
                    sql = sql[:-2] + ")"
                    
                    sql = sql + " VALUES (" + str(idValue) + ", \""
                    
                    for value in row:
                        sql += value + "\", \""
                    sql = sql[:-3]
                    sql += ");"
                    
                    # print(sql)
                    c = conn.cursor()
                    c.execute(sql)
                    conn.commit()
                    
                    c.close()
            f.close()             
    
    def exportWin(self):
        """Initialises window for exporting a table's contents to a CSV file"""
        self.exportWin = App(500, 300)
        self.exportWin.title("Export table data")
        
        exportText = Label(self.exportWin, text = "Select table to export to file in '.csv' format", anchor = "center")
        exportText.pack(side="top", fill="x")
        
        #Create listbox to display tables
        listbox = Listbox(self.exportWin, selectmode = "single")
               
        # Add fancified table names to the listbox
        for table in self.tables:
            listbox.insert(END, titleCase(table))
        listbox.pack(fill="x")
        
        #Export Button passes table name to exportTable function
        exportButton = Button(self.exportWin, text = "Export", command = lambda table=table: self.exportTable(self.tables[listbox.curselection()[0]]))
        exportButton.pack(fill="x")
        
        self.exportWin.mainloop()
        
    def exportTable(self, table):
        """Exports the contents of a table to a .csv file"""
        
        print("Table: " + table)
        
        filename = filedialog.asksaveasfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")), defaultextension = ".csv", initialfile= str(titleCase(table) + ".csv"))
        if filename:  # Check if a file was actually selected
            tableContents = []
            sqlStatement = "SELECT * FROM " + table
            
            c= conn.cursor()
            queryResults = c.execute(sqlStatement)
            
            #Get Table Columns
            headers = []
            for col in queryResults.description[1:]:
                headers.append(col[0])
                
            #Add contents of table to array
            fetchStatement = c.fetchall()
                    
            tableContents.append(headers)
            
            for row in fetchStatement:
                tableContents.append(row[1:])
            print(tableContents)
            c.close()

            # open file in write mode
            with open(filename, 'w', newline='') as file:
                # create a csv writer object
                csv_writer = csv.writer(file)
                
                # write the rows of data
                csv_writer.writerows(tableContents)
            
            self.exportWin.destroy()


class PrimaryTab(Frame):
    """Creates a Primary Tab that all other frames and tabs will lie under"""
    def __init__(self, root, tabHandler, name) -> None:
        super().__init__(root)
        
        self.name = name
        self.configure(bg="white")
        
        
        #Make children stretch horizontally
        self.grid_columnconfigure(0, weight = 1)
        self.grid(row=0, column=0, sticky="nesw")
        # self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        tabHandler.add(self, text = self.name)
                
        self.tabID = tabHandler.index("end") - 1



class TableFrame(Frame):
    """Creates a frame with a Treeview and scrollbars that will scale to fit the outmost frame"""
    def __init__(self, root, table = "", width = 0, height = 0) -> None:
        super().__init__(root)

        # #Set Style of application
        # self.style = ttk.Style(self)
        # self.style.theme_use('clam')

        self.table = table        
        self.columns = []
        self.sort = ""
        
        #If not blank table CONDITION FOR DEBUGGING
        if table != "":
            #Get Table Columns
            sqlCommand = """SELECT * FROM {}""".format(self.table)
            c = conn.cursor()
            queryResults = c.execute(sqlCommand)
            
            #Get Table Columns
            for col in queryResults.description:
                self.columns.append(col[0])
            c.close()

        #Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.grid_columnconfigure(0, minsize=width)
        self.grid_rowconfigure(0, minsize=height)

        self.treeFrame = Frame(self, bg="white") # Set Frame for table and scrollbars
        self.treeFrame.grid(column=0, row = 0, sticky="nesw")
        
        #Define The Table
        self.tree = ttk.Treeview(self.treeFrame, show="headings", selectmode="browse")
        
        self.tree.tag_configure('oddrow', background='#BBE6E4')
        self.tree.tag_configure('evenrow', background='#F0F6F6') 
        
        ####################################################################################
        ###### USE PLACE FOR THE TREEVIEW AND SCROLLBARS TO FIX THE OUT-OF-FRME ISSUE ######
        ####################################################################################
        self.tree.place(relx = 0, rely = 0, relwidth=1 , relheight = 1)

        # Set the header info
        self.tree['columns'] = [x for x in self.columns]
        for x in self.columns:
            
            #If column is password, notes, or procedure then make it invisible by setting width to 0
            if x == "password" or x == "notes" or x == "procedure":
                self.tree.column(x, anchor=CENTER, minwidth=0, width=0, stretch=False) 
            #If column is Lesson Title, Lesson Objective, Materials, or Procedure then make it's width larger  
            elif x == "lesson_title" or x == "lesson_objective" or x == "materials":
                print("LARGER WIDTH")
                self.tree.column(x, anchor=CENTER, minwidth=90, width=300, stretch=False)
            else:
                self.tree.column(x, anchor=CENTER, minwidth=30, width=120, stretch=False)   
                             
            self.tree.heading(x, text = titleCase(x), command=lambda x=x: self.headingPushed(x) ,anchor=CENTER)
            
            

        ### Scrollbars ###
        #Vertical
        self.verticalScroll = ttk.Scrollbar(self, orient = "vertical", command = self.tree.yview)
        self.verticalScroll.grid(row = 0, column = 1, sticky="ns")
        #Horizontal
        self.horizontalScroll = ttk.Scrollbar(self, orient = "horizontal", command = self.tree.xview)
        self.horizontalScroll.grid(row = 1, column = 0, sticky="ew")
        #Set Treeview to set scrollbar info
        self.tree.configure(yscrollcommand=self.verticalScroll.set)
        self.tree.configure(xscrollcommand=self.horizontalScroll.set)
        
        
        if (table!=""): #CONDITION USED FOR DEBUGGING
            self.fillTable()
    
    def fillTable(self, command = "*"):
        """Fills the table with the results of a SQL command"""
                
        c = conn.cursor()
        #If the userRole is the same as the table name then only show the logged in user's details
        if userRole == self.table.lower():
            command = """SELECT * FROM {} WHERE ID = '{}'""".format(self.table, loggedInUserID)
        elif command == "*":
            command = """SELECT {} FROM {}""".format(command, self.table)
        
        #sqlcommand is the command passed to the class by the user
        sqlCommand = command
        
        #If the user is a teacher then only show students that are connected to them through lesson bookings
        if userRole == "teacher" and self.table.lower() == "student":
            print("Getting students connected to teacher")            
            #sqlcommand2 is to only select students who are connected to the teacher through lesson bookings
            sqlCommand2 = """SELECT * FROM STUDENT WHERE ID IN (SELECT studentID FROM STUDENT_BOOKING WHERE teacherID = '{}')""".format(loggedInUserID)
            
            #Join the two commands
            sqlCommand = """SELECT DISTINCT t1.*
                FROM ({}) AS t1
                JOIN ({}) AS t2
                ON t1.ID = t2.ID""".format(sqlCommand2, sqlCommand)

        #If the user is a student then only show lesson bookings that that student has made
        elif userRole == "student" and self.table.lower() == "student_booking":
            print("Getting bookings connected to student")
            #sqlcommand2 is to only select bookings that are connected to the student
            sqlCommand2 = """SELECT * FROM STUDENT_BOOKING WHERE studentID = '{}'""".format(loggedInUserID)
            
            #Join the two commands
            sqlCommand = """SELECT DISTINCT t1.*
                FROM ({}) AS t1
                JOIN ({}) AS t2
                ON t1.ID = t2.ID""".format(sqlCommand2, sqlCommand)
                
        #If the user is a teacher and the table is either student_booking or lesson_report then only show results that are connected to that teacher
        elif userRole == "teacher" and (self.table.lower() == "student_booking" or self.table.lower() == "lesson_report"):
            print("Getting bookings connected to teacher")
            #sqlcommand2 is to only select students or bookings that are connected to the teacher
            sqlCommand2 = """SELECT * FROM '{}' WHERE teacherID = '{}'""".format(self.table, loggedInUserID)
            
            #Join the two commands
            sqlCommand = """SELECT DISTINCT t1.*
                FROM ({}) AS t1
                JOIN ({}) AS t2
                ON t1.ID = t2.ID""".format(sqlCommand2, sqlCommand)

        #Get SQL results
        c.execute(sqlCommand)
        queryResults = c.fetchall()
        self.insertRows(queryResults)
        c.close()

        return sqlCommand
        
    def insertRows(self, rows):
        """Inserts the rows from given list into the Treeview table"""
        #Clear Table
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        #Check the headers of the table for Foreign Keys, and if they are present then replace the values in the rows with a meaningful name from the foreign table
        # for each column
        for x in range(len(self.columns)):
            # if the column is a teacher foreign key
            if self.columns[x].lower() == "teacherid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Teacher", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the full name of the teacher from the foreign table
                    name = self.getForeignTablePersonName("TEACHER", row[x])
                    # print("TeacherID Found: " + str(name))
                    
                    #Replace the teacherID in the new row with the full name
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(name[0] + " " + name[1])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
                # print(newRecords)
                
            # if the column is a student foreign key
            elif self.columns[x].lower() == "studentid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Student", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the full name of the student from the foreign table
                    name = self.getForeignTablePersonName("STUDENT", row[x])
                    # print("StudentID Found: " + str(name))
                    
                    #Replace the studentID in the new row with the full name
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(name[0] + " " + name[1])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
                
            # if the column is a customer foreign key
            elif self.columns[x].lower() == "customerid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Customer", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the full name of the customer from the foreign table
                    name = self.getForeignTablePersonName("CUSTOMER", row[x])
                    
                    #Replace the customerID in the new row with the full name
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(name[0] + " " + name[1])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
                
            # if the column is a lesson_plan foreign key
            elif self.columns[x].lower() == "lessonplansid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Lesson Title", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the lesson title of the lesson_plan from the foreign table
                    title = self.getForeignTableLessonPlanTitle(row[x])
                    # print("LessonPlanID Found: " + str(title))
                    
                    #Replace the lessonPlanID in the new row with the lesson title
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(title[0])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
                
            # if the column is a cafe_item foreign key
            elif self.columns[x].lower() == "cafeitemid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Cafe Item", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the item name of the cafe_item from the foreign table
                    name = self.getForeignTableItemName("CAFE_ITEM", row[x], "description")
                    # print("CafeItemID Found: " + str(name))
                    
                    #Replace the cafeItemID in the new row with the item name
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(name[0])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
            
            # if the column is a music_item foreign key
            elif self.columns[x].lower() == "musicitemid":
                #Replace the header with a suitable name
                self.tree.heading(self.columns[x], text = "Music Item", command=lambda x=x: self.headingPushed(self.columns[x]) ,anchor=CENTER)
                newRecords = []
                for row in rows:
                    newRow = []
                    #Get the item name of the cafe_item from the foreign table
                    name = self.getForeignTableItemName("MUSIC_ITEM", row[x], "model")
                    # print("CafeItemID Found: " + str(name))
                    
                    #Replace the musicItemID in the new row with the item name
                    for y in range(len(row)):
                        if y == x:
                            newRow.append(name[0])
                        else:
                            newRow.append(row[y])
                    newRecords.append(newRow)
                #Replace rows with newRecords
                rows = newRecords
        
        #Insert into Table Columns
        count = len(rows)
        for row in rows:
            # print(row)
            record = []
            for x in range(len(row)):
                record.append(row[x])                
            
            #Insert into table with alternating row colours
            if(count%2 == 0):
                self.tree.insert("", END, values = record, tags = ('oddrow',))  
            else:
                self.tree.insert("", END, values = record, tags = ('evenrow',))  
            count +=1
        
    def getForeignTablePersonName(self, table, ID):
        """Gets the name of the person from the foreign table"""
        c = conn.cursor()
        sqlCommand = """SELECT forename, surname FROM {} WHERE ID = '{}'""".format(table, ID)
        c.execute(sqlCommand)
        queryResults = c.fetchall()
        c.close()
        return queryResults[0]
    
    def getForeignTableLessonPlanTitle(self, ID):
        """Gets the title of the lesson plan from the foreign table"""
        c = conn.cursor()
        sqlCommand = """SELECT lessonTitle FROM LESSON_PLAN WHERE ID = '{}'""".format(ID)
        c.execute(sqlCommand)
        queryResults = c.fetchall()
        c.close()
        return queryResults[0]
    
    def getForeignTableItemName(self, table, ID, column):
        """Gets the name of the cafe item from the foreign table"""
        c = conn.cursor()
        sqlCommand = """SELECT {} FROM {} WHERE ID = '{}'""".format(column, table, ID)
        c.execute(sqlCommand)
        queryResults = c.fetchall()
        c.close()
        return queryResults[0]
        
        
    def headingPushed(self, column):
        """Sorts the table by the column that was pushed"""
        if "date" in column.lower():
            self.sortDate(column)
        elif column == "ID":
            self.sortNum(column) 
        else:
            print("Non-specified column. Sorting as string")
            self.sortString(column)
    
    def sortDate(self, column):
        """Sorts the table by the dates in the column"""
        dates = OrderedDict()
        rows = [(self.tree.set(item, column).lower(), item) for item in self.tree.get_children('')]
        
        #get dates        
        for row in rows:
            dates[row[1]]=(row[0])
        
        #put in format day/month/year/rowID
        formattedDates = []
        i = 0
        for key in dates:
            i += 1
            date = dates[key]
            if date != "none":
                year = int(date[-4:])
                month = int(date[3:5])
                day = int(date[:2])
            else:
                year, month, day = 0, 0, 0
            formattedDates.append((day, month, year, key))
        
        #Sort the dates
        sortedDates = mergeSortDates(formattedDates)
        
        #If already sorting by Date, then flip
        if self.sort == column:
            self.sort = column + "Invert"
            sortedDates = sortedDates[::-1]
        else:
            self.sort = column

        #Put back in format for inserting into treeview
        for i in range(len(rows)):
            self.tree.move(sortedDates[i][3], '', i)
            
        #Color alternating rows
        for i in range(0, len(self.tree.get_children(""))):
            if i % 2 == 0:
                self.tree.item(self.tree.get_children("")[i], tags='evenrow')
            else:
                self.tree.item(self.tree.get_children("")[i], tags='oddrow')


    
    def sortString(self, column):
        """Sorts the table by the strings in the column"""
        rows = [(self.tree.set(item, column).lower(), item) for item in self.tree.get_children('')]
        sorted = mergeSortString(rows)

        #If already sorting by String, then flip
        if self.sort == column:
            self.sort = column + "Inverted"
            sorted = sorted[::-1]
        else:
            self.sort = column

        for index, (values, item) in enumerate(sorted):
            self.tree.move(item, '', index)
            
        #Color alternating rows
        for i in range(0, len(self.tree.get_children(""))):
            if i % 2 == 0:
                self.tree.item(self.tree.get_children("")[i], tags='evenrow')
            else:
                self.tree.item(self.tree.get_children("")[i], tags='oddrow')
    
    
    def sortNum(self, column):
        """Sorts the table by the numbers in the column"""
        rows = [(self.tree.set(item, column).lower(), item) for item in self.tree.get_children('')]
        sorted = mergeSortInt(rows)

        #If already sorting by Int, then flip
        if self.sort == column:
            self.sort = column + "Inverted"
            sorted = sorted[::-1]
        else:
            self.sort = column

        for index, (values, item) in enumerate(sorted):
            self.tree.move(item, '', index)  
        
        #Color alternating rows
        for i in range(0, len(self.tree.get_children(""))):
            if i % 2 == 0:
                self.tree.item(self.tree.get_children("")[i], tags='evenrow')
            else:
                self.tree.item(self.tree.get_children("")[i], tags='oddrow')  

class TextFrame(Frame):
    """Creates a frame with a Text widget and scrollbars that will scale to fit the outmost frame"""
    def __init__(self, root, width = 0, height = 0) -> None:
        super().__init__(root)

        #Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0), weight=1)
        
        self.grid_columnconfigure(0, minsize=width)
        self.grid_rowconfigure(0, minsize=height)

        self.treeFrame = Frame(self, bg="white") # Set Frame for table and scrollbars
        self.treeFrame.grid(column=0, row = 0, sticky="nesw")
        
        self.treeFrame.grid_columnconfigure(0, weight=1)

        
        #Define The Table
        self.text = Text(self.treeFrame, wrap = 'word', state = DISABLED)
        
        
        ####################################################################################
        ###### USE PLACE FOR THE TREEVIEW AND SCROLLBARS TO FIX THE OUT-OF-FRME ISSUE ######
        ####################################################################################
        self.text.place(relx = 0, rely = 0, relwidth=1 , relheight = 1)
        
        ### Scrollbars ###
        #Vertical
        self.verticalScroll = ttk.Scrollbar(self, orient = "vertical", command = self.text.yview)
        self.verticalScroll.grid(row = 0, column = 1, sticky="ns")
        #Horizontal
        self.horizontalScroll = ttk.Scrollbar(self, orient = "horizontal", command = self.text.xview)
        self.horizontalScroll.grid(row = 1, column = 0, sticky="ew")
        #Set Treeview to set scrollbar info
        self.text.configure(yscrollcommand=self.verticalScroll.set)
        self.text.configure(xscrollcommand=self.horizontalScroll.set)

def mergeSortDates(dates):
    """Sorts a list of dates in the format (day, month, year)"""
    # base case
    if len(dates) == 1:
        return dates
    
    # divide list into two halves
    mid = len(dates)//2
    left_dates = dates[:mid]
    right_dates = dates[mid:]
    
    # recursively sort each half
    left_dates = mergeSortDates(left_dates)
    right_dates = mergeSortDates(right_dates)
    
    # merge the two halves together
    sorted_dates = []
    i = j = 0
    while i < len(left_dates) and j < len(right_dates):
        date = left_dates[i]
        today = right_dates[j]
        if (date[2] < today[2] or 
            (date[2] == today[2] and date[1] < today[1]) or
            (date[2] == today[2] and date[1] == today[1] and date[0] < today[0])):
            sorted_dates.append(date)
            i += 1
        else:
            sorted_dates.append(today)
            j += 1
    
    # add any remaining elements in the left list
    while i < len(left_dates):
        sorted_dates.append(left_dates[i])
        i += 1
    
    # add any remaining elements in the right list
    while j < len(right_dates):
        sorted_dates.append(right_dates[j])
        j += 1
    
    # return the sorted list
    return sorted_dates

def mergeSortInt(integers):
    """Sorts a list of integers"""
    # base case
    if len(integers) == 1:
        return integers
    
    # divide list into two halves
    mid = len(integers)//2
    left_integers = integers[:mid]
    right_integers = integers[mid:]
    
    # recursively sort each half
    left_integers = mergeSortInt(left_integers)
    right_integers = mergeSortInt(right_integers)
    
    # merge the two halves together
    sorted_integers = []
    i = j = 0
    while i < len(left_integers) and j < len(right_integers):
        left_integer = left_integers[i]
        right_integer = right_integers[j]
        if (int(left_integer[0]) < int(right_integer[0])): 
            sorted_integers.append(left_integer)
            i += 1
        else:
            sorted_integers.append(right_integer)
            j += 1
    
    # add any remaining elements in the left list
    while i < len(left_integers):
        sorted_integers.append(left_integers[i])
        i += 1
    
    # add any remaining elements in the right list
    while j < len(right_integers):
        sorted_integers.append(right_integers[j])
        j += 1
    
    # return the sorted list
    return sorted_integers

def mergeSortString(strings):
    """Sorts a list of strings"""
    # base case
    if len(strings) == 1:
        return strings
    
    # divide list into two halves
    mid = len(strings)//2
    left_strings = strings[:mid]
    right_strings = strings[mid:]
    
    # recursively sort each half
    left_strings = mergeSortString(left_strings)
    right_strings = mergeSortString(right_strings)
    
    # merge the two halves together
    sorted_strings = []
    i = j = 0
    while i < len(left_strings) and j < len(right_strings):
        left_string = left_strings[i]
        right_string = right_strings[j]
        if (left_string[0] < right_string[0]): 
            sorted_strings.append(left_string)
            i += 1
        else:
            sorted_strings.append(right_string)
            j += 1
    
    # add any remaining elements in the left list
    while i < len(left_strings):
        sorted_strings.append(left_strings[i])
        i += 1
    
    # add any remaining elements in the right list
    while j < len(right_strings):
        sorted_strings.append(right_strings[j])
        j += 1
    
    # return the sorted list
    return sorted_strings

class RecordEntry(Entry):
    """Entry widget that validates input based on the column type"""
    def __init__(self, root, column, table, *args, **kwargs) -> None:
        super().__init__(root, *args, **kwargs)
        self.column = column
        self.table = table
        
    def validate(self):
        """Validates the entry based on the column type"""
        self.valid = True
        #No need to validate ID unless creating a new row
        #Check what Validation is needed
        # if "ID" in self.column:
        #     # print("Validating " + self.get() + " as ID")
        #     self.validateID()
        
        #Check if the entry is empty
        if (self.get() == "None") or self.get() == "":
            pass
        elif "email" in self.column.lower():
            # print("Validating " + self.get() + " as email")
            self.validateEmail()
        elif "phone" in self.column.lower():
            # print("Validating " + self.get() + " as phone number")
            self.validatePhone()
        elif "date" in self.column.lower():
            # print("Validating " + self.get() + " as date")
            self.validatePastDate()
        elif "username" in self.column.lower():
            # print("Validating " + self.get() + " as name")
            self.validateUsername()
        elif "password" in self.column.lower():
            # print("Validating " + self.get() + " as password")
            self.validatePassword()
        elif "name" in self.column.lower():
            # print("Validating " + self.get() + " as name")
            self.validateName()
        elif self.column.lower() == "title":
            self.lookupCheck(lookup=["Mr", "Mrs", "Ms", "Dr", "Prof"])
        elif "job" in self.column.lower():
            self.lookupCheck(lookup=["Manager", "Employee"])
        elif self.column.lower() == "lesson_day":
            self.lookupCheck(lookup=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        elif self.column.lower() == "lesson_time":
            self.lookupCheck(lookup=["Morning", "Afternoon", "Evening"])
        elif self.column.lower() == "lesson_length":
            self.lookupCheck(lookup=["30", "45", "60", "90"])
        elif self.column.lower() == "lesson_cost":
            self.rangeCheck(min=0, max=100)
        elif self.column.lower() == "lesson_frequency":
            self.lookupCheck(lookup=["Weekly", "Fortnightly", "Monthly"])

            
        
        #Return False if the validation failed        
        if self.valid == False:
            return False
            
    def validateID(self):
        """Validates the entry as an ID"""
        valid = True
        
        #Presence Check, must not be blank
        if self.get() == "":
            valid = False
            messagebox.showerror('Couldn\'t add record', str("ID column can not be blank"))
        #Length check, must be below 8 digits
        elif len(self.get()) > 8:
            valid = False
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is more than 8 digits"))
        #Type check, must be integer
        else:
            try:
                #Unique check, must be only ID with that ID and also performs Type check
                #Get all ID's in table
                query = str("SELECT " + self.column + " FROM " + self.table)
                c = conn.execute(query)
                rows = c.fetchall()
                c.close()
                
                #Number of ID's matching this one
                matches = 0
                for id in rows:
                    #If the ID matches
                    if (int(self.get()) == id[0]):
                        matches += 1 #increment matches count by one
                        
                if matches != 0:
                    valid = False
                    print("ID must be unique")
            except:
                valid = False
                print(str(type(self.get())) + " is not an integer")       
                
        return valid
            
        
    def validatePastDate(self):
        """Validates the entry as a date in the past"""
        #Checks the entry contents with the regular expression:
        #\d marks any digit [0-9]
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + "is not a valid date"))
            self.valid = False
        else:
            #Run range check to ensure date is in the past
            today = [datetime.today().strftime('%d'), datetime.today().strftime('%m'), datetime.today().strftime('%Y')]
            date = [self.get()[:2], self.get()[3:5], self.get()[6:10]]
            # print("Today's date is: " + str(today) + " and the given date is " + str(date))

            if (date[2] > today[2] or 
                    (date[2] == today[2] and date[1] > today[1]) or
                    (date[2] == today[2] and date[1] == today[1] and date[0] > today[0])):
                messagebox.showerror('Invalid Credentials!', str(self.get() + " is a date in the future"))
                self.valid = False
    
    def validateEmail(self):
        """Validates the entry as an email address"""
        #Checks the entry contents with the regular expression:
        #^ marks start of string
        #\S+ marks any number of non-whitespace characters
        #$ marks the end of the string
        if not re.match(r"^\S+@\S+\.\S+$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a valid email address"))
            self.valid = False
    
    def validateUsername(self):
        """Validates the entry as a username"""
        #Checks the entry contents with the regular expression:
        if not re.match(r"^[A-Za-z][\S]{2,23}$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a valid username"))
            self.valid = False
            
    def validatePassword(self):
        """Validates the entry as a password"""
        #Password must be at least 8 characters long, have one uppercase letter, one lowercase letter, one number and one special character:
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a valid password"))
            self.valid = False
            
    def validateName(self):
        """Validates the entry as a name"""
        #Checks the entry contents with the regular expression:
        if not re.match(r"^[A-Z][a-z]{2,25}$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a human name"))
            self.valid = False
    
    def validatePhone(self):
        """Validates the entry as a UK phone number"""
        if not re.match(r"^\+44\d{10}$|^(0\d{10})$", self.get()):
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a valid UK phone number"))
            self.valid = False

    def lookupCheck(self, lookup):
        """Checks if the entry is in the lookup table"""
        if self.get() not in lookup:
            messagebox.showerror('Invalid Credentials!', str(self.get() + " is not a valid " + self.column + "\nMust be one of " + str(lookup) + "\nOr leave blank"))
            self.valid = False
            
    def rangeCheck(self, min, max):
        """Checks if the entry is in the given range"""
        if float(self.get()) < min or float(self.get()) > max:
            messagebox.showerror('Invalid Credentials!', str(self.column + " must be between " + str(min) + " and " + str(max) + "\n" + str(self.get()) + " is not valid"))
            self.valid = False
        
        
class DateRange(Frame):
    """A frame containing two date entries to return a date range from the associated sql table"""
    def __init__(self, root, label, table, column) -> None:
        super().__init__(root)
        
        self.table = table
        self.column = column
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.label = Label(self, text = label)
        self.label.grid(row = 0, column = 0, columnspan = 3, sticky = "ew", padx = (10, 10), pady = (10, 0))
        
        self.startLabel = Label(self, text = "After Date:")
        self.startLabel.grid(row = 1, column = 0, sticky = "w", padx = (10, 0), pady = (10, 0))
        
        self.startEntry = Entry(self, textvariable = StringVar(value = "01/01/1920"))
        self.startEntry.grid(row = 1, column = 1, sticky = "ew", padx = (0, 10), pady = (10, 0))
        
        self.endLabel = Label(self, text = "Before Date:")
        self.endLabel.grid(row = 2, column = 0, sticky = "w", padx = (10, 0), pady = (10, 0))
        
        self.endEntry = Entry(self, textvariable = StringVar(value = "01/01/2020"))
        self.endEntry.grid(row = 2, column = 1, sticky = "ew", padx = (0, 10), pady = (10, 0))
        
        self.submitButton = Button(self, text = "Submit", command = self.submit)
        self.submitButton.grid(row = 1, column = 2, rowspan = 2, sticky = "nsew", padx = (0, 10), pady = (10, 0))
        
    def submit(self):
        """Validates the dates and date range then filters treeview results that are in the range"""
        
        if self.startEntry.get() == "":
            startDate = "01/01/1920"
        else:
            startDate = self.startEntry.get()
        if self.endEntry.get() == "":
            endDate = "01/01/2220"
        else:
            endDate = self.endEntry.get()
        
        valid = self.validateDateRange(startDate, endDate)
        
        if valid:
            print(self.column)
            self.table.filterDateRange(startDate, endDate, self.column)         
            
    
    def validateDateRange(self, start, end):
        """Validates the range of dates provided are valid dates and in the correct order"""
        #Checks the first date with the regular expression:
        #\d marks any digit [0-9]
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", start):
            messagebox.showerror('Invalid Date!', str(start + " is not a valid date"))
            return False
        elif not re.match(r"^\d{2}/\d{2}/\d{4}$", end):
            messagebox.showerror('Invalid Date!', str(end + " is not a valid date"))
            return False
        else:
            #Run range check to ensure dates are in correct order
            startDate = [start[:2], start[3:5], start[6:10]]
            endDate = [end[:2], end[3:5], end[6:10]]

            if (startDate[2] > endDate[2] or 
                    (startDate[2] == endDate[2] and startDate[1] > endDate[1]) or
                    (startDate[2] == endDate[2] and startDate[1] == endDate[1] and startDate[0] > endDate[0])):
                messagebox.showerror('Invalid Date Range!', str(start + " is not before " + end))
                return False
            else:
                return True


class NumberRange(Frame):
        """A frame containing two number entries to return a number range from the associated sql table"""
        def __init__(self, root, label, table, column) -> None:
            super().__init__(root)
            
            self.table = table
            self.column = column
            self.grid_columnconfigure((0, 1, 2), weight=1)
            
            self.label = Label(self, text = label)
            self.label.grid(row = 0, column = 0, columnspan = 3, sticky = "ew", padx = (10, 10), pady = (10, 0))
            
            self.startLabel = Label(self, text = "Above:")
            self.startLabel.grid(row = 1, column = 0, sticky = "w", padx = (10, 0), pady = (10, 0))
            
            self.startEntry = Entry(self)
            self.startEntry.grid(row = 1, column = 1, sticky = "ew", padx = (0, 10), pady = (10, 0))
            
            self.endLabel = Label(self, text = "Below:")
            self.endLabel.grid(row = 2, column = 0, sticky = "w", padx = (10, 0), pady = (10, 0))
            
            self.endEntry = Entry(self)
            self.endEntry.grid(row = 2, column = 1, sticky = "ew", padx = (0, 10), pady = (10, 0))
            
            self.submitButton = Button(self, text = "Submit", command = self.submit)
            self.submitButton.grid(row = 1, column = 2, rowspan = 2, sticky = "nsew", padx = (0, 10), pady = (10, 0))
            
        def submit(self):
            """Validates the numbers and number range then filters treeview results that are in the range"""
            
            if self.startEntry.get() == "":
                start = 0
            else:
                start = self.startEntry.get()
            if self.endEntry.get() == "":
                end = 9999
            else:
                end = self.endEntry.get()
            
            start = float(start)
            end = float(end)
            
            valid = self.validateNumberRange(start, end)
            
            if valid:
                self.table.filterNumberRange(start, end, self.column)    
            
                
        def validateNumberRange(self, start, end):
            """Validates the range of numbers provided to emsure they are valid numbers and in the correct order"""
            #Checks the numbers with the regular expression, must be a float:
            
            print("Start: " + str(start) + " End: " + str(end))
            
            if not re.match(r"^\d{1,4}(\.\d{1,2})?$", str(start)):
                messagebox.showerror('Invalid Number!', str(start) + " is not a valid number")
                return False
            elif not re.match(r"^\d{1,4}(\.\d{1,2})?$", str(end)):
                messagebox.showerror('Invalid Number!', str(end) + " is not a valid number")
                return False            
            else:
                #Run range check to ensure numbers are in correct order
                if start > end:
                    messagebox.showerror('Invalid Number Range!', str(start) + " is not before " + str(end))
                    return False
                else:
                    return True


class Record(Frame):
    """A frame containing the record fields for a table"""
    def __init__(self, root, table) -> None:
        super().__init__(root)
        
        # print("Record associated with: " + table)

        self.grid_columnconfigure((0), weight=1)

        self.tableFrame = LabelFrame(self)
        self.tableFrame.grid(row = 0, column = 0, sticky ="new", pady = (5, 10), padx = (10, 10))
        self.tableFrame.grid_columnconfigure(0, weight=1)

        ###Query Results Table
        self.table = TableFrame(self.tableFrame, table, 620, 350)
        self.table.grid(row = 0, column = 0, sticky ="new")
        #Bind left click on record to call selectedItem
        self.table.tree.bind('<ButtonRelease-1>', self.selectedItem)
        # Bind delete key to delete selected item
        self.table.tree.bind('<Delete>', self.deleteRecord)

        self.inputFrame = Frame(self)
        self.inputFrame.grid(row = 1, column = 0, sticky ="nesw", pady = (5, 10), padx = (10, 10))
        self.inputFrame.grid_columnconfigure((0,1), weight=1)
        
        
        ###Record Fields
        self.record = LabelFrame(self.inputFrame, text = "Record")
        self.record.grid(row = 0, column = 0, sticky ="nesw", padx=10, pady=5)
        
        #Create a list of entries and a dictionary of entry variables
        self.entries = []
        self.entryVars = OrderedDict() #Ordered dictionary to keep track of the entry variables
        for x in range(len(self.table.columns)):
            #Order the entries in a 3 column grid
            self.entryVars[self.table.columns[x]] = StringVar()
            col = 2*(x%3)
            row = (x+1) - (x%3)

            #Create a label for each entry
            Label(self.record, text = titleCase(str(self.table.columns[x] + ":")), anchor="w", justify="left").grid(row = row, column = col, padx=(10,0), pady=8, sticky="w")
            
            #If the column is a password column, hide the text
            if self.table.columns[x].lower() == "password":
                self.entries.append(RecordEntry(self.record, self.table.columns[x], self.table.table, textvariable=self.entryVars[self.table.columns[x]], show='*'))
            else:
                self.entries.append(RecordEntry(self.record, self.table.columns[x], self.table.table, textvariable=self.entryVars[self.table.columns[x]]))
            
            #Place the entry in the grid
            self.entries[x].grid(row = row, column=col + 1, padx=(5,10))
        
        #If the table is a student, or customer table add a birthdate range search
        if self.table.table.lower() == "customer" or self.table.table.lower() == "student":
            ###Frame for containing the range search fields
            self.rangeFrame = LabelFrame(self.inputFrame, text = "Range Search")
            self.rangeFrame.grid(row = 0, column = 1, sticky ="nesw", padx=10, pady=5)
            
            self.birthdateRange = DateRange(self.rangeFrame, "Birthdate", self, 7) #7 is the column number of birthdate
            self.birthdateRange.grid(row = 0, column = 0, sticky ="nesw", padx=10, pady=5)
            
        #If the table is an employee or teacher add a birthday and hire date range search
        if self.table.table.lower() == "employee" or self.table.table.lower() == "teacher":
            ###Frame for containing the range search fields
            self.rangeFrame = LabelFrame(self.inputFrame, text = "Range Search")
            self.rangeFrame.grid(row = 0, column = 1, sticky ="nesw", padx=10, pady=5)
            
            self.birthdateRange = DateRange(self.rangeFrame, "Birthdate", self, 7) #7 is the column number of birthdate
            self.birthdateRange.grid(row = 0, column = 0, sticky ="nesw", padx=10, pady=5)
            
            self.hireDateRange = DateRange(self.rangeFrame, "Hire Date", self, 8) #8 is the column number of hire date
            self.hireDateRange.grid(row = 1, column = 0, sticky ="nesw", padx=10, pady=5)
        
        #If the table is an item table add a price range search
        if self.table.table.lower() == "cafe_item":
            ###Frame for containing the range search fields
            self.rangeFrame = LabelFrame(self.inputFrame, text = "Range Search")
            self.rangeFrame.grid(row = 0, column = 1, sticky ="nesw", padx=10, pady=5)
            
            self.priceRange = NumberRange(self.rangeFrame, "Price", self, 3) #3 is the column number with the prices
            self.priceRange.grid(row = 0, column = 0, sticky ="nesw", padx=10, pady=5)
            
        elif self.table.table.lower() == "music_item":
            ###Frame for containing the range search fields
            self.rangeFrame = LabelFrame(self.inputFrame, text = "Range Search")
            self.rangeFrame.grid(row = 0, column = 1, sticky ="nesw", padx=10, pady=5)
            
            self.priceRange = NumberRange(self.rangeFrame, "Price", self, 4) #4 is the column number with the prices
            self.priceRange.grid(row = 0, column = 0, sticky ="nesw", padx=10, pady=5)
            
        
        
        ###Commands
        self.query = LabelFrame(self, text = "Commands")
        self.query.grid(row = 2, column = 0, sticky="ew", padx=10, pady=5)
        
        self.clearFieldsButton = Button(self.query, text = "Clear Fields", command=partial(self.clearFields))
        self.clearFieldsButton.pack(side = "left", padx=(10,0), pady=(0,10))
        
        self.updateButton = Button(self.query, text = "Update", command=self.updateRecord)
        self.updateButton.pack(side = "left", padx=(10,0), pady=(0,10))
        
        #managers can search, add and delete all records, employees can only search, add and delete records from the item tables and the customer table
        if userRole == "manager" or (userRole == "employee" and ("item" in table.lower()) or (table.lower() == "customer")):
                        
            self.searchButton = Button(self.query, text = "Search", command=self.searchQuery)
            self.searchButton.pack(side = "left", padx=(10,0), pady=(0,10))
            
            self.addRecordButton = Button(self.query, text = "Add Record", command=partial(self.addRecord))
            self.addRecordButton.pack(side = "left", padx=(10,0), pady=(0,10))
            
            self.deleteRecordButton = Button(self.query, text = "Delete Record", command=partial(self.deleteRecord))
            self.deleteRecordButton.pack(side = "left", padx=(10,0), pady=(0,10))
            
        #Teachers can only search from STUDENT and LESSON_BOOKING tables, but can search and add to the LESSON_REPORT tables
        if userRole == "teacher":
            if "student" in table.lower() or "lesson" in table.lower():
                self.searchButton = Button(self.query, text = "Search", command=self.searchQuery)
                self.searchButton.pack(side = "left", padx=(10,0), pady=(0,10))
                
                #Teachers can not update LESSON_REPORT or LESSON_PLAN
                if table.lower() == "lesson_plan":
                    self.updateButton.destroy()
                    
            if "lesson_report" in table.lower():
                self.addRecordButton = Button(self.query, text = "Add Record", command=partial(self.addRecord))
                self.addRecordButton.pack(side = "left", padx=(10,0), pady=(0,10))
        
        

        ### MATCHING TABLE INFO ###
        # self.matchedTable = TableFrame(self, width=500, height = 300)
        # self.matchedTable.grid(row = 0, column = 1, sticky = "new", pady = (5, 10), padx = (0,10))
        # self.matchedTable.grid_columnconfigure(0, weight=1)
    
    def selectedItem(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Get values from selected item in tree"""
        self.selection = self.table.tree.item(self.table.tree.focus())['values']
        
        #If selection is empty, return
        if not self.selection:
            return
        
        print(str(self.selection))
        
        #Execute sql statement to get data from the record at this ID
        c = conn.cursor()
        sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.selection[0])
        c.execute(sql)
        self.selection = c.fetchone()
        c.close()
        
        #set record entries with selected values and keep a record of the unchanged values
        for i in range(len(self.selection)):
            self.entryVars[self.table.columns[i]].set(self.selection[i])
            self.originalValue = self.entryVars
           

    ### BUTTON COMMANDS ###
    def addRecord(self):
        """Add a record to the table"""
        if self.validate() and self.entries[0].validateID():
            c = conn.cursor()

            sql = "INSERT INTO " + self.table.table +" ("

            ### Select specific columns to add
            for i in range(len(self.entryVars)):
                if self.entries[i].get() != "": #If entry field not empty
                    sql += str(self.table.columns[i] + ", ")
            
            sql = sql[:-2]
            sql += ") VALUES ("
            
            for i in range(len(self.entryVars)):
                value = self.entries[i].get()
                
                if value != "": #If entry field not empty
                    sql += "'" + str(value + "', ")
            
            sql = sql[:-2]
            sql += ");"
            c.execute(sql)
            c.close()
            self.table.fillTable()
        
    def updateRecord(self):
        """Update a record in the table"""
        
        #Check if at least 1 field have been filled
        filled_vars = 0
        for i in range(len(self.entryVars)):
                value = self.entries[i].get()
                if value != "":
                    filled_vars += 1
        
        if filled_vars >= 1:
            
            if self.validate():
                c = conn.cursor()

                #sql statement definition
                sql = "UPDATE " + self.table.table + " SET "

                ### Select specific columns to add
                for i in range(len(self.entryVars)):
                    value = self.entries[i].get()
                    if value != "":
                        sql += str(self.table.columns[i] + " = '" + value + "', ")

                
                sql = sql[:-2] #remove comma and space at end of for loop
                sql += " WHERE id = '" + self.entryVars[self.table.columns[0]].get() + "';"
                print(sql)
                c.execute(sql)
                conn.commit()
                c.close()
                self.table.fillTable() #update table
                messagebox.showinfo("Success!", "Successfully Updated Record!")
        
    def validate(self):
        """Validate all entries"""
        valid = True
        for i in range(len(self.entries)):
            if self.entries[i].validate() == False:
                print("Something is invalid there buckeroo")
                valid = False
        return valid    
    
    def deleteRecord(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Delete a record from the table"""        
        if messagebox.askokcancel("ARE YOU SURE", "ARE YOU CERTAIN!!!???\n(this can not be undone)", icon='warning'):
            c = conn.cursor()
            sql = "DELETE FROM " + self.table.table + " WHERE id = " + self.entries[0].get() + ";"
            c.execute(sql)
            c.close()
            self.table.fillTable()
            self.clearFields()
            
    def clearFields(self):
        """Clear all entry fields"""
        for i in range(len(self.entryVars)):
            self.entryVars[self.table.columns[i]].set("")       
            
    def searchQuery(self):
        """Create and execute search query"""
        query = str("SELECT * FROM " + self.table.table + " WHERE ")
        numberOfEntries = len(self.entryVars)
        emptyVars = 0
        
        for x in range(len(self.entryVars)):
            key = list(self.entryVars)[x]
            value = self.entries[x].get()
            
            if value == "" or value == "None":
                emptyVars += 1
            else:
                query += str(key + " = \"" + value + "\" AND " )
        
        #If there were no values entered
        if emptyVars == numberOfEntries:
            print("No values entered, displaying whole table")
            return self.table.fillTable() #Return the sql command executed for the Range check functions
        #If there was a value entered
        else:    
            query = query[:-5]
            print(query)
            return self.table.fillTable(query) #Return the sql command executed for the Range check functions

    def filterDateRange(self, startDate, endDate, column):
        
        #Get the query set in the Records frame
        sqlSearchQuery = self.searchQuery()
        print("Search Query: ", sqlSearchQuery)
        c = conn.cursor()
        c.execute(sqlSearchQuery)
        queryResults = c.fetchall()
        c.close()
        
        results = [row for row in queryResults]
        
        # Convert the start and end dates to datetime objects
        startDate = datetime.strptime(startDate, '%d/%m/%Y')
        endDate = datetime.strptime(endDate, '%d/%m/%Y')

        # Create an empty list to store the selected dates
        rowsInRange = []

        # Loop through each date in the input list
        for row in results:
            # Check if the date is not None
            if row[column] != 'None':
                # Convert the date string to a datetime object
                date = datetime.strptime(row[column], '%d/%m/%Y')

                # Check if the date falls within the given range
                if startDate <= date <= endDate:
                    # Add the date to the list of selected dates
                    rowsInRange.append(row)
                
        print(rowsInRange)
        self.table.insertRows(rowsInRange)

    def filterNumberRange(self, startNumber, endNumber, column):
        
        #Get the query set in the Records frame
        sqlSearchQuery = self.searchQuery()
        print("Search Query: ", sqlSearchQuery)
        c = conn.cursor()
        c.execute(sqlSearchQuery)
        queryResults = c.fetchall()
        c.close()
        
        results = [row for row in queryResults]
        
        # Create an empty list to store the selected numbers
        rowsInRange = []

        # Loop through each number in the input list
        for row in results:
            # Check if the number is not None
            if row[column] != 'None':
                # Convert the number to a float rounded to 2 decimal places
                number = float(row[column])

                # Check if the date falls within the given range
                if startNumber <= number <= endNumber:
                    # Add the date to the list of selected dates
                    rowsInRange.append(row)
                
        print(rowsInRange)
        self.table.insertRows(rowsInRange)

class Booking(Record):
    """Class for handling bookings"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     

        self.grid_columnconfigure((0,1), weight=1)
    
        self.calculationEstimate = ""
        self.table.tree["selectmode"] = "extended" 

        #Bind return key to calculateCost()
        self.table.tree.bind("<Return>", lambda e: self.calculateCost())

        ### Calculation results
        self.revenueFrame = TextFrame(self, width=500, height = 300)
        self.revenueFrame.grid(row = 0, column = 1, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.revenueFrame.grid_columnconfigure(0, weight=1)
        
        self.exportCalculationFrame = LabelFrame(self, text = "Export")
        self.exportCalculationFrame.grid(row = 1, column = 1, sticky="nesw")
        
        self.calculateButton = Button(self.exportCalculationFrame, text = "Calculate", command = self.calculateCost)
        self.calculateButton.grid(row = 0, column = 0)
        
        self.clearButton = Button(self.exportCalculationFrame, text = "Clear", command = self.clearCalculation)
        self.clearButton.grid(row = 0, column = 1)
        
        Label(self.exportCalculationFrame, text = "Export as .txt file: ").grid(row = 1, column = 0)
        
        self.exportButton = Button(self.exportCalculationFrame, text = "Export", command = self.exportCalculation)
        self.exportButton.grid(row = 1, column = 1)
                
    def clearCalculation(self):
        """Clear the calculation results"""
        #Clear calculationEstimate string
        self.calculationEstimate = ""
        #Clear the Text widget
        self.revenueFrame.text['state'] = "normal"
        self.revenueFrame.text.delete(1.0, END)
        self.revenueFrame.text['state'] = "disabled"
        
    def calculateCost(self):
        """Calculate the cost of the selected rows"""
        #Get selected rows
        curItems = self.table.tree.selection()
        
        frequencyDict = {"Weekly": 4, "Fortnightly": 2, "Monthly": 1}

        #If selection is not empty        
        if len(curItems) != 0:
            
            #define cost estimate text and mobthly cost variables
            self.calculationEstimate = ""
            self.monthlyRevenue = 0

            #Clear the Text widget
            self.revenueFrame.text['state'] = "normal"
            self.revenueFrame.text.delete(1.0, END)
            
            #Loop through each selected row
            for item in curItems:
                selectedItem = self.table.tree.item(item)['values']
        
                #Calculate the monthly cost and the calculation estimate text
                monthlyCost = float(frequencyDict[selectedItem[4]]) * float(selectedItem[8]) * float(1 - selectedItem[11])
                
                if monthlyCost != 0:
                    self.calculationEstimate += "User ID '" + str(selectedItem[0]) + "' has " + str(selectedItem[4]) + " monthly lessons, each costing £" + str(selectedItem[8]) + " resulting in a monthly revenue of: £" + str(monthlyCost) + "\n"
                    self.monthlyRevenue += monthlyCost
            
            #Add the total monthly revenue to the text
            self.calculationEstimate += "\nTotal Monthly Estimate for Selected Lessons: £" + str(self.monthlyRevenue)
            
            #Set the Text() widget to display the information
            self.revenueFrame.text.insert(END, self.calculationEstimate)
            self.revenueFrame.text['state'] = "disabled"
        else:
            messagebox.showerror("No Selected Records","Please Select a row")
                
    def exportCalculation(self):
        """Export the calculation results to a text file"""
        #If calculation not empty
        if self.calculationEstimate != "":
            #Get current date
            currentDate = str(datetime.today().strftime('%d/%m/%Y'))

            #Set export Log details        
            exportTitle = "=" * 32 + "\n" + currentDate + ": " + self.table.table + " Monthly Revenue Estimate:"
            
            #Create a file object in write mode
            file = open("LessonEstimate.txt", 'a', encoding='utf-8')

            #Write string to the file
            file.write(exportTitle + "\n" + self.calculationEstimate + "\n")

            #Close the file
            file.close()
            
            #Clear calculationEstimate and confirm export completed
            self.calculationEstimate = ""
            self.revenueFrame.text['state'] = "normal"
            self.revenueFrame.text.delete(1.0, END)
            self.revenueFrame.text.insert(END, "Successfully Exported")
            self.revenueFrame.text['state'] = "disabled"
        else:
            print("Empty Calculation")
            self.revenueFrame.text['state'] = "normal"
            self.revenueFrame.text.delete(1.0, END)
            self.revenueFrame.text.insert(END, "Nothing to export")
            self.revenueFrame.text['state'] = "disabled"
    
class Report(Record):
    """Class for handling lesson reports"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     

        self.grid_columnconfigure((0,1), weight=1)

        ### Calculation results
        self.noteFrame = LabelFrame(self, text = "Report Notes")
        self.noteFrame.grid(row = 0, column = 1, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.noteFrame.grid_columnconfigure((0), weight=1)
        
        self.noteText = TextFrame(self.noteFrame, width=500, height = 300)
        self.noteText.grid(row = 0, column = 0, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.noteText.grid_columnconfigure(0, weight=1)
        self.noteText.text['state'] = "normal"
        
        self.displayNotes = LabelFrame(self.noteFrame, text = "Note Commands")
        self.displayNotes.grid(row = 1, column = 0, sticky="nesw")
        
        Label(self.displayNotes, text = "Make changes to note: ").grid(row = 0, column = 0)
        
        self.editButton = Button(self.displayNotes, text = "Edit", command = self.editNote)
        self.editButton.grid(row = 0, column = 1)
        
        self.saveNotes = Button(self.displayNotes, text = "Save Changes", command = self.saveNote)
        self.saveNotes.grid(row = 0, column = 2)
    
    def selectedItem(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Callback method to get values from selected item in tree"""
        self.selection = self.table.tree.item(self.table.tree.focus())['values']
        
        #If the selection is not blank
        if len(self.selection) != 0:
            
            #Execute sql statement to get data from the record at this ID
            c = conn.cursor()
            sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.selection[0])
            c.execute(sql)
            self.selection = c.fetchone()
            c.close()
            
            #set record entries with selected values and keep a record of the unchanged values
            for i in range(len(self.selection)):
                self.entryVars[self.table.columns[i]].set(self.selection[i])
                self.originalValue = self.entryVars
            
            #Set the text widget to display the notes
            self.noteText.text['state'] = "normal"
            self.noteText.text.delete(1.0, END)
            self.noteText.text.insert(END, self.selection[6])
            self.noteText.text['state'] = "disabled"
        
    def editNote(self):
        """Edit the notes for the selected record"""
        #Get the current notes
        self.noteText.text['state'] = "normal"
    
    def saveNote(self):
        print("Saving changes")
        
        sqlQuery = "UPDATE " + self.table.table + " SET Notes = \"" + self.noteText.text.get(1.0, END) + "\" WHERE ID = " + str(self.selection[0])
        c = conn.cursor()
        c.execute(sqlQuery)
        conn.commit()
        c.close()
        self.noteText.text['state'] = "disabled"
        self.table.fillTable() #update table
        
class Plan(Record):
    """Class for handling lesson plans"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     

        self.grid_columnconfigure((0,1), weight=1)

        ### Calculation results
        self.procedureFrame = LabelFrame(self, text = "Lesson procedure")
        self.procedureFrame.grid(row = 0, column = 1, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.procedureFrame.grid_columnconfigure((0), weight=1)
        
        self.procedureText = TextFrame(self.procedureFrame, width=500, height = 300)
        self.procedureText.grid(row = 0, column = 0, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.procedureText.grid_columnconfigure(0, weight=1)
        self.procedureText.text['state'] = "normal"
        
        self.displayprocedures = LabelFrame(self.procedureFrame, text = "Procedure Commands")
        self.displayprocedures.grid(row = 1, column = 0, sticky="nesw")
        
        Label(self.displayprocedures, text = "Make changes to procedure: ").grid(row = 0, column = 0)
        
        self.editButton = Button(self.displayprocedures, text = "Edit", command = self.editprocedure)
        self.editButton.grid(row = 0, column = 1)
        
        self.saveprocedures = Button(self.displayprocedures, text = "Save Changes", command = self.saveprocedure)
        self.saveprocedures.grid(row = 0, column = 2)
    
    def selectedItem(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Get values from selected item in tree"""
        self.selection = self.table.tree.item(self.table.tree.focus())['values']
        
        #If the selection is not blank
        if len(self.selection) != 0:
            
            #Execute sql statement to get data from the record at this ID
            c = conn.cursor()
            sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.selection[0])
            c.execute(sql)
            self.selection = c.fetchone()
            c.close()
            
            #set record entries with selected values and keep a record of the unchanged values
            for i in range(len(self.selection)):
                self.entryVars[self.table.columns[i]].set(self.selection[i])
                self.originalValue = self.entryVars
            
            #Set the text widget to display the procedures
            self.procedureText.text['state'] = "normal"
            self.procedureText.text.delete(1.0, END)
            self.procedureText.text.insert(END, self.selection[4])
            self.procedureText.text['state'] = "disabled"
        
    def editprocedure(self):
        """Edit the procedures for the selected record"""
        #Get the current procedures
        self.procedureText.text['state'] = "normal"
    
    def saveprocedure(self):
        print("Saving changes")
        
        sqlQuery = "UPDATE " + self.table.table + " SET procedure = \"" + self.procedureText.text.get(1.0, END) + "\" WHERE ID = " + str(self.selection[0])
        c = conn.cursor()
        c.execute(sqlQuery)
        conn.commit()
        c.close()
        self.procedureText.text['state'] = "disabled"
        self.table.fillTable() #update table
        
class Sale(Record):
    """Class for handling sale reports"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     
        
        #Set the item table used to get item info for the sale report
        self.itemTable = self.table.table[:-5] + "ITEM"

        self.grid_columnconfigure((0,1), weight=1)
        
        self.table.tree["selectmode"] = "extended"
        
        
        # #All employees can search and add records
        if userRole == "employee":
            self.searchButton = Button(self.query, text = "Search", command=self.searchQuery)
            self.searchButton.pack(side = "left")
                
            self.addRecordButton = Button(self.query, text = "Add Record", command=partial(self.addRecord))
            self.addRecordButton.pack(side = "left")
        
        ### Calculation results
        self.salesFrame = LabelFrame(self, text = "Sales Estimate")
        self.salesFrame.grid(row = 0, column = 1, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.salesFrame.grid_columnconfigure((0), weight=1)
        
        self.salesText = TextFrame(self.salesFrame, width=500, height = 300)
        self.salesText.grid(row = 0, column = 0, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.salesText.grid_columnconfigure(0, weight=1)
    
    def selectedItem(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Get values from selected item in tree"""
        self.selection = self.table.tree.item(self.table.tree.focus())['values']
        curItems = self.table.tree.selection()
        
        #Execute sql statement to get data from the record at this ID
        c = conn.cursor()
        sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.selection[0])
        c.execute(sql)
        self.selection = c.fetchone()
        c.close()
        
        #set record entries with selected values and keep a record of the unchanged values
        for i in range(len(self.selection)):
            self.entryVars[self.table.columns[i]].set(self.selection[i])
            self.originalValue = self.entryVars
        
        #Get the value of each selected item from the SQL table instead of the selection
        actualCurItems = []
        for record in curItems:
            #Execute sql statement to get data from the record at this ID
            c = conn.cursor()
            sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.table.tree.item(record)['values'][0])
            c.execute(sql)
            actualCurItems.append(c.fetchone())
            c.close()
        
        #Set the current items to the actual items from the SQL table
        curItems = actualCurItems
        
        #If selection is not empty        
        if len(curItems) != 0:
            #define cost estimate text and monthly cost variables
            salesCost = 0
            
            #Loop through each selected row
            for item in curItems:
                #Get the price of the item                
                c = conn.cursor()
                c.execute(str("SELECT price FROM " + self.itemTable + " WHERE ID = " + str(item[1])))
                price = c.fetchone()[0]
                c.close()
                
                salesCost += price * int(item[3])
                
            # print("Total Revenue: £" + str(salesCost))
                        
            #Set the text widget to display the sales
            self.salesText.text['state'] = "normal"
            self.salesText.text.delete(1.0, END)
            self.salesText.text.insert(END, str("Total Revenue: £" + str(round(salesCost, 2))))
            self.salesText.text['state'] = "disabled"


class Inventory(Record):
    """Class for handling inventory information"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     
        
        #Set the item table used to get item info for the sale report
        self.itemTable = self.table.table[:-9] + "ITEM"

        self.grid_columnconfigure((0,1), weight=1)
        
        self.table.tree["selectmode"] = "extended"
        
        #Only the manager can update or delete records, but all employees can search and add records
        if userRole != "manager":
            self.updateButton.destroy()
            
        self.searchButton = Button(self.query, text = "Search", command=self.searchQuery)
        self.searchButton.pack(side = "left")
            
        self.addRecordButton = Button(self.query, text = "Add Record", command=partial(self.addRecord))
        self.addRecordButton.pack(side = "left")
        
        
        ### Calculation results
        self.inventoryFrame = LabelFrame(self, text = "Inventory Estimate")
        self.inventoryFrame.grid(row = 0, column = 1, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.inventoryFrame.grid_columnconfigure((0), weight=1)
        
        self.inventoryText = TextFrame(self.inventoryFrame, width=500, height = 300)
        self.inventoryText.grid(row = 0, column = 0, sticky = "nesw", pady = (5, 10), padx = (0,10))
        self.inventoryText.grid_columnconfigure(0, weight=1)
        self.inventoryText.text['state'] = "normal"
    
    def selectedItem(self, a): #Must take empty parameter 'a' as tkinter's callback passes 2 args
        """Get values from selected item in tree"""
        self.selection = self.table.tree.item(self.table.tree.focus())['values']
        curItems = self.table.tree.selection()
        
        #Execute sql statement to get data from the record at this ID
        c = conn.cursor()
        sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.selection[0])
        c.execute(sql)
        self.selection = c.fetchone()
        c.close()
        
        #set record entries with selected values and keep a record of the unchanged values
        for i in range(len(self.selection)):
            self.entryVars[self.table.columns[i]].set(self.selection[i])
            self.originalValue = self.entryVars
        
        #Get the value of each selected item from the SQL table instead of the selection
        actualCurItems = []
        for record in curItems:
            #Execute sql statement to get data from the record at this ID
            c = conn.cursor()
            sql = "SELECT * FROM " + self.table.table + " WHERE " + self.table.columns[0] + " = " + str(self.table.tree.item(record)['values'][0])
            c.execute(sql)
            actualCurItems.append(c.fetchone())
            c.close()
        
        #Set the current items to the actual items from the SQL table
        curItems = actualCurItems
        
        #If selection is not empty        
        if len(curItems) != 0:
            
            #define cost estimate text and mobthly cost variables
            inventoryCost = 0
            
            #Loop through each selected row
            for item in curItems:
                # selectedItem = self.table.tree.item(item)['values']
                
                c = conn.cursor()
                c.execute(str("SELECT price FROM " + self.itemTable + " WHERE ID = " + str(item[1])))
                price = c.fetchone()[0]
                c.close()
                
                inventoryCost += price * int(item[2])
                
            # print("Total Revenue: £" + str(inventoryCost))
                        
            #Set the text widget to display the inventory
            self.inventoryText.text['state'] = "normal"
            self.inventoryText.text.delete(1.0, END)
            self.inventoryText.text.insert(END, str("Estimated inventory value: £" + str(round(inventoryCost, 2))))
            self.inventoryText.text['state'] = "disabled"
        
    def editinventory(self):
        """Edit the inventory for the selected record"""
        #Get the current inventory
        self.inventoryText.text['state'] = "normal"
    
    def saveinventory(self):
        print("Saving changes")
        
        sqlQuery = "UPDATE " + self.table.table + " SET " + self.table.columns[4] + " = \"" + self.inventoryText.text.get(1.0, END) + "\" WHERE ID = " + str(self.selection[0])
        c = conn.cursor()
        c.execute(sqlQuery)
        conn.commit()
        c.close()
        self.inventoryText.text['state'] = "disabled"
        self.table.fillTable() #update table
        
        
                
def selectRecords():
    """Activate the record tab and hide the others"""
    recordFrame.pack(fill = "both", expand = 1)
    try:
        stockFrame.forget()
    except:
        # print("Stock frame not yet created")
        pass
    try:
        lessonFrame.forget()
    except:
        # print("Lesson frame not yet created")
        pass
    try:
        salesFrame.forget()
    except:
        # print("Sales frame not yet created")
        pass
        
def selectLessons():
    """Activate the lesson tab and hide the others"""
    lessonFrame.pack(fill = "both", expand = 1)
    try:
        stockFrame.forget()
    except:
        # print("Stock frame not yet created")
        pass
    try:
        recordFrame.forget()
    except:
        # print("Record frame not yet created")
        pass
    try:
        salesFrame.forget()
    except:
        # print("Sales frame not yet created")
        pass

def selectStock():
    """Activate the stock tab and hide the others"""
    stockFrame.pack(fill = "both", expand = 1)
    try:
        recordFrame.forget()
    except:
        # print("Record frame not yet created")
        pass
    try:
        lessonFrame.forget()
    except:
        # print("Lesson frame not yet created")
        pass
    try:
        salesFrame.forget()
    except:
        # print("Sales frame not yet created")
        pass
    
def selectSales():
    """Activate the sales tab and hide the others"""
    salesFrame.pack(fill = "both", expand = 1)
    try:
        recordFrame.forget()
    except:
        # print("Record frame not yet created")
        pass
    try:
        lessonFrame.forget()
    except:
        # print("Lesson frame not yet created")
        pass
    try:
        stockFrame.forget()
    except:
        # print("Stock frame not yet created")
        pass
    

def titleCase(inputString):
    """Convert a string to title case and remove underscores, also places spaces between capital letters"""
    #Replace underscores with spaces
    string = inputString.replace('_', ' ')
    #Add spaces between lowercase letters that are preceded by uppercase
    i = 1
    while i < len(string):
        if string[i].isupper() and string[i-1].islower():
            string = string[:i] + ' ' + string[i:]
            i += 1
        i += 1
    #Convert string to title case
    string = string.title()
    
    #Check if "ID" is present in the string and keep it in all caps
    if "Id" in string:
        string = string.replace("Id", "ID")
        string = string.replace("Id ", "ID ")
    
    return string

    


if __name__ == "__main__":
    """Main function run when the program is started"""

    splash = Splash(466, 372)

    handler = FileHandler("savedata.lzl")

    Login()
