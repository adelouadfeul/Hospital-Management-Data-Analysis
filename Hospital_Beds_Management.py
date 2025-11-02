#!/usr/bin/env python
# coding: utf-8

# # Hospital Management Data Analysis — Introduction
# 
# This analysis explores hospital operations, patient outcomes, and staff dynamics using data on patients, services, and staff schedules. It examines trends in patient satisfaction, bed occupancy, refusal rates, and staff availability, as well as the impact of events and seasonal patterns. The goal is to identify insights that can improve resource allocation, service quality, and patient care.

# ## loading library

# In[1339]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.simplefilter('ignore')
plt.style.use('fivethirtyeight')


# ## data reading

# In[9]:


patients=pd.read_csv("D:\hospita_mangemant\patients.csv")
services_weekly=pd.read_csv("D:\hospita_mangemant\services_weekly.csv")
staff=pd.read_csv("D:\hospita_mangemant\staff.csv")
staff_schedule=pd.read_csv("D:\hospita_mangemant\staff_schedule.csv")


# In[1306]:


patients.info()


# In[1308]:


services_weekly.info()


# In[1310]:


staff.info()


# In[1312]:


staff_schedule.info()


# # 1 📅 HOSPITAL WEEKLY STATS
# 
# Table: ['week', 'month', 'service', 'available_beds', 'patients_request', 'patients_admitted', 'patients_refused', 'patient_satisfaction', 'staff_morale', 'event']
# 
# How does staff morale correlate with patient satisfaction?
# 
# What is the bed occupancy rate by week and service?
# 
# Which services have the highest patient refusal rates, and why?
# 
# How do special events (e.g., epidemics, staff strikes) affect patient admissions and morale?
# 
# Is there a seasonal trend in the number of patient requests?

# In[1341]:


# How does staff morale correlate with patient satisfaction?
staff_corr=services_weekly.staff_morale.corr(services_weekly.patient_satisfaction)
if staff_corr < .7 :
    print(f'staff moral correlation with patient saatisfaction is {staff_corr:.4f} wich is weak')
else : print(f'staff moral correlation with patient saatisfaction is {staff_corr:.4f} wich is high')

sns.regplot(x='staff_morale', y='patient_satisfaction', data=services_weekly, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
plt.title('Staff Morale vs Patient Satisfaction')
plt.xlabel('Staff Morale')
plt.ylabel('Patient Satisfaction')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


# In[ ]:





# In[1343]:


# What is the bed occupancy rate by week and service?
services_weekly['bed_occ']=(services_weekly['patients_admitted'] / services_weekly['available_beds']) * 100

bed_occ_by_week=services_weekly.groupby('week')['bed_occ'].mean().reset_index()
print(bed_occ_by_week,'\n')

plt.plot(services_weekly['week'],services_weekly['bed_occ'])
plt.title('Bed Occupancy Rate by Week')
plt.xlabel('Week')
plt.ylabel('Bed Occupancy Rate (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

service_occ_by_service=services_weekly.groupby('service')['bed_occ'].mean().reset_index()
print(service_occ_by_service,'\n')

plt.bar(service_occ_by_service['service'],service_occ_by_service['bed_occ'])
plt.title('Bed Occupancy Rate by Week')
plt.xlabel('service')
plt.ylabel('Bed Occupancy Rate (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()


# In[ ]:





# In[1345]:


# Which services have the highest patient refusal rates, and why?
services_weekly['patient_refusal_rate']=services_weekly['patients_refused']/services_weekly['patients_request'] *100

patient_refusal_rate=services_weekly.groupby('service')['patient_refusal_rate'].mean().sort_values(ascending=False).reset_index()
print(patient_refusal_rate,'\n')

labels=list(patient_refusal_rate['service'])
values=list(patient_refusal_rate['patient_refusal_rate'])
plt.pie(values, labels=labels,autopct='%1.1f%%',startangle=50,explode=(0.04, 0.02, 0.02, 0.02))
plt.title('Hospital Bed Usage by Service')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

correlation_of_patient_ref_rt=services_weekly[['patient_refusal_rate', 'staff_morale', 'patient_satisfaction','available_beds','patients_request','staff_morale']].corr()['patient_refusal_rate'].sort_values(ascending=False).reset_index().iloc[1:]
print(correlation_of_patient_ref_rt,'\n')

plt.scatter(services_weekly['patient_refusal_rate'],services_weekly['patients_request'])
plt.title('Graph showing patient refusal rate correlation with patients_request')
plt.xlabel('patients request')
plt.ylabel('Bed Occupancy Rate (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

correlation_of_patient_refuse_rate_by_service=services_weekly.groupby('service')[['patients_request','patient_refusal_rate']].mean().reset_index().sort_values(ascending=False,by='patient_refusal_rate')
print(correlation_of_patient_refuse_rate_by_service,'\n')
reason = "In the Emergency service, high patient requests are the main reason for the high patient refusal rate."
print(reason)


# In[ ]:





# In[459]:


# How do special events (e.g., epidemics, staff strikes) affect patient admissions and morale?

summary_table_of_event_affection=services_weekly.groupby('event')[['patients_admitted','staff_morale']].mean().reset_index()
print(summary_table_of_event_affection,'\n')


# In[ ]:





# In[1347]:


# Is there a seasonal trend in the number of patient requests?  seasonal_trand=

services_weekly['month_name']=services_weekly['month'].map({1: 'January', 2: 'February', 3: 'March', 4: 'April', 
                                                            5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September'
                                                            , 10: 'October', 11: 'November', 12: 'December'})
services_weekly['season']=services_weekly['month'].apply(lambda x: 'Winter' if x in [12,1,2] else 'Spring' if x in [3,4,5] else 
                                                         'Summer' if x in [6,7,8] else 'Autumn' if x in [9,10,11] else None)

seasonal_trend_in_pat_req=services_weekly.groupby(['month_name','month'])['patients_request'].sum().reset_index().sort_values(ascending=True,by='month')

seasons = {
    'Winter': ['December','January','February'],
    'Spring': ['March','April','May'],
    'Summer': ['June','July','August'],
    'Autumn': ['September','October','November']
}
colors = []
for month in seasonal_trend_in_pat_req['month_name']:
    if month in seasons['Winter']:
        colors.append('skyblue')
    elif month in seasons['Spring']:
        colors.append('lightgreen')
    elif month in seasons['Summer']:
        colors.append('red')
    else:
        colors.append('lightcoral')
plt.figure(figsize=(12,6))
plt.bar(seasonal_trend_in_pat_req['month_name'], seasonal_trend_in_pat_req['patients_request'], color=colors)
plt.plot(seasonal_trend_in_pat_req['month_name'], seasonal_trend_in_pat_req['patients_request'], color='blue', marker='o', linewidth=2)
plt.title('Patient Requests by Month (Seasonal Trend Highlighted)')
plt.xlabel('Month')
plt.ylabel('Number of Patient Requests')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()  
print('yes there is seasonality in the patients requests in Winter')


# In[252]:


services_weekly


# In[ ]:





# # 2 🏥 PATIENT DATA ANALYSIS
# 
# Table: ['patient_id', 'name', 'age', 'arrival_date', 'departure_date', 'service', 'satisfaction']
# 
# What is the average length of stay for patients by service?
# 
# Is there any correlation between patient age and satisfaction score?
# 
# Which service has the highest average satisfaction rating?
# 
# What is the trend of patient admissions over time (monthly)?
# 
# What is the distribution of patient ages? Are there outliers?

# In[553]:


#What is the average length of stay for patients by service?
patients['patient_time_stayed_by_days']=pd.to_datetime(patients['departure_date'])-pd.to_datetime(patients['arrival_date'])
avg_stay_by_service=patients.groupby('service')['patient_time_stayed_by_days'].mean()

for col,time in avg_stay_by_service.items():
    print(f'the average length of stay in the  {col.upper()} service is : {time}')


# In[ ]:





# In[1349]:


# Is there any correlation between patient age and satisfaction score?
corr_value_betwin_age_satis=patients[['age','satisfaction']].corr().loc['age','satisfaction']
plt.scatter(patients['age'],patients['satisfaction'])
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
if corr_value_betwin_age_satis < 0.7:
    print(f'the correlation value is :{corr_value_betwin_age_satis:.2f} so there is weak correlation betwin age and satisfaction')
else :print(f'the correlation value is :{corr_value_betwin_age_satis:.2f} so there is strong correlation betwin age and satisfaction')
    


# In[ ]:





# In[604]:


#Which service has the highest average satisfaction rating?
avg_satisfation_by_service=patients.groupby('service')['satisfaction'].mean().sort_values(ascending=False).reset_index()
print(avg_satisfation_by_service,'\n')
print(f'the highest average satisfaction rating it in {avg_satisfation_by_service.loc[0,"service"].upper()} service')


# In[ ]:





# In[1351]:


#What is the What is the trend of patient admissions over time (monthly)? 
trend_patient_admissions_by_month=services_weekly.groupby(['month','month_name'])['patients_admitted'].sum().reset_index()
print(trend_patient_admissions_by_month)


plt.plot(trend_patient_admissions_by_month['month_name'], trend_patient_admissions_by_month['patients_admitted'], color='blue', marker='o', linewidth=2)
plt.title('Patient admitted by Month')
plt.xlabel('Month')
plt.ylabel('Number of Patient admitted')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()  


# In[1353]:


# What is the distribution of patient ages? Are there outliers?
bins=round((patients.age.max() - patients.age.min())/5)


plt.hist(patients.age,bins=bins,edgecolor='black')
plt.title('the distribution of patient ages')
plt.xlabel('ages')
plt.ylabel('count of ages')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()  

plt.figure(figsize=(2,5))
sns.boxplot(patients.age,vert=True, patch_artist=True)
plt.title('Box Plot of Patient Ages')
plt.ylabel('Age')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
print('As we see in the box plot there is no outliers')


# In[ ]:





# In[ ]:





# # 3 👩‍⚕️ STAFF DATA
# 
# Table: ['staff_id', 'staff_name', 'role', 'service']
# 
# How many staff are assigned to each service?
# 
# What is the distribution of roles (e.g., doctors, nurses, admin)?
# 
# Which services have the highest staff-to-patient ratio?

# In[712]:


# How many staff are assigned to each service?
staff_count_in_service=staff.groupby('service')['staff_id'].count()
for col ,count in staff_count_in_service.items():
    print(f'number of staff assigned in {col.upper()} service is {count}')


# In[ ]:





# In[1355]:


#What is the distribution of roles (e.g., doctors, nurses, admin)?
staff.groupby('role').size().plot(kind='bar')
plt.title('Distribution of Staff Roles')
plt.ylabel('Number of Staff')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()


# In[ ]:





# In[852]:


# Which services have the highest staff-to-patient ratio?
staff_to_patient=pd.merge(staff,patients,on='service')

high_ratio_data=staff_to_patient.groupby('service')[['staff_id','patient_id']].nunique().reset_index()
high_ratio_data['ratio']=high_ratio_data['staff_id'] / high_ratio_data['patient_id']

highest_on_service=high_ratio_data.sort_values(ascending=True,by='ratio').loc[0,'service']

print(f'service with the highest ratio staff-to-patient is {highest_on_service}' )


# In[ ]:





# In[764]:


staff_to_patient.head()


# In[694]:





# # 4 📆 STAFF ATTENDANCE DATA
# 
# Table: ['week', 'staff_id', 'staff_name', 'role', 'service', 'present']
# 
# What is the average staff attendance rate per week and per service?
# 
# Which staff members have the lowest attendance, and what’s their role?
# 
# Is there a relationship between staff presence and patient satisfaction or morale?
# 
# Does staff attendance decrease during high-event weeks (e.g., epidemics)?
# 
# Is there a link between services with high patient refusal rates and low staff availability?

# In[1357]:


# What is the average staff attendance rate per week and per service?

avg_attendence_by_week=(staff_schedule.groupby('week')['present'].mean()*100).reset_index()
print(f'* average staff attendance rate per week : \n ---------------------------------------\n {avg_attendence_by_week}')
plt.plot(avg_attendence_by_week['week'],avg_attendence_by_week['present'])
plt.title('the average staff attendance rate per week')
plt.xlabel('week')
plt.ylabel('attendance rate')
plt.xticks(rotation=45)
#plt.grid(True, linestyle='--', alpha=0.5)
plt.show()  
avg_attendence_by_service=(staff_schedule.groupby('service')['present'].mean()*100).reset_index()

print(f'* average staff attendance rate per service :\n ---------------------------------------\n{avg_attendence_by_service}')

labels=list(avg_attendence_by_service['service'])
values=list(avg_attendence_by_service['present'])
plt.pie(values, labels=labels,autopct='%1.1f%%',startangle=50,explode=(0.04, 0.02, 0.02, 0.02))
plt.title('staff attendance rate per service')
plt.show()


# In[1299]:





# In[1221]:


# Which staff members have the lowest attendance, and what’s their role?
v=staff_schedule.groupby('staff_name')[['present','role']].agg({'present': 'sum','role': 'unique'}).reset_index()
min_attendence=v['present'].min()
print('the staff members with lowest attendence are :')
for name,count in v.iterrows():
    if count.present == min_attendence:
        print(f'{count.staff_name} with {count.present} attendence in role {count.role[0].upper()}')


# In[ ]:





# In[1270]:


# Is there a relationship between staff presence and patient satisfaction ?
data_merged_p_s=pd.merge(staff_schedule,patients,on='service')
present_satisafaction_corr=pd.merge(staff_schedule,patients,on='service').groupby('present')['satisfaction'].mean().reset_index()
present_satisafaction_corr

corr_value_present_satisf=data_merged_p_s['present'].corr(data_merged_p_s['satisfaction'])

if corr_value_present_satisf < 0.7:
    print(f'the correlation value is :{corr_value_betwin_age_satis:.2f} so there is weak correlation betwin present and satisfaction')
else :print(f'the correlation value is :{corr_value_betwin_age_satis:.2f} so there is strong correlation betwin present and satisfaction')


# In[ ]:





# In[1333]:


# Is there a link between services with high patient refusal rates and low staff availability?
staff_availability = (staff_schedule.groupby('service')['present'].mean()*100).reset_index().rename(columns={'present': 'staff_availability'})

merged = pd.merge(services_weekly, staff_availability, on='service')
corr = merged['patient_refusal_rate'].corr(merged['staff_availability'])
if corr < 0.7:
    print(f'the correlation value is :{corr:.2f} so there is weak correlation betwin patient refusal rate and staff availability')
else :print(f'the correlation value is :{corr:.2f} so there is strong correlation betwin patient refusal_rate and staff availability')

