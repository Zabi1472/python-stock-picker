import requests
import json
import sys

API_URL = "https://www.alphavantage.co/query"

# List to store purchased stocks
purchased_stocks = []
total_spent = 0

def get_stock_price(symbol):
    global total_spent
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": "SJJH1MR4JZIEPZXK"
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    if "Global Quote" in data:
        stock_data = data["Global Quote"]
        try:
            price = stock_data["05. price"]
            change_percent = stock_data["10. change percent"]
            print(f"{symbol}: Price: {price} | Change: {change_percent}")

            # Prompt the user to buy
            buy_option = input("Enter 'buy' to purchase the stock or press Enter to continue: ")
            if buy_option.lower() == "buy":
                quantity = input("Enter the number of shares you wanna purchase: ")
                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        raise ValueError
                except ValueError:
                    print(f"Invalid quantity please enter a positive integer.")
                    return
        
            #total price
            total_price = float(price) * quantity
            
            if total_spent + total_price > 10000:
               print(f"You dont have enough funds for this order.")
            else:
                total_spent += total_price
                # Add the purchased stock to the list
                purchased_stocks.append((symbol, price, quantity, total_price))
                print(f"You have successfully purchased {quantity} shares of {symbol.upper()}.")
                print(f"For a total price of {total_price}.")

                
        except KeyError:
            print(f"No data available for the stock symbol: {symbol}.")
    else:
        print(f"Stock symbol not found.")


# Start the loop
while True:
    # Prompt the user for a stock symbol or 'exit' to quit
    stock_symbol = input("Enter a stock symbol (or 'exit' to quit): ")

    # Check if the user wants to exit
    if stock_symbol.lower() == "exit":
        break

    else:
        # Fetch and display the stock price and change percentage
        get_stock_price(stock_symbol)

# Print the purchased stocks
print_portfolio = input("If you want to check your portfolio, enter 'yes'. Otherwise, enter 'no': ")
if print_portfolio.lower() == "yes":
    if purchased_stocks:
        print("Purchased Stocks:")
        for stock, price, quantity, total_price in purchased_stocks:
            print(f"{stock}: Price: {price} | Quantity: {quantity} | Total Price: {total_price}")
    else:
        print("No stocks have been purchased.")
elif print_portfolio.lower() == "no":
    sys.exit("Exiting the program. Have a nice day!")
else:
    print("Invalid input. Please enter either 'yes' or 'no'.")
