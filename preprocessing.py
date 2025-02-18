import kagglehub
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

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
df2 = df2.replace([" ", "NA", "na", "--", "null"], pd.NA)

# Drop Unfillable NA Values
df1 = df1.dropna(subset=['make', 'model', 'trim', 'color', 'interior', 'sale_year'])
df2 = df2.dropna(subset=['make', 'model', 'trim', 'sale_year', 'zipcode'])

# Fill NA Values with Median
df1['condition'] = df1['condition'].fillna(df1['condition'].median())
df1['odometer'] = df1['odometer'].fillna(df1['odometer'].median())
df1['mmr'] = df1['mmr'].fillna(df1['mmr'].median())

# Merge DataFrames
# merged_df = pd.concat([df1, df2], ignore_index=True)

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

# Ensure saledate is a datetime object


# CPI data
cpi_data = {
    1980: 82.4, 1981: 90.9, 1982: 96.5, 1983: 99.6, 1984: 103.9, 1985: 107.6,
    1986: 109.6, 1987: 113.6, 1988: 118.3, 1989: 124.0, 1990: 130.7, 1991: 136.2,
    1992: 140.3, 1993: 144.5, 1994: 148.2, 1995: 152.4, 1996: 156.9, 1997: 160.5,
    1998: 163.0, 1999: 166.6, 2000: 172.2, 2001: 177.1, 2002: 179.9, 2003: 184.0,
    2004: 188.9, 2005: 195.3, 2006: 201.6, 2007: 207.3, 2008: 215.3, 2009: 214.5,
    2010: 218.1, 2011: 224.9, 2012: 229.6, 2013: 233.0, 2014: 236.7, 2015: 237.0,
    2016: 240.0, 2017: 245.1, 2018: 251.1, 2019: 255.7, 2020: 258.8, 2021: 270.9,
    2022: 292.0, 2023: 306.8, 2024: 315.6
}

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








