import datetime
import sys
import altair as alt
import pandas as pd
import requests
import requests_cache

requests_cache.install_cache()

LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}



def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Arguments:
        - date (datatime.date) : Date that will be given in the API-request, defaults to todays date.
        - location (str) : One of the five electricity regions in Norway. Defaults to Oslo (East-Norway)

    Returns:
        - df (pd.DataFrame) : Pandas DataFrame containing the electricity pricing for all hours in the given day.
    """
    if date is None:
        date = datetime.date.today()

    day = date.day
    if day < 10:
        day = f"0{day}"
    
    month = date.month
    if month < 10:
        month = f"0{month}"

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
    r = requests.get(url)
    
    df = pd.DataFrame(r.json(), columns=["NOK_per_kWh", "time_start"])
    df["time_start"] = pd.to_datetime(df["time_start"])

    return df



def fetch_all_areas(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Arguments:
        - end_date (datatime.date) : The last date the API will be requested for.
        - days (int) : How many days leading up to end_Date the API will be requested for.
        - locations (tuple) : The key-values in the LOCATION-CODES dictionary.

    Returns:
        - df (pd.DataFrame) : A combined dataframe of all the dates and locations.
    """
    if end_date is None:
        end_date = datetime.date.today()

    df_list = []
    for i in range(days):
        for j in range(len(locations)):
            date = end_date - datetime.timedelta(days=i)
            temp = fetch_day_prices(date, locations[j])
            temp["location_code"] = locations[j]
            temp["location"] = LOCATION_CODES[locations[j]]
            df_list.append(temp)

    df = pd.concat(df_list, ignore_index=True)

    return df



def fetch_single_area(
    end_date: datetime.date = None,
    days: int = 7,
    location: str = "NO1",
) -> pd.DataFrame:
    """Fetch prices for multiple days for a single location into a single DataFrame

    Arguments:
        - end_date (datatime.date) : The last date the API will be requested for.
        - days (int) : How many days leading up to end_Date the API will be requested for.
        - locations (str) : ....

    Returns:
        - df (pd.DataFrame) : ...
    """
    if end_date is None:
        end_date = datetime.date.today()

    df_list = []
    for i in range(days):
        date = end_date - datetime.timedelta(days=i)
        temp = fetch_day_prices(date, location)
        temp["location_code"] = location
        temp["location"] = LOCATION_CODES[location]
        df_list.append(temp)

    df = pd.concat(df_list, ignore_index=True)

    return df



def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Arguments:
        - df (pd.DataFrame) : The DataFrame that is going to be visualized in a line plot.

    Returns:
        - chart (alt.Chart) : The chart/line plot.
    """
    chart = alt.Chart(df).mark_line().encode(
        x="time_start:T",
        y="NOK_per_kWh",
        color="location"
    ).properties(
        title="Electricity prices"
    ).interactive()

    return chart



if __name__ == "__main__":
    if len(sys.argv) == 1:
        df = fetch_all_areas()
    else:
        df = fetch_single_area(location=sys.argv[1])
    chart = plot_prices(df)
    chart.show()