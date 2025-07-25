# Data Ingestion from MTA Open Data Program
*Source:* [MTA Open Data Portal](https://data.ny.gov/browse?Dataset-Information_Agency=Metropolitan+Transportation+Authority&limitTo=datasets&sortBy=relevance&page=1&pageSize=20)

We used two main sources of data:
1) [*MTA Subway Stations*](https://data.ny.gov/Transportation/MTA-Subway-Stations/39hk-dx4f/about_data): which is a static CSV file containing information on all MTA Subway stations in NYC as of July 25, 2025
2) [*MTA Subway Hourly Ridership: Beginning 2025*](https://data.ny.gov/Transportation/MTA-Subway-Hourly-Ridership-Beginning-2025/5wq4-mkjj/about_data): which we queried using the API supported by [Socrata](https://dev.socrata.com/) due to the large amounts of data. We randomly selected 20 dates in 2025 and gathered ridership data for each station.