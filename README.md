# Employment & Poverty in the United States

## Abstract:

How has income and the poverty rate changed over the years? This project takes a brief look into employment and poverty with the analysis being broken down at three different levels: national, state and county. While both topics are analyzed separately, we do attempt to look at any possible relationships between the two as well. After carefully analyzing all our data, we were able to answer the following questions:

- National Level:
  1. How has the poverty rate changed over time?
  2. How does annual median income compare to the poverty threshold over time?
  3. In the year 2022, how many occupations have an annual median income of 100k plus?
- State Level:
  1. Do certain geographical areas tend to have higher poverty?
  2. Do areas with generally higher or lower poverty tend to have different proportions of employees working in different job sectors?
  3. How have poverty rates changed relative to income in recent years?
- County Level:
  1. Is there a correlation between income and poverty rate?
  2. Is there a correlation between unemployment and poverty rate? 

![Map](https://github.com/sammoe60/data-vikings/blob/main/Documentation/poverty_rates_and_population_us_map.png?raw=true)

## Collaborators:
- Kendra Johnson
- Jake Uhl
- Sam Moe

## Contents:
- #### [Dashboard](./Dashboard)
  - A PDF and JPG of our dashboard
- #### [Database](./Database)
  - Entity Relationship Diagram (ERD)
  - Jupyter Notebook containing the code to load data into our database
  - SQL file containing code to create our tables in our database
- #### [Documentation](./Documentation)
  - Presentation slides
  - Project plan
  - Visualization from our analysis
  - Technical report
- #### [Jupyter-Notebooks](./Jupyter-Notebooks)
  - Python files containing code demonstrating the use of Kafka (consumer / producer)
  - Jupyter Notebook containing code for our Exploratory Data Analysis (EDA)
  - Jupyter Notebook containing code for our Extract Transform Load (ETL) process 
- #### [Machine-Learning](./Machine-Learning)
  - A visual demonstrating the performance of our model
  - Jupyter Notebooks containing the code to create and test our model
  - A CSV file that contains the data used to generate the model
- #### [Processed-CSVs](./Processed-CSVs)
  - All CSVs post Extraction and Transformation 
- #### [Raw-Data](./Raw-Data)
  - Downloaded files from websites that have yet to undergo the ETL process 

## Contributions:

#### Kendra Johnson:
- Analysis of employment and poverty at the county level
- Machine learning (XGBoost regression to predict poverty levels)
- Kafka producer & consumer

#### Jake Uhl:
- Analysis of employment and poverty at the national level
- SQL database design

#### Sam Moe:
- Analysis of employment and poverty at the state level
- Machine learning (random forest regression to predict poverty levels)
- Dashboard creation and formatting

## Sources
- https://www.bls.gov/oes/tables.htm
- https://apps.deed.state.mn.us/lmi/laus/Default.aspx
- https://www.census.gov/data/developers/data-sets/Poverty-Statistics.html
- https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
- https://simplemaps.com/data/us-counties
