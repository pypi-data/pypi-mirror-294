import requests
import argparse
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

def get_geolocation():
    try:
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        return f"{data['city']}, {data['region']}, {data['country_name']}"
    except:
        return "Philadelphia, Pennsylvania, United States"  # Default fallback

def get_weather(location):
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url)
    return response.json()

def weather_icon(condition):
    icons = {
        "Sunny": "☀️ ", "Clear": "🌙", "Partly cloudy": "⛅",
        "Cloudy": "☁️ ", "Overcast": "☁️ ", "Mist": "🌫️ ",
        "Patchy rain nearby": "🌦️ ", "Patchy light drizzle": "🌧️ ",
        "Light drizzle": "🌧️ ", "Patchy light rain": "🌧️ ",
        "Light rain": "🌧️ ", "Moderate rain at times": "🌧️ ",
        "Moderate rain": "🌧️ ", "Heavy rain at times": "🌧️ ",
        "Heavy rain": "🌧️ ", "Light freezing rain": "🌨️ ",
        "Moderate or heavy freezing rain": "🌨️ ", "Light snow": "🌨️ ",
        "Moderate snow": "🌨️ ", "Heavy snow": "🌨️ ",
        "Patchy moderate snow": "🌨️ ", "Patchy heavy snow": "🌨️ ",
        "Thundery outbreaks possible": "⛈️ ",
    }
    return icons.get(condition, "❓")

def get_ascii_art(condition):
    sunny = """
    \\   /
     .-.
  ― (   ) ―
     `-'
    /   \\
    """
    
    partly_cloudy = """
   \\  /
 _ /"".-.
   \\_(   ).
   /(___(__) 
    """
    
    cloudy = """
      .--.
   .-(    ).
  (___.__)__)
    """
    
    rainy = """
     .-.
    (   ).
   (___(__)
    ' ' ' '
   ' ' ' '
    """
    
    snowy = """
     .-.
    (   ).
   (___(__)
    *  *  *
   *  *  *
    """
    
    thundery = """
     .-.
    (   ).
   (___(__)
    ⚡'⚡'⚡
   ⚡'⚡'⚡
    """
    
    condition = condition.lower()
    if "sun" in condition or "clear" in condition:
        return sunny
    elif "partly cloudy" in condition:
        return partly_cloudy
    elif "cloud" in condition or "overcast" in condition:
        return cloudy
    elif "rain" in condition or "drizzle" in condition:
        return rainy
    elif "snow" in condition:
        return snowy
    elif "thunder" in condition:
        return thundery
    else:
        return sunny  # default to sunny if condition is not recognized

def create_weather_panel(data):
    current = data['current_condition'][0]
    weather_desc = current['weatherDesc'][0]['value']
    ascii_art = get_ascii_art(weather_desc)
    
    temp = f"Temperature: {current['temp_F']}°F"
    feels_like = f"Feels like: {current['FeelsLikeF']}°F"
    wind = f"Wind: ← {current['windspeedMiles']} mph"
    visibility = f"Visibility: {current['visibility']} mi"
    precip = f"Precipitation: {current['precipInches']} in"
   
    content = f"{ascii_art}\n{weather_desc}\n\n{temp}\n{feels_like}\n{wind}\n{visibility}\n{precip}"
    return Panel(Align.center(content), title="Current Weather", expand=False, border_style="bold")

def create_forecast_table(forecasts):
    table = Table(title="3-Day Forecast", show_header=True, header_style="bold magenta")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Time", style="cyan")
    table.add_column("Weather", style="green")
    table.add_column("Temp", justify="right", style="yellow")
    table.add_column("Wind", justify="right", style="red")
    table.add_column("Precip", justify="right", style="blue")

    for day in forecasts[:3]:  # Display 3 days
        date = datetime.strptime(day['date'], "%Y-%m-%d")
        for period, time in [('Morning', '600'), ('Noon', '1200'), ('Evening', '1800'), ('Night', '0')]:
            hourly = next(h for h in day['hourly'] if h['time'] == time)
            weather_desc = hourly['weatherDesc'][0]['value']
            icon = weather_icon(weather_desc)
            temp = f"{hourly['tempF']}°F ({hourly['FeelsLikeF']}°F)"
            wind = f"← {hourly['windspeedMiles']}-{int(hourly['windspeedMiles']) + 2} mph"
            precip = f"{hourly['precipInches']} in ({hourly['chanceofrain']}%)"
           
            table.add_row(
                date.strftime('%a %d %b') if period == 'Morning' else "",
                period,
                Text(f"{icon} {weather_desc}"),
                temp,
                wind,
                precip
            )

    return table

def display_weather(data):
    console = Console()
    location = f"{data['nearest_area'][0]['areaName'][0]['value']}, {data['nearest_area'][0]['region'][0]['value']}, {data['nearest_area'][0]['country'][0]['value']}"
   
    console.print(f"[bold blue]Weather report for {location}[/bold blue]")
    console.print(create_weather_panel(data))
    console.print(create_forecast_table(data['weather']))

def main():
    parser = argparse.ArgumentParser(description="Get weather information for a location.")
    parser.add_argument("--location", nargs='+', help="Location for weather information")
    args = parser.parse_args()

    if args.location:
        location = " ".join(args.location)
    else:
        location = get_geolocation()
        print(f"No location provided. Using geolocation: {location}")

    weather_data = get_weather(location)
    display_weather(weather_data)

if __name__ == "__main__":
    main()