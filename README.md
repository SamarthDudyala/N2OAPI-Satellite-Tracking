# N2OAPI-Satellite-Tracking
Satellite Tracker with N2YO API

This Python script allows you to track satellites above any city worldwide using the N2YO API.  
You can view satellite details, total satellites overhead within a 15 km radius, and get the next visible pass times converted to Indian Standard Time (IST).

---

## Features

- Input a city name to get its latitude and longitude.
- List total satellites above the city within a 15 km radius.
- Display names and NORAD IDs of satellites overhead.
- Input a satellite's NORAD ID to:
  - View its TLE (Two-Line Element) data.
  - See the next visible pass time in IST.
- Display next visible pass time of the ISS (International Space Station) over the city.

---

## Requirements

- Python 3.x
- [N2YO API key](https://www.n2yo.com/api/) (free registration required)
- Python packages:
  - `requests`
  - `geopy`
  - `pytz`

Install the required packages using:

```bash
pip install requests geopy pytz
