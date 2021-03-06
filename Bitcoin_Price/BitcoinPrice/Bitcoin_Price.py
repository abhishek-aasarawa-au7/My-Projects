import requests
import time
import sys
from datetime import datetime


def help():
    print("Format is : Bitcoin_Price command price")
    print("The following command is acceptable:")
    print("\tn : if you do not want to set any bound")
    print("\tl : if you want to set only Lower Bound.")
    print("\tu : if you want to set only Upper Bound.")
    print("\tb : if you want to set both bounds.")
    print("\t Lower Bound should come before Upper Bound")


# Notification function if bitcoin price falls from given lower bound.
def emergency(value):
    data = {"value1": value}
    url = 'https://maker.ifttt.com/trigger/emergency_message/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD'
    requests.post(url, json=data)


# Notification function if bitcoin price cross the upper bound
def bounce(value):
    data = {"value1": value}
    url = 'https://maker.ifttt.com/trigger/bounce/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD'
    requests.post(url, json=data)


# Regular updating of price of bitcoin.
def update(price_list):
    price_list = "<br>".join(price_list)
    data = {"value1": price_list}
    url = 'https://maker.ifttt.com/trigger/bitcoin_price/with/key/jQMPZa_jNCtD7FIGhD9uohInvAIVB7-_XI1H_GCh2xD'
    requests.post(url, json=data)


# Function for taking price of bitcoin from API.
def getting_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = (requests.get(url)).json()
    value = response['bpi']['USD']['rate']
    value = float(value.replace(",", ""))
    date_time = datetime.now().strftime("%D %H:%M")
    return [date_time, value]


# Function for governing all type of notifications.
def notify(Lower_bound, Upper_bound):
    # Two variable for keeping time of last notifiaction of out of range price.
    time_lower = 0
    time_upper = 0
    count1 = 0
    count2 = 0
    price_list = []   # For saving 5 prices of bitcoin of different time.
    # Infinte Loop
    while True:
        # For getting price of bitcoin,
        # function will return a list [price, time].
        price = getting_price()
        # Checking if price is lower than lower bound
        # and if user set the lower bound or not.
        if price[1] < Lower_bound and Lower_bound != 0:
            # The price of bitcoin will shows in Italic.
            price[1] = "<i>{}</i>".format(price[1])
            # If time for last calling of emergency function is more than
            # or equal to 1 hour, it will call again.
            if count1 == 0 or time_lower >= 3600:
                emergency(price[1])
                count1 = 1
                # Setting time again to 0.
                time_lower = 0
        # Checking if price is more than upper bound
        # and if user set upper bound or not.
        elif price[1] > Upper_bound and Upper_bound != 0:
            # The price of bitcoin will shows in Bold.
            price[1] = "<b>{}</b>".format(price[1])
            # If time for last calling of bounce function is more than
            # or equal to 1 hour, it will call again.
            if count2 == 0 or time_upper >= 3600:
                bounce(price[1])
                count2 = 1
                # Setting time again to 0.
                time_upper = 0
        # Making format in "Date Time: $Price".
        price = "{}: ${}".format(price[0], price[1])
        price_list.append(price)
        # If we get 5 values then we will call update function.
        if len(price_list) >= 5:
            update(price_list)
            # Emptying List.
            price_list = []

        # keeping track of time.
        time_lower += 60*5
        time_upper += 60*5
        # Stoping program for 5 minutes
        time.sleep(60*5)


# We are taking upper and lower bound so chceking
# if lower bound is lower than upper bound or not.
def main():

    if 2 <= len(sys.argv) <= 4:

        if sys.argv[1] == "n":
            Lower_bound = 0
            Upper_bound = 0
            notify(Lower_bound, Upper_bound)

        elif sys.argv[1] == "l":
            Lower_bound = int(sys.argv[2])
            Upper_bound = 0
            notify(Lower_bound, Upper_bound)

        elif sys.argv[1] == "u":
            Lower_bound = 0
            Upper_bound = int(sys.argv[2])
            notify(Lower_bound, Upper_bound)

        elif sys.argv[1] == "b":
            Lower_bound = int(sys.argv[2])
            Upper_bound = int(sys.argv[3])
            if Lower_bound > Upper_bound and Upper_bound != 0:
                print("Lower Bound should come before than Upper Bound.")
            else:
                notify(Lower_bound, Upper_bound)

        elif sys.argv[1] == "h":
            help()

        else:
            help()

    else:
        help()


if __name__ == "__main__":
    main()
