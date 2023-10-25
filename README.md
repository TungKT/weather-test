# Weather Test

---

## Introduction

Weather Test is a tool that get weather (temperature in Celsius and in Fahrenheit, Humidity) of Singapre
in website weather.com for Day and Night under 10 days tab then validate values by compare temperature in Celsius and in Fahrenheit

This tool was developed base on python unittest framework.


### Requirements

python 3.X later  
pandas==1.3.5  
requests==2.28.2  
beautifulsoup4==4.9.3  
tabulate==0.9.0  


### Installation

option 1: [Git Clone]  

    git clone https://github.com/TungKT/weather-test.git  
    cd weather-test  
    pip install . 

option 2: [install directly]  

    pip install git+https://github.com/TungKT/weather-test.git@v2.0.0  

### Code Structure

    weather_test/
    ├── library
    │   ├── __init__.py
    │   ├── get_weather.py
    │   └── utils.py
    ├── suites
    |   ├── __init__.py
    |   └── weather_test.py
    ├── .gitignore
    ├── runtest.py
    ├── README.md
    └── setup.py

### How to use

    $ run-weather-test -h

    usage: run-weather-test [-h] --interval INTERVAL --duration DURATION
                            [-d OUTPUT_DIR]
    Using for run weather test multiple times with interval and duration time

    optional arguments:
    -h, --help            show this help message and exit
    --interval INTERVAL   interval time to run test (unit: second)
    --duration DURATION   duration time to run test (unit: second)
    -d OUTPUT_DIR, --output_dir OUTPUT_DIR
                            output directory where to save test log, default is
                            "./result/"  

    $ run-weather-test --interval INTERVAL_TIME --duration DURATION_TIME
    It will excute test weather of Singapore every INTERVAL_TIME seconds in DURATION_TIME seconds.
    After run test, result will be saved in file OUTPUT_DIR/detail_test.log and summary result will be save in file OUTPUT_DIR/report_summary.txt.  

    For example:
        run-weather-test --interval 3600 --duration 86400
        # it will execute test weather of Singapore every 1 hour in a day
