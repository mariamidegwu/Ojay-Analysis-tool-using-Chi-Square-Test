from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages
from tkinter.filedialog import askopenfilename
import pdfkit
from tkinter import Toplevel
from tkinter import Toplevel, Button, Tk, Menu
from tkinter import font
import pandas as pd
from pdf2image import convert_from_path
import seaborn as sns
from os import path
import codecs
from PIL import ImageTk, Image
import db_config
import pymysql
from scipy.stats import chi2_contingency
import csv
import os, sys
from tkinter import ttk, messagebox
from tkinter import filedialog
import os
import win32api
import tempfile
import win32print
import webbrowser
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
plt.style.use('bmh')
config = pdfkit.configuration(wkhtmltopdf="C:/ANALYSISAPP/wkhtmltopdf/bin/wkhtmltopdf.exe")


db= pymysql.connect(host=db_config.DB_SERVER,
                          user=db_config.DB_USER,
                          password=db_config.DB_PASS,
                          database=db_config.DB)
cur = db.cursor()


global textarea
global fminid


def contr_database():
  tree.delete(*tree.get_children())
  tree.pack(side='left', padx=0, pady=0)
  cur.execute("delete from analysis1")
  messagebox.showinfo("Reset", "Reset Successfull.")
  db.commit()


# converting file to csv
def calcsv():
    messagebox.showinfo("CSV file activated",
                        "Ensure you select your variables and chart before clicking on the post analysis button")
    df_tips= pd.read_csv(r"C:/ANALYSISAPP/mop.csv")
    df_cont = pd.crosstab(index=df_tips['GENDER'], columns=df_tips['DIAGNOSIS'])
    stat, p, dof, expected = chi2_contingency(df_cont)
    df_chi2 = ((df_cont - expected) ** 2) / expected
    df_chi2.loc[:, 'Total'] = df_chi2.sum(axis=1)
    df_chi2.loc['Total'] = df_chi2.sum()
    bac= pd.crosstab(index=df_tips.DIAGNOSIS, columns=df_tips.DIAGNOSIS, values=df_tips.AGE, aggfunc='median')
    bac1= pd.crosstab(index=df_tips.DIAGNOSIS, columns=df_tips.GENDER, values=df_tips.AGE, aggfunc='std')
    bac2= pd.crosstab(index=df_tips.DIAGNOSIS, columns=df_tips.DIAGNOSIS, values=df_tips.AGE, aggfunc='std')
    bac.to_csv("C:/ANALYSISAPP/pinky.csv")
    bac1.to_csv("C:/ANALYSISAPP/pinky1gd.csv")
    bac2.to_csv("C:/ANALYSISAPP/pinky2.csv")
    df_chi2.to_csv("C:/ANALYSISAPP/oj1.csv")
    with open("pinky.csv", "r") as src:
        reader = csv.reader(src)
        data = []
        for row in reader:
            data.append(row)
    result1 = data[1][1]
    result2 = data[2][2]
    result3 = data[3][3]
    print(result1, result2, result3)
    columnNames = ['FEVER', 'MALARIA', 'TYPHOID']
    with open("ojmd.csv", "w", newline='') as mele:
        dw = csv.writer(mele, delimiter=',')
        mele.write(','.join(columnNames) + '\n')
        mele.write(str(result1) + "," + str(result2) + "," + str(result3))

    with open("pinky2.csv", "r") as src1:
        reader1 = csv.reader(src1)
        data1 = []
        for row1 in reader1:
            data1.append(row1)
    result1e = data1[1][1]
    result2e = data1[2][2]
    result3e = data1[3][3]
    print(result1e, result2e, result3e)
    columnNamese = ['FEVER', 'MALARIA', 'TYPHOID']
    with open("ojag.csv", "w", newline='') as melee:
        dwe = csv.writer(melee, delimiter=',')
        melee.write(','.join(columnNamese) + '\n')
        melee.write(str(result1e) + "," + str(result2e) + "," + str(result3e))


def load_csv():
  db = pymysql.connect(host=db_config.DB_SERVER,
                         user=db_config.DB_USER,
                         password=db_config.DB_PASS,
                         database=db_config.DB)

  cur = db.cursor()
  filename = filedialog.askopenfilename()
  with open(filename, 'r') as input, open('test.csv', 'w') as output:
      output.writelines(line.upper() for line in input)
  f = open('test.csv')
  reader = csv.DictReader(f, delimiter=',')
  for row in reader:
    emp_id = row['AGE']
    name = row['GENDER']
    dt = row['DATE']
    ti = row['DIAGNOSIS']
    tree.insert(parent='',index='end',  text='', values=(emp_id, name, dt,ti))
    columnNames = ['AGE', 'GENDER','DATE','DIAGNOSIS']
    with open("mop.csv", "w", newline='') as mele:
        dw = csv.writer(mele, delimiter=',')
        mele.write(','.join(columnNames) + '\n')
        for cm in tree.get_children():
            row2 = tree.item(cm)['values']
            dw.writerow(row2)
    with open("ben.csv", "w", newline='') as mycmtr:
        csvwriter = csv.writer(mycmtr,delimiter=',')
        for row_cm in tree.get_children():
            row1 = tree.item(row_cm)['values']
            csvwriter.writerow(row1)
  cur.execute(
      "CREATE TABLE IF NOT EXISTS `analysis1` (AGE VARCHAR(30), GENDER VARCHAR(20), DATE VARCHAR(50),DIAGNOSIS VARCHAR(50))")
  with open("ben.csv", 'r', encoding='utf-8')as ret:
      all_values3 = []
      for rtar in csv.reader(ret, delimiter=","):
          value3 = (rtar[0], rtar[1], rtar[2], rtar[3])
          all_values3 = [value3]
          query3 = "insert into analysis1(AGE,GENDER,DATE,DIAGNOSIS)values(%s,%s,%s,%s)"
          cur.executemany(query3, all_values3)
          ret.flush()
          db.commit()

def ingrp2():
    global q
    global textarea
    global fm
    global incmbut1
    global lnb
    global alpha
    global red
    global fig21
    global lbn
    pap1 = v1.get()
    pap2 = v11.get()
    pap3 = v2.get()
    alpha = 0.05
    df = pd.read_csv(r"mop.csv")
    fd = "<style>table, th, td {border:1px solid black;}</style>"
    sdg = "width:70%"
    crosstab = pd.crosstab(index=df['GENDER'], columns=df['DIAGNOSIS'])
    stat, p, dof, expected = chi2_contingency(crosstab)
    print("stat value is " + str(stat))
    print("p value is " + str(p))
    print("dof value is " + str(dof))
    sq6 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='FEVER' AND GENDER='F'"
    sq5 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='FEVER' AND GENDER='M'"
    sq2 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='MALARIA' AND GENDER='F'"
    sq1 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='MALARIA' AND GENDER='M'"
    sq4 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='TYPHOID' AND GENDER='F'"
    sq3 = "SELECT COUNT(DIAGNOSIS) FROM analysis1 WHERE DIAGNOSIS='TYPHOID' AND GENDER='M'"

    rumn = cur.execute(sq1)
    rumn = cur.fetchone()[0]
    ruman = cur.execute(sq2)
    ruman = cur.fetchone()[0]
    rumbn = cur.execute(sq3)
    rumbn = cur.fetchone()[0]
    rumcn = cur.execute(sq4)
    rumcn = cur.fetchone()[0]
    rumdn = cur.execute(sq5)
    rumdn = cur.fetchone()[0]
    rumen = cur.execute(sq6)
    rumen = cur.fetchone()[0]
    a.set(rumn)
    a1.set(ruman)
    b.set(rumbn)
    b1.set(rumcn)
    c.set(rumdn)
    c1.set(rumen)
    d = rumn + rumbn + rumdn
    d1 = ruman + rumcn + rumen
    e = rumn + ruman
    e1 = rumbn + rumcn
    e2 = rumdn + rumen
    f = d + d1

    jk = pd.read_csv("ojmd.csv")
    jk.to_html("med.htm")
    htmlfile = jk.to_html()
    jk1 = pd.read_csv("ojag.csv")
    jk1.to_html("med3.htm")
    htmlfile1 = jk1.to_html()
    jk2 = pd.read_csv("pinky1gd.csv")
    jk2.to_html("med4.htm")
    htmlfile2 = jk2.to_html()
    jk3 = pd.read_csv("oj1.csv")
    jk3.to_html("med1.htm")
    htmlfile3 = jk3.to_html()

    def pdf():
        q = textarea.get("1.0", "end-1c")
        options = {"enable-local-file-access": None, "quiet": ""}
        pdfkit.from_string(q, 'my.pdf', verbose=True, options=options, configuration=config)
        print("pdf created")
        os.startfile("my.pdf")

    if pap1 == "DIAGNOSIS" and pap2 == "GENDER" and pap3 =="BOX-PLOT CHART":
        data = pd.read_csv(r"mop.csv", low_memory=False)
        data.head()
        datar = data['DATE'].apply(lambda x: pd.Timestamp(x).strftime('%B'))
        fig, axarr = plt.subplots(2, 2, figsize=(17, 12), dpi=80, facecolor='w', edgecolor='k')
        sns.set(style="white")
        sns.countplot(x='AGE', hue='GENDER', data=data, ax=axarr[0][0], linewidth=3,
                      edgecolor=sns.color_palette('Greys_r', 24))
        axarr[0][0].set_title('Distribution of Patient Age and Gender')
        sns.countplot(x='GENDER', hue='DIAGNOSIS', data=data, ax=axarr[0][1], palette="Accent_r")
        axarr[0][1].set_title('Distribution of Patient Gender and Diagnosis')
        sns.countplot(x=datar, hue='GENDER', data=data, ax=axarr[1][0], palette="Accent_r")
        axarr[1][0].set_title('Distribution of Patient Date and Gender')
        sns.countplot(x='DIAGNOSIS', hue='AGE', data=data, ax=axarr[1][1], palette="Accent_r")
        axarr[1][1].set_title('Distribution of Patient Diagnosis and Age')
        fig.suptitle('Frequency Distribution of Different Categories of Variables', fontsize=20)
        plt.savefig('dis.png')
        df = pd.read_csv(r"mop.csv")
        df.head()
        fig21 = plt.figure(figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
        # sns.boxplot(x='DIAGNOSIS', y='AGE', data=df)
        sns.boxplot(x='DIAGNOSIS', y='AGE', hue='GENDER', data=df)
        plt.savefig('scat.png')
        messagebox.showinfo("Statistical Report will generate in 7-sec",
                            "Click on the 'ok' button below a Submit Group Analysis Button will appear click on it ")
        textarea = Text(fminid)
        textarea['font'] = "Arial 20"
        textarea['bg'] = "cyan"
        textarea['borderwidth'] = 2
        textarea.insert(END, f"""<div><img src="C:/ANALYSISAPP/ojayicon.png" />""")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<h5 style=""color:blue>OJAY ANALYSIS TOOL</h5>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</div>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"<form><i>")
        textarea.insert(END,
                        """<p><h3><center><b><u><i>REPORT SHOWING THE ANALYSIS OF MALARIA,TYPHOID AND FEVER</p></i></u></b></center>""")
        textarea.insert(END, f"<br><u>Statistical Report of Diagnosis and various Standard Deviation </u></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of students  medium age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile}</br>")
        textarea.insert(END, f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile1}</br>")
        textarea.insert(END,
                        f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis and Gender</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile2}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<u>Statistical Test Report Verifying The Significant Relationship Between Diagnosis And Gender</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Observed Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Expected Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n--------------------FEMALE------------------- /-------------------MALE---------------- ")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n-----FEVER------MALARIA-----TYPHOID--/---FEVER----MALARIA---TYPHOID")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n{expected}")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Chi-Square Value</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile3}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>Degree of Freedom \n{dof}</br>")
        textarea.insert(END, f"<br>Chi-Square Value \n{stat}</br>")
        textarea.insert(END, f"<br>P-Value \n{p}</br>")
        textarea.insert(END, f"<br>")
        if p <= alpha:
            textarea.insert(END,
                            f"\n As the p-value is Less than 0.05, we reject the NULL hypothesis and accept the alternative hypothesis that state that the variables has a significant relationship")
        else:
            textarea.insert(END,
                            f"\nAs the p-value is greater than 0.05, we accept the NULL hypothesis that state that the variables do not have any significant relationship")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</h3>")
        textarea.insert(END, f"</h1>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form></i>")
        textarea.insert(END, f"<form>")
        textarea.insert(END, f"{fd}")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<h4><center><b><u><i>TABLE SHOWING THE DISTRIBUTION OF DATA</i></u></b></center></h4>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form>")
        textarea.insert(END, f"<form>")
        textarea.insert(END, """\n<center><img src="C:/ANALYSISAPP/dis.png" /></center>""")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</br>")
        textarea.insert(END,
                        f"\n<h4><center><b><u><i>SEABORN BOX-PLOT OF MEDIAN AGES OF STUDENTS WHO ARE  DIAGNOSIS WITH THE DISEASES GROUPED BY GENDER AND DIAGNOSIS</i></u></b></center></h4>")
        textarea.insert(END, """<center><img src="C:/ANALYSISAPP/scat.png" /></center>""")
        textarea.insert(END, f"</form>")
        textarea.bind("<Control-b>", pdf)
        lnb = Button(root,text="SUBMIT GROUP ANALYSIS", background='red', command=pdf)
        lnb.place(x=0, y=0)

    elif pap1 == "DIAGNOSIS" and pap2 == "GENDER" and pap3 =="BAR CHART":
         data = pd.read_csv(r"mop.csv", low_memory=False)
         data.head()
         datar = data['DATE'].apply(lambda x: pd.Timestamp(x).strftime('%B'))
         fig, axarr = plt.subplots(2, 2, figsize=(17, 12), dpi=80, facecolor='w', edgecolor='k')
         sns.set(style="white")
         sns.countplot(x='AGE', hue='GENDER', data=data, ax=axarr[0][0], linewidth=3,
                       edgecolor=sns.color_palette('Greys_r', 24))
         axarr[0][0].set_title('Distribution of Patient Age and Gender')
         sns.countplot(x='GENDER', hue='DIAGNOSIS', data=data, ax=axarr[0][1], palette="Accent_r")
         axarr[0][1].set_title('Distribution of Patient Gender and Diagnosis')
         sns.countplot(x=datar, hue='DIAGNOSIS', data=data, ax=axarr[1][0], palette="Accent_r")
         axarr[1][0].set_title('Distribution of Patient Date and Diagnosis')
         sns.countplot(x='DIAGNOSIS', hue='AGE', data=data, ax=axarr[1][1], palette="Accent_r")
         axarr[1][1].set_title('Distribution of Patient Diagnosis and Age')
         fig.suptitle('Frequency Distribution of Different Categorical Variable', fontsize=16)
         plt.savefig('dis2.png')
         survey = pd.read_csv(r"mop.csv", low_memory=False)
         survey['AGE'].std()
         fiIg, ax = plt.subplots(figsize=(8, 4))
         se = survey.groupby(['DIAGNOSIS', 'GENDER']).agg(AGE=('AGE', 'std'))
         se.plot(kind='barh', ax=ax, fontsize=7)
         plt.savefig('bar1.png')
         survey1 = pd.read_csv(r"mop.csv", low_memory=False)
         survey1['AGE'].std()
         fi4g, ax = plt.subplots(figsize=(8, 4))
         se1 = survey1.groupby(['DIAGNOSIS']).agg(AGE=('AGE', 'std'))
         se1.plot(kind='barh', ax=ax, color='green', fontsize=8)
         plt.savefig('bar2.png')
         messagebox.showinfo("Statistical Report will generate in 7-sec",
                             "Click on the 'ok' button below a Submit Group Analysis Button will appear click on it ")
         textarea = Text(fminid)
         textarea['font'] = "Arial 20"
         textarea['bg'] = "cyan"
         textarea['borderwidth'] = 2
         textarea.insert(END, f"""<div><img src="C:/ANALYSISAPP/ojayicon.png" />""")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n<h5 style=""color:blue>OJAY ANALYSIS TOOL</h5>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"</div>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"<form><i>")
         textarea.insert(END,
                         """<p><h3><center><b><u><i>REPORT SHOWING THE ANALYSIS OF MALARIA,TYPHOID AND FEVER</p></i></u></b></center>""")
         textarea.insert(END, f"<br><u>Statistical Report of Diagnosis and various Standard Deviation </u></br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n<u>Report of students  medium age grouped by Diagnosis</u>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>{htmlfile}</br>")
         textarea.insert(END, f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis</u>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>{htmlfile1}</br>")
         textarea.insert(END, f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis and Gender</u>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>{htmlfile2}</br>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END,
                         f"\n<u>Statistical Test Report Verifying The Significant Relationship Between Diagnosis And Gender</u>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n<u>Report of Observed Value</u>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END,
                         f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                         f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                         f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n<u>Report of Expected Value</u>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END,
                         f"\n--------------------FEMALE------------------- /-------------------MALE---------------- ")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n-----FEVER------MALARIA-----TYPHOID--/---FEVER----MALARIA---TYPHOID")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n{expected}")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"\n<u>Report of Chi-Square Value</u>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>{htmlfile3}</br>")
         textarea.insert(END, f"<br></br>")
         textarea.insert(END, f"<br>Degree of Freedom \n{dof}</br>")
         textarea.insert(END, f"<br>Chi-Square Value \n{stat}</br>")
         textarea.insert(END, f"<br>P-Value \n{p}</br>")
         textarea.insert(END, f"<br>")
         if p <= alpha:
             textarea.insert(END,
                             f"\n As the p-value is Less than 0.05, we reject the NULL hypothesis and accept the alternative hypothesis that state that the variables has a significant relationship")
         else:
             textarea.insert(END,
                             f"\nAs the p-value is greater than 0.05, we accept the NULL hypothesis that state that the variables do not have any significant relationship")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END, f"</h3>")
         textarea.insert(END, f"</h1>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"</form></i>")
         textarea.insert(END, f"<form>")
         textarea.insert(END, f"{fd}")
         textarea.insert(END, f"<br>")
         textarea.insert(END,
                         f"\n<h4><center><b><u><i>TABLE SHOWING THE DISTRIBUTION OF DATA</i></u></b></center></h4>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"<br>")
         textarea.insert(END,
                         f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                         f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                         f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
         textarea.insert(END, f"</br>")
         textarea.insert(END, f"</form>")
         textarea.insert(END, f"<form>")
         textarea.insert(END,
                         """\n<center><img src="C:/ANALYSISAPP/dis2.png" /></center>""")
         textarea.insert(END,
                         f"\n<h4><center><b><u><i>STANDARD DEVIATION OF STUDENTS AGES DIAGNOSED WITH THE DISEASES GROUPED BY DIAGNOSIS AND GENDER</i></u></b></center></h4>")
         textarea.insert(END,
                         """<center><img src="C:/ANALYSISAPP/bar1.png" /></center>""")
         textarea.insert(END,
                         f"\n<h4><center><b><u><i>STANDARD DEVIATION OF STUDENTS AGES DIAGNOSED WITH THE DISEASES GROUPED BY DIAGNOSIS</i></u></b></center></h4>")
         textarea.insert(END,
                         """<center><img src="C:/ANALYSISAPP/bar2.png" /></center>""")
         textarea.insert(END, f"</form>")
         textarea.bind("<Control-b>", pdf)
         lnb = Button(root, text="SUBMIT GROUP ANALYSIS", background='red', command=pdf)
         lnb.place(x=0, y=0)

    elif pap1 == "DIAGNOSIS" and pap2 == "GENDER" and pap3 == "PIE CHART":
        data = pd.read_csv(r"mop.csv", low_memory=False)
        data.head()
        datar = data['DATE'].apply(lambda x: pd.Timestamp(x).strftime('%B'))
        fig, axarr = plt.subplots(2, 2, figsize=(17, 12), dpi=80, facecolor='w', edgecolor='k')
        sns.set(style="white")
        sns.countplot(x='AGE', hue='GENDER', data=data, ax=axarr[0][0], linewidth=3,
                      edgecolor=sns.color_palette('Greys_r', 24))
        axarr[0][0].set_title('Distribution of Patient Age and Gender')
        sns.countplot(x='GENDER', hue='DIAGNOSIS', data=data, ax=axarr[0][1], palette="Accent_r")
        axarr[0][1].set_title('Distribution of Patient Gender and Diagnosis')
        sns.countplot(x=datar, hue='DIAGNOSIS', data=data, ax=axarr[1][0], palette="Accent_r")
        axarr[1][0].set_title('Distribution of Patient Date and Diagnosis')
        sns.countplot(x='DIAGNOSIS', hue='AGE', data=data, ax=axarr[1][1], palette="Accent_r")
        axarr[1][1].set_title('Distribution of Patient Diagnosis and Age')
        fig.suptitle('Frequency Distribution of Different Categorical Variable', fontsize=16)
        plt.savefig('dis3.png')
        survey = pd.read_csv(r"mop.csv")
        survey['AGE'].std()
        print(survey.std())
        fig4, ax = plt.subplots(figsize=(8, 5))
        groupby_count1 = survey.groupby(['GENDER']).agg(AGE=('AGE', 'std'))
        print('Count of values, grouped by the GENDER: ' + str(groupby_count1))
        yer = survey.groupby('DIAGNOSIS')['DIAGNOSIS'].size()
        explode = (0.1, 0, 0)
        yer.plot(kind="pie", autopct='%1.1f%%', subplots=True, explode=explode, shadow=True, ax=ax, startangle=90,
                 fontsize=10,
                 wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'}, textprops={'size': 'x-large'})
        ax.set_title("INFECTED RATE OF STUDENTS", font="century", fontsize=9)
        ax.legend(bbox_to_anchor=(1, 0), loc='lower right', bbox_transform=fig4.transFigure, prop={'size': 8})
        plt.savefig('pie.png')
        messagebox.showinfo("Statistical Report will generate in 7-sec",
                            "Click on the 'ok' button below a Submit Group Analysis Button will appear click on it ")
        textarea = Text(fminid)
        textarea['font'] = "Arial 20"
        textarea['bg'] = "cyan"
        textarea['borderwidth'] = 2

        textarea.insert(END, f"""<div><img src="C:/ANALYSISAPP/ojayicon.png" />""")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<h5 style=""color:blue>OJAY ANALYSIS TOOL</h5>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</div>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"<form><i>")
        textarea.insert(END,
                        """<p><h3><center><b><u><i>REPORT SHOWING THE ANALYSIS OF MALARIA,TYPHOID AND FEVER</p></i></u></b></center>""")
        textarea.insert(END, f"<br><u>Statistical Report of Diagnosis and various Standard Deviation </u></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of students  medium age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile}</br>")
        textarea.insert(END, f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile1}</br>")
        textarea.insert(END,
                        f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis and Gender</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile2}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<u>Statistical Test Report Verifying The Significant Relationship Between Diagnosis And Gender</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Observed Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Expected Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n--------------------FEMALE------------------- /-------------------MALE---------------- ")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n-----FEVER------MALARIA-----TYPHOID--/---FEVER----MALARIA---TYPHOID")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n{expected}")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Chi-Square Value</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile3}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>Degree of Freedom \n{dof}</br>")
        textarea.insert(END, f"<br>Chi-Square Value \n{stat}</br>")
        textarea.insert(END, f"<br>P-Value \n{p}</br>")
        textarea.insert(END, f"<br>")
        if p <= alpha:
            textarea.insert(END,
                            f"\n As the p-value is Less than 0.05, we reject the NULL hypothesis and accept the alternative hypothesis that state that the variables has a significant relationship")
        else:
            textarea.insert(END,
                            f"\nAs the p-value is greater than 0.05, we accept the NULL hypothesis that state that the variables do not have any significant relationship")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</h3>")
        textarea.insert(END, f"</h1>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form></i>")
        textarea.insert(END, f"<form>")
        textarea.insert(END, f"{fd}")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<h4><center><b><u><i>TABLE SHOWING THE DISTRIBUTION OF DATA</i></u></b></center></h4>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form>")
        textarea.insert(END, f"<form>")
        textarea.insert(END,
                        """\n<center><img src="C:/ANALYSISAPP/dis3.png" /></center>""")
        textarea.insert(END,
                        f"\n<h4><center><u><i>PIE-CHART SHOWING PERCENTAGES OF INFECTION</i></u></center></h4>")
        textarea.insert(END,
                        """<center><img src="C:/ANALYSISAPP/pie.png" /></center>""")
        textarea.insert(END, f"</form>")
        textarea.bind("<Control-b>", pdf)
        lnb = Button(root, text="SUBMIT GROUP ANALYSIS", background='red', command=pdf)
        lnb.place(x=0, y=0)
    elif pap1 == "DIAGNOSIS" and pap2 == "GENDER" and pap3 == "BAR-2 CHART":
        plt.style.use('bmh')
        data = pd.read_csv(r"mop.csv", low_memory=False)
        data.head()
        datar = data['DATE'].apply(lambda x: pd.Timestamp(x).strftime('%B'))
        fig, axarr = plt.subplots(2, 2, figsize=(17, 12), dpi=80, facecolor='w', edgecolor='k')
        sns.set(style="white")
        sns.countplot(x='AGE', hue='GENDER', data=data, ax=axarr[0][0], linewidth=3,
                      edgecolor=sns.color_palette('Greys_r', 24))
        axarr[0][0].set_title('Distribution of Patient Age and Gender')
        sns.countplot(x='GENDER', hue='DIAGNOSIS', data=data, ax=axarr[0][1], palette="Accent_r")
        axarr[0][1].set_title('Distribution of Patient Gender and Diagnosis')
        sns.countplot(x=datar, hue='DIAGNOSIS', data=data, ax=axarr[1][0], palette="Accent_r")
        axarr[1][0].set_title('Distribution of Patient Date and Diagnosis')
        sns.countplot(x='DIAGNOSIS', hue='AGE', data=data, ax=axarr[1][1], palette="Accent_r")
        axarr[1][1].set_title('Distribution of Patient Diagnosis and Age')
        fig.suptitle('Frequency Distribution of Different Categorical Variable', fontsize=16)
        plt.savefig('dis4.png')
        myDf = pd.read_csv(r"mop.csv", low_memory=False)
        myDf.head()
        myfield = myDf['GENDER']
        myfreq = myfield.value_counts()
        mykeys = myfreq.keys()
        myvals = myfreq.values
        myfreqtable = pd.DataFrame({'GENDER': mykeys, 'Frequency': myvals})
        myfreqtable['Percent'] = myfreqtable['Frequency'] / myfreqtable['Frequency'].sum() * 100
        myfreqtable = myfreqtable.sort_values(by=['Frequency'], ascending=False)
        myfreqtable = myfreqtable.reset_index(drop=True)
        myfreqtable['Cumulative Percent'] = myfreqtable['Frequency'].cumsum() / myfreqtable['Frequency'].sum() * 100
        fig32, ax = plt.subplots()
        ax.set_xlabel('GENDER')
        ax.bar('GENDER', 'Frequency', data=myfreqtable)
        ax.set_ylabel("percent")
        ax.set_ylim(ymin=0)
        ax2 = ax.twinx()
        ax2.plot('GENDER', 'Cumulative Percent', data=myfreqtable, marker='o', color='red')
        ax2.set_ylabel("Cumulative Percent")
        ax2.set_ylim(ymin=0)
        plt.savefig('bar22.png')
        messagebox.showinfo("Statistical Report will generate in 7-sec",
                            "Click on the 'ok' button below a Submit Group Analysis Button will appear click on it ")
        textarea = Text(fminid)
        textarea['font'] = "Arial 20"
        textarea['bg'] = "cyan"
        textarea['borderwidth'] = 2

        textarea.insert(END, f"""<div><img src="C:/ANALYSISAPP/ojayicon.png" />""")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<h5 style=""color:blue>OJAY ANALYSIS TOOL</h5>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</div>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"<form><i>")
        textarea.insert(END,
                        """<p><h3><center><b><u><i>REPORT SHOWING THE ANALYSIS OF MALARIA,TYPHOID AND FEVER</p></i></u></b></center>""")
        textarea.insert(END, f"<br><u>Statistical Report of Diagnosis and various Standard Deviation </u></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of students  medium age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile}</br>")
        textarea.insert(END, f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile1}</br>")
        textarea.insert(END,
                        f"\n<u>Report of Standard Deviation of students age grouped by Diagnosis and Gender</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile2}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<u>Statistical Test Report Verifying The Significant Relationship Between Diagnosis And Gender</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Observed Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Expected Value</u>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n--------------------FEMALE------------------- /-------------------MALE---------------- ")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n-----FEVER------MALARIA-----TYPHOID--/---FEVER----MALARIA---TYPHOID")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n{expected}")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"\n<u>Report of Chi-Square Value</u>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>{htmlfile3}</br>")
        textarea.insert(END, f"<br></br>")
        textarea.insert(END, f"<br>Degree of Freedom \n{dof}</br>")
        textarea.insert(END, f"<br>Chi-Square Value \n{stat}</br>")
        textarea.insert(END, f"<br>P-Value \n{p}</br>")
        textarea.insert(END, f"<br>")
        if p <= alpha:
            textarea.insert(END,
                            f"\n As the p-value is Less than 0.05, we reject the NULL hypothesis and accept the alternative hypothesis that state that the variables has a significant relationship")
        else:
            textarea.insert(END,
                            f"\nAs the p-value is greater than 0.05, we accept the NULL hypothesis that state that the variables do not have any significant relationship")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</h3>")
        textarea.insert(END, f"</h1>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form></i>")
        textarea.insert(END, f"<form>")
        textarea.insert(END, f"{fd}")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"\n<h4><center><b><u><i>TABLE SHOWING THE DISTRIBUTION OF DATA</i></u></b></center></h4>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"<br>")
        textarea.insert(END,
                        f"<table style={sdg}><tr><th>GENDER CATEGORY</th><th>FEVER </th><th>MALARIA</th><th> TYPHOID</th><th>TOTAL</th></tr><tr><td>FEMALE</td>"
                        f"<td>{c1.get()}<td>{a1.get()}<td>{b1.get()}<td>{d1}<td></td></tr><tr><td>MALE</td><td>{c.get()}</td>"
                        f"<td>{a.get()}</td><td>{b.get()}</td><td>{d}</td></tr><tr><td>TOTAL</td><td>{e2}</td><td>{e}</td><td>{e1}</td><td>{f}</td></tr></table>")
        textarea.insert(END, f"</br>")
        textarea.insert(END, f"</form>")
        textarea.insert(END, f"<form>")
        textarea.insert(END,
                        """\n<center><img src="C:/ANALYSISAPP/dis4.png"/></center>""")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</br>")
        textarea.insert(END,
                        f"\n<h4><center><b><u><i>COMPARISON BETWEEN MALE AND FEMALE DIAGONOSIS WITH THE DISEASES</i></u></b></center></h4>")
        textarea.insert(END, f"<br>")
        textarea.insert(END, f"</br>")
        textarea.insert(END,
                        """<center><img src="C:/ANALYSISAPP/bar22.png" /></center>""")
        textarea.insert(END, f"</form>")
        textarea.bind("<Control-b>", pdf)
        lnb = Button(root, text="SUBMIT GROUP ANALYSIS", background='red', command=pdf)
        lnb.place(x=0, y=0)

root = Tk()
root.title("OJAY-ANALYSIS-TOOL USING CHI-SQUARE METHOD")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 700
height = 470
root.config(bg='#355E3B')
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.iconbitmap("ojy.ico")
root.resizable(0, 0)

a=StringVar()
a1=StringVar()
b=StringVar()
b1=StringVar()
c=StringVar()
c1=StringVar()
v1 = StringVar()
v11 = StringVar()
v2 = StringVar()
fm2 = Frame(root, bg='#355E3B', width=700, height=50, bd=8, relief="raise")
fm2.pack(side=TOP)
fm3 = Frame(root, bg='#355E3B', width=700, height=50)
fm3.pack(side=TOP)
fm4 = Frame(fm3, bg='#355E3B', width=200, height=50)
fm4.pack(side=LEFT)
but = Frame(fm3, bg='#355E3B', width=500, height=50)
but.pack(side=RIGHT)
fmmn = Frame(fm3, bg='#355E3B', width=700, height=50, bd=8, relief="raise")
fmmn.pack(side=BOTTOM)
fminid = Frame(width=700, height=300, bd=8, bg='#355E3B', relief="raise")
fminid.place(x=0, y=180)
llb = Label(root, text="BROWSE FOR CSV FILE", bg='#355E3B', fg='black', font=("century", 9))
llb.place(x=3, y=15)
Button(root, text='LOAD CSV', width=12, font=("century", 9), bg='#355E3B', fg='black', command=load_csv).place(x=170,y=12)
Button(root, text='ACTIVATE CSV', width=12, font=("century", 9), bg='#355E3B', fg='black', command=calcsv).place(x=280, y=12)
#Button(root, text='CSV', width=7, font=("century", 9), bg='#355E3B', fg='black', command=perform).place(x=510, y=12)
Button(root, text='RESET VIEW', width=12, font=("century", 9), bg='#355E3B', fg='black', command=contr_database).place(x=584, y=12)
fm = Frame(bg='#355E3B', width=700, height=50, bd=8, relief="raise")
fm.place(x=0, y=80)
v1.set("SELECT VARIABLE 1")
dropv = OptionMenu(fminid, v1, "DIAGNOSIS")
dropv.place(x=0, y=200)
dropv.config(width=20, height=0)
v11.set("SELECT VARIABLE 2")
dropv1 = OptionMenu(fminid, v11, "GENDER")
dropv1.place(x=170, y=200)
dropv1.config(width=20, height=0)
v2.set("SELECT CHART STYLE")
dropv2 = OptionMenu(fminid, v2, 'BOX-PLOT CHART',"BAR CHART", "PIE CHART", "BAR-2 CHART")
dropv2.place(x=345, y=200)
cmtlab1 = Label(fminid, text='GROUP ANALYSIS-FOR STATISTICAL REPORT', width=50, anchor='w',
                font=("century",8))
cmtlab1.place(x=0, y=152)
inidg = Label(fminid, text='VARIABLES----------------------------------------CHART STYLES ', anchor='w',
              bg='#355E3B', fg='black', width=50, font=("century", 8)).place(x=0, y=170)
incmbut1 = Button(fminid, text="POST ANALYSIS", anchor="w", bg='#355E3B', fg='black', command=ingrp2)
incmbut1.place(x=510, y=203)
#incmbut1.place(x=395, y=12)
barx = Scrollbar(fm, orient=HORIZONTAL)
bary = Scrollbar(fm, orient=VERTICAL)
tree = ttk.Treeview(fm, height=10, columns=("AGE", "GENDER", "DATE", 'DIAGNOSIS'), selectmode="extended",
                    yscrollcommand=bary.set, xscrollcommand=barx.set)
bary.config(command=tree.yview)
bary.pack(side=RIGHT, fill=Y)
barx.config(command=tree.xview)
barx.pack(side=BOTTOM, fill=X)
tree.heading("#0", text="", anchor=W)
tree.heading("AGE", text="AGE")
tree.heading("GENDER", text="GENDER")
tree.heading("DATE", text="DATE")
tree.heading("DIAGNOSIS", text="DIAGNOSIS")
tree.column("#0", width=0, stretch=NO)
tree.column('#1', stretch=NO, minwidth=0, width=150)
tree.column('#2', stretch=NO, minwidth=0, width=150)
tree.column('#3', stretch=NO, minwidth=0, width=150)
tree.column('#4', stretch=NO, minwidth=0, width=217)
tree.pack()

root.mainloop()
cur.execute("delete from analysis1")

