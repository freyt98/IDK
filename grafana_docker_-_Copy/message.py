import random
from datetime import datetime, timedelta
import json

SERVICES = ['USAF','USN','USMC','USA']
TRANSPORT_MODES = ['Air','Sea','Land','TBD']
TYPE_AMMO = ['AIM120','AIM9','MK82','MK84','M61','M134','M240','M249','M2','M203','155mm']
DOMESTIC_PLACES = ['MIA','JAX','ATL','DFW','LAX','SFO','SEA','ORD','JFK','BOS','PHL']
FOREIGN_PLACES = ['LHR','CDG','FRA','MAD','FCO','IST','DXB','HKG','NRT','SYD','SIN']
HEADERS = ['ID', 'pda', 'rcn', 'status', 'comments', 'startLocation', 'endLocation', 
           'edd', 'rdd', 'eda', 'SAMM Details', 'TCN', 'NSN', 'nomenclature', 'QTY', 
           'DODIC', 'ST', 'Depot', 'APOE', 'Bol', 'SDT Cost', 'Carrier', 'ETA to APOE', 
           'Delivery Window', 'Truck status', 'SAAM Status']

def generate_random_date(start_date, end_date):
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds())),
    )

def generate_pda(pda_number, starting_date):
    number_items = random.randint(2,8)
    sign_date = starting_date
    items = []
    for i in range(number_items):

        nomenclature = random.choice(TYPE_AMMO)
        service = random.choice(SERVICES)
        quantity = random.randint(10,80)
        transport_mode = random.choice(TRANSPORT_MODES)
        from_location = random.choice(DOMESTIC_PLACES)
        to_location = random.choice(FOREIGN_PLACES)
        transferred = random.randint(int(quantity/2),quantity)
        percent_transferred = str(int((transferred/quantity)*100)) + '%'
        ship_date = starting_date + timedelta(days=random.randint(2,5))
        delivery_date = ship_date + timedelta(days=random.randint(5,19))

        items.append({'service':service, 'nomenclature':nomenclature, 'quantity':quantity, 'transferred':transferred, 'percent_transferred':percent_transferred, 
                      'ship_date':ship_date.strftime('%Y-%m-%d'), 'delivery_date':delivery_date.strftime('%Y-%m-%d'), 'transport_mode':transport_mode, 'from_location':from_location, 
                      'to_location':to_location})

    data = {'pda_number':pda_number,'sign_date':sign_date.strftime('%Y-%m-%d'), 'delivery_date': delivery_date.strftime('%Y-%m-%d'), 'items': items}
    return data

def generate_pdas():
    starting_date = generate_random_date(datetime(2021, 1, 1), datetime(2024, 1, 31)) 
    number_pdas = int(input('Enter the number of PDAs to generate: '))
    pdas_object = []
    for i in range(0,number_pdas):
        pdas_object.append(generate_pda(i, starting_date))
        starting_date += timedelta(days=random.randint(20,30))
    return pdas_object
    
def print_pdas_data(pdas_data):
    for pda in pdas_data:
        for key, value in pda.nomenclatures():
            print(f'PDA Number: {key}')
            print(f'Sign Date: {value["sign_date"]}')
            print('nomenclatures:')
            for nomenclature in value['nomenclatures']:
                print(f'\tService: {nomenclature[0]}')
                print(f'\tnomenclature: {nomenclature[1]}')
                print(f'\tQuantity: {nomenclature[2]}')
                print(f'\tTransferred: {nomenclature[3]}')
                print(f'\tShip Date: {nomenclature[5]}')
                print(f'\tDelivery Date: {nomenclature[6]}')
                print(f'\tTransport Mode: {nomenclature[7]}')
                print(f'\tFrom Location: {nomenclature[8]}')
                print(f'\tTo Location: {nomenclature[9]}')
                print('\n')

def dump_nomenclatures_data_csv():
    pdas_data = generate_pdas()
    with open('pdas_data.csv', 'w') as f:
        f.write(','.join(HEADERS) + '\n')
        for pda in pdas_data:
            for item in pda['items']:
                id = random.randint(1000,9999)
                pda_number = pda['pda_number']
                rcn = random.randint(100000,999999)
                status = random.choice(['Delivered','TBD','OTW'])
                comments = ''
                startLocation = item['from_location']
                endLocation = item['to_location']
                edd = item['ship_date']
                rdd = item['delivery_date']
                eda = item['delivery_date']
                SAMM_Details = ''
                TCN = 'TCN' + str(random.randint(100000,999999))
                NSN = 'NSN' + str(random.randint(100000,999999))
                nomenclature = item['nomenclature']
                QTY = item['quantity']
                DODIC = 'DODIC' + str(random.randint(1000,9999))
                ST = random.randint(0,100)
                Depot = ''
                APOE = item['to_location']
                Bol = 'BOL' + str(random.randint(100000,999999))
                SDT_Cost = random.randint(1000,9999)
                Carrier = random.choice(['Fedex','UPS','USPS'])
                ETA_to_APOE = random.choice(['2021-01-01','2021-01-02','2021-01-03'])
                Delivery_Window = random.choice(['2021-01-01','2021-01-02','2021-01-03'])
                Truck_status = random.choice(['Delivery to X base at XX (date)','TBD'])
                SAAM_Status = random.choice(['delivered XX (date)','TBD'])

                f.write(f'{id},{pda_number},{rcn},{status},{comments},{startLocation},{endLocation},{edd},{rdd},{eda},{SAMM_Details},{TCN},{NSN},{nomenclature},{QTY},{DODIC},{ST},{Depot},{APOE},{Bol},{SDT_Cost},{Carrier},{ETA_to_APOE},{Delivery_Window},{Truck_status},{SAAM_Status}\n')
    print('Your data has been saved to pdas_data.csv')

dump_nomenclatures_data_csv()

'''
0 ID - int
1 pda - string
2 rcn - string
3 status - string
4 comments - string
5 startLocation - string 
6 endLocation -string
7 edd - timestamp / estimaed dep date 
8 rdd - timestamp / required del date
9 eda - timestamp / estimaed del date
10 SAMM Details - SAAM:1234G MissionID: Callsign:
11 TCN - 17char
12 NSN - 13 char
13 nomenclature - string
14 QTY - int
15 DODIC - A525
16 ST - Float
17 Depot - string
18 APOE - string
19 Bol - 13 char string
20 SDT Cost - Double
21 Carrier - string
22 ETA to APOE - timestamp
23 Delivery Window - timestamp
24 Truck status - Delivery to X base at XX (date)
25 SAAM Status - delivered XX (date) 
'''