# LeetTrader

## InvestmentSimulator
**COMP 3900 Group Project, 20T3**

Scrum Master: Stephen Fong

Scrum Members: Jeffrey Yip, Luna Yang, Oliver Guo, Stephen Fong, The Tran {z5194996, z5137430, z5191682, z5191673, z5075710}ad.unsw.edu.au

For coding style, please see [style.md](style.md)

Project Proposal currently at https://docs.google.com/document/d/1zsgIKx4NSf6KvMcyXh27L2-45Z2Wn8Drh5oCXqKEg9g/edit

User stories currently at https://docs.google.com/spreadsheets/d/1i7SLrJjYA4pUAy_juoyw0GSKjq9C_CvKsfS-bi2kkq4/edit

Meeting Record currently at https://docs.google.com/spreadsheets/d/13wvUGb-VASsreEom_8FQIn0RhHlZj1STH8I1AjZZrLU/edit

System Architecture currently at https://app.diagrams.net/#G1ZkLURBTiKzgldmG9Tu277hAKCC48rsgz

Use Case Diagram currently at https://app.diagrams.net/#G1lWNhVEAr1oos60C0-sI2-eYgOQLJYSt1

ER Diagram currently at https://app.diagrams.net/#G14wLbZnKkU2A1pPMKqlVXBp0KtjyaL5bI

Class Diagram currently at https://app.diagrams.net/#G1ItJ5CR8XRURJ2h7F94dfDA3yyno9oPBJ

Interface Diagram currently at https://app.diagrams.net/#G1p5AWh7D17fQBYaWxoNrH7Oxr1PMmqHSO

Flow Diagram currently at https://app.diagrams.net/#G1JiLYfyhUndb77u5k-gWxUgk7IeS6M-jj

APIs usage currently at https://docs.google.com/document/d/1YRUvGNo87vkZKh3YlYKCOZl21fWax3nQcpXpfBu9C1w/edit?usp=sharing

Code Review currently at https://docs.google.com/spreadsheets/d/1utComw0ELxKtZN3wX4K8oQauqzD2dnYj-nBWxyI7iw4/edit

Report currently at https://docs.google.com/document/d/1qXfHPVLkB7GAsk7u71y-b8ypeySqANPO9YS2G3CKgF4/edit?usp=sharing

### Project Description
Potential new investors often want to practice their trading skills without risking real capital.
Investors can look for stocks using a "stock code", with the search resultshowing the stock name,
and latest available unit stock price. The investor can then decide to add the stock to their watchlist,
but can also remove it later on. Hence, this watchlist includes a list of stocks that the investor wants to keep track of,
where each of these stocks includes details on: the stock code, latest available unit stock price,
and the percentage change in the stock unit pricewhen comparing the latest available stock unit price to the previous day's
known stock unit price. To help with visualising the trend of a stock's price, investors can 
also choose to view a graph showing the historical daily closing unit price of any stock 
selected from their watchlist. The system will then depict historical data for the selected 
stock from at least the day when the stock was added to the investor's watchlist. The main 
features of the platform allow investors to simulate placing "buy" and "sell" orders.An 
investor can simulate placing a buy order at the current market price for a given number of 
units of a given stock, after which the stock units for which the order was placed are "simul-
owned" (since no real stock units are actually owned). Investors can also simulate placing sell 
orders for stock units that they "simul-own". In order to help investors understand the 
consequences of their trading history, InvestmentSimulator provides a number of reporting 
capabilities. First, at any time, an investor can see the total profit or loss they would make 
if all of the current stock units they currently simul-own were sold at their current market 
price per unit. To also gain some insight into the performance of individual stocks, investors 
can view the total profit or loss they would make for any given stock that they simul-own, if 
all the units they own for that stock were sold at the current market price per unit. Finally, 
each investor can also see a page listing aggregate statistics for each simul-ownedstock, 
including: total units simul-owned, total current worth of simul-owned units, total paid for 
currently simul-owned units.

---

### Project Objectives
Investors must be able to search for a stock using a "stock code"(also known as stock 
“symbol”), with results indicating the stock name, andlatest available unit price for the 
stock. Each investor must be able to add stocks from search results to their personal visible 
watchlist, and remove stocks from this watch list, with each stock on this watch list showing: 
the stock code, latest available stock price per unit, and the percentage change in the stock 
unit price when comparing the latest available stock unit price to the previous day's known 
stock unit price.Investors must be able to view a graph showing the historical daily closing 
unit price for any stock on their watchlist, where historical data must at least be available 
from the day when the stock was added to the watchlistto now.Investors must be able to 
"simulate" a "buy" order for a given stock at the current market price per unit, for a given 
number of units (note that a "simulated" buy order means that a "buy" order isn't actually 
executed, and the investor doesn't actually own the stock -hence we call stock that is bought 
using a simulated "buy" order "simul-owned"). An investor must be able to "simulate" a "sell" 
order for a given stock at the current market price per unit, for a given number of stock 
units, only for stock-units that they simul-own. Investors must be able to view the total 
profit or loss they would make if all the stock units they currently simul-own were sold at 
their current market price per unit. They must be able to view the total profit or loss they w
ould make for any given stock they simul-own, if all the units they simul-own for that stock were sold at the current market price per unit. Investors must be able to see a page that 
lists aggregate statistics for each stock type simul-owned, including: total units simul-owned, 
total current worth of simul-owned units, total paid for currently simul-owned units.
