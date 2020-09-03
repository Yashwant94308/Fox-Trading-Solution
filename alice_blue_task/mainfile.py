from setup import login
import logging
import datetime
import pandas as pd
from time import sleep
from alice_blue import *

EMA_CROSS_SCRIP = 'RELIANCE'
logging.basicConfig(level=logging.DEBUG)  # Optional for getting debug messages.
# Config

close_stock_price = 0
max_stock_price = 0
min_stock_price = 0
open_stock_price = 0
bid_Qty = 0
offer_Qty = 0
socket_opened = False
alice = None

URL = "https://www.moneycontrol.com/stocks/fno/marketstats/futures/high_oi/homebody.php?opttopic=stkfut&optinst" \
      "=stkfut&sel_mth=1&sort_order=0 "

now = datetime.datetime.now()
Start_time = now.strftime("%H:%M:%S")


def event_handler_quote_update(message):
    global close_stock_price, max_stock_price, min_stock_price, open_stock_price, bid_Qty, offer_Qty
    close_stock_price = message['close']
    min_stock_price = message['low']
    open_stock_price = message['open']
    max_stock_price = message['high']
    bid_Qty = message['bid_quantities']
    offer_Qty = message['ask_quantities']
    print("update", message)


def open_callback():
    global socket_opened
    socket_opened = True


def buy_signal(ins_scrip):  # function for buy stocks
    global alice

    order1 = {"instrument": ins_scrip,
              "order_type": OrderType.StopLossLimit,
              "quantity": 1,
              "price": 280.0,
              "trigger_price": 280.0,
              "stop_loss": 1.0,
              "square_off": 1.0,
              "trailing_sl": 20,
              "transaction_type": TransactionType.Buy,
              "product_type": ProductType.Intraday}
    order2 = {"instrument": ins_scrip,
              "order_type": OrderType.StopLossLimit,
              "quantity": 2,
              "price": 280.0,
              "trigger_price": 280.0,
              "stop_loss": 1.0,
              "square_off": 1.0,
              "trailing_sl": 20,
              "transaction_type": TransactionType.Buy,
              "product_type": ProductType.Intraday}
    order = [order1, order2]
    alice.place_basket_order(order)  # for basket order

    # alice.place_order(transaction_type=TransactionType.Buy,   # for single order
    #                   instrument=ins_scrip,
    #                   quantity=1,  # according to need
    #                   order_type=OrderType.StopLossLimit,
    #                   product_type=ProductType.Intraday,
    #                   price=8.0,  # price must be according to need
    #                   trigger_price=8.0,  # according to need
    #                   stop_loss=1.0,  # max should be 1 for one buy
    #                   square_off=1.0,  # it will provide square off amount
    #                   trailing_sl=20)


def sell_signal(ins_scrip):
    global alice

    order1 = {"instrument": ins_scrip,
              "order_type": OrderType.StopLossLimit,
              "quantity": 1,
              "price": 280.0,
              "trigger_price": 280.0,
              "stop_loss": 1.0,
              "square_off": 1.0,
              "trailing_sl": 20,
              "transaction_type": TransactionType.Sell,
              "product_type": ProductType.Intraday}
    order2 = {"instrument": ins_scrip,
              "order_type": OrderType.StopLossLimit,
              "quantity": 2,
              "price": 280.0,
              "trigger_price": 280.0,
              "stop_loss": 1.0,
              "square_off": 1.0,
              "trailing_sl": 20,
              "transaction_type": TransactionType.Sell,
              "product_type": ProductType.Intraday}
    order = [order1, order2]
    alice.place_basket_order(order)  # for basket order

    # alice.place_order(transaction_type=TransactionType.Sell,    # for simple order
    #                   instrument=ins_scrip,
    #                   quantity=1,  # according to need
    #                   order_type=OrderType.StopLossLimit,
    #                   product_type=ProductType.Intraday,
    #                   price=8.0,  # according to need
    #                   trigger_price=8.0,  # according to need
    #                   stop_loss=1.0,
    #                   square_off=1.0,
    #                   trailing_sl=20)


def main(logings):
    global socket_opened
    global alice

    global EMA_CROSS_SCRIP
    alice = AliceBlue(username=logings.username, password=logings.password, access_token=logings.access_tokan,
                      master_contracts_to_download=['NSE'])  # accessing alice blue
    ins_scrip = alice.get_instrument_by_symbol('NSE', EMA_CROSS_SCRIP)

    print("bal", alice.get_balance())  # get balance / margin limits
    print(alice.get_profile())  # get profile
    print(alice.get_daywise_positions())  # get daywise positions
    print(alice.get_netwise_positions())  # get netwise positions
    print(alice.get_holding_positions())  # get holding positions
    print(alice.get_order_history())  # get order history
    print(alice.get_trade_book())  # get trade book

    socket_opened = False
    alice.start_websocket(subscribe_callback=event_handler_quote_update,
                          socket_open_callback=open_callback,
                          run_in_background=True)

    while not socket_opened:  # wait till socket open & then subscribe
        pass
    alice.subscribe(ins_scrip, LiveFeedType.FULL_SNAPQUOTE)

    current_signal = ''
    while True:
        if datetime.datetime.now().second == 0:

            if current_signal != 'buy':
                if bid_Qty >= offer_Qty and max_stock_price > close_stock_price:
                    buy_signal(ins_scrip)
                    current_signal = 'buy'
            if current_signal != 'sell':
                if offer_Qty > bid_Qty and min_stock_price < open_stock_price:
                    sell_signal(ins_scrip)
                    current_signal = 'sell'
            sleep(1)
        data = pd.DataFrame({"A": ["API key", "API secret", "Client ID", "Password", "Pin", "Start Time", "EXIT Time",
                                   "Max Risk Per Trade", "SL%", "Min bid/offer ratio", "Min Stock Prize",
                                   "Max Stock Price",
                                   "buffer %BO limit Price", "Min % change in Volume", "URL", "Trailing flag"],
                             "B": ["xxxxxx", "xxxxxx", logings.username, logings.password, "PIN", Start_time,
                                   " ", 100, "1.00%", bid_Qty / offer_Qty, min_stock_price, max_stock_price,
                                   "0.20%", "0.00%", URL, "YES"]})
        data.to_excel('stock.xlsx', index=False)

        sleep(2)  # sleep for 200ms


if __name__ == '__main__':
    log = login()
    main(log)
