import requests
import re
import logging
from bs4 import BeautifulSoup
from pandas import DataFrame
from .utils import str_


def get_weather_statis(city="singapore", temp_fmt="celsius"):
    ZIP_CODE = {
        "singapore": "SNXX0006",
    }
    origin_url = "https://weather.com/weather/tenday/l"
    unit = "m" if temp_fmt == "celsius" else "e"
    url = f"{origin_url}/{ZIP_CODE[city]}?unit={unit}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logging.error(f'Get weather error:\n{e}')
        raise(e)
    return soup


def get_temp(daily_statis):
    """
    Get temperature of a day.
    Return: Day temperature, Nigh temperature
    """
    attrs = {
        "data-testid": "TemperatureValue",
        "class": re.compile("^DailyContent--temp.*"),
    }
    temps = daily_statis.find_all("span", attrs=attrs)
    if len(temps) == 1:
        return '-', temps[0].text.strip('°')
    elif len(temps) ==2:
        return temps[0].text.strip('°'), temps[1].text.strip('°')
    else:
        e = 'Has a problem when parsing Temperature'
        logging.error(e)
        raise RuntimeError(e)


def get_humidity(daily_statis):
    """
    Get humidity of a day.
    Return: Day humidity, Nigh humidity
    """
    humidity_sections = daily_statis.find_all("li", attrs={"data-testid": "HumiditySection"})
    if len(humidity_sections) == 1:
        return '-', humidity_sections[0].find("span", attrs={"data-testid": "PercentageValue"}).text
    elif len(humidity_sections) ==2:
        munidity_day = humidity_sections[0].find("span", attrs={"data-testid": "PercentageValue"}).text
        munidity_night = humidity_sections[0].find("span", attrs={"data-testid": "PercentageValue"}).text
        return munidity_day, munidity_night
    else:
        e = 'Has a problem when parsing Humidity'
        logging.error(e)
        raise RuntimeError(e)


def get_weather(city="singapore", temp_fmt="celsius"):
    """
    Get weather (temperature in Celsius or Fahrenheit, humidity) of a city
    Return: a dataframe
    """
    soup = get_weather_statis(city, temp_fmt)
    statis_daily = soup.find_all('details', class_=re.compile("^DaypartDetails--DayPartDetail.+"))
    date = list()
    temp_day = list()
    temp_night = list()
    humi_day = list()
    humi_night = list()
    for statis in statis_daily:
        date.append(statis.find('span', class_=re.compile("^DailyContent--daypartDate.+")).text)
        temp_d, temp_n = get_temp(statis)
        temp_day.append(temp_d)
        temp_night.append(temp_n)
        humi_d, humi_n = get_humidity(statis)
        humi_day.append(humi_d)
        humi_night.append(humi_n)
    if temp_fmt == 'celsius':
        df = DataFrame({
            'DATE': date,
            'DAY_TEMPERATURE_(C)': temp_day,
            'NIGHT_TEMPERATURE_(C)': temp_night,
            'DAY_HUMIDITY': humi_day,
            'NIGHT_HUMIDITY': humi_night
        })
    else:
        df = DataFrame({
            'DATE': date,
            'DAY_TEMPERATURE_(F)': temp_day,
            'NIGHT_TEMPERATURE_(F)': temp_night,
            'DAY_HUMIDITY': humi_day,
            'NIGHT_HUMIDITY': humi_night
        })
    return df


def get_weather_in_celsius_and_fahrenheit(city='singapore'):
    """
    Get weather of a city with temperature in Celsius and in Fahrenheit
    Return: dataframe of temperature in Celsius, dataframe of temperature in fahrenheit
    Note: It will retry to get weather again automaticaly in cases:
        - DATE mismatch (it can happen when get weather in Celsius before 00:00 and get weather in Fahrenheit after 00:00)
        - Time to get weather is mid-day, before mid-day you can get weather for today with both Day Temperature and Night Temperature,
          but after mid-day you can get weather for today with Night Temperature only.
    """
    df_c = get_weather(city, "celsius")
    df_f = get_weather(city, "fahrenheit")
    if df_c['DATE'][0] != df_f['DATE'][0] or \
        df_c['DAY_TEMPERATURE_(C)'][0] == '-' != df_f['DAY_TEMPERATURE_(F)'][0]:
        # Retry to get weather again
        df_c = get_weather(city, "celsius")
    logging.debug(f'weather in Celsius:\n{str_(df_c)}')
    logging.debug(f'weather in Fahrenheit:\n{str_(df_f)}')
    return df_c, df_f


def convert_celsius_to_fahrenheit(table):
    """
    Convert temperature in Celsius to temperature in Fahrenheit
        Fahrenheit = Celsius * 9/5 + 32
    Return a dataframe that inculde both temperature in Celsius and temperature in Fahrenheit (after convert)
    """
    def celsius_to_fahrenheit(celsius):
        if celsius == '-':
            return '-'
        fahrenheit = int(celsius)* 9 / 5 + 32
        return str(round(fahrenheit))

    table['DAY_TEMPERATURE_(F)'] = table['DAY_TEMPERATURE_(C)'].apply(celsius_to_fahrenheit)
    table['NIGHT_TEMPERATURE_(F)'] = table['NIGHT_TEMPERATURE_(C)'].apply(celsius_to_fahrenheit)
    col_order = ['DATE', 'DAY_TEMPERATURE_(C)', 'NIGHT_TEMPERATURE_(C)',
                'DAY_TEMPERATURE_(F)', 'NIGHT_TEMPERATURE_(F)', 'DAY_HUMIDITY', 'NIGHT_HUMIDITY']
    table = table.reindex(columns=col_order)
    logging.debug(f'values table after convert Celsius to Fahrenheit:\n{str_(table)}')
    return table
