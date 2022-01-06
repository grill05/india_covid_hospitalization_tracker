import os,sys
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

if __name__=='__main__':
  #download the repo
  os.system('git clone --depth 1 https://github.com/grill05/misc_bed_availability_scraper && mv misc_bed_availability_scraper/*csv . && rm -rf misc_bed_availability_scraper&&ls -al')
  os.system('git clone --depth 1 https://github.com/grill05/covid19india_data_parser && mv covid19india_data_parser/*.py . && rm -rf covid19india_data_parser&&ls -al')
  import dataparser3 as dp
  
  #get covid19bharat data
  os.system('curl -# -O https://data.covid19bharat.org/csv/latest/states.csv')
  os.system('curl -# -O https://data.covid19bharat.org/csv/latest/districts.csv')
  
  #create chennai plot
  print('chennai')
  a=open('chennai.html','w')  
  
  x=pd.read_csv('tamil_nadu.csv')
  x2=x[x.district=='Chennai']
  
  d,c=zip(*dp.get_cases_district('tn','Chennai'))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  x2=pd.merge(x2,c,how='left')

  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Chennai daily cases vs hospitalizations')
  # ~ fig=px.line(x2,x='date',y=['cases','occupied_o2_beds','occupied_icu_beds'],markers=True,title='Cases vs hospital occupancy in Chennai')
  # ~ fig=px.line(x2,x='date',y=['cases','occupied_o2_beds','occupied_icu_beds'],markers=True,title='Cases vs hospital occupancy in Chennai')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  
  fig=px.line(x2,x='date',y=['occupied_o2_beds','occupied_nono2_beds','occupied_icu_beds','total_o2_beds','total_nono2_beds',       'total_icu_beds'],markers=True,title='Hospital bed occupancy in Chennai')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  a.close()
  
  #create ROTN plot
  print('RoTN')
  a=open('rotn.html','w')  
  
  x=pd.read_csv('tamil_nadu.csv')
  for district in dp.tamil_nadu_districts:
    if district=='Chennai': continue
    try:
      x2=x[x.district==district]
    
      d,c=zip(*dp.get_cases_district('tn',district))
      c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
      x2=pd.merge(x2,c,how='left')
  
      #cases vs hosp
      
      fig = make_subplots(specs=[[{"secondary_y": True}]])
      
      fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
      fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
      fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
      fig.update_xaxes(title_text='Date')
      fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
      fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
      fig.update_layout(title=district+' daily cases vs hospitalizations')
      a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
      
      
      fig=px.line(x2,x='date',y=['occupied_o2_beds','occupied_nono2_beds','occupied_icu_beds','total_o2_beds','total_nono2_beds',       'total_icu_beds'],markers=True,title='Hospital bed occupancy in '+district)
      a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    except:
      print('Failed to create hospitalization plots for '+district)
  a.close()
  
  #bengaluru
  print('bengaluru')
  
  a=open('bengaluru.html','w')  
  
  x=pd.read_csv('data.bengaluru.csv')
  
  d,c=zip(*dp.get_cases_district('ka','Bengaluru Urban'))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  x2=pd.merge(x,c,how='left')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['general_beds_occupancy'], name="Occupied general Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['hdu_beds_occupancy'], name="Occupied HDU Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['icu_beds_occupancy'], name="Occupied ICU Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['ventilator_beds_occupancy'], name="Occupied Ventilator Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Bengaluru daily cases vs hospitalizations')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['general_beds_capacity','general_beds_occupancy','hdu_beds_capacity','hdu_beds_occupancy','icu_beds_capacity','icu_beds_occupancy','ventilator_beds_capacity','ventilator_beds_occupancy'],markers=True,title='Hospital bed occupancy/capacity in Bengaluru')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  a.close()
  
   
  #gurugram
  print('gurugram')
  a=open('gurugram.html','w')  
  
  x=pd.read_csv('gurugram.csv')
  
  d,c=zip(*dp.get_cases_district('hr','Gurugram'))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  x2=pd.merge(x,c,how='left')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['dhc_dchc_occupied'], name="Occupied hospital (DCH+DCHC) Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['dccc_occupied'], name="Occupied DCCC Beds",mode='lines+markers'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Gurugram daily cases vs hospitalizations')
  
  
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  a.close()
  
  #mumbai
  print('mumbai')
  a=open('mumbai.html','w')  
  
  x=pd.read_csv('mumbai.csv')
  del x['cases'] #take case-counts from covid19bharat
  
  d,c=zip(*dp.get_cases_district('mh','Mumbai'))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  c=c[c.cases>0]

  x2=pd.merge(x,c,how='left',on='date')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['general_beds_occupancy'], name="Occupied general Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['O2_occupied'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['ICU_occupied'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['Ventilator_occupied'], name="Occupied Ventilator Beds",mode='lines+markers'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Mumbai daily cases vs hospitalizations')
  
  
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['general_beds_occupancy','O2_occupied','ICU_occupied','Ventilator_occupied','general_beds_capacity','O2_capacity','ICU_capacity','Ventilator_capacity'],markers=True,title='Hospital bed occupancy/capacity in Mumbai')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    
  a.close()
  #pune
  print('pune')
  a=open('pune.html','w')  
  
  x=pd.read_csv('data.pune.csv')
  
  d,c=zip(*dp.get_cases_district('mh','Pune'))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})

  x2=pd.merge(x,c,how='left',on='date')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_normal_beds'], name="Occupied general Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_ventilator_beds'], name="Occupied Ventilator Beds",mode='lines+markers'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Pune daily cases vs hospitalizations')
  
  
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['occupied_normal_beds','occupied_o2_beds','occupied_icu_beds','occupied_ventilator_beds','total_normal_beds','total_o2_beds','total_icu_beds','total_ventilator_beds'],markers=True,title='Hospital bed occupancy/capacity in Pune')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

  #H.P.
  print('H.P.')
  a=open('hp.html','w')  
  
  x=pd.read_csv('data.hp.csv')
  
  d,c=zip(*dp.get_cases('hp',delta=True))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})

  x2=pd.merge(x,c,how='left',on='date')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_normal_beds'], name="Occupied general Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
  
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Himachal Pradesh daily cases vs hospitalizations')
  
  
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['occupied_normal_beds','occupied_o2_beds','occupied_icu_beds','total_normal_beds','total_o2_beds','total_icu_beds'],markers=True,title='Hospital bed occupancy/capacity in Himachal Pradesh')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    
  a.close()

  #M.P.
  print('M.P.')
  a=open('mp.html','w')  
  
  x=pd.read_csv('data.mp.csv')
  
  d,c=zip(*dp.get_cases('mp',delta=True))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})

  x2=pd.merge(x,c,how='left',on='date')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_normal_beds'], name="Occupied general Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
  
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Madhya Pradesh daily cases vs hospitalizations')
  
  
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['occupied_normal_beds','occupied_o2_beds','occupied_icu_beds','total_normal_beds','total_o2_beds','total_icu_beds'],markers=True,title='Hospital bed occupancy/capacity in Madhya Pradesh')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    
  a.close()
  
 #delhi
  print('Delhi.')
  a=open('delhi.html','w')  
  
  x=pd.read_csv('data.delhi.csv')
  
  d,c=zip(*dp.get_cases('dl',delta=True))
  c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  x2=pd.merge(x,c,how='left')
  
  #cases vs hosp
  
  fig = make_subplots(specs=[[{"secondary_y": True}]])
  
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers',line_shape='spline'),secondary_y=False)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_beds'], name="Occupied General Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_oxygen_beds'], name="Occupied O2 Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_covid_icu_beds'], name="Occupied ICU Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_ventilators'], name="Occupied Ventilator Beds",mode='lines+markers',line_shape='spline'),secondary_y=True)
  fig.update_xaxes(title_text='Date')
  fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
  fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
  fig.update_layout(title='Delhi daily cases vs hospitalizations')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  fig=px.line(x2,x='date',y=['occupied_beds', 'occupied_oxygen_beds',
       'occupied_covid_icu_beds', 'occupied_ventilators', 'total_beds', 'total_oxygen_beds', 'total_covid_icu_beds',
       'total_ventilators'],markers=True,title='Hospital bed occupancy/capacity in Delhi')
  a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
  
  a.close()
  
  #kl,tg,ap,uk
  for state in ['kerala','telangana','ap','uttarakhand','chandigarh','nagpur','nashik','vadodara','gandhinagar','wb']:
    print(state.upper())
    a=open(state+'.html','w')  
    
    x=pd.read_csv('data.'+state+'.csv')
    
    if state in ['nagpur','nashik']:
      d,c=zip(*dp.get_cases_district('mh',state.capitalize()))
    elif state in ['vadodara','gandhinagar']:
      d,c=zip(*dp.get_cases_district('gj',state.capitalize()))
    else:
      d,c=zip(*dp.get_cases(state.capitalize().replace('Ap','ap').replace('Wb','wb'),delta=True))
    c=pd.DataFrame({'date':[i.strftime('%Y-%m-%d') for i in d],'cases':c})
  
    x2=pd.merge(x,c,how='left',on='date')
    
    #cases vs hosp
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x=x2['date'],y=x2['cases'], name="Daily cases",mode='lines+markers'),secondary_y=False)
    fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_normal_beds'], name="Occupied general Beds",mode='lines+markers'),secondary_y=True)
    if state not in ['wb']:
      fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_o2_beds'], name="Occupied O2 Beds",mode='lines+markers'),secondary_y=True)
      fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_icu_beds'], name="Occupied ICU Beds",mode='lines+markers'),secondary_y=True)
      if state not in ['telangana']:
        fig.add_trace(go.Scatter(x=x2['date'],y=x2['occupied_ventilator_beds'], name="Occupied Ventilator Beds",mode='lines+markers'),secondary_y=True)
    
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Daily Cases',secondary_y=False)
    fig.update_yaxes(title_text='Bed Occupancy',secondary_y=True)
    fig.update_layout(title=state.upper()+' daily cases vs hospitalizations')
    
    
    a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
    
    available_columns=['occupied_normal_beds','occupied_o2_beds','occupied_icu_beds','total_normal_beds','total_o2_beds','total_icu_beds']
    if state not in ['telangana']:
      available_columns=['occupied_normal_beds','occupied_o2_beds','occupied_icu_beds','occupied_ventilator_beds','total_normal_beds','total_o2_beds','total_icu_beds','total_ventilator_beds']
    if state=='wb':available_columns=['occupied_normal_beds','total_normal_beds']
    fig=px.line(x2,x='date',y=available_columns,markers=True,title='Hospital bed occupancy/capacity in '+state.upper())
    a.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
      
    a.close()
  
