import psycopg2
import pandas as pd



# CONNECT TO DATABASE
# ENTER YOUR OWN DATA

# MY PLAN ON THE NEXT WORK TIME ON THIS IS TO CREATE A SEPERATE .PY WITH VARIABLES
# FOR THESE SO THAT THEY CAN JUST WORK OUT OF THE BOX, BUT I DON'T HAVE TIME AT THIS
# MOMENT - KYLE, 11/1/2024


conn = psycopg2.connect(
    dbname="human_rights",
    user="ENTER USER HERE",
    password= "ENTER PASSWORD HERE",
    host="ENTER HOST HERE",
    port="ENTER PORT HERE"
)



# CONNECT CURSOR



cursor = conn.cursor()



# COUNTRY REFERENCE TABLE. INCLUDES NO DATA THAT SHOULD EVER CHANGE. DATA COULD BE ADDED
# OVER TIME, BUT IT SEEMS UNLIKELY THAT SOMETHING COULD CHANGE

# IF SOMETHING DOES CHANGE, I'D THINK IT WOULD BE AN ADDITIONAL REGION DIVISION,
# WHICH COULD BE CARRIED FORWARD INTO OTHER QUERIES;
# AS IN, IF THE DIVISION BECOMES A STATISTICAL DIVISION, WE ADD THE DISTINCTION,
# AND WE START DIVIDING BASED ON THAT AS WELL.



cursor.execute("""
CREATE TABLE IF NOT EXISTS country_reference (
    global_code CHAR(4),
    global_name TEXT,
    region_code CHAR(4),
    region_name TEXT,
    sub_region_code CHAR(4),
    sub_region_name TEXT,
    intermediate_region_code CHAR(4),
    intermediate_region_name TEXT,
    country_or_area TEXT UNIQUE,
    m49_code CHAR(4) UNIQUE,
    iso_alpha_2_code TEXT,
    iso_alpha_3_code TEXT UNIQUE,                                                            
    PRIMARY KEY (country_or_area, m49_code, iso_alpha_3_code)
);
""")



# THIS IS CREATED TO HANDLE THE DATA THAT ISN'T AS STATIC (LDC, LLDC, SIDS)
# PLEASE NOTE THAT THE DATES ARE YYYY-MM-DD
# DUMMY DATES ADDED AS 2024-01-01



cursor.execute("""
CREATE TABLE IF NOT EXISTS special_status_history_reference (
    country_or_area TEXT,
    m49_code CHAR(3),
    iso_alpha_3_code TEXT,
    least_developed_countries_ldc CHAR(1),
    ldc_status_effective_date DATE,
    land_locked_developing_countries_lldc CHAR(1),
    lldc_status_effective_date DATE,
    small_island_developing_states_sids CHAR(1),     
    sids_status_effective_date DATE,
    PRIMARY KEY (country_or_area, m49_code, iso_alpha_3_code, least_developed_countries_ldc, ldc_status_effective_date, 
                 land_locked_developing_countries_lldc, lldc_status_effective_date, small_island_developing_states_sids, sids_status_effective_date),
    FOREIGN KEY (country_or_area, m49_code, iso_alpha_3_code) REFERENCES country_reference (country_or_area, m49_code, iso_alpha_3_code)
);
""")



# THIS TABLE IS CREATED TO HANDLE THE GLOBAL INDICATOR DEFINITIONS
# THIS TABLE MAY OR MAY NOT BE EDITED AND CHANGED BY ZAINAB.



cursor.execute("""
CREATE TABLE IF NOT EXISTS global_indicator_reference (
    goal_number VARCHAR(10),
    target_number VARCHAR(10),
    indicator_number VARCHAR(10),
    unsd_indicator_codes VARCHAR(10),
    goal_short_title TEXT,
    goal_description TEXT,
    target_description TEXT,
    indicator_description TEXT,
    date_of_adoption DATE,
    PRIMARY KEY (goal_number, target_number, indicator_number, date_of_adoption)
);
""")



# ADD A TABLE TO HANDLE ALL GENERAL COUNTRY STATISTICS, PER INTERNATIONAL SOURCE.
# SOMETHING THAT CAN BE UPDATED IN A BATCH THAT IS FAIRLY WELL UNDERSTOOD.
# GDP, POPULATION, ETC.
# SAVE SPECIFIC TABLES FOR MORE NICHE DATA.



# THIS TABLE WILL RECORD COUNTRY POPULATIONS



cursor.execute("""
CREATE TABLE IF NOT EXISTS population (
    date_of_record DATE,
    iso_alpha_3_code TEXT,
    population INT
);
""")



# THIS TABLE WILL RECORD ECONOMIC DATA



cursor.execute("""
CREATE TABLE IF NOT EXISTS economic_data (
    date_of_record DATE,
    iso_alpha_3_code TEXT,
    gdp BIGINT
);
""")



# THIS TABLE WILL RECORD TRANSPORTATION DATA



cursor.execute("""
CREATE TABLE IF NOT EXISTS transportation_data (
    date_of_record DATE,
    iso_alpha_3_code TEXT,
    registered_vehicles INT
);
""")



# THIS TABLE WILL RECORD HEALTHCARE COVERAGE/ACCESS



cursor.execute("""
CREATE TABLE IF NOT EXISTS healthcare_coverage_data (
    date_of_record DATE,
    iso_alpha_3_code TEXT,
    universal_healthcare CHAR(1) CHECK (universal_healthcare IN ('Y', 'N', 'U')),
    cost_of_healthcare_percent_gdp INT,
    cost_of_healthcare_per_capita INT,
    within_five_miles_of_clinic TEXT
);
""")



# THIS TABLE WILL RECORD DATA ON ILLEGAL ACTIVITIES



cursor.execute("""
CREATE TABLE IF NOT EXISTS illegal_activity_data (
    date_of_record DATE,
    iso_alpha_3_code TEXT
);
""")



# READ THE REFERENCE CSV



unsd_methodology_df = pd.read_csv('un_stat_method/unsd_methodology.csv', sep=';')



# FORMATTING DATA SO THAT THERE ARE NO DECIMAL PLACES



unsd_methodology_df['Global Code'] = pd.to_numeric(unsd_methodology_df['Global Code'], errors='coerce').astype('Int64')
unsd_methodology_df['Region Code'] = pd.to_numeric(unsd_methodology_df['Region Code'], errors='coerce').astype('Int64')
unsd_methodology_df['Sub-region Code'] = pd.to_numeric(unsd_methodology_df['Sub-region Code'], errors='coerce').astype('Int64')
unsd_methodology_df['Intermediate Region Code'] = pd.to_numeric(unsd_methodology_df['Intermediate Region Code'], errors='coerce').astype('Int64')
unsd_methodology_df['M49 Code'] = pd.to_numeric(unsd_methodology_df['M49 Code'], errors='coerce').astype('Int64')



# THIS NEXT LINE OF CODE LIKELY "DOES NOTHING"; IT CHANGES THE NULL TO NONE
# NONE IS THEN CHANGED TO 0 OR DUMMY DATES



unsd_methodology_df = unsd_methodology_df.replace({pd.NA: None})



# DUMMY DATES



unsd_methodology_df['LDC Status Effective Date'] = pd.to_datetime('2024-01-01')
unsd_methodology_df['LLDC Status Effective Date'] = pd.to_datetime('2024-01-01')
unsd_methodology_df['SIDS Status Effective Date'] = pd.to_datetime('2024-01-01')



# NONE TO 0, X TO 1



unsd_methodology_df['Least Developed Countries (LDC)'] = unsd_methodology_df['Least Developed Countries (LDC)'].replace({None: 0, 'x': 1})
unsd_methodology_df['Land Locked Developing Countries (LLDC)'] = unsd_methodology_df['Land Locked Developing Countries (LLDC)'].replace({None: 0, 'x': 1})
unsd_methodology_df['Small Island Developing States (SIDS)'] = unsd_methodology_df['Small Island Developing States (SIDS)'].replace({None: 0, 'x': 1})



# INSERTING INTO SQL



# THIS CODE INSERTS DATA INTO THE COUNTRY REFERENCE TABLE



for index, row in unsd_methodology_df.iterrows():
    cursor.execute("""
                   
        INSERT INTO country_reference (global_code, global_name, region_code, region_name, sub_region_code, sub_region_name,
                                        intermediate_region_code, intermediate_region_name, country_or_area, m49_code,
                                        iso_alpha_2_code, iso_alpha_3_code)
                    
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    
        ON CONFLICT (country_or_area, m49_code, iso_alpha_3_code) DO NOTHING;
    """,
    (row['Global Code'], row['Global Name'], row['Region Code'], row['Region Name'],
     row['Sub-region Code'], row['Sub-region Name'], row['Intermediate Region Code'], row['Intermediate Region Name'],
     row['Country or Area'], row['M49 Code'], row['ISO-alpha2 Code'], row['ISO-alpha3 Code']))



# THIS CODE INSERTS DATA INTO THE SPECIAL STATUS REFERENCE TABLE



for index, row in unsd_methodology_df.iterrows():
    cursor.execute("""
    
        INSERT INTO special_status_history_reference (country_or_area, m49_code, iso_alpha_3_code, least_developed_countries_ldc,
                                            ldc_status_effective_date, land_locked_developing_countries_lldc, 
                                            lldc_status_effective_date, small_island_developing_states_sids,
                                            sids_status_effective_date)

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (country_or_area, m49_code, iso_alpha_3_code, least_developed_countries_ldc, ldc_status_effective_date, 
                    land_locked_developing_countries_lldc, lldc_status_effective_date, small_island_developing_states_sids,
                    sids_status_effective_date) DO NOTHING;
    """,
    
    (row['Country or Area'], row['M49 Code'], row['ISO-alpha3 Code'], row['Least Developed Countries (LDC)'], 
     row['LDC Status Effective Date'], 
     row['Land Locked Developing Countries (LLDC)'], row['LLDC Status Effective Date'],
     row['Small Island Developing States (SIDS)'], row['SIDS Status Effective Date'])

)



# COMMIT TO DATABASE



conn.commit()



# CLOSER CURSOR



cursor.close()



# CLOSE CONNECTION



conn.close()