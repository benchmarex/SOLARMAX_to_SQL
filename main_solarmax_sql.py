"""
Author Marek Pikulski 30.03.2023. benchmarek[at]outlook[dot]com https://github.com/benchmarex

This project downloads data solar production and operating parameters of the photovoltaic system from the Solarmax
inverter via local ethernet connection TCP/IP Solarnet protocol. The data is sent to the local mysql server.
The script is written in Python and invoked using the cron mechanism at intervals of __ minutes.
"""

'''

# There are other such as UGD, UI1, UI2, UI3...but not sure what they do
QUERY_DICT = {
    'KDY': 'Energy today (kWh)', 'KDL': 'Energy yesterday (Wh)', 'KYR': 'Energy this year (kWh)', 'KLY': 'Energy last year (kWh)',
    'KMT': 'Energy this month (kWh)', 'KLM': 'Energy last month (kWh)', 'KT0': 'Total Energy(kWh)', 'IL1': 'AC Current Phase 1 (A)',
    'IL2': 'AC Current Phase 2 (A)', 'IL3': 'AC Current Phase 3 (A)', 'IDC': 'DC Current (A)', 'PAC': 'AC Power (W)',
    'PDC': 'DC Power (W)', 'PRL': 'Relative power (%)', 'TNP': 'Grid period duration',
    'TNF': 'Generated Frequency (Hz)', 'TKK': 'Inverter Temperature (C)', 'UL1': 'AC Voltage Phase 1 (V)',
    'UL2': 'AC Voltage Phase 2 (V)', 'UL3': 'AC Voltage Phase 3 (V)', 'UDC': 'DC Voltage (V)',
    'UD01': 'String 1 Voltage (V)', 'UD02': 'String 2 Voltage (V)', 'UD03': 'String 3 Voltage (V)',
    'ID01': 'String 1 Current (A)', 'ID02': 'String 2 Current (A)', 'ID03': 'String 3 Current (A)',
    'ADR': 'Address', 'TYP': 'Type', 'PIN': 'Installed Power (W)', 'CAC': 'Start Ups (?)', 'KHR': 'Operating Hours',
    'SWV': 'Software Version', 'DDY': 'Date day', 'DMT': 'Date month', 'DYR': 'Date year', 'THR': 'Time hours',
    'TMI': 'Time minutes', 'LAN': 'Language',
    'SAL': 'System Alarms', 'SYS': 'System Status',
    'MAC': 'MAC Address', 'EC00': 'Error Code 0', 'EC01': 'Error Code 1', 'EC02': 'Error Code 2', 'EC03': 'Error Code 3',
    'EC04': 'Error Code 4', 'EC05': 'Error Code 5', 'EC06': 'Error Code 6', 'EC07': 'Error Code 7', 'EC08': 'Error Code 8',
    'BDN': 'Build number',
    'DIN': '?',
    'SDAT': 'datetime ?', 'FDAT': 'datetime ?',
    'U_AC': '?', 'F_AC': 'Grid Frequency', 'SE1': '',
    'U_L1L2': 'Phase1 to Phase2 Voltage (V)', 'U_L2L3': 'Phase2 to Phase3 Voltage (V)', 'U_L3L1': 'Phase3 to Phase1 Voltage (V)'
}


'''


from pythonping import ping
import json
import sys
import datetime
import pymysql
import os
import time
import socket

def get_time():
    # get system time

    now = datetime.datetime.now()
    pm_solartime = now.strftime("%Y-%m-%d %H:%M:%S")
    return (pm_solartime)       # '2022-11-04 22:21:36'

def find_cmd_value(cmd):

    result = ['0', '0', '0', '0']

    # 2 bytes example IDC=6F;
    i = k = resp_.find(cmd)+6

    if resp_[k] == ';':
        k = k - 2   #if 2 char hex
        result[2] = resp_[k]
        k = k + 1
        result[3] = resp_[k]

    # 3 bytes example PAC=1D4;

    k = i + 1

    if resp_[k] == ';':
        k = k - 3  # if 3 char hex
        result[1] = resp_[k]
        k = k + 1
        result[2] = resp_[k]
        k = k + 1
        result[3] = resp_[k]

    k = i + 2

    #4 bytes  example TNF=1385;

    if resp_[k] == ';':
        k = k - 4  # if 3 char hex
        result[0] = resp_[k]
        k = k + 1
        result[1] = resp_[k]
        k = k + 1
        result[2] = resp_[k]
        k = k + 1
        result[3] = resp_[k]


    result = result[0] + result[1] + result[2] + result[3]  # merge list
    result = int(result, 16)   # convert hex to dec

    return result


###########___start program___#################


with open('C:\\Users\\Marek\\PycharmProjects\\pythonProject\\config13.json') as jsonFile:
    jsonObject = json.load(jsonFile)

SOLARMAX_INVERTER_HOST = jsonObject['SOLARMAX_INVERTER_HOST']
SOLARMAX_INVERTER_PORT = jsonObject['SOLARMAX_INVERTER_PORT']

'''
resp = str(ping(SOLARMAX_INVERTER_HOST))
resp = resp.find("Request timed out")

if resp == -1:
        print(SOLARMAX_INVERTER_HOST, 'Host is up')

else:
        print(SOLARMAX_INVERTER_HOST, 'Host is unreachable')
        sys.exit()

# socket and connection make

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SOLARMAX_INVERTER_HOST, SOLARMAX_INVERTER_PORT))

# request to inverter

request=b'{FB;7B;8E|64:TK2;UDC;IDC;PDC;UL1;IL1;PAC;TNF;TKK;KHR;KDY;KLD;KMT;KYR;KT0;PIN;SWV;TNP;PAM;SCD;SE1;SE2;IAM;IEA;IED;UGD;SPC;SPR;DIN;LAN;CAC|2539}'


sock.send(request)

# read response from inverter

response = sock.recv(1024)

# close connection
sock.close()
'''

#response = b'{7B;FB;CC|64:UDC=93D;IDC=165;PDC=69C;UL1=982;IL1=146;PAC=622;TNF=1386;TKK=1E;KHR=2F07;KDY=37;KLD=4D;KMT=1B;KYR=1F;KT0=21CA;PIN=19C8;SWV=F;PAM=157C;IAM=4;IEA=1D;IED=11;UGD=750;DIN=3E2FA;LAN=1;CAC=AB0|31C9}'
#inverter adress 0x7b (123)
response = b'{7B;FB;C9|64:UDC=970;IDC=6F;PDC=218;UL1=960;IL1=67;PAC=1D4;TNF=1385;TKK=17;KHR=2F08;KDY=3D;KLD=4D;KMT=1B;KYR=20;KT0=21CB;PIN=19C8;SWV=F;PAM=157C;IAM=3;IEA=1D;IED=B;UGD=728;DIN=3E2FA;LAN=1;CAC=AB0|3124}'

#response = b'{7B;FB;C9|64:UDC=970;IDC=6F;PDC=218;UL1=960;IL1=67;PAC=1D4;TNF=1385;TKK=17;KHR=2F08;KDY=3D;KLD=4D;KMT=1B;KYR=20;KT0=21CB;PIN=19C8;SWV=F;PAM=157C;IAM=3;IEA=1D;IED=B;UGD=728;DIN=3E2FA;LAN=1;CAC=AB0|3124}'
resp_ = str(response)
print(resp_)

###############___AC GRID___##############

AC_V1 = find_cmd_value('UL1')/10
AC_V2 = 0
AC_V3 = 0
AC_V1_CURRENT = find_cmd_value('IDC')/100
AC_V2_CURRENT = 0
AC_V3_CURRENT = 0
AC_V1_3_ACTIVE_POWER = find_cmd_value('PAC')/2
AC_V1_3_REACTIVE_POWER = 0
AC_V1_3_FREQ = find_cmd_value('TNF')/100
AC_Today_Production = find_cmd_value('KDY')/10
AC_Today_Generation_Time = find_cmd_value('TNP')/10

print(f"\nVoltage AC1 = {AC_V1} V, Current AC1 = {AC_V1_CURRENT} A\n")
print(f"Voltage AC2 = {AC_V2} V, Current AC2 = {AC_V2_CURRENT} A\n")
print(f"Voltage AC3 = {AC_V3} V, Current AC3 = {AC_V3_CURRENT} A\n")
print(f"Active Power AC1_3 = {AC_V1_3_ACTIVE_POWER} W\n")
print(f"Reactive Power AC1_3 = {AC_V1_3_REACTIVE_POWER}VAR\n")
print(f"AC_V1_3_Frequency = {AC_V1_3_FREQ} Hz\n")
print(f"Today_Production = {AC_Today_Production} kWh\n")
print(f"AC_Today_Generation_Time = {AC_Today_Generation_Time} h\n")
###############___AC GRID___#####################

###############___Temperature___#################

TEMP_INVERTER = find_cmd_value('TKK')/10
TEMP_INVERTER_MODULE = find_cmd_value('TK2')/10

print(f"Inverter temperature {TEMP_INVERTER}°C Inverter module temperature {TEMP_INVERTER_MODULE}°C\n")

###############___Temperature___#################

###############___DC ___#################


DC_V1 = find_cmd_value('UDC')/10
DC_V2 = 0
DC_V1_CURRENT = find_cmd_value('IDC')/10
DC_V2_CURRENT = 0

DC_V1_POWER = find_cmd_value('PDC')/10
DC_V2_POWER = 0


DC_V1_INSULATION_TO_GND = 0
DC_V2_INSULATION_TO_GND = 0

DC_V_INSULATION_TO_GND = 0

print(f"Voltage DC1 = {DC_V1} V, Current DC1 = {DC_V1_CURRENT} A, {DC_V1_POWER} W\n")
print(f"Voltage DC2 = {DC_V2} V, Current DC2 = {DC_V2_CURRENT} A, {DC_V2_POWER} W\n")



###############___DC ___#################



######SQL#####
DataMysql = get_time()
print(DataMysql)

sql = f"""INSERT INTO Solarmax (date, Energy, Power_AC, Inverter_temperature, Voltage_AC1, Voltage_AC2, Voltage_AC3,\n
 Current_AC1, Current_AC2, Current_AC3, Power_DC1, Power_DC2, Voltage_DC1, Voltage_DC2, Current_DC1, Current_DC2, \n
 Ac_freq, Module_temperature, Insulation_imp_cath_gnd, Insulation_imp_PV1, Insulation_imp_PV2, AC_reactive_power, AC_Today_Generation_Time) VALUES\n

 ('{DataMysql}', '{AC_Today_Production}','{AC_V1_3_ACTIVE_POWER}', '{TEMP_INVERTER}', '{AC_V1}', '{AC_V2}', '{AC_V3}',\n
  '{AC_V1_CURRENT}','{AC_V2_CURRENT}','{AC_V3_CURRENT}', '{DC_V1_POWER}','{DC_V2_POWER}', '{DC_V1}','{DC_V2}', '{DC_V1_CURRENT}',\n
  '{DC_V2_CURRENT}','{AC_V1_3_FREQ}', '{TEMP_INVERTER_MODULE}', '{DC_V_INSULATION_TO_GND}', '{DC_V1_INSULATION_TO_GND}',\n
  '{DC_V2_INSULATION_TO_GND}', '{AC_V1_3_REACTIVE_POWER}', '{AC_Today_Generation_Time}');"""


print(sql)

SQL_HOST = jsonObject["SQL_HOST"]
SQL_USER = jsonObject["SQL_USER"]
SQL_PASSWORD = jsonObject["SQL_PASSWORD"]
SQL_DATABASE = jsonObject["SQL_DATABASE"]

# Open database connection
db = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

try:
    # Execute the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    db.commit()

except:
    # Rollback in case there is any error
    db.rollback()

# disconnect from server
db.close()


