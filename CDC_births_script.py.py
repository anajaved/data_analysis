
# coding: utf-8
#data source: https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_1994-2003_CDC_NCHS.csv 

# In[4]:


births = open("US_births_1994-2003_CDC_NCHS.csv").read()
births= births.split("\n")
births[:10]


# In[40]:


def read_csv(filename):
    file= open(filename).read()
    file=file.split("\n")
    string_list=file[1:]  #list of strings
    
    final_list=[] 
    
    for each in string_list:
        int_fields=[]
        string_fields = each.split(",")
        for ind in string_fields:
            ind=int(ind)
            int_fields.append(ind)  #separating & making into integers 
            
        final_list.append(int_fields)
    return(final_list)
    
cdc_list = read_csv("US_births_1994-2003_CDC_NCHS.csv") #list of lists



# In[42]:


#calculating number of births per month

def month_births(lists_lists):
    births_per_month = {}
    
    for each in lists_lists:
        month=each[1]
        
        if month in births_per_month:
            births_per_month[month] = births_per_month[month] + each[4]
        else:
            births_per_month[month] = each[4]
            
    return(births_per_month)
    
cdc_month_births = month_births(cdc_list)
print (cdc_month_births)


# In[43]:


#calculating number of births each day of the week

def dow_births(lists):
    births_per_dow= {}
    
    for each in lists:
        day= each[3]
        
        if day in births_per_dow:
            births_per_dow[day]= births_per_dow[day] + each[4]
        else:
            births_per_dow[day]= each[4]
            
    return(births_per_dow)
           
cdc_day_births = dow_births(cdc_list)
print (cdc_day_births)


# In[46]:


#general birth calculations based on column index value

def calc_counts(data,column):
    temp_dict={}

    for each in data:
        col_val=each[column]
    
        if col_val in temp_dict:
            temp_dict[col_val]= temp_dict[col_val] + each[4]
        else:
            temp_dict[col_val]= each[4]
            
    return(temp_dict)


cdc_dow_births = calc_counts(cdc_list, 3)
cdc_year_births = calc_counts(cdc_list, 0)
cdc_month_births = calc_counts(cdc_list, 1)
cdc_dom_births= calc_counts(cdc_list, 2)

