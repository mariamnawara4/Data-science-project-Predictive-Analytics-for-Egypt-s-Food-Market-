
import pandas as pd
import glob
import os
import re
all_data =[]

# --- 1. FIND FILES ---
files = glob.glob("prices files/*.xlsx")
print(f"Found {len(files)} files.")

for file_path in files:
    filename = os.path.basename(file_path)
    
    # --- 2. EXTRACT DATE FROM FILENAME ---
    numbers = re.findall(r'\d+', filename)
    year_str = [n for n in numbers if len(n) == 4][0]
    year = int(year_str)
    month_str =[n for n in numbers if n != year_str and 1 <= int(n) <= 12][0]
    month = int(month_str)
    current_date = f"{year}-{month:02d}-01"  

    # --- 3. READ EXCEL ---
    xl = pd.ExcelFile(file_path)
    target_sheet = 0 
    for sheet_name in xl.sheet_names:
        if 'Table' in sheet_name or 'جدول' in sheet_name:
            target_sheet = sheet_name
            break
    df = pd.read_excel(file_path, sheet_name=target_sheet, header=3)
    

    # --- 4. EXTRACT DATA ---
    price_col_index = 3 
    name_col_index = 7 
    unit_col=1



    # Loop through EVERY row in the Excel sheet
    for index, row in df.iterrows():
        product_name = str(row.iloc[name_col_index]).strip()
        price = row.iloc[price_col_index]
        unit = str(row.iloc[unit_col]).strip()

        # Skip rows that don't have a price or don't have a name (like empty spaces or headers)
        if pd.isna(price) or product_name.lower() in ['nan', '', 'none']:
            continue

            
        all_data.append({
            'Date': current_date,
            'Product': product_name,
            'Price': price,
            'unit': unit,
            'Source_File': filename
        })


df_final = pd.DataFrame(all_data)
df_final = df_final.sort_values(by=['Date', 'Product'])


df_final.to_csv("2021-2026.csv", index=False)
print(f"\nExtracted {len(df_final)} rows.")
print(df_final.head())
print("-" * 40)


unique_products = df_final['Product'].unique()
print(f"\nTotal unique products found: {len(unique_products)}")
print(unique_products)
print("-" * 40)



# Found 61 files.

# Extracted 3793 rows.
#           Date             Product   Price         unit                                        Source_File
# 59  2021-01-01         Apricot Jam   11.78  340جم/ gram  Average Consumer Prices for Key Food Items _ 1...
# 60  2021-01-01  Black Pepper Grain   88.86     كجم/ k.g  Average Consumer Prices for Key Food Items _ 1...
# 2   2021-01-01         Broad Beans   31.26     كجم/ k.g  Average Consumer Prices for Key Food Items _ 1...
# 43  2021-01-01      Buffalo Butter  101.41  850جم/ gram  Average Consumer Prices for Key Food Items _ 1...
# 35  2021-01-01            Catefish   18.54     كجم/ k.g  Average Consumer Prices for Key Food Items _ 1...
# ----------------------------------------

# Total unique products found: 80
# ['Apricot Jam' 'Black Pepper Grain' 'Broad Beans' 'Buffalo Butter'
#  'Catefish' 'Citrus' 'Commodity' 'Corindar' 'Corn Oil' 'Cotton Seed Oil'
#  'Crushed Beans' 'Crushed Lentil' 'Cumin' 'Domestic Chicken'
#  'Domestic Duck' 'Domestic frozen slaughtered white chicken' 'Dry Beans'
#  'Eggplant' 'Farm Cheese' 'Farm Chicken' 'Fresh Milk'
#  'Frozen Macaroni fish' 'Frozen Macrill fish' 'Garlic' 'Green Beans'
#  'Green Papper' 'Guava' 'Imported frozen buffalo meat' 'Lentil' 'Mandarin'
#  'Medium size Cabbag' 'Medium size Cucumber' 'Medium size Pidgeon'
#  'Medium size farm Egg' 'Middle age buffalo & cattle (net meat)'
#  'Mullet Fish' 'Navel Oranges' 'Nesto Cheese' 'Normal Wheat'
#  'Old Roumi Cheese' 'Onion' 'Pack of Tea' 'Packed Honey' 'Packed Sugar'
#  'Packed White Rice' 'Potato' 'Sheep meat with bones' 'Small size Banana'
#  'Small size Squash' 'Stored Full Crème White Cheese' 'Sun Flower Oil'
#  'Tilapia Fish' 'Tomato' 'Unpacked Buffalo butter' 'Unpacked Halva'
#  'Unpacked Imported Cattle’s Butter' 'Unpacked Molasses' 'Unpacked Pasta'
#  'Unpacked Rice' 'Unpacked Tahina' 'Unpacked Wheat Flour 72%'
#  'Yellow Currot without leaps' 'Young age buffalo with bones'
#  'Green Pepper' 'Strawbrry' 'Seed Oranges' 'Romans' 'Cantaloupe'
#  'Watermelon Shillian 6 K' 'Zagloul Dates' 'Watermelon Shilian 6 k' 'Fig'
#  'mandarin' 'Middle age buffalo & cattle               (net meat)'
#  'Strawberry' 'Figs' 'Medium  size farm Egg' 'Pomegranate'
#  'Middle age buffalo & cattle(net meat)' 'Pome granate']
# ----------------------------------------