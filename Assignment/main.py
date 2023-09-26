# Importing all the necessary  libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setting up chrome driver

driver = webdriver.Chrome()

# Calling chrome driver for the link

driver.get('http://www.sunsirs.com/futures-price-daily.html')
driver.maximize_window()
time.sleep(2)
table = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div[4]/table")

# Extracting data from the table

data = []
rows = table.find_elements(By.TAG_NAME, "tr")
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")

    # Getting  data from each cell

    commodity = cells[0].text
    Sectors = cells[1].text
    Yesterday_Price = cells[2].text
    Today_Price = cells[3].text
    Change = cells[4].text


    # Adding data to a list

    data.append({

        "commodity": commodity,
        "sectors": Sectors,
        "Yesterday_Price": Yesterday_Price,
        "Today_Price": Today_Price,
        "Change": Change,

    })

# Creating a data frame using pandas

df = pd.DataFrame(data)

# Closing the driver

driver.quit()

# Counting total number of rows in the table

total_rows = df.shape[0]
print('')
print('Total number of rows in the table  = ', total_rows)
print('')

# Creating an Excel file and transferring data to it (Please make sure to close Excel file before running the program)

df.to_excel("Raw_Data.xlsx", sheet_name="Raw Data")

# Data correction steps needed to analyze the data

df['Today_Price'] = df['Today_Price'].str.replace(',', '')
df['Today_Price'] = pd.to_numeric(df['Today_Price'])

# Finding the commodity with the highest daily price

highest_price = df["Today_Price"].max()
commodity_with_highest_price = df[df["Today_Price"] == highest_price]["commodity"].iloc[0]

# Printing the results

if len(commodity_with_highest_price) == 0:
    commodity_with_highest_price = "(Name not provided in the table)"
print("Commodity with highest daily closing price:", commodity_with_highest_price)
print("Corresponding price:", highest_price)

# Extra: finding the second highest also

temp = df['Today_Price'].nlargest(2).iloc[1]
second_highest_price = temp
commodity_with_2highest_price = df[df["Today_Price"] == temp]["commodity"].iloc[0]

# Printing the result of 2nd highest

print("")
print("Commodity with 2nd highest daily closing price:", commodity_with_2highest_price)
print("Corresponding price:", second_highest_price)


"""
SAMPLE OUTPUT

Total number of rows in the table  =  53

Commodity with highest daily closing price: (Name not provided in the table)
Corresponding price: 153000.0

Commodity with 2nd highest daily closing price: Copper
Corresponding price: 67510.0

"""