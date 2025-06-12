#!pip install yfinance
#!pip install bs4
#!pip install nbformat (You're working with Jupyter notebooks )
#!pip install --upgrade plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Graphing Function
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
            y=stock_data_specific.Close.astype("float"),
            name="Share Price"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
            y=revenue_data_specific.Revenue.astype("float"),
            name="Revenue"
        ),
        row=2, col=1
    )

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    # Show the plot
    fig.show()
    fig.write_html("tesla_graph.html", auto_open=True)

    
#Question 1: Use yfinance to Extract Stock Data (Using the Ticker function enter the ticker symbol 
# of the stock we want to extract data on to create a ticker object. 
# The stock is Tesla and its ticker symbol is TSLA.)
    
tesla =yf.Ticker("TSLA")


#Question 2: Using the ticker object and the function `history` extract stock information and save it in a dataframe 
# named `tesla_data`. Set the `period` parameter to ` "max" ` so we get information for the maximum amount
# of time.
tesla_data = tesla.history(period="max")
print("Tesla Historical Share Price Data:")
print(tesla_data)
print("**************************************************")

#Question 2: Reset the index to turn 'Date' into a column
tesla_data.reset_index(inplace=True)
print("Data after reseting the index:")
print(tesla_data)
print("**************************************************")

# Question 3: Display the first five rows
print("Display the first five rows:")
print(tesla_data.head())
print("**************************************************")

#Question 4: Use Webscraping to Extract Tesla Revenue Data(Use the requests library to download the webpage
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm 
# Save the text of the response as a variable named html_data and print.)
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data =requests.get(url).text
print(f"Html Data by webscrapping:{html_data}")
print("**************************************************")


#Question 5: Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
soup = BeautifulSoup(html_data,"html5")
title =soup.title.text
print(f"The title is : {title}")
print("**************************************************")

# Question 6: Using BeautifulSoup  extract the table with Tesla Revenue
# and store it into a dataframe named tesla_revenue. 
# The dataframe should have columns Date and Revenue.

#1. create an empty data frame using the pd.DataFrame() 
tesla_revenue=pd.DataFrame(columns=["Date" , "Revenue"])
print(f"The newly created DataFrame is: {tesla_revenue}")

#2.!!!!!using BeautifulSoup to extract  rows from the table "Tesla Quarterly Revenue" from the web page.
rows=soup.find_all("tbody")[1].find_all("tr")

#3. extracting data from an HTML table row-by-row and storing each value 
for row in rows:
    col=row.find_all("td")
    date=col[0].text    
    revenue=col[1].text  
    #4. Appending each extracted row to the main DataFrame and ensure that the index is continuous 
    # and doesn't carry over from the original DataFrame.
    tesla_revenue= pd.concat([tesla_revenue,pd.DataFrame({"Date": [date], "Revenue": [revenue]})], ignore_index=True)
print("Tesla Revenue Table:")
print(tesla_revenue)
print("**************************************************")

#Question 7: print out the data frame using the head()
print("Tesla Quaterly Revenue(From the first 5 rows:")
print(tesla_revenue.head())
print("**************************************************")

#Question 8: removes commas , and dollar signs $ from the 'Revenue' column in your tesla_revenu
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "") 

#Question 9:remove an null or empty strings in the Revenue column.
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Question 10: Display the last 5 rows of the tesla_revenue DataFrame
print("Tesla Quarterly Revenue (Last 5 rows):")
print(tesla_revenue.tail())

#Use the make_graph function to graph the Tesla Stock Data
make_graph(tesla_data,tesla_revenue,'Tesla')