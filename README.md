# MY-gen-mix
## About The Project
This project is insipired by https://github.com/djouallah/AEMO

The intention is to understand the fundemental of developing data pipeline using google cloud ecosystem.
Following are the key deliverables for this project
- scrape the data from Malaysia Grid System Operator Website (https://www.gso.org.my/)
  - function1.py is scheduled to run at 4AM (UTC+8) in VM instance to scrap the generation data from the previous day
- store the data in google cloud
  - function1.py will store the daily data in google cloud bucket
  - function2.py will run at after function1.py to transfer the data from the bucket to bigquery
- visualize the data in looker studio
  - https://datastudio.google.com/s/jlz1yVWGaXo
  - to do: add other meaningful visualisations
