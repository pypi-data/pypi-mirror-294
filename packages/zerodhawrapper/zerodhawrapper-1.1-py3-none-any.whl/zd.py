import datetime
import json
import os
import random
import time
import traceback
import kiteconnect
import pandas as pd
from furl import furl
from nsetools import Nse
from prettytable import PrettyTable
from pyotp import TOTP
from webdriver_manager.chrome import ChromeDriverManager

# Install the ChromeDriver and add it to the system PATH.

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


START_TIME = datetime.time(9, 15, 0)
END_TIME = datetime.time(15, 45, 0)


def read_api_key():
    with open("key.json", "r") as f:
        return json.load(f)


def read_credentials():
    with open("credentials.json", "r") as f:
        return json.load(f)


# Waiting for page to load  element
def get_element(driver, xpath):
    return WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, xpath)))




def login():
    if os.path.isfile("access_token.txt") and os.path.getmtime("access_token.txt") > time.time() - 3600:
        with open("access_token.txt", "r") as f:
            access_token = json.loads(f.read())
        return access_token

    credentials = read_credentials()
    api_key = read_api_key()

    kite = kiteconnect.KiteConnect(api_key=api_key.get("api_key"))

    cdpath = ChromeDriverManager().install()
    cdpath = cdpath.split("/")[0]
    # from cd path copy chromedriver.exe to the path where the script is running
    import shutil
    shutil.copy(cdpath + "/chromedriver.exe", os.getcwd())
    options = ChromeOptions()
    # start headed browser
    # options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--log-level=NONE")
    driver = webdriver.Chrome(options=options)
    driver.get(kite.login_url())

    xpaths = {
        "username": "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input",
        "password": "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input",
        "login": "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button",
        "totp": "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[1]/input",
        "click": "/html/body/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/form/div[2]/button"
    }

    # username = driver.find_element("xpath", xpaths["username"])
    username = get_element(driver, xpaths["username"])
    username.send_keys(credentials.get("username"))

    # password = driver.find_element("xpath", xpaths["password"])
    password = get_element(driver, xpaths["password"])
    password.send_keys(credentials.get("password"))

    # login = driver.find_element("xpath", xpaths["login"])
    login = get_element(driver, xpaths["login"])
    login.click()
    time.sleep(0.5)

    time.sleep(3)

    # totp = driver.find_element("xpath", xpaths["totp"])
    totp = get_element(driver, xpaths["totp"])
    totp_token = TOTP(credentials.get("totp")).now()
    totp.send_keys(totp_token)
    # click = driver.find_element("xpath", xpaths["click"])
    click = get_element(driver, xpaths["click"])
    click.click()
    time.sleep(0.5)
    i = 0
    while i < 10:
        try:
            request_token = furl(
                driver.current_url).args["request_token"].strip()
            break
        except Exception:
            time.sleep(0.5)
            i += 1

    data = kite.generate_session(
        request_token, api_secret=api_key.get("api_secret"))
    kite.set_access_token(data["access_token"])
    with open("access_token.txt", "w") as f:
        json.dump(data['access_token'], f)
    driver.close()
    print("Logged in successfully")
    return data['access_token']

def initialize_kite():
    """Initialize and return a KiteConnect client."""
    if 'kite' not in globals():
        api_key = read_api_key()
        access_token = login()
        return kiteconnect.KiteConnect(api_key=api_key.get("api_key"), access_token=access_token)
    return kite

def get_quote(symbol):
    nse = Nse()
    return nse.get_index_quote(symbol)['lastPrice']


def tabulate_dict(dictionary):
    table = PrettyTable()
    table.field_names = ["Name", "Value"]
    for key, value in dictionary.items():
        table.add_row([key, value])
    return table


def send_order(kite, symbol, quantity, transaction_type, order_type, product, price=None, trigger_price=None,
               validity=None, disclosed_quantity=None, squareoff=None, stoploss=None, trailing_stoploss=None, tag=None):
    try:
        order_id = kite.place_order(tradingsymbol=symbol, quantity=quantity, transaction_type=transaction_type,
                                    order_type=order_type, product=product, price=price, trigger_price=trigger_price,
                                    validity=validity, disclosed_quantity=disclosed_quantity, squareoff=squareoff,
                                    stoploss=stoploss, trailing_stoploss=trailing_stoploss, tag=tag)
        print("Order placed. ID is: {}".format(order_id))
        return order_id
    except Exception as e:
        print(traceback.format_exc())
        print("Order placement failed: {}".format(traceback.format_exc()))
        return None


def retrieve_positions(kite):
    try:
        positions = kite.positions()
        print("Positions retrieved successfully")
        return positions
    except Exception as e:
        print(traceback.format_exc())
        print("Position retrieval failed: {}".format(traceback.format_exc()))
        return None


def get_nifty50_futures_symbols(kite):
    # get the nearest expiring nifty50 future contract from kite
    try:
        instruments = kite.instruments("NFO")
        nifty50_futures = [instrument for instrument in instruments if instrument['name'] == 'NIFTY']
        # check if the instrument_type is 'FUT'
        nifty50_futures = [instrument for instrument in nifty50_futures if instrument['instrument_type'] == 'FUT']
        nifty50_futures.sort(key=lambda x: x['expiry'])
        nearest_expiry = nifty50_futures[0]['expiry']
        # get the nearest expiry nifty50 futures
        nearest_expiry_nifty50_futures = [instrument for instrument in nifty50_futures if
                                          instrument['expiry'] == nearest_expiry]
        # get the symbols
        # if only one element, return, else print error
        if len(nearest_expiry_nifty50_futures) == 1:
            print("Nifty50 futures symbols retrieved successfully")
            return nearest_expiry_nifty50_futures[0]
        else:
            print("Could not retrieve nifty50 futures symbols")
            return None
    except Exception as e:
        # print traceback
        print(traceback.format_exc())
        print("Could not retrieve nifty50 futures symbols: {}".format(traceback.format_exc()))
        return None


def get_nearest_nifty_fut_price(kite):
    try:
        nifty50_fut_instrument = get_nifty50_futures_symbols(kite)
        if nifty50_fut_instrument is not None:
            price = kite.quote("NFO:" + nifty50_fut_instrument['tradingsymbol'])
            # create an average of bid and ask to get the mark price
            best_bid = price['NFO:' + nifty50_fut_instrument['tradingsymbol']]['depth']['buy'][0]['price']
            best_ask = price['NFO:' + nifty50_fut_instrument['tradingsymbol']]['depth']['sell'][0]['price']
            mark_price = (best_bid + best_ask) / 2
            if not mark_price:
                # get last traded price
                mark_price = price['NFO:' + nifty50_fut_instrument['tradingsymbol']]['last_price']

            print("Nearest nifty50 futures price retrieved successfully")
            return mark_price
        else:
            print("Could not retrieve nearest nifty50 futures price")
            return None
    except Exception as e:
        print(traceback.format_exc())
        print("Could not retrieve nifty50 futures symbols: {}".format(traceback.format_exc()))
        return None


def check_available_margin(kite):
    # check if available cash is greater than 10,000
    # check if available margin is greater than 10,000
    # return True if both are greater than 10,000
    # return False if either is less than 10,000
    try:
        # get available cash and margin
        available_cash = kite.margins()['equity']['available']['live_balance']
        if available_cash >= 130000:
            print("Available cash and margin are greater than 130,000")
            return True
        else:
            print("Available cash or margin is less than 130,000")
            return False
    except Exception as e:
        print(traceback.format_exc())
        print("Could not check available cash and margin: {}".format(traceback.format_exc()))
        return False


def get_fno_underlyings():
    global kite

    if 'kite' not in locals():
        api_key = read_api_key()
        access_token = login()
        kite = kiteconnect.KiteConnect(api_key=api_key.get("api_key"), access_token=access_token)
    all_instruments = kite.instruments(exchange="NFO")
    underlyings = set([instrument["name"] for instrument in all_instruments])
    return list(underlyings)

def instrument_by_trading_symbol(trading_symbol):
    global kite
    if 'kite' not in locals():
        api_key = read_api_key()
        access_token = login()
        kite = kiteconnect.KiteConnect(api_key=api_key.get("api_key"), access_token=access_token)
    all_instruments = kite.instruments()
    for instrument in all_instruments:
        if instrument['tradingsymbol'] == trading_symbol:
            return instrument


def fetch_and_cache(instrument_token, start, end, interval, oi):
    """Fetch historical data from the KiteConnect API and cache it."""
    kite = initialize_kite()
    print("Fetching data for", instrument_token, start, end, interval, oi)
    data = pd.DataFrame(kite.historical_data(
        instrument_token,
        from_date=start.strftime('%Y-%m-%d'),
        to_date=end.strftime('%Y-%m-%d'),
        interval=interval,
        oi=oi
    ))
    # data.to_csv(cache_path, index=False)
    return data


def get_historical(instrument_token, fdate, tdate, interv, oi):
    """Fetch historical data with caching and correct date segmentation."""
    # Initialize cache directory
    if not os.path.exists('get_historical'):
        os.mkdir('get_historical')


    dateformat = '%Y-%m-%d'

    # Determine date intervals based on interval type
    interval_days = {'day': 1500, '5minute': 70, 'minute': 55, 'hour': 55}
    max_days = interval_days.get(interv, 1500)
    date_delta = datetime.timedelta(days=max_days)

    # Split into sub-intervals if necessary
    current_start = fdate
    dfs = []

    while current_start <= tdate:
        current_end = min(current_start + date_delta, tdate)
        dfs.append(fetch_and_cache(instrument_token, current_start, current_end, interv, oi))
        current_start = current_end + datetime.timedelta(days=1)
        if current_end == tdate:
            break

    # Combine all dataframes and reset index
    df = pd.concat(dfs, ignore_index=True).reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])
    # df.to_csv(filepath, index=False)

    return df

def get_all_futures_underlyings():
    # returns: list of all futures underlyings
    # the list is sorted by name
    # the list contains only unique underlyings
    # the list contains only underlyings that have futures contracts
    all_futures = [instrument for instrument in instruments if instrument.get('tradingsymbol').endswith('FUT') and instrument.get('exchange') == 'NFO']
    all_underlyings = [instrument.get('name') for instrument in all_futures]
    all_underlyings = list(set(all_underlyings))
    all_underlyings = sorted(all_underlyings)
    return all_underlyings


def get_instrument_token_by_underlying(underlying):
    # underlying: underlying name
    # returns: instrument token of the underlying
    # the instrument token is the equity instrument token for the underlying trading on nse:
    # filter instruments for nse and underlying
    potential_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NSE' and instrument.get('tradingsymbol') == underlying]

    # if not found in nse, check in index segment
    if len(potential_instruments) == 0:
        # if underlying is 'NIFTY', try 'NIFTY 50' and 'NIFTY50'
        if underlying == 'NIFTY':
            potential_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NSE' and instrument.get('tradingsymbol') in ['NIFTY 50', 'NIFTY50']]

        # if underlying is 'BANKNIFTY', try 'NIFTY BANK' and 'NIFTYBANK'
        if underlying == 'BANKNIFTY':
            potential_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NSE' and instrument.get('tradingsymbol') in ['NIFTY BANK', 'NIFTYBANK']]

    if len(potential_instruments) == 1:
        return potential_instruments[0].get('instrument_token')
    else:
        print('Error: could not find instrument token for underlying: {}'.format(underlying))
        return None

def test_get_instrument_token_by_underlying():
    # test get_instrument_token_by_underlying
    # get all futures underlyings
    all_underlyings = get_all_futures_underlyings()
    # for each underlying, get the instrument token
    for underlying in all_underlyings:
        print(underlying)
        print(get_instrument_token_by_underlying(underlying))

def get_ohlc_by_instrument_token(instrument_token, start_date, end_date):
    # instrument_token: instrument token of the underlying
    # start_date: start date of the data
    # end_date: end date of the data
    # returns: ohlc data for the underlying
    # the data is sorted by date
    # the data is in the form of a pandas dataframe

    # get ohlc data
    try:
        ohlc = kite.historical_data(instrument_token, start_date, end_date, 'day') # day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
    # check for the following exception kiteconnect.exceptions.InputException: invalid to date
    except kiteconnect.exceptions.InputException as e:
        return None
    # check if data is empty
    if len(ohlc) == 0:
        print('Error: no data for instrument token: {}'.format(instrument_token), 'start date: {}'.format(start_date), 'end date: {}'.format(end_date))
        return None
    # convert to pandas dataframe
    ohlc = pd.DataFrame(ohlc)
    # sort by date
    ohlc = ohlc.sort_values(by='date')
    # convert date to datetime
    ohlc['date'] = pd.to_datetime(ohlc['date'], format='%Y-%m-%d')
    # check max and min date, and do another query if data is missing
    # print('min date: {}'.format(ohlc['date'].min()))
    # print('max date: {}'.format(ohlc['date'].max()))
    #localise timezone of start_date and end_date (GMT+5:30)

    if ohlc['date'].min() > start_date.tz_localize('Asia/Kolkata'):
        print('Error: data is missing between {} and {}'.format(start_date, ohlc['date'].min()))
        missing_data = get_ohlc_by_instrument_token(instrument_token, start_date.tz_localize(None), ohlc['date'].min() - pd.Timedelta(days=1))
        if missing_data is not None:
            ohlc = pd.concat([missing_data, ohlc])
    if ohlc['date'].max() < end_date.tz_localize('Asia/Kolkata'):
        print('Error: data is missing between {} and {}'.format(ohlc['date'].max(), end_date))
        missing_data = get_ohlc_by_instrument_token(instrument_token, ohlc['date'].max().tz_localize(None) + pd.Timedelta(days=1), end_date)
        if missing_data is not None:
            ohlc = pd.concat([ohlc, missing_data])

    # drop duplicates
    ohlc = ohlc.drop_duplicates(subset='date', keep='last')
    # reset index
    ohlc = ohlc.reset_index(drop=True)

    return ohlc

def get_5min_ohlc_by_instrument_token(instrument_token, start_date, end_date):
    # instrument_token: instrument token of the underlying
    # start_date: start date of the data
    # end_date: end date of the data
    # returns: ohlc data for the underlying
    # the data is sorted by date
    # the data is in the form of a pandas dataframe
    # if start date or end date is a datetime.datetime object, convert it to datetime.date
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
    if start_date.weekday() == 5:
        start_date = start_date + pd.Timedelta(days=2)
    if start_date.weekday() == 6:
        start_date = start_date + pd.Timedelta(days=1)
    # if end_date is not a trading day, set it to the previous trading day
    if end_date.weekday() == 5:
        end_date = end_date - pd.Timedelta(days=1)
    if end_date.weekday() == 6:
        end_date = end_date - pd.Timedelta(days=2)
    # get ohlc data
    # break timeframes into 99 day chunks
    query_start_dates = [start_date + pd.Timedelta(days=99 * i) for i in range(int((end_date - start_date).days / 99) + 1)]
    query_end_dates = [start_date + pd.Timedelta(days=99 * (i + 1)) for i in range(int((end_date - start_date).days / 99) + 1) if start_date + pd.Timedelta(days=99 * (i + 1)) < end_date]
    query_end_dates.append(end_date)

    ohlc = pd.DataFrame()
    for query_start_date, query_end_date in zip(query_start_dates, query_end_dates):
        try:
            output = kite.historical_data(instrument_token, query_start_date, query_end_date, '5minute') # day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
            # check the length of the output
            if len(output) == 0:
                print('Error: no data for instrument token: {}'.format(instrument_token), 'start date: {}'.format(query_start_date), 'end date: {}'.format(query_end_date))
                print('Retrying...')
                output = kite.historical_data(instrument_token, query_start_date, query_end_date, '5minute') # day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
                if len(output) == 0:
                    print('Still no data. Skipping...')
                    continue
            if len(output):
                output = pd.DataFrame(output)
                output = output.sort_values(by='date')
                output['date'] = pd.to_datetime(output['date'], format='%Y-%m-%d %H:%M:%S')
                ohlc = pd.concat([ohlc, output])
            else:
                continue
        except Exception as e:
            print('Error: {}'.format(e))
    if not len(ohlc):
        return None
    # reset index
    ohlc = ohlc.reset_index(drop=True)
    # check for missing data
    if len(ohlc) > 0:
        # check max and min date, and do another query if data is missing
        # print('min date: {}'.format(ohlc['date'].min()))
        # print('max date: {}'.format(ohlc['date'].max()))
        #localise timezone of start_date and end_date (GMT+5:30)
        # ideal start timestamp time = 9:15 AM, ideal end timestamp time = 3:30 PM
        ideal_start_timestamp = pd.Timestamp(year=start_date.year, month=start_date.month, day=start_date.day, hour=9, minute=15, tz='Asia/Kolkata')
        ideal_end_timestamp = pd.Timestamp(year=end_date.year, month=end_date.month, day=end_date.day, hour=15, minute=25, tz='Asia/Kolkata')
        if ohlc['date'].min() > ideal_start_timestamp:
            print('Error: data is missing between {} and {}'.format(ideal_start_timestamp, ohlc['date'].min()))
            missing_data = get_5min_ohlc_by_instrument_token(instrument_token, ideal_start_timestamp.tz_localize(None), ohlc['date'].min().tz_localize(None) - pd.Timedelta(days=1))
            if missing_data is not None:
                ohlc = pd.concat([missing_data, ohlc])
        if ohlc['date'].max() < ideal_end_timestamp:
            print('Error: data is missing between {} and {}'.format(ohlc['date'].max(), ideal_end_timestamp))
            missing_data = get_5min_ohlc_by_instrument_token(instrument_token, ohlc['date'].max().tz_localize(None), ideal_end_timestamp.tz_localize(None))
            if missing_data is not None:
                ohlc = pd.concat([ohlc, missing_data])
    # drop duplicates
    ohlc = ohlc.drop_duplicates(subset=['date'])
    # sort by date
    ohlc = ohlc.sort_values(by='date')
    # reset index
    ohlc = ohlc.reset_index(drop=True)

    return ohlc

def get_min_ohlc_by_instrument_token(instrument_token, start_date, end_date, oi=False, retry=True):
    # instrument_token: instrument token of the underlying
    # start_date: start date of the data
    # end_date: end date of the data
    # returns: ohlc data for the underlying
    # the data is sorted by date
    # the data is in the form of a pandas dataframe

    # get ohlc data
    # break timeframes into 99 day chunks
    # if start_date is not a trading day, set it to the next trading day
    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()
    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()
    if start_date.weekday() == 5:
        start_date = start_date + pd.Timedelta(days=2)
    if start_date.weekday() == 6:
        start_date = start_date + pd.Timedelta(days=1)
        # if end_date is not a trading day, set it to the previous trading day
    if end_date.weekday() == 5:
        end_date = end_date - pd.Timedelta(days=1)
    if end_date.weekday() == 6:
        end_date = end_date - pd.Timedelta(days=2)
    query_start_dates = [start_date + pd.Timedelta(days=30 * i) for i in range(int((end_date - start_date).days / 30) + 1)]
    query_end_dates = [start_date + pd.Timedelta(days=30 * (i + 1)) for i in range(int((end_date - start_date).days / 30) + 1) if start_date + pd.Timedelta(days=30 * (i + 1)) < end_date]
    query_end_dates.append(end_date)

    ohlc = pd.DataFrame()
    for query_start_date, query_end_date in zip(query_start_dates, query_end_dates):
        try:
            output = kite.historical_data(instrument_token, query_start_date, query_end_date, 'minute', oi=oi) # day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
            # check the length of the output
            if len(output) == 0:
                print('Error: no data for instrument token: {}'.format(instrument_token), 'start date: {}'.format(query_start_date), 'end date: {}'.format(query_end_date))
                print('Retrying...')
                output = kite.historical_data(instrument_token, query_start_date, query_end_date, 'minute', oi=oi) # day, 3minute, 5minute, 10minute, 15minute, 30minute, 60minute
                if len(output) == 0:
                    print('Still no data. Skipping...')
                    continue
            if len(output):
                output = pd.DataFrame(output)
                output = output.sort_values(by='date')
                output['date'] = pd.to_datetime(output['date'], format='%Y-%m-%d %H:%M:%S')
                ohlc = pd.concat([ohlc, output])
            else:
                continue
        except Exception as e:
            print('Error: {}'.format(e))
    if not len(ohlc):
        return None
    # reset index
    ohlc = ohlc.reset_index(drop=True)
    # check for missing data
    if len(ohlc) > 0 and retry:
        # check max and min date, and do another query if data is missing
        # print('min date: {}'.format(ohlc['date'].min()))
        # print('max date: {}'.format(ohlc['date'].max()))
        #localise timezone of start_date and end_date (GMT+5:30)
        # ideal start timestamp time = 9:15 AM, ideal end timestamp time = 3:30 PM
        ideal_start_timestamp = pd.Timestamp(year=start_date.year, month=start_date.month, day=start_date.day, hour=9, minute=15, tz='Asia/Kolkata')
        ideal_end_timestamp = pd.Timestamp(year=end_date.year, month=end_date.month, day=end_date.day, hour=15, minute=29, tz='Asia/Kolkata')
        if ohlc['date'].min() > ideal_start_timestamp:
            print('Error: data is missing between {} and {}'.format(ideal_start_timestamp, ohlc['date'].min()))
            missing_data = get_min_ohlc_by_instrument_token(instrument_token, ideal_start_timestamp.tz_localize(None), ohlc['date'].min().tz_localize(None) - pd.Timedelta(days=1), oi=oi)
            if missing_data is not None:
                ohlc = pd.concat([missing_data, ohlc])
        if ohlc['date'].max() < ideal_end_timestamp:
            print('Error: data is missing between {} and {}'.format(ohlc['date'].max(), ideal_end_timestamp))
            missing_data = get_min_ohlc_by_instrument_token(instrument_token, ohlc['date'].max().tz_localize(None), ideal_end_timestamp.tz_localize(None), oi=oi)
            if missing_data is not None:
                ohlc = pd.concat([ohlc, missing_data])
    # drop duplicates
    ohlc = ohlc.drop_duplicates(subset=['date'])
    # sort by date
    ohlc = ohlc.sort_values(by='date')
    # reset index
    ohlc = ohlc.reset_index(drop=True)

    return ohlc



def get_instrument_token_for_niftybees():
    # returns: instrument token of the NIFTYBEES ETF
    # the instrument token is the equity instrument token for the underlying trading on nse:

    # filter instruments for nse and 'NIFTYBEES'
    potential_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NSE' and instrument.get('tradingsymbol') == 'NIFTYBEES']

    if len(potential_instruments) == 1:
        return potential_instruments[0].get('instrument_token')
    else:
        print('Error: could not find instrument token for NIFTYBEES')
        return None


def get_nifty50_index_token():
    # returns: instrument token of the NIFTY 50 index
    # the instrument token is the index instrument token for the underlying trading on nse:

    # filter instruments for nse and 'NIFTY 50'
    potential_instruments = [instrument for instrument in instruments if instrument.get('segment') == 'INDICES' and instrument.get('name')=='NIFTY 50']

    if len(potential_instruments) == 1:
        return potential_instruments[0].get('instrument_token')
    else:
        print('Error: could not find instrument token for NIFTY 50')
        return None

def underlyings_of_all_fno():
    # returns a list of trading symbols of all fno instruments
    fno_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NFO']
    underlyings = [instrument.get('name') for instrument in fno_instruments]
    underlyings = list(set(underlyings))
    underlying_instruments = [instrument for instrument in instruments if instrument.get('exchange') == 'NSE' and instrument.get('tradingsymbol') in underlyings]
    underlyings = [instrument.get('tradingsymbol') for instrument in underlying_instruments]
    underlyings = list(set(underlyings))
    # check that underlying's exchange should be NSE

    return underlyings



api_key = read_api_key()
access_token = login()
kite = kiteconnect.KiteConnect(api_key=api_key.get("api_key"), access_token=access_token)
instruments = kite.instruments()



