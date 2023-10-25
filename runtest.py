import unittest
import time
import datetime
import logging
import argparse
import os
from pandas import DataFrame
from library import str_


def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def config_logging(output_dir):
    """
    Config logging to print output to console and log file
    """
    # Create the logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Create a FileHandler
    make_dir(output_dir)
    output_log = os.path.join(output_dir, 'detail_test.log')
    file_handler = logging.FileHandler(output_log, 'w+')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


def make_summary_report(results, start_time, stop_time, output_dir):
    """
    Make summary report and save it in file report_summary
    """
    # config logger to save report to a new file
    output_log_summary = os.path.join(output_dir, 'report_summary.txt')
    logger = logging.getLogger()
    file_handler = logging.FileHandler(output_log_summary, 'w+')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # process results and make report
    summary = DataFrame(results)
    columns_map = {
        'test_number': 'TEST NUMBER',
        'name': 'NAME',
        'start_time': 'START TIME',
        'stop_time': 'STOP TIME',
        'elapsed_time': 'ELAPSED TIME',
        'status': 'RESULT'
    }
    summary.rename(columns=columns_map, inplace=True)
    col_order = [v for _, v in columns_map.items()]
    summary = summary.reindex(columns=col_order)
    test_results = summary['RESULT']
    logger.info("""
Summary Information: | Total = {} | Pass = {} | Fail = {} | Error = {} |
Start Time:          {}
End Time:            {}
Elapsed Time:        {}
    """.format(
        len(test_results),
        len([p for p in test_results if p == 'Pass']),
        len([f for f in test_results if f == 'Fail']),
        len([e for e in test_results if e == 'Error']),
        str(start_time),
        str(stop_time),
        str(stop_time - start_time)
    ))
    logger.info('Test Statistics\n' + str_(summary))


# Custom unittest TestResult class to get more statistic of test cases
class TestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_result = {}

    def startTest(self, test):
        super(TestResult, self).startTest(test)
        self.test_result['name'] = test
        self.test_result['start_time'] = datetime.datetime.now()

    def stopTest(self, test):
        super(TestResult, self).stopTest(test)
        self.test_result['stop_time'] = datetime.datetime.now()
        elapsed_time = self.test_result['stop_time'] - self.test_result['start_time']
        self.test_result['start_time'] = self.test_result['start_time'].strftime('%Y-%m-%d %H:%M:%S')
        self.test_result['stop_time'] = self.test_result['stop_time'].strftime('%Y-%m-%d %H:%M:%S')
        self.test_result['elapsed_time'] = str(elapsed_time)
        if hasattr(test, '_outcome'):
            result = test._outcome.result
            if result.errors:
                self.test_result['status'] = "Error"
            elif result.failures:
                self.test_result['status'] = "Fail"
            else:
                self.test_result['status'] = "Pass"


# Custom TestRunner to apply new custom unittest TestResult
class TestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return TestResult(self.stream, self.descriptions, self.verbosity)


# Main function to load test case and run test case multiple times then summary results
def runtest(interval, duration, output_dir):
    logger = config_logging(output_dir)
    runner = TestRunner()
    results = []
    start_time = datetime.datetime.now()
    total_count = duration//interval
    for i in range(total_count):
        if i > 0:
            logger.info(f'sleep {interval}s ({round(interval/3600, 3)}h) ...')
            time.sleep(interval)
        logger.info('*'*10 + f' start (test_number = {i+1}) ' + '*'*10)
        suite = unittest.TestLoader().loadTestsFromName('suites.weather_test.WeatherTest')
        result = runner.run(suite).test_result
        result['test_number'] = i+1
        results.append(result)
        logger.info('*'*10 + f' finish (test_number = {i+1}) ' + '*'*10)
    stop_time = datetime.datetime.now()
    make_summary_report(results, start_time, stop_time, output_dir)


def main():
    # Define command line arguments
    parser = argparse.ArgumentParser(description='Using for run weather test multiple times with interval and duration time')
    parser.add_argument('--interval', type=int, required=True, help='interval time to run test (unit: second)')
    parser.add_argument('--duration', type=int, required=True, help='duration time to run test (unit: second)')
    parser.add_argument('-d', '--output_dir', type=str, required=False, default='result',
                        help='output directory where to save test log, default is "./result/"')
    # Parse the arguments
    args = parser.parse_args()
    interval, duration, output_dir = args.interval, args.duration, args.output_dir

    # run test
    runtest(interval, duration, output_dir)


if __name__ == '__main__':
    main()
