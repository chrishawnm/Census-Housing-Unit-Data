import requests
import ast
from geopy.geocoders import Nominatim
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-colorblind')

geolocator = Nominatim(user_agent="idk")

#add you API key
YOUR_KEY = ''

# Provide the state you want to analyze
State_Input = "Michigan"

# given the state by you, this dictionary extracts the ID that the census provided for each state
CensusCodeDict = {}
with open("CensusStateCodes.txt") as f:
    for line in f:
        (State, CensusStateCode) = line.split(",")
        CensusCodeDict[State] = int(CensusStateCode)

CensusStateCodeValue = CensusCodeDict[State_Input]

if CensusStateCodeValue < 10:
    CensusStateCodeValue = '0' + str(CensusStateCodeValue)

# obtaing the api data
data = requests.get(
    'https://api.census.gov/data/2018/pep/population?get=DATE_CODE,DATE_DESC,POP,GEONAME,STATE&for=county:*&in=state:'
    + str(CensusStateCodeValue)
    + '&key=' + YOUR_KEY)

countiesdata = requests.get('https://api.census.gov/data/2018/pep/population?get=GEONAME&for=county:*&in=state:'
                            + str(CensusStateCodeValue)
                            + '&key=' + YOUR_KEY)

# assigning the data to a variable
data = data.text
countiesdata = countiesdata.text

# since the data is given in a list within a list we can use the
# literal to convert it to an actual list within a list from a string
x = ast.literal_eval(data)
y = ast.literal_eval(countiesdata)

# extracting only the relevant data needed within the list
populationdata = []
for each in x[1:]:
    populationdata.append(each[1:-3])

popdata = []
year = ''
sorter = 0
for each in populationdata:
    year = each[0][int(each[0].find('/', 3) + 1):int(each[0].find(' '))]
    popdata.insert(sorter, [year, each[1], each[2]])
    sorter += 1

# extracting only the relevant data needed within the list
counties = []
for each in y[1:]:
    counties.append(each[0])

# deleting duplicates
counties = list(dict.fromkeys(counties))

# retrieving the longitude and latitude for each county
index = 0
counties_long_lat = []
while index < len(counties):
    location = geolocator.geocode(counties[index])
    counties_long_lat.insert(index * 2, [counties[index], location.latitude, location.longitude])
    index += 1

# header for the population data and counties data
#popdata.insert(0, ['Year', 'Population', 'County'])
#counties_long_lat.insert(0, ['County', 'Latitude', 'Longitude'] )

p1 = DataFrame.from_records(popdata, columns=['Year', 'Population', 'County'])
c1 = DataFrame.from_records(counties_long_lat, columns=['County', 'Latitude', 'Longitude'])

df3 = pd.merge(p1, c1)

#converting population to integer to be used in analysis
df3["Population"] = pd.to_numeric(df3["Population"])

#Provide a year to visualize
VisYear = '2012'

#filtering data by that month
df3byYear = df3.loc[df3["Year"]== VisYear]

#correlation
###print(df3.corr())

#heatmap of U.S.
print(plt.show(df3byYear.plot(kind ="scatter", x = 'Longitude', y = 'Latitude' ,figsize = (7,7)
                              ,label = "Estimated Population for Year " + VisYear + " of " + State_Input
                              ,alpha = .3
                              ,s=df3byYear['Population']*.001)))
