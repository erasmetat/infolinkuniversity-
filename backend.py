import requests
from bs4 import BeautifulSoup
import sqlite3

global_sessions = requests.session()

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "http://iuh.edu.et/", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

home_page = global_sessions.get("https://iuh.edu.et/Account/Login")
set_cookie = home_page.headers['Set-Cookie']
cookie = set_cookie[36:191]
soup = BeautifulSoup(home_page.text,'html.parser')
input_tag = soup.find_all(attrs={"name" : "__RequestVerificationToken"})
RequestVerificationToken = input_tag[0]['value']

def session_control(tele_id,logins_info):
    conn = sqlite3.connect('Infolink.db')
    spliter = logins_info.split()
    user_name = spliter[0]
    password = spliter[1]
    sessions = login(user_name,password)
    cursor = conn.cursor()
    id = int(tele_id)
    token = str(sessions)
    cursor.execute("REPLACE INTO user_data(ID, Session) VALUES (?, ?)",(id,token))
    conn.commit()
    print("Records inserted........")
    conn.close()

def login(user_name,password):
    login_url = "https://iuh.edu.et/Account/Login"
    login_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA": cookie}
    login_data = {"Today": "14/06/2014", "UserName": user_name, "Password": password , "__RequestVerificationToken": RequestVerificationToken}
    s = requests.post(login_url, headers=headers, cookies=login_cookies, data=login_data,allow_redirects=False)
    ss=s.cookies
    token_string = str(ss)
    token_split = token_string.split()
    token_last = (token_split[1])
    return token_last[20:]

def CurrentCourse(tele):
    conn = sqlite3.connect('Infolink.db')
    current_course = []
    tele_id = int(tele)
    current_link_course =[]
    # dic_link_course
    current_course_dic = {}
    cursor = conn.cursor()
    while True:
                check = cursor.execute("select exists(select 1 from user_data where ID=?) limit 1",(tele_id,)) 
                if check.fetchone()[0]==0:
                    try_again={"k":"You are not logged in \n Please logged in again"}
                    return try_again        
                else:
                    selected = cursor.execute("SELECT Session FROM user_data WHERE ID = ?",(tele_id,)) 
                    session = selected.fetchall()
                    tmp_session = str(session)
                    session_splited = tmp_session[3:-4]
                    current_course_url = "https://iuh.edu.et/Students/CurrentCourses"
                    current_course_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                    html = global_sessions.get(current_course_url, headers=headers, cookies=current_course_cookies)
                    soup = BeautifulSoup(html.text,'html.parser')
                    class_id = soup.find_all(attrs={"class" : "info-box-text"})
                    for span in class_id:
                        current_course.append(str(span.text).strip(" "))
                    key = range(len(current_course))
                    for i in key:
                        current_course_dic[i] = current_course[i]
                    soupp = BeautifulSoup(html.text,'html.parser')
                    data = soupp.findAll('div',attrs={'class':'col-12 col-sm-6 col-md-4'})
                    for div in data:
                        links = div.findAll('a')
                    for a in links: 
                        current_link_course.append("https://iuh.edu.et" + a['href'])
                    # dic_link_course  = {current_course[i]: current_link_course[i] for i in range(len(current_course))}
                    current_course = []
                    return current_course_dic
def CompletedCourse(tele):
    conn = sqlite3.connect('Infolink.db')
    tele_id = int(tele)
    completed_course = []
    completed_link_course =[]
    # completed_dic_link_course ={}
    completed_course_dic = {}
    cursor = conn.cursor()
    while True:
                check = cursor.execute("select exists(select 1 from user_data where ID=?) limit 1",(tele_id,))
                if check.fetchone()[0]==0:
                    try_again=('You are not logged in \n Please logged in again').upper()
                    return try_again
                else:
                    selected = cursor.execute("SELECT Session FROM user_data WHERE ID = ?",(tele_id,)) 
                    session = selected.fetchall()
                    tmp_session = str(session)
                    session_splited = tmp_session[3:-4]
                    completed_cource_url = "https://iuh.edu.et/Students/CompletedCourses"
                    completed_cource_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                    html = global_sessions.get(completed_cource_url, headers=headers, cookies=completed_cource_cookies)
                    soup = BeautifulSoup(html.text,'html.parser')
                    class_id = soup.find_all(attrs={"class" : "info-box-text"})
                    for span in class_id:
                        completed_course.append(str(span.text).strip(" "))
                    key = range(len(completed_course))
                    for i in key:
                        completed_course_dic[i] = completed_course[i]
                    soupp = BeautifulSoup(html.text,'html.parser')
                    data = soupp.findAll('div',attrs={'class':'col-12 col-sm-6 col-md-4'})
                    for div in data:
                        links = div.findAll('a')
                        for a in links: 
                            completed_link_course.append("https://iuh.edu.et" + a['href'])
                    # completed_dic_link_course = {completed_course[i]: completed_link_course[i] for i in range(len(completed_course))}
                    completed_course = []
                    return completed_course_dic  

def single_current_course (course_name_splited,tele):
    conn = sqlite3.connect('Infolink.db')
    tele_id = int(tele)
    current_course = []
    current_link_course =[]
    dic_link_course ={}
    current_course_dic = {}
    cursor = conn.cursor()
    course_name = course_name_splited[21:]
    while True:
                check = cursor.execute("select exists(select 1 from user_data where ID=?) limit 1",(tele_id,))
                if check.fetchone()[0]==0:
                    try_again=('You are not logged in \n Please logged in again').upper()
                    return try_again               
                else:
                    selected = cursor.execute("SELECT Session FROM user_data WHERE ID = ?",(tele_id,)) 
                    session = selected.fetchall()
                    tmp_session = str(session)
                    session_splited = tmp_session[3:-4]
                    current_course_url = "https://iuh.edu.et/Students/CurrentCourses"
                    current_course_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                    html = global_sessions.get(current_course_url, headers=headers, cookies=current_course_cookies)
                    soup = BeautifulSoup(html.text,'html.parser')
                    class_id = soup.find_all(attrs={"class" : "info-box-text"})
                    for span in class_id:
                        current_course.append(str(span.text).strip(" "))
                    key = range(len(current_course))
                    for i in key:
                        current_course_dic[i] = current_course[i]
                    soupp = BeautifulSoup(html.text,'html.parser')
                    data = soupp.findAll('div',attrs={'class':'col-12 col-sm-6 col-md-4'})
                    for div in data:
                        links = div.findAll('a')
                        for a in links: 
                            current_link_course.append("https://iuh.edu.et" + a['href'])
                    dic_link_course  = {current_course[i]: current_link_course[i] for i in range(len(current_course))}
                    if course_name in dic_link_course:
                        single_cource = dic_link_course[course_name]
                        current_course_url = single_cource
                        current_course_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                        html = global_sessions.get(current_course_url, headers=headers, cookies=current_course_cookies)
                        soup = BeautifulSoup(html.text,'html.parser')
                        data = []
                        for tr in soup.find('table', class_='table table-striped').find_all('tr'):
                            row = [td.text for td in tr.find_all('td')]
                            data.append(row)
                        class_h4 = soup.find_all(attrs={"class" : "bg-info elevation-3"})
                        total_mark = (class_h4[0].text).strip()
                        data.append([total_mark])
                        return data

    
def single_completed_course (course_name_splited,tele):
    conn = sqlite3.connect('Infolink.db')
    tele_id = int(tele)
    completed_course = []
    completed_link_course =[]
    completed_dic_link_course ={}
    completed_course_dic = {}
    cursor = conn.cursor()
    course_name = course_name_splited[23:]
    while True:
                check = cursor.execute("select exists(select 1 from user_data where ID=?) limit 1",(tele_id,))
                if check.fetchone()[0]==0:
                    try_again=('You are not logged in \n Please logged in again').upper()
                    return try_again             
                else:
                    selected = cursor.execute("SELECT Session FROM user_data WHERE ID = ?",(tele_id,)) 
                    session = selected.fetchall()
                    tmp_session = str(session)
                    session_splited = tmp_session[3:-4]
                    completed_cource_url = "https://iuh.edu.et/Students/CompletedCourses"
                    completed_cource_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                    html = global_sessions.get(completed_cource_url, headers=headers, cookies=completed_cource_cookies)
                    soup = BeautifulSoup(html.text,'html.parser')
                    class_id = soup.find_all(attrs={"class" : "info-box-text"})
                    for span in class_id:
                        completed_course.append(str(span.text).strip(" "))
                    key = range(len(completed_course))
                    for i in key:
                        completed_course_dic[i] = completed_course[i]
                    soupp = BeautifulSoup(html.text,'html.parser')
                    data = soupp.findAll('div',attrs={'class':'col-12 col-sm-6 col-md-4'})
                    for div in data:
                        links = div.findAll('a')
                        for a in links: 
                            completed_link_course.append("https://iuh.edu.et" + a['href'])
                    completed_dic_link_course = {completed_course[i]: completed_link_course[i] for i in range(len(completed_course))}
                    if course_name in completed_dic_link_course:
                        single_cource = completed_dic_link_course[course_name]
                        completed_course_url = single_cource
                        completed_course_cookies = {".AspNetCore.Antiforgery.vi6nHzO_AYA":cookie, ".AspNetCore.Session": session_splited}
                        html = global_sessions.get(completed_course_url, headers=headers, cookies=completed_course_cookies)
                        soup = BeautifulSoup(html.text,'html.parser')
                        data = []
                        for tr in soup.find('table', class_='table table-striped').find_all('tr'):
                            row = [td.text for td in tr.find_all('td')]
                            data.append(row)
                        class_h4 = soup.find_all(attrs={"class" : "bg-info elevation-3"})
                        total_mark = (class_h4[0].text).strip()
                        data.append([total_mark])
                        # print(data)
                        return data