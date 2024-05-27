import datetime
from typing import List, Optional
import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    LOCATION_CODES,
    fetch_day_prices,
    fetch_all_areas,
    fetch_single_area,
    plot_prices
)

app = FastAPI()
templates = Jinja2Templates(directory="template")



@app.get("/")
def render_html_template(request: Request):
    #Render the html template
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "location_codes": LOCATION_CODES.keys(),
            "today": str(datetime.date.today())
        }
    )



@app.get("/plot_prices.json")
def strompris_json(
    locations: Optional[List[str]] = Query(default=list(LOCATION_CODES.keys())),
    end: Optional[datetime.date] = None,
    days: Optional[int] = 7
    ):
    df = fetch_all_areas(locations=locations, end_date=end, days=days)
    chart = plot_prices(df)
    return chart.to_dict()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=5000)