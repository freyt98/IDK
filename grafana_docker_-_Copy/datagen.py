import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuration
database_config = {
    'dbname': 'postgres',  # Replace with your database name
    'user': 'shoc',  # Replace with your database username
    'password': 'JustKeepSwimming',  # Replace with your database password
    'host': 'localhost',  # Replace with your database host
    'port': '5432'  # Replace with your database port
}

# Establish a database connection
conn = psycopg2.connect(
    dbname=database_config['dbname'],
    user=database_config['user'],
    password=database_config['password'],
    host=database_config['host'],
    port=database_config['port']
)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Predefined list of military equipment or gear
military_equipment = [
    'Rifle', 'Helmet', 'Body Armor', 'Night Vision Goggles', 'Combat Boots',
    'Tactical Vest', 'Handgun', 'Grenade', 'Radio', 'First Aid Kit',
    'Backpack', 'Binoculars', 'Canteen', 'Flashlight', 'Gas Mask',
    'Gloves', 'GPS', 'Sleeping Bag', 'Tent', 'Rope'
]

# Function to generate random data with constraints
def generate_random_data():
    edd = fake.date_time_this_year()
    rdd = edd + timedelta(days=random.randint(1, 10))
    eda = rdd + timedelta(days=random.randint(1, 10))
    ETA_to_APOE = fake.date_time_this_year()
    Delivery_Window = ETA_to_APOE + timedelta(days=random.randint(1, 10))

    return {
        'pda': fake.word(),
        'rcn': fake.word(),
        'status': fake.random_element(elements=('Pending', 'In Transit', 'Delivered')),
        'comments': fake.sentence(),
        'startLocation': fake.city(),
        'endLocation': fake.city(),
        'edd': edd,
        'rdd': rdd,
        'eda': eda,
        'SAMM_Details': fake.sentence(),
        'TCN': fake.lexify(text='?' * 17),
        'NSN': fake.lexify(text='?' * 13),
        'nomenclature': random.choice(military_equipment),
        'QTY': fake.random_int(min=1, max=100),
        'DODIC': fake.word(),
        'ST': fake.random_number(digits=2, fix_len=True) + random.random(),
        'Depot': fake.word(),
        'APOE': fake.word(),
        'Bol': fake.lexify(text='?' * 13),
        'SDT_Cost': fake.random_number(digits=5) + random.random(),
        'Carrier': fake.company(),
        'ETA_to_APOE': ETA_to_APOE,
        'Delivery_Window': Delivery_Window,
        'Truck_status': fake.random_element(elements=('On Schedule', 'Delayed', 'Completed')),
        'SAAM_Status': fake.random_element(elements=('Active', 'Inactive')),
        'Mode': fake.random_element(elements=('air', 'ground', 'sea')),
        'high_priority': random.random() < 0.1  # 10% chance of being True
    }

# Insert data into the table
def insert_data(cursor, data):
    insert_query = """
    INSERT INTO deliverytable (
        pda, rcn, status, comments, startLocation, endLocation, edd, rdd, eda, SAMM_Details, 
        TCN, NSN, nomenclature, QTY, DODIC, ST, Depot, APOE, Bol, SDT_Cost, Carrier, 
        ETA_to_APOE, Delivery_Window, Truck_status, SAAM_Status, Mode, high_priority
    ) VALUES (
        %(pda)s, %(rcn)s, %(status)s, %(comments)s, %(startLocation)s, %(endLocation)s, %(edd)s, %(rdd)s, %(eda)s, %(SAMM_Details)s, 
        %(TCN)s, %(NSN)s, %(nomenclature)s, %(QTY)s, %(DODIC)s, %(ST)s, %(Depot)s, %(APOE)s, %(Bol)s, %(SDT_Cost)s, %(Carrier)s, 
        %(ETA_to_APOE)s, %(Delivery_Window)s, %(Truck_status)s, %(SAAM_Status)s, %(Mode)s, %(high_priority)s
    )
    """
    cursor.execute(insert_query, data)

# Generate and insert multiple rows of data
for _ in range(100):  # Adjust the number to insert more or fewer rows
    data = generate_random_data()
    insert_data(cursor, data)

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully")