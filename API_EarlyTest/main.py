from tiingoAPI import *
from translateAPI import *


# Print company name, last price and changed of one stock
print("========= TEST 1: SINGLE STOCK ========= ")
code = "AAPL"
n = getName(code)
p = getLastPrice(code)
delta = getPrevChange(code)
print("The last price of " + n + " is {}.".format(p))
print("The percentage change compare to prev day is equal to {:.2f}%".format(
    delta*100))
print()

# Print company name, last price and changed of multiple stock
print("========= TEST 2: MULTI STOCK ========= ")
code2 = "AMZN"
lastPrices = getLastPriceOfAll([code, code2])
print("The last prices of " + code + " and " + code2 + " are:")
for p in lastPrices:
    print(p)
print()

print("========= END OF TEST ========= ")
