import requests
import openai
import urllib3
import json
from pydantic import BaseModel
from datetime import datetime

global g_mntacum, g_mntplan

# 1. Obtener datos de SAP Business One mediante la API
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_ENDPOINT = "https://23.88.83.123:50047/b1s/v1/Login"

data = {
    'CompanyDB': 'ZZ_VINOTECA_11122024',
    'UserName': 'manager',
    'Password': 'vinolv2022'
}

r = requests.post(url=API_ENDPOINT, json=data, verify=False)

b1session_cookie = r.cookies.get('B1SESSION')
b1session_ROUTEID = r.cookies.get('ROUTEID')

class Aglobal(BaseModel):
    nroacuerdotulo: str
    fecini: str
    fecfin: str
    mntinversion: int
    importeacum: int
    importeplan: int


url = "https://23.88.83.123:50047/b1s/v1/BlanketAgreements?$select=DocNum,StartDate,EndDate,U_Monto_Inversion,BlanketAgreements_ItemsLines&$filter=BPCode eq 'C78016900-1'"
headers = {
   
    "Cookie":"B1SESSION=" +b1session_cookie+"; ROUTEID="+b1session_ROUTEID+"",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, verify=False)
orders_data = response.json()

# 2. Procesar los datos (ejemplo: calcular total de ventas)
#total_ventas = sum(order['DocTotal'] for order in orders_data['value'])
#numero_ordenes = len(orders_data['value'])

value_list = orders_data.get("value", [])

# Recorrer los acuerdos y acceder a 'BlanketAgreements_ItemsLines'
for agreement in value_list:
    # Acceder a las líneas de ítems
    x_docnum = agreement.get("DocNum")
    x_startdate = agreement.get("StartDate")
    x_enddate = agreement.get("EndDate")
    x_monto_inversion = agreement.get("U_Monto_Inversion")

    items_lines = agreement.get("BlanketAgreements_ItemsLines", [])
    
    # Imprimir las líneas de ítems
    
    for line in items_lines:
        x_mntacum=f"{line['CumulativeAmountLC']}"
        x_mntplan=f"{line['PlannedAmountLC']}"
        g_mntacum=x_mntacum
        g_mntplan=x_mntplan
    #    print(f"CumulativeAmountLC: {line['CumulativeAmountLC']}")
    #    print(f"PlannedAmountLC: {line['PlannedAmountLC']}")

    fecha_original = datetime.strptime(x_startdate, "%Y-%m-%dT%H:%M:%SZ")
    fecha_inicio = fecha_original.strftime("%Y%m%d")

    fecha_original = datetime.strptime(x_enddate, "%Y-%m-%dT%H:%M:%SZ")
    fecha_fin = fecha_original.strftime("%Y%m%d")

    x_json={'DocNum': x_docnum, 'FechaIni': fecha_inicio, 'FechaFin': fecha_fin, 'MontoInversion': x_monto_inversion, 'MontoAcum': g_mntacum, 'MontoPlan': g_mntplan}

#    hoy = datetime.now()
#    print(hoy)

#    fecha_original = datetime.strptime(x_startdate, "%Y-%m-%dT%H:%M:%SZ")
#    fecha_formateada = fecha_original.strftime("%Y%m%d")
#    print(fecha_formateada)

    print(json.dumps(x_json,indent=4))