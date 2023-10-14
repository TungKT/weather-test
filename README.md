# Weather Test

---

## Introduction

Weather Test is a tool that get weather (temperature in Celsius and in Fahrenheit, Humidity) of Singapre
in website weather.com for Day and Night under 10 days tab then validate values by compare temperature in Celsius and in Fahrenheit

This tool was developed base on python unittest framework.


### Requirements

python 3.X later  
pandas=1.3.5  
requests==2.28.2  
beautifulsoup4==4.9.3  
tabulate==0.9.0  


### Installation

[Git Clone]  

    git clone ssh://git@git.dasannetworks.com:7999/ysuite/dal.git  
    cd weather_test  
    pip install -r requirements.txt  


### Code Structure

    weather_test/
    ├── library
    │   ├── __init__.py
    │   ├── get_weather.py
    │   └── utils.py
    ├── suites
    |   ├── __init__.py
    |   └── weather_test.py
    ├── result
    │   ├── detail_test.log
    │   └── report_summary.txt 
    ├── .gitignore
    ├── runtest.py
    ├── README.md
    └── requirements.txt

### How to use

$ python runtest.py --help
usage: runtest.py [-h] --interval INTERVAL --duration DURATION  

Using for run weather test multiple times with interval and duration time  

optional arguments:  
  -h, --help           show this help message and exit  
  --interval INTERVAL  interval time to run test (unit: second)  
  --duration DURATION  duration time to run test (unit: second)  

$ python runtest.py --interval <INTERVAL_TIME> --duration <DURATION>  
It will excute test weather of Singapore every <INTERVAL_TIME> seconds in <DURATION> seconds.  
After run test, result will be saved in file ./result/detail_test.log and summary result will be save in file ./result/report_summary.txt.  

For example:  
    python runtest.py --interval 3600 --duration 86400  
    # it will execute test weather of Singapore every 1 hour in a day  
