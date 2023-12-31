import mysql.connector as s
import os

C=s.connect(host="localhost", user="root",passwd="1234")
if C.is_connected()==False:
    print("Error connecting to MySQL database.")

cursor=C.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Movieflix")
cursor.execute("USE Movieflix")
cursor.execute('''CREATE TABLE IF NOT EXISTS Movies
(
    Mno INT(2) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Genre VARCHAR(20) NOT NULL,
    Year INT(4) NOT NULL,
    Rating FLOAT(2,1) NOT NULL,
    MPA_Rating VARCHAR(5) NOT NULL,
    Runtime VARCHAR(6) NOT NULL,
    Premium VARCHAR(3) NOT NULL,
    Movie_Link VARCHAR(2048) NOT NULL
)
''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Customers
(
    Cno INT(2) PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Mobile_No INT(10) NOT NULL,
    E_Mail VARCHAR(320) NOT NULL,
    Premium VARCHAR(3) NOT NULL,
    Password VARCHAR(127) NOT NULL
)
''')

isUserLoggedIn=False

LOGO = '''
█ █ █ █▀▀ █   █▀▀ █▀█ █▀▄▀█ █▀▀   ▀█▀ █▀█   █▀▄▀█ █▀█ █ █ █ █▀▀ █▀▀ █   █ ▀▄▀
▀▄▀▄▀ ██▄ █▄▄ █▄▄ █▄█ █ ▀ █ ██▄    █  █▄█   █ ▀ █ █▄█ ▀▄▀ █ ██▄ █▀  █▄▄ █ █ █
'''

def Break():
    print("====================================================================================================")

def MaxLen(names):
    return len(max(names, key=len))

def MakeSpace(x):
    return "".join([" " for i in range(x)])

def PrintMovie(Squery):
    SerialNos = []
    Names = []
    Genres = []
    RDates = []
    PGRates = []
    Ratings = []
    Durations = []
    Premium=[]
    cursor.execute(Squery)
    _data = cursor.fetchall();
    string = ""
    for i in _data:
        SerialNos.append(str(i[0]))
        Names.append(i[1])
        Genres.append(i[2])
        RDates.append(str(i[3]))
        Ratings.append(str(i[4]))
        PGRates.append(i[5])
        Durations.append(i[6])
        Premium.append(i[7])
    maxSNoLen = MaxLen(SerialNos)
    maxNameLen = MaxLen(Names)
    maxGenreLen = MaxLen(Genres)
    maxRDateLen = MaxLen(RDates)
    maxPGLen = MaxLen(PGRates)
    maxRatingLen = MaxLen(Ratings)
    maxDurations = MaxLen(Durations)
    print(f"| M  | Movie Name{MakeSpace(maxNameLen - 10)} | Genre{MakeSpace(maxGenreLen - 5)} | Year{MakeSpace(maxRDateLen - 4)} | Ratings{MakeSpace(maxRatingLen - 7)} | PG Rating{MakeSpace(maxPGLen - 9)} | Duration{MakeSpace(maxDurations - 8)} | Premium   |\n")
    for i in range(len(Names)):
        string += f"| {SerialNos[i]}{MakeSpace(maxSNoLen - len(str(SerialNos[i])))} | {Names[i]}{MakeSpace(maxNameLen - len(str(Names[i])))} | {Genres[i]}{MakeSpace(maxGenreLen - len(Genres[i]))} | {RDates[i]}{MakeSpace(maxRDateLen - len(str(RDates[i])))} | {Ratings[i]}{MakeSpace(maxRatingLen - len(str(Ratings[i])) + 4)} | {PGRates[i]}{MakeSpace(maxPGLen - len(PGRates[i]) + 4)} | {Durations[i]}{MakeSpace(maxDurations - len(Durations[i]) + 2)} | {Premium[i]}{MakeSpace(9 - len(Premium[i]))} |\n"
    print(string)
        
def OpenLink(query):
    cursor.execute(query)
    _data = cursor.fetchall()
    if _data[0][1].lower()=="no":
        os.startfile(_data[0][0])
    elif _data[0][1].lower()=="yes" and isUserLoggedIn:
        os.startfile(_data[0][0])
    else:
        print("\nYou need to sign in to watch premium movies")
        StartPage()
    HomePage()

def StartPage():
    Break()
    global isUserLoggedIn
    print(LOGO)
    Start_Input=int(input('''
\t\t\t\t1) Sign in
\t\t\t\t2) Sign up
\t\t\t\t3) Guest Mode
\t\t\t\t\t\t\tChoose 1, 2, 3
\t\t\t\t'''))
    if Start_Input==1:
        Input_Username=input("Enter Username:")
        Input_Password=input("Enter Password:")
        cursor.execute("SELECT Username FROM Customers")
        U=cursor.fetchall()
        cursor.execute("SELECT Password FROM Customers")
        P=cursor.fetchall()
        if (Input_Username,) in U and (Input_Password,) in P:
            isUserLoggedIn = True
            HomePage()
        else:
            print("Wrong Credentials...Try Again")
            StartPage()
    if Start_Input==2:
        cursor.execute("SELECT * FROM Customers")
        Count=cursor.fetchall()
        Calculate_Cno=len(Count) + 1
        Input_Username=input("Enter Username: ")
        Input_Password=input("Enter Password: ")
        Input_Mobile_No=int(input("Enter Mobile Number: "))
        Input_E_Mail=input("Enter E-Mail: ")
        cursor.execute(f"INSERT INTO Customers VALUES({Calculate_Cno},\"{Input_Username}\",{Input_Mobile_No},\"{Input_E_Mail}\",\"No\",\"{Input_Password}\")")
        C.commit()
        StartPage()
    if Start_Input==3:
        isUserLoggedIn = False
        HomePage()

def HomePage():
    Break()
    print(LOGO)
    User_Input=int(input(f'''
\t\t\t\t1) All Movies
\t\t\t\t2) Latest Movies
\t\t\t\t3) Top Rated
\t\t\t\t4) Select Genre
\t\t\t\t5) Search Movies
\t\t\t\t6) Staff Mode
\t\t\t\t\t\t\tChoose 1,2,3,4,5,6\t\tYou Are Currently {"Signed In" if isUserLoggedIn else "Signed Out"}
\t\t\t\t'''))
    Break()

    if User_Input==1:
        PrintMovie("SELECT Mno, Name, Genre, Year, Rating, MPA_Rating, Runtime, Premium FROM Movies ORDER BY Name")
        Watch=input("Enter the movie number you want to watch: ")
        OpenLink(f"SELECT Movie_Link, Premium FROM Movies WHERE Mno=\"{Watch}\"")
    if User_Input==2:
        PrintMovie("SELECT Mno, Name, Genre, Year, Rating, MPA_Rating, Runtime, Premium FROM Movies ORDER BY Year DESC")
        Watch=input("Enter the movie number you want to watch: ")
        OpenLink(f"SELECT Movie_Link, Premium FROM Movies WHERE Mno=\"{Watch}\"")
    if User_Input==3:
        PrintMovie("SELECT Mno, Name, Genre, Year, Rating, MPA_Rating, Runtime, Premium FROM Movies ORDER BY Rating DESC")
        Watch=input("Enter the movie number you want to watch: ")
        OpenLink(f"SELECT Movie_Link, Premium FROM Movies WHERE Mno=\"{Watch}\"")
    if User_Input==4:
        cursor.execute("SELECT DISTINCT Genre FROM Movies ORDER BY Genre")
        Genre_Input=input("Select a Genre:\n" + "".join([f"\t{x[0]}\n" for x in cursor.fetchall()]))
        cursor.execute("SELECT Genre FROM Movies ORDER BY Genre")
        if ((Genre_Input,) in cursor.fetchall()):
            PrintMovie(f"SELECT * FROM Movies WHERE Genre=\"{Genre_Input}\"")
        Watch=input("Enter the movie number you want to watch: ")
        OpenLink(f"SELECT Movie_Link, Premium FROM Movies WHERE Mno=\"{Watch}\"")
    if User_Input==5:
        Search_Input=input("Search Movie Name: ")
        cursor.execute("SELECT Name From Movies")
        for i in cursor.fetchall():
            if Search_Input == i[0]:
                PrintMovie(f"SELECT Mno, Name, Genre, Year, Rating, MPA_Rating, Runtime, Premium FROM Movies WHERE Name = \"{Search_Input}\"")
                Watch=input("Enter the movie number you want to watch: ")
                OpenLink(f"SELECT Movie_Link, Premium FROM Movies WHERE Mno=\"{Watch}\"")
            else:
                print('''\t  404 Error\n\tMovie not found''')
                if input("Would you like to add a movie? ").lower()=="y":
                    input("Enter Movie Name: ")
                    print("Your movie has been sent to the moderators to verify")
                    HomePage()
                else:
                    HomePage()
    if User_Input==6:
        if input("Enter Staff Password:") == "Staff":
            MN=int(input('''\t\tWelcome Staff\n\tEnter number of movies you want to add: '''))
            print('''Add movies in the form - INSERT INTO MOVIES VALUES(<Mno>,<Movie Name>,<Genre>,<Year>,<Rating>,<MPA Rating>,<Runtime>,<Premium>,<Movie Link>)''')
            for i in range(MN):
                Execute=input("Execute: ")
                cursor.execute(Execute)
                C.commit()
            print("\nAll movies entered!!!")
            HomePage()
        else:
            print("Wrong Staff Credentials")
            HomePage()
StartPage()
