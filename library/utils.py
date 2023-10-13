from pandas import DataFrame
from tabulate import tabulate
import logging


def FMSG(msg):
    return 'Failed: {}'.format(msg)


def MSG(msg):
    return 'Passed: {}'.format(msg)


def str_(df):
    return str(tabulate(df, headers='keys', tablefmt='psql', showindex=False, colalign=['center', ]*len(df.columns)))


def core_compare(columns, actual, expect):
    def convert_result(row):
        if row == "both":
            return True
        elif row == "right_only":
            return False
    actual = DataFrame(actual, columns=columns)
    expect = DataFrame(expect, columns=columns)
    merged = actual.merge(expect, on=columns, how='right', indicator=True)
    merged['result'] = merged['_merge'].map(lambda x: convert_result(x))
    table = merged[columns + ["result"]]
    res = all(table['result'].tolist())
    return res, table


def compare_table(columns, actual, expect):
    res, table = core_compare(columns, actual, expect)
    logging.debug("* actual *\n{}".format(str_(actual)))
    logging.debug("* result compare with expect table *\n{}".format(str_(table)))

    fmsg = FMSG("Actual values are not matched with expect")
    pmsg = MSG("Actual values are matched with expect")
    if not res:
        raise AssertionError(fmsg)
    else:
        logging.debug(pmsg)
