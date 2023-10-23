import unittest
import logging
from library import get_weather_in_celsius_and_fahrenheit, convert_celsius_to_fahrenheit, compare_table


class WeatherTest(unittest.TestCase):

    def test_temperature(self):
        logging.info('[Step 1]: Get weather in Singapore in Celsius and Fahrenheit format')
        weather_c, weather_f = get_weather_in_celsius_and_fahrenheit()

        logging.info('[Step 2]: Convert temperature from Celsius format to Fahrenheit format')
        weather_c = convert_celsius_to_fahrenheit(weather_c)

        logging.info('[Step 3]: Validate temperature in Fahrenheit  with temperature in Celsius')
        columns = ['DATE', 'DAY_TEMPERATURE_(F)', 'NIGHT_TEMPERATURE_(F)']
        compare_table(columns, weather_f, weather_c)


if __name__ == '__main__':
    unittest.main()
