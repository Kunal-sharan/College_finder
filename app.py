import re

import requests
from bs4 import BeautifulSoup
import streamlit as st
from streamlit_sortables import sort_items
from langchain_google_genai import GoogleGenerativeAI
import pandas as pd
def scrape(url):
    arr=[]
    headers = {
        "User-Agent": "Guest",  # Access as Guest
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:    # if request granted
        soup = BeautifulSoup(response.content, 'html.parser')

        for i in soup.find_all("table"):
            arr.append(i)

    return arr

def scrape_headings(url):
    arr=[]
    headers = {
        "User-Agent": "Guest",  # Access as Guest
    }

    response = requests.get(url, headers=headers)


    soup = BeautifulSoup(response.content, 'html.parser')

    for i in soup.find_all("h2"):
        if len(i.get_text()) >0 and "Round" in i.get_text():
          arr.append(i.get_text())

    return arr

def scrape_headings_esarl(url):
    arr=[]
    headers = {
        "User-Agent": "Guest",  # Access as Guest
    }

    response = requests.get(url, headers=headers)


    soup = BeautifulSoup(response.content, 'html.parser')

    for i in soup.find_all("h2"):
          arr.append(i.get_text())

    return arr

def scrape_the_pw(arr):
  s=BeautifulSoup(f'''{arr}''',"html.parser")
  head=[]
  a=s.find('tr')
  st=BeautifulSoup(f'''{a}''',"html.parser")
  for i in st.find_all('td'):
    head.append(i.get_text().replace("\n",""))
  data=[]
  all=s.find_all('tr')
  for i in range(2,len(all)):
    b=BeautifulSoup(f'''{all[i]}''',"html.parser")
    for i in b.find_all('td'):
      data.append((i.get_text()).replace("\n"," "))
  return[head,data]
c=[]
def create_df(head,data):
  first=[]
  data_new=[]
  for i in range(len(data)):
    if "Course" not in data[i]:
      data_new.append(data[i])
    else:
      break
  for i in range(0,len(data_new),len(head)):
    ar=[]
    for j in range(i,i+len(head)):
      # print(j)
      if j<len(data_new):
        ar.append(data_new[j])
    first.append(ar)
  df=pd.DataFrame(first,columns=head)
  return df

def get_the_iits(url):
    headers = {
          "User-Agent": "Guest",  # Access as Guest
      }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:    # if request granted
        soup = BeautifulSoup(response.content, 'html.parser')

    head=[]
    data=[]
    table=soup.find("table")
    soup=BeautifulSoup(f'''{table}''',"html.parser")
    head=soup.find_all('td')
    # print(head)
    # print(data)
    for i in range(5,len(head),4):
      c=head[i].get_text().replace("\t","").replace("\n","").split(",")
      try:
        data.append(c[1].replace("\xa0","").replace(" ",""))
      except:
        continue
    return data

sorted_items=[]
@st.cache_data
def get_the_iits_links(url):
    headers = {
          "User-Agent": "Guest",  # Access as Guest
      }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:    # if request granted
        soup = BeautifulSoup(response.content, 'html.parser')

    head=[]
    data=[]
    iit=[]
    table=soup.find("table")
    soup=BeautifulSoup(f'''{table}''',"html.parser")
    head=soup.find_all('td')
    # print(head)
    # print(data)
    for i in range(7,len(head),4):
      c=head[i].get_text().replace("\t","").replace("\n","")
      try:
        if "iitdh" not in c:
          data.append(c.replace("\xa0","").replace(" ",""))
      except:
        continue
    for i in range(5,len(head),4):
      c=head[i].get_text().replace("\t","").replace("\n","").split(",")
      try:
        iit.append(c[1].replace("\xa0","").replace(" ","").lower())
      except:
        continue
    return [data,iit]

def check_elements_in_string(my_array, my_string):
    for i, element in enumerate(my_array):
        if element in my_string:
            return i
    return -1

# ("I only have data for IIT Gandhinagar , IIT Guwahati , IIT Hyderabad , IIT Delhi , IIT Ropar , IIT Mandi , IIT Bhilai ")    
@st.cache_data
def get_all_colleges():
  iits=get_the_iits_links("https://www.education.gov.in/iits")
  net_headings=[]
  all_cutoffs=[]
  net_headings.append(scrape_headings_esarl("https://www.esaral.com/jee/iit-gandhinagar-cut-off/")[0])
  s=BeautifulSoup(f'''{scrape("https://www.esaral.com/jee/iit-gandhinagar-cut-off/")[1]}''',"html.parser")
  head=[]
  foru=[]
  for i in s.find('tr'):
    a=i.get_text().replace("\n","")
    if len(a)>0:
      head.append(a)
  data=[]
  for i in s.find_all('td'):
    a=i.get_text().replace("\n","")
    if len(a)>0:
      data.append(a)
  first=[]
  for i in range(len(head),len(data),len(head)):
      ar=[]
      for j in range(i,i+len(head)):
        # print(j)
        if j<len(data):
          ar.append(data[j])
      first.append(ar)
  df=pd.DataFrame(first,columns=head)
  col_off=[]
  for i in range(len(df)):
    col_off.append({"College":f"IIT GandhiNagar","Branch":f"{str(df[f'{head[0]}'].iloc[i])}","Open":f"{int(df[f'{head[1]}'].iloc[i])}","close":f"{int(df[f'{head[2]}'].iloc[i])}","link":f"{iits[0][0]}","Place":f"gandhinagar"})
  for i in range(1,len(iits[1])):
    arr=scrape(f"https://www.pw.live/exams/jee/iit-{str(iits[1][i]).lower()}-jee-advanced-cutoff/")
    headings=scrape_headings(f"https://www.pw.live/exams/jee/iit-{str(iits[1][i]).lower()}-jee-advanced-cutoff/")
    if len(arr)>0 and len(headings)>0:

      for i in range(0,len(headings)):
        c.append(create_df(scrape_the_pw(arr[i])[0],scrape_the_pw(arr[i])[1]))
      net_college_cuttoff=[headings,c]

      # len(net_college_cuttoff[0])

      for i in range(len(net_college_cuttoff[1])):
        try:
          if "General" in net_college_cuttoff[0][i].replace("\xa0",""):
            net_headings.append(net_college_cuttoff[0][i].replace("\xa0",""))
            for j in range(len(net_college_cuttoff[1][i])):
              a=check_elements_in_string(iits[1],net_college_cuttoff[0][i].lower())
              col_off.append({"College":f"{net_college_cuttoff[0][i].replace('JEE Advanced Cutoff 2023','').replace('General Category','')}",
                            "Branch":f"{net_college_cuttoff[1][i][f'{list(net_college_cuttoff[1][i].columns.values)[0]}'][j]}",
                            "Open":f"{int(net_college_cuttoff[1][i][f'{list(net_college_cuttoff[1][i].columns.values)[1]}'][j])}",
                            "close":f"{int(net_college_cuttoff[1][i][f'{list(net_college_cuttoff[1][i].columns.values)[2]}'][j])}",
                              "link":f"{iits[0][a]}",
                              "Place":f"{iits[1][a]}"})
              foru.append(iits[1][a])


          else:
            continue
        except:
          continue
        all_cutoffs.append(col_off)

    else:
      continue
  foru=list(set(foru))
  return [[all_cutoffs,net_headings],foru]

n=get_all_colleges()[0]

def check_if_empty(arr):
    for i in range(len(arr)):
      for j in range(len(arr[i])):
        if len(arr[i][1])>0:
          return True
    return False
@st.cache_data
def final():
  final_data=[]
  for i in range(len(n[0])):
    for j in range(len(n[0][i])):
      final_data.append(n[0][i][j])
  df=pd.DataFrame(final_data)
  return df
arr=[]
# b=st.button("Clear_cache")
# if b:
  # st.cache_data.clear()
  # st.success("Done")
# st.set_page_config(layout='wide')
iit_rank=st.text_input("Enter your Jee advance rank if your is in in between 21 and 13890 ")
df=final()
iits_foru=[]
if iit_rank:
  for i in range(len(df["Open"])):
    if int(iit_rank) >= int(df["Open"].iloc[i]) and int(iit_rank) <= int(df["close"].iloc[i]):
      arr.append(df.iloc[i])
  d_f=pd.DataFrame(arr)
  iits_foru.append(list(set(d_f["Place"].values.tolist())))
  if not d_f.empty:
    st.dataframe(d_f)

@st.experimental_fragment
def main_2():
 

  if len(iits_foru)>0:
    st.warning(("I only have the placements data for IIT Gandhinagar , IIT Guwahati , IIT Hyderabad , IIT Delhi , IIT Ropar , IIT Mandi , IIT Bhilai "))
    original_items = [
        {'header': 'Available IIT options  ',  'items':iits_foru[0]},
        {'header': 'Compare Any Two based on placements', 'items': []}
    ]
    sorted_item = sort_items(original_items, multi_containers=True)
    sorted_items.append(sorted_item)  
    # st.write(type(sorted_items))  
    if len(sorted_item[1].get("items"))>2:
      st.error("Only 2 items allowed for comparison ")
     


main_2()
def create_df_placement(head,data):
    first=[]
    for i in range(0,len(data),len(head)):
      ar=[]
      for j in range(i,i+len(head)):
        # print(j)
        if j<len(data):
          ar.append(data[j])
      first.append(ar)
    df=pd.DataFrame(first,columns=head)
    return df

def extract_First(url):
  headers = {
        "User-Agent": "Guest",  # Access as Guest
    }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  arr=soup.find_all(['p'])[:2]
  para=""
  for i in range(len(arr)):
    para+=arr[i].get_text()+"\n"

  return para

def extract_all_Tables(url):
  headers = {
        "User-Agent": "Guest",  # Access as Guest
    }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  arr=soup.find_all("table")
  return arr

def get_placements_Indian_exp(url):
    para=extract_First(url)
    arr=extract_all_Tables(url)
    new_arr=[]
    for i in range(len(arr)):
      new_arr.append(scrape_the_pw(arr[i]))
    all_df=[]
    for i in range(len(new_arr)):
      all_df.append(create_df_placement(new_arr[i][0],new_arr[i][1]))
    return [para,all_df]
    
but=st.button("Show Placement Data")
new_arr=[]
if but:
    all_placements_data=[]
    if len(sorted_items[0])>0:
       
        
        for i in range(len(sorted_items[0][1].get("items"))):
        
          all_placements_data.append(get_placements_Indian_exp(f"https://education.indianexpress.com/university/iit-{sorted_items[0][1].get('items')[i]}-indian-institute-of-technology-placements"))
        new_arr.append(all_placements_data)    
        if len(all_placements_data)>0:
        
            for k in range(len(all_placements_data)):
              for i in range(len(all_placements_data[k])):
                if(type(all_placements_data[k][i])==str):
                  st.write(all_placements_data[k][i])
                else:
                  for j in range(len(all_placements_data[k][i])):
                    st.dataframe(all_placements_data[k][i][j])
                      
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_AI"])

@st.experimental_fragment
def get_AI_help():
    butt=st.button("Compare the two based on the placements data")
    if butt and but:
        # st.warning("I only have data for IIT Gandhinagar , IIT Guwahati , IIT Hyderabad , IIT Delhi , IIT Ropar , IIT Mandi , IIT Bhilai ")        
    # llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets["GOOGLE_AI"])
        if len(new_arr[0])==2:
            if check_if_empty(new_arr[0]):
              st.markdown(
                  llm.invoke(
                      f'''compare the two colleges using all the given factors decide which one is better {new_arr[0]}'''
                  )
              )
            else:
              st.error("No data or press 'Show placement data' first")
        else:
            st.error(f"only {len(new_arr)} colleges can't compare")
get_AI_help()            
            
