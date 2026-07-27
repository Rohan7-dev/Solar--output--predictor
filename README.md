# Solar Smart: Engineering & ROI ☀️

A Streamlit web app that estimates real-time solar PV output for any city and 
translates it into financial savings — combining live weather data with 
photovoltaic engineering fundamentals (temperature derating, irradiance loss) 
rather than just a flat capacity estimate.

## Why I Built This

As an EEE student interested in energy systems, I wanted to move beyond the 
textbook assumption that a solar panel always produces its "rated" output. 
In reality, panel output depends heavily on ambient temperature and cloud 
cover — this project models that gap and shows the user exactly how much 
power (and money) is lost to real-world conditions versus lab conditions.

## What It Does

Given a city, system size (kW), monthly electricity usage, and tariff rate, 
the app:

- Fetches live weather data (temperature, cloud cover) for the location via 
  the OpenWeatherMap API
- Calculates **actual power output** by applying two efficiency losses to 
  the rated panel capacity:
  - **Thermal derating** — panels lose ~0.5% efficiency per °C above 25°C 
    (standard test condition temperature)
  - **Cloud/irradiance loss** — up to 80% output loss under full cloud cover
- Estimates daily/monthly energy production (using a 5 peak-sun-hour 
  assumption)
- Compares the user's current electricity bill against their projected bill 
  with solar, and shows estimated monthly savings

## Tech Stack

- **Streamlit** — web app framework and UI
- **OpenWeatherMap API** — live temperature & cloud cover data
- **Pandas** — data handling for charts
- **Altair** — interactive visualizations (power comparison, bill comparison)

## Engineering Logic  
cloud_efficiency = 1 - (cloud_cover% / 100 × 0.8)
heat_loss = max(0, (temp°C - 25) × 0.005)
actual_power = rated_power × cloud_efficiency × (1 - heat_loss)


