import kagglehub
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import re
from uszipcode import SearchEngine

#!pip install "sqlalchemy_mate<2.0.0" USE THIS VERSION TO AVOID IMPORT ERRORS FROM USZIPCODE

# CPI data
cpi_data = {
    1913: 9.9, 1914: 10.0, 1915: 10.1, 1916: 10.9, 1917: 12.8, 1918: 15.0, 1919: 17.3, 1920: 20.0,
    1921: 17.9, 1922: 16.8, 1923: 17.1, 1924: 17.1, 1925: 17.5, 1926: 17.7, 1927: 17.4, 1928: 17.2,
    1929: 17.2, 1930:  16.7, 1931: 15.2, 1932: 13.6, 1933: 12.9, 1934: 13.4, 1935: 13.7, 1936: 13.9,
    1937: 14.4, 1938: 14.1, 1939: 13.9, 1940: 14.0, 1941: 14.7, 1942: 16.3, 1943: 17.3, 1944: 17.6,
    1945: 18.0, 1946: 19.5, 1947: 22.3, 1948: 24.0, 1949: 23.8, 1950: 24.1, 1951: 26.0, 1952: 26.6,
    1953: 26.8, 1954: 26.9, 1955: 26.8, 1956: 27.2, 1957: 28.1, 1958: 28.9, 1959: 29.2, 1960: 29.6,
    1961: 29.9, 1962: 30.3, 1963: 30.6, 1964: 31.0, 1965: 31.5, 1966: 32.5, 1967: 33.4, 1968: 34.8,
    1969: 36.7, 1970: 38.8, 1971: 40.5, 1972: 41.8, 1973: 44.4, 1974: 49.3, 1975: 53.8, 1976: 56.9,
    1977: 60.6, 1978: 65.2, 1979: 72.6, 1980: 82.4, 1981: 90.9, 1982: 96.5, 1983: 99.6, 1984: 103.9,
    1985: 107.6, 1986: 109.6, 1987: 113.6, 1988: 118.3, 1989: 124.0, 1990: 130.7, 1991: 136.2,
    1992: 140.3, 1993: 144.5, 1994: 148.2, 1995: 152.4, 1996: 156.9, 1997: 160.5, 1998: 163.0, 1999: 166.6, 
    2000: 172.2, 2001: 177.1, 2002: 179.9, 2003: 184.0, 2004: 188.9, 2005: 195.3, 2006: 201.6, 2007: 207.3, 
    2008: 215.3, 2009: 214.5, 2010: 218.1, 2011: 224.9, 2012: 229.6, 2013: 233.0, 2014: 236.7, 2015: 237.0,
    2016: 240.0, 2017: 245.1, 2018: 251.1, 2019: 255.7, 2020: 258.8, 2021: 270.9,
    2022: 292.0, 2023: 306.8, 2024: 315.6
}

# Download latest version
path = kagglehub.dataset_download("syedanwarafridi/vehicle-sales-data")
path2 = kagglehub.dataset_download("tsaustin/us-used-car-sales-data")
path = path + "/car_prices.csv"
path2 = path2 + "/used_car_sales.csv"


# Load Data
df1 = pd.read_csv(path)
df2 = pd.read_csv(path2)

print("DATA LOADED")

# Extract Year from Sale Date
df1["sale_year"] = df1["saledate"].str.extract(r'(\d{4})').astype(float).astype("Int64")

# Preprocessing

# Drop Columns
df1 = df1.drop(columns=['body', 'transmission', 'vin', 'seller', "saledate"])
df2 = df2.drop(columns=['Engine', 'BodyType', 'NumCylinders', 'DriveType', 'ID'])


# Rename Columns for Merging
df2.rename(columns={
    "pricesold": "sellingprice",
    "Make": "make",
    "Year": "year",
    "Model": "model",
    "Trim": "trim",
    "Mileage": "odometer",
    "yearsold": "sale_year"
}, inplace=True)

# Replace Missing Values
df1 = df1.replace([" ", "NA", "na", "--", "null"], pd.NA)

# Drop Unfillable NA Values
df1 = df1.dropna(subset=['make', 'model', 'trim', 'color', 'interior', 'sale_year'])

# Fill NA Values with Median
df1['condition'] = df1['condition'].fillna(df1['condition'].median())
df1['odometer'] = df1['odometer'].fillna(df1['year'] * 10000) # assume 10000 miles per year 
df1['mmr'] = df1['mmr'].fillna(df1['mmr'].median())

# MALO FILL DF2 MISSING VALUES HERE FROM NOTES ONCE DONE WITH THAT WE CAN UNCOMMENT MERGE DATAFRAMES BELOW
# STATE CORRECTION HERE AS WELL 
search = SearchEngine()
def get_state(zipcode):
    zipcode_str = str(zipcode).strip()

    # Full zipcode: exactly 5 digits
    if re.fullmatch(r'\d{5}', zipcode_str):
        result = search.by_zipcode(zipcode_str)
        if result and result.state:
            return result.state
        else:
            return "Unknown"
    # Partial zipcode: 3 digits followed by two asterisks, e.g., "940**"
    elif re.fullmatch(r'\d{3}\*\*', zipcode_str):
        prefix = zipcode_str[:3]
        # Query for any zipcode that starts with the prefix
        results = search.query(prefix + "*", returns=1)
        if results and results[0].state:
            return results[0].state
        else:
            return "Unknown"
    else:
        # For any other format, return "Unknown"
        return "Unknown"
df2['state'] = df2['zipcode'].apply(get_state)
df2['trim'] = df2['trim'].fillna("Unknown")
# Replace empty strings (or strings with just spaces) with "unknown"
df2.loc[df2['trim'].str.strip() == "", 'trim'] = "Unknown"

# Merge DataFrames
merged_df = pd.concat([df1, df2], ignore_index=True)

# Convert sale_price to 2024 dollars
merged_df["2024_price"] = merged_df["sellingprice"] * (cpi_data[2024] / merged_df["sale_year"].map(cpi_data))


# Summaries
# missing_summary_df1 = pd.DataFrame({
#     "Missing Values": df1.isnull().sum(),
#     "Missing Percentage (%)": (df1.isnull().sum() / len(df1)) * 100
# })
# print(missing_summary_df1)


# missing_summary_df2 = pd.DataFrame({
#     "Missing Values": df2.isnull().sum(),
#     "Missing Percentage (%)": (df2.isnull().sum() / len(df2)) * 100
# })
# print(missing_summary_df2)



# SHAWN FILL IN ROW ADJUSTED INFLATION HERE 


# Convert CPI data to a DataFrame
cpi_df = pd.DataFrame(list(cpi_data.items()), columns=['cpi_year', 'cpi'])
cpi_df['inflation_factor'] = cpi_df['cpi'].apply(lambda x: cpi_data[2024] / x)

# Assign inflation factor for 2024 explicitly
cpi_df.loc[cpi_df['cpi_year'] == 2024, 'inflation_factor'] = 1.0

# Extract the sale year from saledate
# df1['sale_year'] = df1['saledate'].dt.year already done above

# Ensure no duplicate columns exist before merging
if 'inflation_factor' in df1.columns:
    df1 = df1.drop(columns=['inflation_factor'])

# Merge CPI inflation
df1 = df1.merge(cpi_df[['cpi_year', 'inflation_factor']], left_on='sale_year', right_on='cpi_year', how='left')
df1 = df1.drop(columns=['cpi_year'])  # Drop the CPI year

# Step 1: Get unique combinations of year and trim
unique_combinations = df1[['year', 'trim']].drop_duplicates()

# Step 2: Generate 2024 rows for unique combinations
def generate_2024_rows(chunk):
    results = []
    for _, row in chunk.iterrows():
        new_row = row.copy()
        new_row['saledate'] = pd.Timestamp('2024-01-01')  # Set sale date to 2024
        new_row['sale_year'] = 2024  # Set sale year to 2024
        # Use the CPI formula for inflation adjustment
        new_row['sellingprice'] = df1.loc[
            (df1['year'] == row['year']) & (df1['trim'] == row['trim']),
            'sellingprice'
        ].mean() * (cpi_data[2024] / cpi_data[row['year']])
        new_row['inflation_factor'] = 1.0  # Inflation factor for 2024 is 1
        results.append(new_row)
    return pd.DataFrame(results)

# Step 3: Process unique combinations with multiprocessing
def chunkify(dataframe, n_chunks):
    chunk_size = int(np.ceil(len(dataframe) / n_chunks))
    return [dataframe.iloc[i:i + chunk_size] for i in range(0, len(dataframe), chunk_size)]

if __name__ == '__main__':
    num_cores = min(cpu_count(), 4)  # Use up to 4 cores
    chunks = chunkify(unique_combinations, num_cores)  # Split unique combinations into chunks

    with Pool(num_cores) as pool:
        results = pool.map(generate_2024_rows, chunks)

    # Combine results from all processes
    generated_rows_df = pd.concat(results, ignore_index=True)

    # Combine the generated rows
    extended_df = pd.concat([df1, generated_rows_df], ignore_index=True)

    # Format the saledate
    extended_df['saledate'] = pd.to_datetime(extended_df['saledate']).dt.strftime('%m/%d/%Y')







