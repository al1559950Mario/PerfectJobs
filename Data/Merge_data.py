import pandas as pd
from datetime import date
from pathlib import Path
import os.path

year = 2021
month = 11
day = 9
#carpeta
BASE_DIR = Path(__file__).resolve().parent
print("carpeta: ", BASE_DIR)
#rutas de los archivos
ruta1 = os.path.join(BASE_DIR,"Empleos_TI_Ian_{}.csv".format(date(year, month, day).strftime('%Y%m%d')))
ruta2 = os.path.join(BASE_DIR,"Empleos_TI_Mario_{}.csv".format(date(year, month, day).strftime('%Y%m%d')))
ruta3 = os.path.join(BASE_DIR,"Empleos_TI_Jezrrel_{}.csv".format(date(year, month, day).strftime('%Y%m%d')))
ruta4 = os.path.join(BASE_DIR,"Empleos_TI_Cecy_{}.csv".format(date(year, month, day).strftime('%Y%m%d')))
print(ruta1)
print(ruta2)
print(ruta3)
print(ruta4)
#importar datos 
data1 = pd.read_csv(ruta1)
data2 = pd.read_csv(ruta2)
data3 = pd.read_csv(ruta3)
data4 = pd.read_csv(ruta4)
#Merge data and drop duplicates
data_completa = pd.concat([data1, data2, data3, data4], axis=0)
data_completa = data_completa.dropna(subset=["Title","Description"])
data_completa["Title"] = data_completa["Title"].str.lower()
data_completa["Location"] = data_completa["Location"].str.lower()
data_completa["Company"] = data_completa["Company"].str.lower()
data_completa = data_completa.drop_duplicates(subset=["Title", "Location", "Company"])
#clean data
#rango salarial se pasa a min salario y max salario
data_completa["Salary"] = data_completa["Salary"].str.replace("\\$","", regex = True)
data_completa["Salary"] = data_completa["Salary"].str.replace(",","" )
salario = data_completa["Salary"].str.split('\sa\s', expand=True)
salario.columns = ['Salary_min', 'Salary_max']
data_completa = pd.concat([data_completa, salario], axis=1)
data_completa['Salary_min']= data_completa['Salary_min'].replace(['No especificado'],[None])
data_completa['Salary_min'] = data_completa.Salary_min.astype('float')
data_completa['Salary_max'] = data_completa.Salary_max.astype('float')
#remoto a boleano
data_completa['Remoto']= data_completa['Remoto'].replace(['Remote'],[True])
data_completa['Remoto']= data_completa['Remoto'].replace([None],[False])
data_completa['Remoto'] = data_completa.Remoto.astype('bool')
#fecha de acceso a fecha y,m,d
data_completa["Accessed_Date"] = pd.to_datetime(data_completa["Accessed_Date"], format="%Y-%m-%d")
#guardar data
data_completa.to_csv("Data\Data_completa_{}.csv".format(date(year, month, day).strftime('%Y%m%d')), index=False)

