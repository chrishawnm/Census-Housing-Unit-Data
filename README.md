# Census-Population-Estimate-Data
Cleaning up data for data analysis and visualizations within pandas module

I'm essentially extracting the API data and cleaning it to use with the pandas dataframe to create some pretty cool heatmaps and analytics

Steps to take to run script:
Download both files (py and text file)

pip install the following modules if they aren't already on your machine:
 requests,
 ast,
 pandas as pd,
 matplotlib.pyplot,
 seaborn, and  
 *geopy
 
Obtain an API Key from from the Census Bureau, can read steps here: 'https://towardsdatascience.com/getting-census-data-in-5-easy-steps-a08eeb63995d'

Here are some of the other variables you can requests in your API: 'https://www.census.gov/data/developers/data-sets/popest-popproj/popest.html'

*I use the geoup library to extract the longitude and latitude for each county 

Here's an example of a heatmap I did of Michigan estimated population data for 2012 using the census bureau data
![Image of heatmap](https://github.com/chrishawnm/Census-Population-Estimate-Data-API/blob/master/Estimated%20Population.JPG)
