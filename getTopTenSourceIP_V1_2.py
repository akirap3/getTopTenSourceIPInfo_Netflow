#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json, os, time, requests, csv, sys, re
import pandas as pd
from json import loads
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from dicttoxml import dicttoxml
from pprint import pprint
from xml.etree import ElementTree


# In[ ]:


def getXMLfile(response):
    # getName
    name = response.json()['devDetails']['hdrTitle']
    
    # create xml files accordingly
    responesContent = response.content
    convertToDict = json.loads(responesContent)
    xml = dicttoxml(convertToDict)
    file = open(os.getcwd()+"\\input.xml", "wb")
    file.write(xml)
    time.sleep(.500)
    file.close()
    time.sleep(.500)
    
    # if there is existed fiile, remove it. And pass the error
    try:
        os.remove(os.getcwd()+"\\"+name+".xml")
    except os.error:
        pass

    # clean unwanted data
    with open(os.getcwd()+"\\input.xml", "r", encoding = "utf8") as infile, open(os.getcwd()+"\\"+name+".xml", "wb") as outfile:
        data = infile.read()
        time.sleep(.500)
        data = data.replace(' type="str"', '')
        time.sleep(.500)
        data = data.replace(' type="dict"', '')
        time.sleep(0.500)
        data = data.replace(' type="bool"', '')
        time.sleep(0.500)
        data = data.replace(' type="list"', '')
        time.sleep(0.500)
        data = bytes(data, encoding = "utf8")
        time.sleep(.500)
        outfile.write(data)
        time.sleep(.500)

    # close files and remove the temporary 
    infile.close()
    os.remove(os.getcwd()+"\\input.xml")
    outfile.close()


# In[ ]:


def xmlConvertToCSV(response):
    # getName
    name = response.json()['devDetails']['hdrTitle']
       
    # Read the files
    tree = ElementTree.parse(name+".xml")
    root = tree.getroot()

    # change the working directory
    os.chdir(os.getcwd()+"\\CSVFILE")

    # creat a file for writing
    sitescope_data = open(name+".csv",'w',newline='',encoding='utf-8')
    csvwriter = csv.writer(sitescope_data)
    
    # define column name
    col_names = ['hdrTitle','app','Prot','dscp','dst','src','port','dstport','dscpCode','traffic']
    csvwriter.writerow(col_names)
       
    # write rowdata to csv file
    for event in root.findall('Data/item'):  
        
        event_data = []
        hdrTitle = root.find('devDetails/hdrTitle')
        if hdrTitle != None :
            hdrTitle = hdrTitle.text        
        event_data.append(hdrTitle)
        
        app = event.find('app')
        if app != None :
            app = app.text
        event_data.append(app)

        prot = event.find('prot')
        if prot != None :
            prot = prot.text
        event_data.append(prot)

        dscp = event.find('dscp')
        if dscp != None :
            dscp = dscp.text
        event_data.append(dscp)

        dst = event.find('dst')
        if dst != None :
            dst = dst.text
        event_data.append(dst)

        src = event.find('src')
        if src != None :
            src = src.text
        event_data.append(src)

        port = event.find('port')
        if port != None :
            port = port.text
        event_data.append(port)

        dstport = event.find('dstport')
        if dstport != None :
            dstport = dstport.text
        event_data.append(dstport)

        dscpCode = event.find('dscpCode')
        if dscpCode != None :
            dscpCode = dscpCode.text
        event_data.append(dscpCode)

        traffic = event.find('traffic')
        if traffic != None :
            traffic = traffic.text
        event_data.append(traffic)

        csvwriter.writerow(event_data)

    sitescope_data.close()

    dataframe = pd.read_csv(name+".csv")
    os.chdir('../')


# In[ ]:


def combineAllCSVtoOneXLSX():
    # get path where csv files locate
    newdir = os.getcwd()+"\\CSVFILE" 
    
    # list csv file names and put into a list
    names = os.listdir(newdir)

    writer = pd.ExcelWriter('combined.xlsx')
    for name in names:
        path = os.path.join(newdir, name)
        data = pd.read_csv(path, encoding="utf8", index_col=0)
        data.to_excel(writer, sheet_name=name)
    writer.save()


# In[ ]:


def deleteXMLfile(response):
    # getName
    name = response.json()['devDetails']['hdrTitle']
    try:
        os.remove(os.getcwd()+"\\"+name+".xml")
    except os.error:
        pass


# In[ ]:


window = tk.Tk()
window.withdraw()

# define specific IN/OUT via interaction GUI
inOrOut = simpledialog.askstring(title="IN or OUT", prompt="Please enter IN or OUT :")
messagebox.showinfo("Information", "DATA is " + inOrOut)
print("YOU CHOOSE TRAFFIC 'IN'")

# define specific rows via interaction GUI
rows = simpledialog.askstring(title="Rows?", prompt="Please enter a row number:")
messagebox.showinfo("Information", "Rows are " + rows)
print("YOU CHOOSE " + rows + " ROWS")

# define specific startTime via interaction GUI
startTime = simpledialog.askstring(title="StartTime", prompt="Please enter start time : for example=> 2020-04-01 00:00")
messagebox.showinfo("Information", "StartTime is " + startTime)
print("START TIME IS: " + startTime)

# define specific endTime via interaction GUI
endTime = simpledialog.askstring(title="EndTime", prompt="Please enter end time : for example=> 2020-05-01 00:00")
messagebox.showinfo("Information", "The neighbor is " + endTime)
print("END TIME IS: " + endTime)

extendedQuery = "&Data=" + inOrOut+ "&rows=" + rows + "&StartTime=" + startTime + "&EndTime=" + endTime


# In[ ]:


# get the AIP list for each customer from text file
with open(os.getcwd()+"\\clientAIPlists.txt", "r") as f:
    clientAPIURLs = f.readlines()
    
# remove whitespace characters like `\n` at the end of each line
clientAPIURLs = [x.strip() for x in clientAPIURLs] 

# delete the even index number items which are notes in text file
del clientAPIURLs[0::2]

# declare a list to save requests
index = 0
clientResponseList= list(range(0, len(clientAPIURLs)))

# get a list of requests of all clients
while index < len(clientAPIURLs):
    for APIURL in clientAPIURLs:
        APIURL = APIURL + extendedQuery
        clientResponseList[index] = requests.get(APIURL)
        index = index + 1
       
# create a document
try:
    os.mkdir(os.getcwd()+"\\CSVFILE")
except os.error:
    pass


# In[ ]:


print("Processing............")
for client in clientResponseList:
    # get all the xml files
    getXMLfile(client)
    # get all the csv files
    xmlConvertToCSV(client)
    # delete xml file
    deleteXMLfile(client)
    
# combine all cav files into one xlsx file named combined.xlsx
combineAllCSVtoOneXLSX()
# inform the process has been completed
messagebox.showinfo("Information", "Success !! The Process has been completed. Check out the combined.xlsx")

