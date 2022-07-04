import pyupbit
import requests
from pandas import DataFrame
import time
import datetime

tickers = pyupbit.get_tickers("KRW")
url = "https://api.upbit.com/v1/ticker"
querystring = {"markets": tickers}
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers, params=querystring)
dfs = DataFrame(response.json())
df_sort_index = dfs.sort_values(by=['acc_trade_price_24h'], axis=0, ascending=False)
main = df_sort_index[:30]['market']
list_from_df = main.values.tolist()

access = ""
secret = ""
upbit = pyupbit.Upbit(access, secret)

df3 = upbit.get_balances()
dfs1 = DataFrame(df3)
df_sort_index1 = dfs1.sort_values(by=['avg_buy_price'], axis=0, ascending=False)
main3 = df_sort_index1[:1]
list_dfs = main3.values.tolist()
for i in list_dfs:
    name1 = i[0]
    name2 = "KRW-" + name1

tickers = list_from_df

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def sell_time_process(ticker):
    now = datetime.datetime.now()
    start_time = get_start_time("KRW-BTC")
    final_time = start_time + datetime.timedelta(days=1)
    average_price = upbit.get_avg_buy_price(ticker)
    now_price = pyupbit.get_current_price(ticker)
    end_time = final_time - datetime.timedelta(seconds=90)
    if end_time < now < final_time: 
        print(ticker, now_price, average_price)
        print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "매도")
        sell_log = sell_current_price(ticker)
        print(sell_log)
        time.sleep(300)
def sell_process(ticker):
    now_price = pyupbit.get_current_price(ticker)
    average_price = upbit.get_avg_buy_price(ticker)
    profit_rate = 1.1 # 수익률 (1.1 -> 10%)
    # 현재가격이 구매가보다 10프로 보다 크다면
    if (average_price >0) and (now_price >= average_price * profit_rate):
        print(ticker, now_price, average_price)
        print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "매도")
        # 매도
        sell_log = sell_current_price(ticker)
        print(sell_log)
        #time.sleep(300)
    elif average_price == 0:
        print(ticker, "가 없습니다. ")
    
    
def sell_low_process(ticker):
    ###############10프로
    now_price = pyupbit.get_current_price(ticker)
    average_price = upbit.get_avg_buy_price(ticker)
    profit_rate = 0.967 # 수익률 (1.1 -> 10%)
    # 현재가격이 구매가보다 10프로 보다 크다면
    if (average_price >0) and (now_price <= average_price * profit_rate):
        print(ticker, now_price, average_price)
        print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "매도")
        # 매도
        sell_log = sell_current_price(ticker)
        print(sell_log)

def sell_current_price(ticker):
    """
    현재가 매도 함수
    :param ticker:  매도하고자 하는 코인명
    :return: None
    """
    unit = upbit.get_balance(ticker)
    return upbit.sell_market_order(ticker, unit)

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma10(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=10)
    ma5 = df['close'].rolling(10).mean().iloc[-1]
    return ma5

def get_ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=20)
    ma5 = df['close'].rolling(20).mean().iloc[-1]
    return ma5

def get_low_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['close'].iloc[-2]#1,2,4
    return ma5

def get_low_close(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['low'].iloc[-2]#1,2,4
    return ma5

def get_current_close(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['close'].iloc[-1]#1,2,4
    return ma5

def get_ma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['open'].iloc[-2]#1,2,4
    return ma5

def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['open'].iloc[-3]
    return ma5

def get_ma45(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    ma5 = df['open'].iloc[-4]
    return ma5

def get_ma60(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=6)
    ma5 = df['open'].iloc[-5]
    return ma5

def get_ma75(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=6)
    ma5 = df['open'].iloc[-6]
    return ma5

def get_vma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=5)
    vma5 = df['volume'].rolling(5).mean().iloc[-1]
    return vma5

def get_vma15(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=15)
    vma5 = df['volume'].rolling(15).mean().iloc[-1]
    return vma5

def get_vma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=30)
    vma5 = df['volume'].rolling(30).mean().iloc[-1]
    return vma5

def get_current_volume(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=1)
    vma5 = df['volume'].iloc[-1]
    return vma5

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

GRAPH_UP = 10
GRAPH_DOWN = 20

def is_up_or_down(df):
    last_close = df['close'][-1]
    last_open_price = df['open'][-1]
    if last_close - last_open_price > 0:
        return GRAPH_UP
    else:
        return GRAPH_DOWN

def get_high_price(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    high_price = (df.iloc[0]['open']*1.045) 
    return high_price
    
def make_df_add_average_volume(ticker, interval, rolling_value, count=20):
    """
    거래량 평균이 추가된 데이터프레임
    :param ticker: 캔들 정보를 표시할 코인
    :param interval: 캔들정보 1분, 10분, 등..
    :param rolling_value: 이동평균 갯수
    :param count: 서버에서 취득할 데이터 수
    :return: pandas dataframe
    """
    try:
        df = pyupbit.get_ohlcv(ticker, interval, count=count)

        df['average'] = df['volume'].rolling(window=rolling_value).mean().shift(1)
        return df
    except:
        return 1

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def buy_process(ticker):
 try:
     if upbit.get_avg_buy_price(ticker) == 0:
         krw = get_balance("KRW")
         total_weight = krw * 0.1995
         ma5 = get_ma5(ticker)
         ma10 = get_ma10(ticker)
         #ma20 = get_ma20(ticker)
         #high_price = get_high_price(ticker)
         ma15 = get_ma15(ticker)
         ma30 = get_ma30(ticker)
         ma45 = get_ma45(ticker)
         low_ma15 = get_low_ma15(ticker)
         if ma5 < ma10 :
             current_close = get_current_close(ticker)
             low_close = get_low_close(ticker)
             if current_close < low_close :
                 current_price = get_current_price(ticker)
                 if current_price < low_ma15 :
                     #ma10 = get_ma10(ticker)
                     #ma20 = get_ma20(ticker)
                     if ma15 < ma30 :
                         vma15 = get_vma15(ticker)
                         if ma30 < ma45 :
                             #target_price = get_target_price(ticker, 0.7)
                             current_volume = get_current_volume(ticker)
                             ma60 = get_ma60(ticker)
                             if ma45 < ma60 :                                                                        
                                 vma30 = get_vma30(ticker)
                                 vma5 = get_vma5(ticker)
                                 if vma30 < vma5:
                                     vma5 = get_vma5(ticker)
                                     if vma15 < vma5 :
                                         current_volume = get_current_volume(ticker)
                                         if vma5 < current_volume :
                                             print('\033[30m', time.strftime('%m-%d %H:%M:%S'), ticker, "구매")
                                             # 구매 시그널
                                             buy_log = upbit.buy_market_order(ticker, total_weight)
                                             print(buy_log)
                                             #if not buy_log:
                                                 #print("구매하려하였으나 못삼 ㅜㅠ")
 except:
     print("error")

while True:
    print("반복문 시작")
    for ticker in tickers: 
        #sell_time_process(ticker)
        #buy_process(ticker)     # 매수
        sell_process(ticker)    # 매도
        #sell_low_process(ticker)
        buy_process(ticker)
        #sell_time_process(ticker)
        time.sleep(0.05)
        

        
