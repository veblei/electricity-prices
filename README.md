# Norway Electricity Prices

Python program that compares the electricity prices (NOK_per_kWh) for the five price areas in Norway over the last week.

Download dependecies with `pip install -r requirements.txt`.

Run program with `python3 main.py`.

Fetches prices from [Strømpris API](https://www.hvakosterstrommen.no/strompris-api) with *requests*. Combines day prices for the different areas into a single *pandas* dataframe. Visualizes the dataframe with *altair* in a line plot.

<img src="visualization.png"/>