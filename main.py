import os.path
import sys 
import Lead
import math
import random
from datetime import datetime

#NOTE: psycopg2 library doesn't compile in python3, python subprocess 
# terminal command is to be run on this file
import psycopg2

import time

start_time = time.time()

conn = None

def parseName(name):
    if (name.find('e:++>')> -1):
        name = name[name.find('e:++>')+5 : len(name)]
    return name

def getSuiteType(suite):
    suite = suite.lower()    
    if (suite.find('studio') >-1):
        return 'Studio'
    elif (suite.find('penthouse') > -1 or suite.find('pent house') > -1):
        return 'Penthouse'
    if (suite.find('1') >-1):
        if (suite.find('den') > -1):
            return '1 Bedroom + Den'
        return '1 Bedroom'
    elif (suite.find('2') > -1):
        if (suite.find('den') > -1):
            return '2 Bedrooms + Den'
        return '2 Bedrooms'
    elif (suite.find('3') > -1):
        return '3 Bedroom'
    return "Unknown Suite Type"

def inquiryDateTime(dateTime):
    return dateTime + "0"

def inquiryDate(dateTime):
    local =''
    for c in dateTime:
        if (c=='2' and local ==''):
            local += c
        if (local != ''):
            local +=c 
            if (len(local)== 4):
                break
    dateTime = dateTime[0 : dateTime.find(local) + 4]
    return dateTime

def isEmpty(string):
    for c in string:
        if c.isalpha():
            return False
        elif c.isdigit():
            return False
    return True



f = open("formsAutoInfo.txt", "r")
line = f.readlines()
query = ''
queryList =[]
i =0

try:  
    lead = Lead.Lead()
    invalid = False
    while line :
        if (line[i].find('..................') >-1):
            if (query != ''):
                queryList.append(query)
                query = ''

        ln1 = line[i+1].rstrip("\n\r")
        ln = line[i+2].rstrip("\n\r")

        ID = random.randint(800,214700000)

        i+=1
        if line[i].find('inquiry date') != -1  and  line[i][0] == '@':
            if isEmpty(ln):
                print("invalid inquiry date")
                invalid = True
            elif ln.find('asswordinfo.txt') == -1:
                lead.set_inquiry_date(inquiryDateTime(ln))

        elif line[i].find('additional comments') != -1 and  line[i][0] == '@':
            if ln.find('subject: new corporate check-in to: ') != -1:
                print("invalid comments")
                invalid = True
            else:
                lead.set_additional_comments(ln)   
                # print(lead.get_additional_comments())

        elif line[i].find('form type') != -1 and  line[i][0] == '@':
        # make sure no other form names contain this abbreviation
            if ln.find('si') != -1 or ln.find('tfa') != -1 or ln.find('tfr') != -1:
                lead.set_from_web(True)
            else:
                lead.set_from_web(False)
            lead.set_contact_form(ln)
            # print(lead.get_contact_form())

            
        elif line[i].find('suite type') != -1 and  line[i][0] == '@':
            temp = ln.lower()
            temp = temp.replace("one", "1").replace('two', '2').replace('three', '3')
            lead.set_suite_type(getSuiteType(temp))

                    
        elif line[i].find('name') != -1 and  line[i][0] == '@':
            lead.set_name(parseName(ln))
        
        # assumes that phone number cannot have an alpahbetic character
        elif line[i].find('phone number') != -1  or line[i].find('phone') != -1\
        or line[i].find('telephone') != -1 and  line[i][0] == '@':
            dontshow = False
            for c in ln:
                if c.isalpha():
                    dontshow = True
            if not dontshow:
                lead.set_phone_number(ln)
                
        elif line[i].find('country') != -1 and  line[i][0] == '@':
            ln = ln.upper()
            lead.set_country(ln)
            # print(lead.get_country())
        
        elif line[i].find('email') != -1 and  line[i][0] == '@':
            if ln.find('@') == -1 or ln.find('.') ==-1 :
                invalid = True
                print("invalid email")
            elif isEmpty(ln):
                badEmail = True
            else:
                lead.set_email(ln)
                # print(lead.get_email())

        
        elif line[i].find('date is flexible') != -1 and  line[i][0] == '@':
            if ln.find("are flexible"):
                lead.set_flexible(True)
                # print(lead.get_flexible())
            else: 
                lead.set_flexible(False)
                # print(lead.get_flexible())

        elif line[i].find('parking required') != -1 and  line[i][0] == '@':
            lnlower = ln.lower()
            ln = ln.replace("one", "1").replace('two', '2')

            if isEmpty(ln) or lnlower.find('none') != -1:
                lead.set_parking_required_bool(False)
                lead.set_parking_required('')                
            else:
                lead.set_parking_required_bool(True)
                lead.set_parking_required(ln)
    
        elif line[i].find('purpose of stay') != -1 and  line[i][0] == '@':
            lead.set_purpose_of_stay(ln)
            
        
        elif line[i].find('location') != -1 and  line[i][0] == '@':
            lead.set_location(ln)
 
        elif line[i].find('budget per night') != -1 and  line[i][0] == '@':
            lead.set_budget_per_night(ln)
 
        elif line[i].find('number of guests') != -1 and  line[i][0] == '@':
            try:
                ln = int(ln)
                lead.set_number_of_guests(ln)

            except:
                if ln.find(" ") != -1:
                    for c in reversed(ln):
                        if c.isdigit(): 
                            lead.set_number_of_guests(int(c))

        elif line[i].find('number of adults') != -1 and  line[i][0] == '@':
            try:
                ln = int(ln)
                lead.set_number_of_adults(ln)
            except:
                if ln.find(" ") != -1:
                    for c in reversed(ln):
                        if c.isdigit():
                            lead.set_number_of_adults(int(c))     
        elif line[i].find('number of children') != -1 and  line[i][0] == '@':
            try:
                ln = int(ln)
                lead.set_number_of_children(ln)
            except:
                if ln.find(" ") != -1:
                    for c in reversed(ln):
                        if c.isdigit():
                            lead.set_number_of_children(int(c))
    
        # double check this/might be missing something 
        elif line[i].find('where did you hear about us?') != -1 and  line[i][0] == '@':
            lead.set_how_you_heard(ln)

        elif (line[i].find('move in date') != -1 or line[i].find('start date') != -1 or line[i].find('check in') != -1) and  line[i][0] == '@':
            lead.set_check_in(ln)
            # print(ln)
    
        elif (line[i].find('move out date') != -1 or line[i].find('end date') != -1 or line[i].find('check out') != -1) and  line[i][0] == '@':
            lead.set_check_out(ln)
            # print(ln)

        
        elif line[i].find("..................")!= -1 :
            if not invalid:    
                timestamp = datetime.now()

                query ="INSERT INTO leads VALUES ("

                query += str (ID)
                query += ","
                query += "'"
                query += str(lead.get_email())
                query += "',"
                query += "'"
                query += str(timestamp)
                query += "',"
                query += "'"
                query += str(timestamp)
                query += "',"
                query += "'"
                query += str(lead.get_inquiry_date())
                query += "',"
                query += "'"
                # do some processing on the dates
                query += str(lead.get_check_in())
                query += "',"
                query += "'" 
                query += str(lead.get_check_out())
                query += "',"
                query += "'"
                query += str(lead.get_suite_type())
                query += "',"
                query += "'"
                query += str(lead.get_name())
                query += "',"
                query += "'"
                query += str(lead.get_phone_number())
                query += "',"
                query += "'"
                query += str(lead.get_from_web())
                query += "',"
                query += "'"
                query += str(lead.get_contact_form())
                query += "',"
                query += "'"
                query += str(lead.get_purpose_of_stay())
                query += "',"
                query += "'"
                query += str(lead.get_parking_required_bool())
                query += "',"
                query += "'"
                query += str(lead.get_parking_required())
                query += "',"
                query += "'"
                query += str(lead.get_number_of_guests())
                query += "',"
                query += "'"
                query += str(lead.get_number_of_adults())
                query += "',"
                query += "'"
                query += str(lead.get_number_of_children())
                query += "',"
                query += "'"
                query += str(lead.get_additional_comments())
                query += "',"
                query += "'"
                query += str(lead.get_country())
                query += "',"
                query += "'"
                query += str(lead.get_how_you_heard())
                query += "',"
                query += "'"
                query += str(lead.get_budget_per_night())
                query += "',"
                query += "'"
                query += str(lead.get_location())
                query += "',"
                query += "'"
                query += str(lead.get_flexible())
                query += "'"

                query += ");"

                print (lead.get_inquiry_date())
                # print(query)
                # change this line to connect to the prod database!
                # try:

                    # print("Sucessfully injected lead into database via..... \n[" + query + "]" )
                # except:
                #     print("Unable to connect to database or unable to inject lead into the database")
                #     f = open("mailPasswordInfo.txt", "a+")

                #     # other lines are dependent on this line do not change 
                #     f.write("Unable to inject lead email '" + lead.get_email() + "' into the database \n")
                #     lead = Lead.Lead()



            else:
                invalid = False 


except IndexError:
    pass



conn = psycopg2.connect("dbname='svstings' user='svs' host='localhost'")
cur = conn.cursor()
cur.execute("SELECT * FROM leads")
leadsObj = cur.fetchall()

# print (queryList)
for query in queryList:
    invalid = False
    for leads in leadsObj:
        email = ''
        suite_type = ''
        i=0
        for lead in leads:
            # could be dangerous if a comment or another fields has an unexpected @ 

            lead = str (lead)
            if (lead.find("@") >-1 ):
            # and leads.index(lead) != len(leads)-1):
                email= lead 
            elif ((lead.find('Bedroom') >-1 and 
            (lead.find('1')> -1 or lead.find('2')  >-1 or lead.find('3') >-1) 
            or lead.find('Studio') >-1 or lead.find('Penthouse') >-1)
            ):
                suite_type = lead
            i+=1 
        if (query.find(email) >-1 and query.find(suite_type)):
            invalid = True
    if (not invalid):
        cur.execute(query)
        conn.commit()
print("--- %s seconds ---" % (time.time() - start_time))
