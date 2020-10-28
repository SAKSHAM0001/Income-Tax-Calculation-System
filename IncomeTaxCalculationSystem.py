from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import smtplib
import random
import time
import datetime
from tkinter import messagebox
import mysql.connector


root = Tk()
root.geometry("1340x700+0+0")
root.title("Income Tax Calculator")
root.configure(background='cadet blue')

MainFrame=Frame(root,bd=10,width=1350,height=700,relief=RIDGE,bg="cadet blue")
MainFrame.pack()

TopFrame=Frame(MainFrame,bd=5,width=1300,height=40,relief=RIDGE,bg="cadet blue")
TopFrame.pack(side=TOP,fill=X)

lblTitle=Label(TopFrame, font=('arial', 35, 'bold'), width=43, text="Income Tax Calculator", padx=32,bg="cadet blue",fg="white")
lblTitle.grid()

MiddleFrame=Frame(MainFrame,bd=5,width=1340,height=490,relief=RIDGE)
MiddleFrame.pack()

BottomFrame=Frame(MainFrame,bd=5,width=1340,height=70,relief=RIDGE)
BottomFrame.pack(fill=BOTH)

LeftFrame=Frame(MiddleFrame,bd=5,width=1340,height=400,bg="cadet blue",relief=RIDGE)
LeftFrame.pack(side=LEFT,fill=Y)

LeftFrame1=Frame(LeftFrame,bd=5,width=600,height=190,padx=2,relief=RIDGE)
LeftFrame1.pack(side=TOP,pady=0,fill=BOTH)
LeftFrame1Left=Frame(LeftFrame1,bd=5,width=600,height=185,padx=2,bg="cadet blue",relief=RIDGE)
LeftFrame1Left.pack(side=TOP,fill=X)
        
LeftFrame2=Frame(LeftFrame,bd=5,width=600,height=200,padx=2,relief=RIDGE)
LeftFrame2.pack(side=TOP,pady=0,fill=BOTH)
LeftFrame2Left=Frame(LeftFrame2,bd=5,width=600,height=195,padx=2,bg="cadet blue",relief=RIDGE)
LeftFrame2Left.pack(side=TOP,fill=BOTH)
        
RightFrame1=Frame(MiddleFrame,bd=5,width=320,height=400,padx=2,bg="cadet blue",relief=RIDGE)
RightFrame1.pack(side=RIGHT)
RightFrame1a=Frame(RightFrame1,bd=5,width=310,height=300,padx=2,pady=2,relief=RIDGE)
RightFrame1a.pack(side=TOP)

# ==============================Variables=====================
PaymentRef = StringVar()
Name = StringVar()
Pan = StringVar()
TaxPayer = StringVar()
TaxPeriod = StringVar()

dateRef = StringVar()
Income = StringVar()
TaxableIncome = StringVar()
NonTaxableIncome = StringVar()
TaxPaid = StringVar()

GrossPay = StringVar()
Deduction = StringVar()
NetPay = StringVar()

dateRef.set(time.strftime("%d/%m/%y"))

ReferenceId = StringVar()
mail_id=StringVar()

# =============================Functions==================
def savedata():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="GUI7")
    mycursor=mydb.cursor()
    #mycursor.execute("use GUI7")
    #mycursor.execute("show databases")
    #for db in mycursor:
    #    print(db)
    #mycursor.execute("create table ProjectTable(ReferenceId varchar(255),name varchar(255),pan varchar(255),year varchar(255),total_income varchar(255),tax_paid varchar(255),Net_pay varchar(255),Tax_Payer varchar(255),mail_id varchar(255))")
    #print("table created")
    username=Name.get()
    pan=Pan.get()
    mail=mail_id.get()
    income=Income.get()
    year=TaxPeriod.get()
    if username and pan and mail and income and year:
        mycursor.execute("insert into ProjectTable values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(PaymentRef.get(),Name.get(),Pan.get(),
                                                                                           TaxPeriod.get(),Income.get(),
                                                                                           TaxPaid.get(),NetPay.get(),TaxPayer.get(),mail_id.get()))
        re=PaymentRef.get()
        re1=(int(re))
        refid=("select * from ProjectTable where ReferenceId LIKE "+str(re1))
        mycursor.execute(refid)
        rows =mycursor.fetchall()
        IncomeRecord.delete(*IncomeRecord.get_children())
        if len(rows)!=0:
            for row in rows:
                vv=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
                IncomeRecord.insert('',END,values=vv)
        mydb.commit()
        
        messagebox.showinfo("Success", "Data Saved Successfully.")
    else:
        messagebox.showwarning('Warning','Please fill all required details')
    mydb.close()
    
def viewData():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="GUI7")
    mycursor = mydb.cursor()
    #mycursor.execute("use GUI7")
    mycursor.execute("select * from ProjectTable")
    rows = mycursor.fetchall()
    if len(rows)!=0:
        IncomeRecord.delete(*IncomeRecord.get_children())
        for row in rows:
            IncomeRecord.insert('',END,values=row)
        mydb.commit()
    mydb.close()
def check():
    sear=ReferenceId.get()
    if sear:
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="GUI7")
        mycursor=mydb.cursor()
        re=ReferenceId.get()
        re1=(int(re))
        refid=("select * from ProjectTable where ReferenceId LIKE "+str(re1))
        mycursor.execute(refid)
        rows =mycursor.fetchall()
        IncomeRecord.delete(*IncomeRecord.get_children())
        if len(rows)!=0:
            for row in rows:
                vv=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
                IncomeRecord.insert('',END,values=vv)
                messagebox.showinfo("Details","Data Found ")
        else:
            reset()
            messagebox.showinfo("Details","Data not found")
    else:
        messagebox.showwarning('Warning','Please Enter Reference Id ')
    

def delete1(ReferenceId):
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="",database="GUI7")
    mycursor = mydb.cursor()
    #mycursor.execute("use GUI7")
    mycursor.execute("DELETE from ProjectTable where ReferenceId =%s",(ReferenceId,))
    mydb.commit()
    mydb.close()
def delete():
    if(len(PaymentRef.get())!=0):
        delete1(row[0])
        reset()
        viewData()
        messagebox.showinfo("Success", "Data Deleted Successfully.")
    else:
        messagebox.showwarning('Warning','Please Select Data To Delete')
    
    
            
def remove():
    for row in IncomeRecord.get_children():
        IncomeRecord.delete(row)
def get(event):
    global row
    cursor_row=IncomeRecord.focus()
    contents=IncomeRecord.item(cursor_row)
    row=contents['values']
    #print(row)
    PaymentRef.set(row[0])
    Name.set(row[1])
    Pan.set(row[2])
    TaxPeriod.set(row[3])
    Income.set(row[4])
    TaxPaid.set(row[5])
    NetPay.set(row[6])
    TaxPayer.set(row[7])
    mail_id.set(row[8])
    TaxableIncome.set("")
    NonTaxableIncome.set("")
    Deduction.set("")
    
    
def iExit():
    iExit = tkinter.messagebox.askyesno("Income Tax Calculator", "Confirm if you want to exit")
    if iExit > 0:
        root.destroy()
        return


def reset():
    PaymentRef.set("")
    Name.set("")
    Pan.set("")
    TaxPayer.set("Select")
    TaxPeriod.set("Select")
    Income.set("")
    TaxableIncome.set("")
    NonTaxableIncome.set("")
    TaxPaid.set("")
    GrossPay.set("")
    Deduction.set("")
    NetPay.set("")
    mail_id.set("")
    
    remove()
def send():
    username=Name.get()
    pan=Pan.get()
    mail=mail_id.get()
    income=Income.get()
    year=TaxPeriod.get()
    if username and pan and mail and income and year:
        def sendmail(email, password, message1):
            id = mail_id.get()
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, id, message1)
            server.quit()

        message = "Reference no = " + str(PaymentRef.get()) + "\n" + "Name = " + str(
        Name.get()) + "\n" + "PAN number =" + str(Pan.get()) + "\n" +  "Tax Year = " + str(
        TaxPeriod.get()) + " \nTax  = " + str(TaxPaid.get())   + "\n Netpay = " + str(NetPay.get())
    
        sendmail("mail@gmail.com","Password",message)
        messagebox.showinfo("Success", "Data Sent Successfully.")
    else:
        messagebox.showwarning('Warning','Please Select Data To Send')
    

        

def  remaing(x):
    TaxPaid.set(str(x))
    final=int(Income.get())-x
    NetPay.set(str(final))

    
def IncomeTax():
    global username,pan,mail,income,year
    username=Name.get()
    pan=Pan.get()
    mail=mail_id.get()
    income=Income.get()
    year=TaxPeriod.get()
    tp=TaxPayer.get()
    if username and pan and mail and income and year!='Select' and tp!='Select':
        if tp=='Individual':
            x = random.randint(100340, 699812)
            randomRef = str(x)
            PaymentRef.set(randomRef)

            user_amount=Income.get()
            user_amount=int(user_amount)
            if user_amount <= 250000:
                TaxableIncome.set("0")
                Deduction.set("0")
                NonTaxableIncome.set(str(user_amount))
                remaing(0)
            if user_amount > 250000 and (user_amount <= 500000):
                tax = ((user_amount-250000) / 100) * 5
                TaxableIncome.set(str(user_amount-250000))
                Deduction.set("0")
                NonTaxableIncome.set(str(250000))
                remaing(tax)
            if user_amount > 500000 and (user_amount <= 750000):
                tax = 12500 + ((user_amount - 500000) / 100) * 10
                TaxableIncome.set(str(user_amount-500000))
                Deduction.set(str(12500))
                NonTaxableIncome.set(str(500000))
                remaing(tax)
            if user_amount > 750000 and (user_amount <= 1000000):
                tax = 37500 + ((user_amount - 750000) / 100) * 15
                TaxableIncome.set(str(user_amount-750000))
                Deduction.set(str(37500))
                NonTaxableIncome.set(str(750000))
                remaing(tax)
            if user_amount > 1000000 and (user_amount <= 1250000):
                tax = 75000 + ((user_amount - 1000000) / 100) * 20
                TaxableIncome.set(str(user_amount-1000000))
                Deduction.set(str(75000))
                NonTaxableIncome.set(str(1000000))
                remaing(tax)
            if user_amount > 1250000 and (user_amount <= 1500000):
                tax = 125000 + ((user_amount - 1250000) / 100) * 25
                TaxableIncome.set(str(user_amount-1250000))
                Deduction.set(str(125000))
                NonTaxableIncome.set(str(1250000))
                remaing(tax)
            if user_amount > 1500000:
                tax = 187500+((user_amount-1500000) / 100) * 30
                TaxableIncome.set(str(user_amount - 1500000))
                NonTaxableIncome.set(str(1500000))
                Deduction.set(str(187500))
                remaing(tax)
    
        
        elif tp=='Domestic Company':
            x = random.randint(100340, 699812)
            randomRef = str(x)
            PaymentRef.set(randomRef)

            user_amount=Income.get()
            user_amount=int(user_amount)
            if user_amount <= 250000:
                TaxableIncome.set("0")
                Deduction.set("0")
                NonTaxableIncome.set(str(user_amount))
                remaing(0)
            if user_amount > 250000 and (user_amount <= 500000):
                tax = ((user_amount-250000) / 100) * 15
                TaxableIncome.set(str(user_amount-250000))
                Deduction.set("0")
                NonTaxableIncome.set(str(250000))
                remaing(tax)
            if user_amount > 500000 and (user_amount <= 750000):
                tax = 12500 + ((user_amount - 500000) / 100) * 20
                TaxableIncome.set(str(user_amount-500000))
                Deduction.set(str(12500))
                NonTaxableIncome.set(str(500000))
                remaing(tax)
            if user_amount > 750000 and (user_amount <= 1000000):
                tax = 37500 + ((user_amount - 750000) / 100) * 25
                TaxableIncome.set(str(user_amount-750000))
                Deduction.set(str(37500))
                NonTaxableIncome.set(str(750000))
                remaing(tax)
            if user_amount > 1000000 and (user_amount <= 1250000):
                tax = 75000 + ((user_amount - 1000000) / 100) * 30
                TaxableIncome.set(str(user_amount-1000000))
                Deduction.set(str(75000))
                NonTaxableIncome.set(str(1000000))
                remaing(tax)
            if user_amount > 1250000 and (user_amount <= 1500000):
                tax = 125000 + ((user_amount - 1250000) / 100) * 35
                TaxableIncome.set(str(user_amount-1250000))
                Deduction.set(str(125000))
                NonTaxableIncome.set(str(1250000))
                remaing(tax)
            if user_amount > 1500000:
                tax = 187500+((user_amount-1500000) / 100) * 40
                TaxableIncome.set(str(user_amount - 1500000))
                NonTaxableIncome.set(str(1500000))
                Deduction.set(str(187500))
                remaing(tax)
        
        
    
        elif tp=='Foreign Company':
            x = random.randint(100340, 699812)
            randomRef = str(x)
            PaymentRef.set(randomRef)

            user_amount=Income.get()
            user_amount=int(user_amount)
            if user_amount <= 250000:
                TaxableIncome.set("0")
                Deduction.set("0")
                NonTaxableIncome.set(str(user_amount))
                remaing(0)
            if user_amount > 250000 and (user_amount <= 500000):
                tax = ((user_amount-250000) / 100) * 20
                TaxableIncome.set(str(user_amount-250000))
                Deduction.set("0")
                NonTaxableIncome.set(str(250000))
                remaing(tax)
            if user_amount > 500000 and (user_amount <= 750000):
                tax = 12500 + ((user_amount - 500000) / 100) * 25
                TaxableIncome.set(str(user_amount-500000))
                Deduction.set(str(12500))
                NonTaxableIncome.set(str(500000))
                remaing(tax)
            if user_amount > 750000 and (user_amount <= 1000000):
                tax = 37500 + ((user_amount - 750000) / 100) * 30
                TaxableIncome.set(str(user_amount-750000))
                Deduction.set(str(37500))
                NonTaxableIncome.set(str(750000))
                remaing(tax)
            if user_amount > 1000000 and (user_amount <= 1250000):
                tax = 75000 + ((user_amount - 1000000) / 100) * 35
                TaxableIncome.set(str(user_amount-1000000))
                Deduction.set(str(75000))
                NonTaxableIncome.set(str(1000000))
                remaing(tax)
            if user_amount > 1250000 and (user_amount <= 1500000):
                tax = 125000 + ((user_amount - 1250000) / 100) * 40
                TaxableIncome.set(str(user_amount-1250000))
                Deduction.set(str(125000))
                NonTaxableIncome.set(str(1250000))
                remaing(tax)
            if user_amount > 1500000:
                tax = 187500+((user_amount-1500000) / 100) * 45
                TaxableIncome.set(str(user_amount - 1500000))
                NonTaxableIncome.set(str(1500000))
                Deduction.set(str(187500))
                remaing(tax)
    else:
        mbox1 = messagebox.showwarning('Warning','Please fill all required details')
    
        

    
lbldate = Label(LeftFrame1Left, font=('arial', 12, 'bold'), text="Date", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lbldate.grid(row=0, column=0,sticky=W)
txtdate = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=dateRef, bd=8,width=40,justify='left')
txtdate.grid(row=0, column=1)

        
lblName = Label(LeftFrame1Left, font=('arial', 12, 'bold'), text="Name*", bd=8, justify='left', fg="white",bg="cadet blue",padx=5)
lblName.grid(row=1, column=0,sticky=W)
txtName = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=Name, bd=8,width=40,justify='left')
txtName.grid(row=1, column=1)
        
lblPan = Label(LeftFrame1Left, font=('arial', 12, 'bold'), text="PAN*", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lblPan.grid(row=2, column=0,sticky=W)
txtPan = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=Pan, bd=8,width=40,justify='left')
txtPan.grid(row=2, column=1)

lblIncome = Label(LeftFrame1Left, font=('arial', 12, 'bold'), text="Total Income*                  ", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lblIncome.grid(row=3, column=0,sticky=W)
txtIncome = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=Income, bd=8,width=40,justify='left')
txtIncome.grid(row=3, column=1)

lblMail = Label(LeftFrame1Left, font=('arial', 12, 'bold'), text="E-Mail*", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lblMail.grid(row=4, column=0,sticky=W)
txtMail = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=mail_id, bd=8,width=40,justify='left')
txtMail.grid(row=4, column=1)
        
lblTaxPeriod=Label(LeftFrame1Left,font=('arial',12,'bold'),text="Assesment Year*", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lblTaxPeriod.grid(row=5,column=0,sticky=W)
"""
txtTaxPeriod = Entry(LeftFrame1Left, font=('arial', 12, 'bold'), textvariable=TaxPeriod, bd=9,width=40,justify='left')
txtTaxPeriod.grid(row=5, column=1)

"""
cboTaxPeriod=ttk.Combobox(LeftFrame1Left,textvariable=TaxPeriod,state='readonly',font=('arial',12,'bold'),width=39,justify='left')
cboTaxPeriod['value']=('Select','2020-21','2019-20','2018-19')
cboTaxPeriod.current(0)
cboTaxPeriod.grid(row=5,column=1)


lblTaxPayer=Label(LeftFrame1Left,font=('arial',12,'bold'),text="Tax Payer*", bd=8, justify='left',fg="white",bg="cadet blue", padx=5)
lblTaxPayer.grid(row=6,column=0,sticky=W)
cboTaxPayer=ttk.Combobox(LeftFrame1Left,textvariable=TaxPayer,state='readonly',font=('arial',12,'bold'),width=39,justify='left')
cboTaxPayer['value']=('Select','Individual','Domestic Company','Foreign Company')
cboTaxPayer.current(0)
cboTaxPayer.grid(row=6,column=1)


lblRef = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Reference ID", bd=11, justify='left',fg="white",bg="cadet blue", padx=5)
lblRef.grid(row=0, column=0,sticky=W)
txtRef = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=PaymentRef, bd=10,width=40,justify='left')
txtRef.grid(row=0, column=1)
        
# --------------
lblNTI = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Non Taxable Income   ", bd=10, justify='left',fg="white",bg="cadet blue", padx=5)
lblNTI.grid(row=1, column=0, sticky=W)
txtNTI = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=NonTaxableIncome, bd=10,width=40,justify='left')
txtNTI.grid(row=1, column=1)
#----------------
lblTI = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Taxable Income", bd=10, justify='left',fg="white",bg="cadet blue", padx=5)
lblTI.grid(row=2, column=0, sticky=W)
txtTI = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=TaxableIncome, bd=10,width=40,justify='left')
txtTI.grid(row=2, column=1)
# --------------
lblTP = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Tax Paid", bd=9, justify='left', fg="white",bg="cadet blue",padx=5)
lblTP.grid(row=4, column=0, sticky=W)
txtTP = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=TaxPaid, bd=9,width=40,justify='left')
txtTP.grid(row=4, column=1)
#----------------------
lblDeduction = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Surcharge", bd=9, justify='left', fg="white",bg="cadet blue",padx=5)
lblDeduction.grid(row=3, column=0, sticky=W)
txtDeduction = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=Deduction, bd=8,width=40,justify='left')
txtDeduction.grid(row=3, column=1)
#-----------------------
lblNetPay = Label(LeftFrame2Left, font=('arial', 12, 'bold'), text="Net Income", bd=9, justify='left',fg="white",bg="cadet blue", padx=5)
lblNetPay.grid(row=5, column=0, sticky=W)
txtNetPay = Entry(LeftFrame2Left, font=('arial', 12, 'bold'), textvariable=NetPay, bd=8,width=40,justify='left')
txtNetPay.grid(row=5, column=1)

# ==============Buttons==========
btnTotal = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold') ,width=11,
                  text="Calculate Tax ", command=IncomeTax, justify='right').grid(row=0, column=0)
btnsave = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=7,
                  text="Save", command=savedata).grid(row=0, column=1)
btnReset = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=8,
                  text="Clear", command=reset).grid(row=0, column=4)
btnsummary = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=9,
                 text="Summary", command=viewData).grid(row=0, column=2)
btndelete = Button(BottomFrame, padx=2, pady=1, bd=2,fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=8,
                 text="Delete", command=delete).grid(row=0, column=3)
btnExit = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=10,
                 text="Exit", command=iExit).grid(row=0, column=8)
btnExit = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=10,
                 text="Send Mail", command=send).grid(row=0, column=7)
btnsearch = Button(BottomFrame, padx=2, pady=1, bd=2, fg="white",bg="cadet blue", font=('arial', 16, 'bold'), width=9,
                 text="search", command=check).grid(row=0, column=6)
txtName = Entry(BottomFrame, font=('arial', 16, 'bold'), textvariable=ReferenceId, bd=8, width=24, justify='left')
txtName.grid(row=0, column=5, pady=1)

#---------------------table----------------
scroll_y=Scrollbar(RightFrame1a,orient=VERTICAL)
scroll_x=Scrollbar(RightFrame1a,orient=HORIZONTAL)
IncomeRecord=ttk.Treeview(RightFrame1a,height=24,columns=("PaymentRef","Name","Pan","TaxPeriod","Income","TaxPaid","NetPay","TaxPayer","mail_id"),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.config(command=IncomeRecord.yview)
scroll_x.config(command=IncomeRecord.xview)
IncomeRecord.pack(fill=BOTH,expand=1)

IncomeRecord.heading("PaymentRef",text="ReferenceId")
IncomeRecord.heading("Name",text="Name")
IncomeRecord.heading("Pan",text="Pan")
IncomeRecord.heading("TaxPeriod",text="Year")
IncomeRecord.heading("Income",text="Income")
IncomeRecord.heading("TaxPaid",text="Tax Paid")
IncomeRecord.heading("NetPay",text="Net Income")
IncomeRecord.heading("TaxPayer",text="Tax Payer")
IncomeRecord.heading("mail_id",text="E-Mail")


IncomeRecord['show']='headings'

IncomeRecord.column("PaymentRef",width=80)
IncomeRecord.column("Name",width=70)
IncomeRecord.column("Pan",width=70)
IncomeRecord.column("TaxPeriod",width=60)
IncomeRecord.column("Income",width=80)
IncomeRecord.column("TaxPaid",width=80)
IncomeRecord.column("NetPay",width=80)
IncomeRecord.column("TaxPayer",width=115)
IncomeRecord.column("mail_id",width=130)

IncomeRecord.bind("<ButtonRelease-1>",get)
viewData() 
          
remove()

root.mainloop()


