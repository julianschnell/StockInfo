This repo contains so far two (very basic) Python scripts:


## GetIndexContent.py

This script checks the website finanzen.net for a couple of stock indices. It scrapes the stocks of each index and its ISIN and saves them in a database.

## analystcheck.py

This script expects a query for a certain stock and searches on finanzen100.de for the appropriate ISIN to this stock. Then, it scrapes analyst opinions to the specific stock from onvista.de and saves them in a database. 
