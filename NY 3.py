# -*- coding: utf-8 -*-
"""
Created on Sat Jul 6 10:38:33 2024

@author: guill
"""


'''


conda install -c conda-forge chap --yes
conda install -c conda-forge geopandas --yes
conda install -c conda-forge folium --yes
conda install -c conda-forge plotly --yes
conda install -c conda-forge shapely --yes
conda install -c conda-forge fiona --yes
conda install -c conda-forge pyproj --yes
conda install -c conda-forge rtree --yes

'''
# pip install pandas geopandas folium plotly

import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import plotly.express as px
import chap
import shap


ny_build = pd.read_csv('ny-housing-new-york-units-by-building.csv')
ny_build_2 = pd.read_csv('ny-housing-new-york-units-by-building.csv')
ny_build = ny_build.dropna(axis=1, how='all')
ny_build_2 = ny_build_2.dropna(axis=1, how='all')  


ny_build.columns # below
ny_build.shape # (4959, 42)
ny_build.describe()
has_duplicates = ny_build.duplicated().any() # No
print(ny_build.isnull().sum()) 

'''
Project ID                               0
Project Name                             0
Program Group                            2
Project Start Date                       0
Project Completion Date               1389
Building ID                            993
Number                                   0
Street                                   0
Borough                                  0
Postcode                              1053
BBL                                   1112
BIN                                   2368
Community Board                          0
Council District                         8
Census Tract                          1047
NTA - Neighborhood Tabulation Area    1047
Latitude                              1053
Longitude                             1053
Latitude (Internal)                   1118
Longitude (Internal)                  1118
Building Completion Date              1214
Reporting Construction Type              0
Extended Affordability Only              0
Prevailing Wage Status                   0
Extremely Low Income Units               0
Very Low Income Units                    0
Low Income Units                         0
Moderate Income Units                    0
Middle Income Units                      0
Other Income Units                       0
Studio Units                             0
1-BR Units                               0
2-BR Units                               0
3-BR Units                               0
4-BR Units                               0
5-BR Units                               0
6-BR+ Units                              0
Unknown-BR Units                         0
Counted Rental Units                     0
Counted Homeownership Units              0
All Counted Units                        0
Total Units                              0
dtype: int64
'''
ny_build.info() 

'''
 0   Project ID                          4959 non-null   int64  
 1   Project Name                        4959 non-null   object 
 2   Program Group                       4957 non-null   object 
 3   Project Start Date                  4959 non-null   object 
 4   Project Completion Date             3570 non-null   object 
 5   Building ID                         3966 non-null   float64
 6   Number                              4959 non-null   object 
 7   Street                              4959 non-null   object 
 8   Borough                             4959 non-null   object 
 9   Postcode                            3906 non-null   float64
 10  BBL                                 3847 non-null   float64
 11  BIN                                 2591 non-null   float64
 12  Community Board                     4959 non-null   object 
 13  Council District                    4951 non-null   float64
 14  Census Tract                        3912 non-null   object 
 15  NTA - Neighborhood Tabulation Area  3912 non-null   object 
 16  Latitude                            3906 non-null   float64
 17  Longitude                           3906 non-null   float64
 18  Latitude (Internal)                 3841 non-null   float64
 19  Longitude (Internal)                3841 non-null   float64
 20  Building Completion Date            3745 non-null   object 
 21  Reporting Construction Type         4959 non-null   object 
 22  Extended Affordability Only         4959 non-null   object 
 23  Prevailing Wage Status              4959 non-null   object 
 24  Extremely Low Income Units          4959 non-null   int64  
 25  Very Low Income Units               4959 non-null   int64  
 26  Low Income Units                    4959 non-null   int64  
 27  Moderate Income Units               4959 non-null   int64  
 28  Middle Income Units                 4959 non-null   int64  
 29  Other Income Units                  4959 non-null   int64  
 30  Studio Units                        4959 non-null   int64  
 31  1-BR Units                          4959 non-null   int64  
 32  2-BR Units                          4959 non-null   int64  
 33  3-BR Units                          4959 non-null   int64  
 34  4-BR Units                          4959 non-null   int64  
 35  5-BR Units                          4959 non-null   int64  
 36  6-BR+ Units                         4959 non-null   int64  
 37  Unknown-BR Units                    4959 non-null   int64  
 38  Counted Rental Units                4959 non-null   int64  
 39  Counted Homeownership Units         4959 non-null   int64  
 40  All Counted Units                   4959 non-null   int64  
 41  Total Units                         4959 non-null   int64  
dtypes: float64(9), int64(19), object(14)
memory usage: 1.6+ MB

'''
ny_build.head(4)
ny_build.tail(4)
ny_build.dtypes
ny_build.nunique()

'''
Project ID                            2583
Project Name                          1591
Program Group                            4
Project Start Date                    1178
Project Completion Date               1063
Building ID                           3948
Number                                1932
Street                                1080
Borough                                  5
Postcode                               137
BBL                                   3260
BIN                                   2551
Community Board                         63
Council District                        51
Census Tract                           610
NTA - Neighborhood Tabulation Area     152
Latitude                              3796
Longitude                             3792
Latitude (Internal)                   2995
Longitude (Internal)                  3223
Building Completion Date              1150
Reporting Construction Type              2
Extended Affordability Only              2
Prevailing Wage Status                   2
Extremely Low Income Units             140
Very Low Income Units                  166
Low Income Units                       199
Moderate Income Units                   88
Middle Income Units                    105
Other Income Units                       4
Studio Units                           121
1-BR Units                             159
2-BR Units                             151
3-BR Units                              78
4-BR Units                              29
5-BR Units                               8
6-BR+ Units                              5
Unknown-BR Units                        20
Counted Rental Units                   266
Counted Homeownership Units            111
All Counted Units                      290
Total Units                            346
dtype: int64

'''
ny_build.value_counts
ny_build.select_dtypes(include='number')

'''
Content
The Department of Housing Preservation and Development (HPD) reports on buildings, units, and projects that began after January 1, 2014 
and are counted towards the Housing New York plan. 
The Housing New York Units by Building file presents this data by building, 
and includes building-level data, such as house number, street name, BBL, and BIN for each building in a project. 
The unit counts are provided by building. For additional documentation, including a data dictionary, review the attachments in the “About this Dataset” section of the Primer landing page.

Columns Description:
1) Project ID --> The Project ID is a unique numeric identifier assigned to each project by HPD.
2) Project Name --> The Project Name is the name assigned to the project by HPD.
    - Confidential 20%
    - Nehemiah Spring Creek Homes at Gateway Estates 2%
    - Other 78%
3) Program Group --> 
    - Multifamily Finance Program 51%
    - Multifamily Incentives Program 24%
    - Other (1234) 25%
4) Project Start Date --> The Project Start Date is the date of the project loan or agreement closing.
    - From 03/01/2014 to 31/12/2020 
5) Project Completion Date --> The Project Completion Date is the date that the last building in the project was completed. If the project has not yet
    - From 03/01/2014 to 13/01/2021
6) Building ID The Building ID is a unique numeric identifier assigned to each building by HPD.
7) Number --> The House Number is the street number in the building’s address. E.g., the house number is ‘100’ in ‘100 Gold Street.’
8) Street --> The Street Name is the name of the street in the building’s address. E.g., the street name is ‘Gold Street’ in ‘100 Gold
9) Borough --> The Borough is the borough where the building is located.
    - Manhattan
    - Brox
    - Brooklyn
    - Queens
    - Staten Island
10) Postcode --> Zip code
11) BBL --> The BBL (Borough, Block, and Lot) is a unique identifier for each tax lot in the City.
12) BIN --> The BIN (Building Identification Number) is a unique identifier for each building in the City.
13) Community Board --> The Community Board field indicates the New York City Community District where the building is located.
14) Council District --> The Council District indicates the New York City Council District where the building is located.
15) Census Track --> The Census Tract indicates the 2010 U.S. Census Tract where the building is located.
16) NTA - Neighborhood Tabulation Area --> The Neighborhood Tabulation Area indicates the New York City Neighborhood Tabulation Area where the building is located.
17) Latitude --> The Latitude and Longitude specify the location of the property on the earth’s surface. The coordinates
18) Longitude --> The Latitude and Longitude specify the location of the property on the earth’s surface. The coordinates
19) Latitude (Internal) --> The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s surface. The
20) Longitude (Internal) --> The Latitude (Internal) and Longitude (Internal) specify the location of the property on the earth’s surface. The
21) Building Completition Date --> The Building Completion Date is the date the building was completed. The field is blank if the building has not
22) Reporting Construction Type --> The Reporting Construction Type field indicates whether the building is categorized as ‘new construction’ or 'preservation'
    - Preservation 60%
    - New Construction 40%
23) Extended Affordability Only --> The Extended Affordability Only field indicates whether the project is considered to be Extended
    - False 81%
    - True 19%
24) Prevaliling Wage Status --> The Prevailing Wage Status field indicates whether the project is subject to prevailing wage requirements, such
    - Non Prevailing Wage 98%
    - Prevailing Wage 2%
25) Extremely Low Income --> Extremely Low Income Units are units with rents that are affordable to households earning 0 to 30% of the area median
26) Very Low Income Units --> Very Low Income Units are units with rents that are affordable to households earning 31 to 50% of the area median
27) Low Income Units --> Low Income Units are units with rents that are affordable to households earning 51 to 80% of the area median income
28) Moderate Income Units --> Moderate Income Units are units with rents that are affordable to households earning 81 to 120% of the area median
29) Middle Income Units --> Middle Income Units are units with rents that are affordable to households earning 121 to 165% of the area median income
30) Other Income Units --> Other Units are units reserved for building superintendents.
31) Studio Units --> Studio Units are units with 0-bedrooms.
32) 1-BR Units --> 1-BR Units are units with 1-bedroom.
33) 2-BR Units --> 2-BR Units are units with 2-bedrooms.
34) 3-BR Units --> 3-BR Units are units with 3-bedrooms.
35) 4-BR Units --> 4-BR Units are units with 4-bedrooms.
36) 5-BR Units --> 5-BR Units are units with 5-bedrooms.
37) 6-BR+ Units --> 6-BR+ Units are units with 6-bedrooms or more.
38) Unknown-BR Units --> are units with an unknown number of bedrooms.
39) Counted Rental Units --> are the units in the building, counted toward the Housing New York plan, where assistance has
40) Counted Homeownership Units --> are the units in the building, counted toward the Housing New York Plan, where assistance
41) All Counted Units --> The Counted Units field indicates the total number of affordable units, counted towards the Housing New York
42) Total Units --> field indicates the total number of units, affordable and market rate, in each building.
    
    
    
'''

#%%

ny_project = pd.read_csv('ny-housing-new-york-units-by-project.csv')
ny_project_2 = pd.read_csv('ny-housing-new-york-units-by-project.csv')
ny_project = ny_build.dropna(axis=1, how='all')
ny_project_2 = ny_build_2.dropna(axis=1, how='all')  


ny_project.columns # below
ny_project.shape # (2583, 18)
ny_project.describe()
has_duplicates = ny_project.duplicated().any() # No
print(ny_project.isnull().sum()) 
'''
Project ID                        0
Project Name                      0
Project Start Date                0
Project Completion Date         591
Extended Affordability Only       0
Prevailing Wage Status            0
Planned Tax Benefit            1072
Extremely Low Income Units        0
Very Low Income Units             0
Low Income Units                  0
Moderate Income Units             0
Middle Income Units               0
Other Income Units                0
Counted Rental Units              0
Counted Homeownership Units       0
All Counted Units                 0
Total Units                       0
Senior Units                      0
dtype: int64
'''
ny_project.info() 
'''
 #   Column                       Non-Null Count  Dtype 
---  ------                       --------------  ----- 
 0   Project ID                   2583 non-null   int64 
 1   Project Name                 2583 non-null   object
 2   Project Start Date           2583 non-null   object
 3   Project Completion Date      1992 non-null   object
 4   Extended Affordability Only  2583 non-null   object
 5   Prevailing Wage Status       2583 non-null   object
 6   Planned Tax Benefit          1511 non-null   object
 7   Extremely Low Income Units   2583 non-null   int64 
 8   Very Low Income Units        2583 non-null   int64 
 9   Low Income Units             2583 non-null   int64 
 10  Moderate Income Units        2583 non-null   int64 
 11  Middle Income Units          2583 non-null   int64 
 12  Other Income Units           2583 non-null   int64 
 13  Counted Rental Units         2583 non-null   int64 
 14  Counted Homeownership Units  2583 non-null   int64 
 15  All Counted Units            2583 non-null   int64 
 16  Total Units                  2583 non-null   int64 
 17  Senior Units                 2583 non-null   int64 
dtypes: int64(12), object(6)
'''
ny_project.head(4)
ny_project.tail(4)
ny_project.dtypes
ny_project.nunique()
'''
Project ID                     2583
Project Name                   1591
Project Start Date             1178
Project Completion Date        1063
Extended Affordability Only       2
Prevailing Wage Status            2
Planned Tax Benefit              10
Extremely Low Income Units      160
Very Low Income Units           154
Low Income Units                215
Moderate Income Units            93
Middle Income Units              89
Other Income Units               12
Counted Rental Units            319
Counted Homeownership Units      88
All Counted Units               341
Total Units                     385
Senior Units                     91
dtype: int64
'''
ny_project.value_counts
ny_project.select_dtypes(include='number')

'''
Content
The Department of Housing Preservation and Development (HPD) reports on buildings, units, and projects that began after January 1, 2014 and are counted towards the Housing New York plan. 
The Housing New York Units by Building file presents this data by building, and includes building-level data, such as house number, street name, BBL, and BIN for each building in a project. 
The unit counts are provided by building. 

1) Project ID --> is a unique numeric identifier assigned to each project by HPD.
2) Project Name --> is the name assigned to the project by HPD.
    -Confidential 38%
3) Project Start Date --> Project Start Date is the date of the project loan or agreement closing.
    - From 03/01/2014 to 31/12/2020 
4) Project Completion Date --> The Project Completion Date is the date that the last building in the project was completed. If the project has not yet
    - From 03/01/2014 to 13/01/2021
5) Extended Affordability Only --> The Extended Affordability Only field indicates whether the project is considered to be Extended
    - True 8%
    - False 92%
6) Prevaling Wage--> The Prevailing Wage Status field indicates whether the project is subject to prevailing wage requirements, such
    - Non Prevailing Wage 97%
    - Prevailing Wage 3%
7) Planned Tax Benefit --> The Planned Tax Benefit field indicates the type of tax benefit that is anticipated for the project at the time of the
    - null 42%
    - 421a 30%
    - Other 28%
8) Extremely Low Income Units --> are units with rents that are affordable to households earning 0 to 30% of the area median
9) Very Low Income Units are units with rents that are affordable to households earning 31 to 50% of the area median
10) Low Income Units are units with rents that are affordable to households earning 51 to 80% of the area median income
    
'''


# ADDING A NEW DATASET 
#%% CRIME DATASET

ny_crime = pd.read_csv('ny-NYPD_Complaint_Data_Current__Year_To_Date__20240713.csvNYPD_Complaint_Data_Current__Year_To_Date__20240713.csv')
ny_crime_2 = ny_crime.copy()

ny_crime = ny_crime_2.dropna(axis=1, how='all')  
ny_crime_2 = ny_crime_2.dropna(axis=1, how='all')  

ny_crime.columns # below
ny_crime.shape # (2583, 18)
ny_crime.describe()
has_duplicates = ny_crime.duplicated().any() # No
print(ny_crime.isnull().sum()) 

'''
### Column Descriptions Summary

1) CMPLNT_NUM: 
   - Randomly generated persistent ID for each complain
2) ADDR_PCT_CD: 
   -  The precinct in which the incident occurred.
3) BORO_NM: 
   - The name of the borough in which the incident occurred.
4) CMPLNT_FR_DT: 
   -  Exact date of occurrence for the reported event (or starting date of occurrence, if CMPLNT_TO_DT exists).
5) CMPLNT_FR_TM: 
   -  Exact time of occurrence for the reported event (or starting time of occurrence, if CMPLNT_TO_TM exists).
6) CMPLNT_TO_DT: 
   -  Ending date of occurrence for the reported event, if exact time of occurrence is unknown.
7) CMPLNT_TO_TM: 
   -  Ending time of occurrence for the reported event, if exact time of occurrence is unknown.
8) CRM_ATPT_CPTD_CD: 
   -  Indicator of whether the crime was successfully completed or attempted, but failed or was interrupted prematurely.
9) HADEVELOPT: 
   -  Name of NYCHA housing development of occurrence, if applicable.
10) HOUSING_PSA: 
   -  Development Level Code.
11) JURISDICTION_CODE: 
   - Jurisdiction responsible for incident. Either internal, like Police(0), Transit(1), and Housing(2); or external(3), like Correction, Port Authority, etc.
12) JURIS_DESC: 
   - Description of the jurisdiction code.
13) KY_CD: 
   - Three-digit offense classification code.
14) LAW_CAT_CD: 
   - Level of offense: felony, misdemeanor, violation.
15) LOC_OF_OCCUR_DESC: 
   - Specific location of occurrence in or around the premises; inside, opposite of, front of, rear of.
16) OFNS_DESC: 
   -  Description of offense corresponding with key code.
17) PARKS_NM: 
   - Name of NYC park, playground, or greenspace of occurrence, if applicable (state parks are not included).
18) PATROL_BORO: 
   - The name of the patrol borough in which the incident occurred.
19) PD_CD: 
   - Three-digit internal classification code (more granular than Key Code).
20) PD_DESC: 
   - Description of internal classification corresponding with PD code (more granular than Offense Description).
21) PREM_TYP_DESC: 
   - Specific description of premises; grocery store, residence, street, etc.
22) RPT_DT: 
   - Date event was reported to police.
23) STATION_NAME: 
   - Transit station name.
24) SUSP_AGE_GROUP: 
   - Suspect’s Age Group.
25) SUSP_RACE: 
   - Suspect’s Race Description.
26) SUSP_SEX: 
   - Suspect’s Sex Description.
27) TRANSIT_DISTRICT: 
   - Transit district in which the offense occurred.
28) VIC_AGE_GROUP: 
   - Victim’s Age Group.
29) VIC_RACE: 
   - Victim’s Race Description.
30) VIC_SEX: 
   - Victim’s Sex Description.
31) X_COORD_CD: 
   - X-coordinate for New York State Plane Coordinate System, Long Island Zone, NAD 83, units feet (FIPS 3104).
32) Y_COORD_CD: 
   - Y-coordinate for New York State Plane Coordinate System, Long Island Zone, NAD 83, units feet (FIPS 3104).
33) Latitude: 
   - Midblock Latitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326).
34) Longitude: 
   - Midblock Longitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326).
35) Lat_Lon: 
   - Combined latitude and longitude.
36) New Georeferenced Column: 
   - New georeferenced column combining latitude and longitude.

CMPLNT_NUM                       0
ADDR_PCT_CD                      0
BORO_NM                          0
CMPLNT_FR_DT                     0
CMPLNT_FR_TM                     0
CMPLNT_TO_DT                  7240
CMPLNT_TO_TM                     0
CRM_ATPT_CPTD_CD                 0
HADEVELOPT                       0
HOUSING_PSA                 128581
JURISDICTION_CODE                0
JURIS_DESC                       0
KY_CD                            0
LAW_CAT_CD                       0
LOC_OF_OCCUR_DESC                0
OFNS_DESC                        0
PARKS_NM                         0
PATROL_BORO                      0
PD_CD                           87
PD_DESC                          0
PREM_TYP_DESC                    0
RPT_DT                           0
STATION_NAME                     0
SUSP_AGE_GROUP                   0
SUSP_RACE                        0
SUSP_SEX                         0
TRANSIT_DISTRICT            131402
VIC_AGE_GROUP                    0
VIC_RACE                         0
VIC_SEX                          0
X_COORD_CD                       2
Y_COORD_CD                       2
Latitude                         2
Longitude                        2
Lat_Lon                          2
New Georeferenced Column         2
dtype: int64

'''

ny_value = pd.read_excel('ny-home_values.xlsx')

ny_crime = pd.read_csv('ny-NYPD_Complaint_Data_Current__Year_To_Date__20240713.csv')

ny_build = pd.read_csv('ny-housing-new-york-units-by-building.csv')
ny_build_2 = pd.read_csv('ny-housing-new-york-units-by-building.csv')

ny_project = pd.read_csv('ny-housing-new-york-units-by-project.csv')
ny_project_2 = pd.read_csv('ny-housing-new-york-units-by-project.csv')

    
#%% EDA Explorarion Data Analysis

# Display basic information about ny_build
print("Housing New York Units by Building (ny_build):")
print(ny_build_2.info())
print(ny_build_2.describe())
print("Missing values in ny_build:")
print(ny_build_2.isnull().sum())

# Display basic information about ny_project
print("\nHousing New York Units by Project (ny_project):")
print(ny_project_2.info())
print(ny_project_2.describe())
print("Missing values in ny_project:")
print(ny_project_2.isnull().sum())

# Basic statistics for numerical columns in ny_build
ny_build_2_numerical_stats = ny_build_2.describe()
print(ny_build_2_numerical_stats)

# Distribution and unique counts of categorical columns in ny_build
ny_build_2_categorical_distribution = ny_build_2.select_dtypes(include='object').apply(lambda x: x.value_counts())
print(ny_build_2_categorical_distribution)

# Handling missing values in ny_build
ny_build_2_missing_values = ny_build_2.isnull().sum()
print(ny_build_2_missing_values)

# Basic statistics for numerical columns in ny_project
ny_project_2_numerical_stats = ny_project_2.describe()
print(ny_project_2_numerical_stats)

# Distribution and unique counts of categorical columns in ny_project
ny_project_2_categorical_distribution = ny_project_2.select_dtypes(include='object').apply(lambda x: x.value_counts())
print(ny_project_2_categorical_distribution)

# Handling missing values in ny_project
ny_project_2_missing_values = ny_project_2.isnull().sum()
print(ny_project_2_missing_values)


#%% 25% data preprocessing

# Correlation matrix


import seaborn as sns
import matplotlib.pyplot as plt


# Function to calculate and plot correlation matrix
def plot_correlation_matrix(df, title):
    # Extract numerical columns
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calculate correlation matrix
    corr_matrix = numerical_df.corr()
    
    # Plot correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, square=True)
    plt.title(f'Correlation Matrix: {title}')
    plt.show()

# Calculate and plot correlation matrix for each dataset
plot_correlation_matrix(ny_build_2, 'NY Housing Units by Building')
plot_correlation_matrix(ny_project_2, 'NY Housing Units by Project')
plot_correlation_matrix(ny_crime, 'NY Crime Data')
plot_correlation_matrix(ny_value, 'NY Home Values')


#%% NY BUILD


from sklearn.preprocessing import OneHotEncoder

# Cleaning ny_build_2

ny_build_2.value_counts
ny_build_2.nunique()
ny_project_2.value_counts
ny_project_2.nunique()

'''
Project ID                            2583 : This column even though is a number, we have to use it to merge it ny_project_2
Project Name                          1591 : Is the project name, I am goint to erase it, with the project ID is enough but for the extra analysis I will need it.
Program Group                            4 : Type of financing program, I do not know which one is more important, to do any type of encoder, minmax.
Project Start Date                    1178 : At the end I am going to erase it, cause it cannot be turned into a number
Project Completion Date               1063 : A date, will be erase, is almost empty. And we are not doing a time series.
Building ID                           3948 : Is an identification number, for ML will be erased.
Number                                1932 : Is an identification number, for ML will be erased.
Street                                1080 : Is the name of the street, will be erased for Ml.
Borough                                  5 : It is important and I would love to do Minmax but as I do not know the order would be erase for ML. 
Postcode                               137 : Useful to merge with another datsets.
BBL                                   3260 : With the Postcode would be enough for the ML model, besides there are several nan values
BIN                                   2551 : With the Postcode would be enough for the ML model, besides there are several nan values
Community Board                         63 : With the Postcode would be enough for the ML model, besides there are several nan values
Council District                        51 : With the Postcode would be enough for the ML model, besides there are several nan values
Census Tract                           610 : The value of the census, is not really interesting
NTA - Neighborhood Tabulation Area     152 : It could have been very interesting, cause there are many datasets based on this info, but with the Zip code is enough.
Latitude                              3796 : I am going to use to merge with the ny_crime and then erase it for the ML model.
Longitude                             3792 : I am going to use to merge with the ny_crime and then erase it for the ML model.
Latitude (Internal)                   2995 : It's almost like a duplicate, so we erase it.
Longitude (Internal)                  3223 : It's almost like a duplicate, so we erase it.
Building Completion Date              1150 : We are not doing a Times Series, so we must erase it, and eventhough we have the start-date and the end-date, and we could substract them for analysis, but as there are lots of nan, it's not worthy. 
Reporting Construction Type              2 : I Use OneHotEncoder
Extended Affordability Only              2 : I Use OneHotEncoder
Prevailing Wage Status                   2 : I Use OneHotEncoder
Extremely Low Income Units             140 : I'll keep it.
Very Low Income Units                  166 : I'll erase it, cause it has a correlation with low and extremely low.
Low Income Units                       199 : I'll keep it
Moderate Income Units                   88 : I'll keep it.
Middle Income Units                    105 : I'll keep it
Other Income Units                       4 : I'll keep it
Studio Units                           121 : I'll keep it
1-BR Units                             159 : I'll keep it
2-BR Units                             151 : I'll keep it, I know it has a strong correlation but is useful for the analysis.
3-BR Units                              78 : I'll keep it
4-BR Units                              29 : I'll keep it
5-BR Units                               8 : I'll keep it
6-BR+ Units                              5 : I'll keep it
Unknown-BR Units                        20 : I'll keep it
Counted Rental Units                   266 : With total units is enough
Counted Homeownership Units            111 : With total units is enough
All Counted Units                      290 : With total units is enough
Total Units                            346 : I'll keep it
dtype: int64

'''
selected_columns = [
    'Project ID', 'Project Name', 'Program Group', 'Extremely Low Income Units', 
    'Low Income Units', 'Moderate Income Units', 
    'Middle Income Units', 'Other Income Units', 'Studio Units', '1-BR Units', 
    '2-BR Units', '3-BR Units', '4-BR Units', '5-BR Units', '6-BR+ Units', 
    'Unknown-BR Units', 'Total Units', 'Latitude', 
    'Longitude', 'Postcode', 'Reporting Construction Type', 
    'Extended Affordability Only', 'Prevailing Wage Status'
]
ny_build_filtered = ny_build[selected_columns]

# Encode categorical variables using OneHotEncoder
categorical_columns = ['Program Group', 'Reporting Construction Type', 'Extended Affordability Only', 'Prevailing Wage Status']
encoder = OneHotEncoder(sparse_output=False, drop='first')
encoded_cols = encoder.fit_transform(ny_build_filtered[categorical_columns])
encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(categorical_columns))

# Combine encoded columns with the original dataframe
ny_build_encoded = pd.concat([ny_build_filtered.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
ny_build_filtered = ny_build_encoded.drop(columns=categorical_columns)  # Drop original categorical columns

ny_build_filtered.nunique()

ny_build_filtered = ny_build_filtered.loc[ny_build_filtered.nunique(axis=1) != 1]
# I will use ny_build_filtered to at the end do the extra analysis

# Cleaning ny_project_2


#%% NY PROJECT

'''
Project ID                        0 Matain it for the part 4 extra analysis, and for the merge, but later I will erase it.
Project Name                      0 Matain it for the part 4 extra analysis, and for the merge, but later I will erase it.
Project Start Date                0 Again, I am not doing a time series, and the completitin date is almost empty, so it's useless.
Project Completion Date         591 I'll erase it
Extended Affordability Only       0 Use OneHotEncoder
Prevailing Wage Status            0 Use OneHotEncoder
Planned Tax Benefit            1072 Erase it, cause eventhough is useful, I cannot not know which one is more important.
Extremely Low Income Units        0 I'll keep it
Very Low Income Units             0 I'll erase it, as I did with the other one
Low Income Units                  0 I'll keep it
Moderate Income Units             0 I'll keep it
Middle Income Units               0 I'll keep it
Other Income Units                0 I'll keep it
Counted Rental Units              0 With total units is enough
Counted Homeownership Units       0 With total units is enough
All Counted Units                 0 With total units is enough
Total Units                       0 I'll keep it
dtype: int64
'''

selected_columns_project = [
    'Project ID', 'Project Name', 'Extended Affordability Only', 
    'Prevailing Wage Status', 'Extremely Low Income Units', 'Low Income Units', 
    'Moderate Income Units', 'Middle Income Units', 'Other Income Units', 
    'Total Units',
]
ny_project_filtered = ny_project[selected_columns_project]

# Handle missing values (if any)
# In this case, there are no missing values in the columns we are keeping.

# Encode categorical variables using OneHotEncoder
categorical_columns_project = ['Extended Affordability Only', 'Prevailing Wage Status']
encoder_project = OneHotEncoder(sparse_output=False, drop='first')
encoded_cols_project = encoder_project.fit_transform(ny_project_filtered[categorical_columns_project])
encoded_df_project = pd.DataFrame(encoded_cols_project, columns=encoder_project.get_feature_names_out(categorical_columns_project))

# Combine encoded columns with the original dataframe
ny_project_encoded = pd.concat([ny_project_filtered.reset_index(drop=True), encoded_df_project.reset_index(drop=True)], axis=1)
ny_project_filtered = ny_project_encoded.drop(columns=categorical_columns_project) 

ny_project_filtered.nunique()

# Remove rows where all columns have the same value in ny_project_filtered
ny_project_filtered = ny_project_filtered.loc[ny_project_filtered.nunique(axis=1) != 1]
# Drop rows where Latitude, Longitude, or Postcode are missing in ny_build_filtered
ny_build_filtered = ny_build_filtered.dropna(subset=['Latitude', 'Longitude', 'Postcode'])


#%% NY CRIME

ny_crime = ny_crime_2.dropna(axis=1, how='all')  
ny_crime_2 = ny_crime_2.dropna(axis=1, how='all')  


#%% CENSUS INFORMATION

import pandas as pd

ny_census = pd.read_csv('nyc_census_tracts.csv')
ny_census_2 = pd.read_csv('nyc_census_tracts.csv')
ny_census = ny_census.dropna(axis=1, how='all')
ny_census_2 = ny_census_2.dropna(axis=1, how='all')  

ny_census.columns # below

'''
Index(['CensusTract', 'County', 'Borough', 'TotalPop', 'Men', 'Women',
       'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Citizen', 'Income',
       'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment'],
      dtype='object')
'''


ny_census.shape # (2167, 36)
ny_census.describe()
has_duplicates = ny_census.duplicated().any() # No
print(ny_census.isnull().sum()) 

ny_census_block= pd.read_csv('census_block_loc.csv')
ny_census_block = ny_census_block.dropna(axis=1, how='all')

ny_census_block.shape # (38396, 6)
ny_census_block.describe()
has_duplicates = ny_census_block.duplicated().any() # No
print(ny_census_block.isnull().sum()) 

ny_census = ny_census.dropna(thresh=len(ny_census.columns) - 3 + 1)
ny_census_block = ny_census_block.dropna(thresh=len(ny_census_block.columns) - 3 + 1)


# Manipulate BlockCode in ny_census_block to match with CensusTract in ny_census
ny_census_block['BlockCode2'] = ny_census_block['BlockCode'].astype(str).str[:-4]
ny_census_block['BlockCode2'] = pd.to_numeric(ny_census_block['BlockCode2'], errors='coerce')
ny_census_block.rename(columns={'BlockCode2': 'CensusTract'}, inplace=True)

# Consolidate census block data
ny_census_block_grouped = ny_census_block.groupby('CensusTract').agg({'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()

# Merge the datasets
merged_census = pd.merge(ny_census, ny_census_block_grouped, on='CensusTract', how='left')

merged_census.to_excel('merged_census.xlsx', index=False)

merged_census.columns

'''
Index(['CensusTract', 'County', 'Borough', 'TotalPop', 'Men', 'Women',
       'Hispanic', 'White', 'Black', 'Native', 'Asian', 'Citizen', 'Income',
       'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'Latitude', 'Longitude'],
      dtype='object')
'''
import seaborn as sns
import matplotlib.pyplot as plt


# Function to calculate and plot correlation matrix
def plot_correlation_matrix(df, title):
    # Extract numerical columns
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calculate correlation matrix
    corr_matrix = numerical_df.corr()
    
    # Plot correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, square=True)
    plt.title(f'Correlation Matrix: {title}')
    plt.show()

# Calculate and plot correlation matrix for each dataset
plot_correlation_matrix(merged_census, 'NY Housing Units by Building')


#%% Income Distribution

import matplotlib.pyplot as plt

# Plot the scatter plot for income distribution
plt.figure(figsize=(10, 8))
scatter = plt.scatter(
    merged_census['Longitude'],
    merged_census['Latitude'],
    c=merged_census['Income'],
    cmap='viridis',
    alpha=0.6,
    edgecolors='w',
    linewidth=0.5
)
plt.colorbar(scatter, label='Income')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Income Distribution in NYC')
plt.grid(True)
plt.show()


#%%

ny_crime = pd.read_csv('ny-NYPD_Complaint_Data_Current__Year_To_Date__20240713.csv')

def plot_correlation_matrix(df, title):
    # Extract numerical columns
    numerical_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calculate correlation matrix
    corr_matrix = numerical_df.corr()
    
    # Plot correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True, square=True)
    plt.title(f'Correlation Matrix: {title}')
    plt.show()

# Calculate and plot correlation matrix for each dataset
plot_correlation_matrix(ny_crime, 'Crime')

ny_crime.columns

'''
Columns to drop from ny_crime:

CMPLNT_NUM
DateTime columns, we are not going to predict times series at the end.
CMPLNT_FR_DT
CMPLNT_FR_TM
CMPLNT_TO_DT
CMPLNT_TO_TM
HADEVELOPT
HOUSING_PSA --> Full of nan values
JURISDICTION_CODE --> only useful if you want to know about judge organiztion
JURIS_DESC
KY_CD non numerical variable, could be useful, but other variables can offer me the same info.
LOC_OF_OCCUR_DESC --> non numerical, and I do not find it pretty usefull. 
OFNS_DESC  --> very useful, but is the same as LAW_CAT_CD, and we are going to use this one.
PARKS_NM --> name of parks (I do not find it useful)
PATROL_BORO --> not useful
PD_DESC --> again we have another column that gives the same information
PREM_TYP_DESC --> we could use encoder, but I don't think a street is more important than grocery, so I cannot give a value.
TRANSIT_DISTRICT --> full of nan values


Columns to transfrom from ny_crime:
CRM_ATPT_CPTD_CD --> OneHotEncoder --> Attempted 0 and Completed 1
LAW_CAT_CD --> We will use encoder. The order is midemeanor as 0, felony as 1 and violation as 2.
SUSP_SEX --> Use one hot encoder



'''

'''
### Column Descriptions Summary

1) CMPLNT_NUM: 
   - Randomly generated persistent ID for each complain
2) ADDR_PCT_CD: 
   -  The precinct in which the incident occurred.
3) BORO_NM: 
   - The name of the borough in which the incident occurred.
4) CMPLNT_FR_DT: 
   -  Exact date of occurrence for the reported event (or starting date of occurrence, if CMPLNT_TO_DT exists).
5) CMPLNT_FR_TM: 
   -  Exact time of occurrence for the reported event (or starting time of occurrence, if CMPLNT_TO_TM exists).
6) CMPLNT_TO_DT: 
   -  Ending date of occurrence for the reported event, if exact time of occurrence is unknown.
7) CMPLNT_TO_TM: 
   -  Ending time of occurrence for the reported event, if exact time of occurrence is unknown.
8) CRM_ATPT_CPTD_CD: 
   -  Indicator of whether the crime was successfully completed or attempted, but failed or was interrupted prematurely.
9) HADEVELOPT: 
   -  Name of NYCHA housing development of occurrence, if applicable.
10) HOUSING_PSA: 
   -  Development Level Code.
11) JURISDICTION_CODE: 
   - Jurisdiction responsible for incident. Either internal, like Police(0), Transit(1), and Housing(2); or external(3), like Correction, Port Authority, etc.
12) JURIS_DESC: 
   - Description of the jurisdiction code.
13) KY_CD: 
   - Three-digit offense classification code.
14) LAW_CAT_CD: 
   - Level of offense: felony, misdemeanor, violation.
15) LOC_OF_OCCUR_DESC: 
   - Specific location of occurrence in or around the premises; inside, opposite of, front of, rear of.
16) OFNS_DESC: 
   -  Description of offense corresponding with key code.
17) PARKS_NM: 
   - Name of NYC park, playground, or greenspace of occurrence, if applicable (state parks are not included).
18) PATROL_BORO: 
   - The name of the patrol borough in which the incident occurred.
19) PD_CD: 
   - Three-digit internal classification code (more granular than Key Code).
20) PD_DESC: 
   - Description of internal classification corresponding with PD code (more granular than Offense Description).
21) PREM_TYP_DESC: 
   - Specific description of premises; grocery store, residence, street, etc.
22) RPT_DT: 
   - Date event was reported to police.
23) STATION_NAME: 
   - Transit station name.
24) SUSP_AGE_GROUP: 
   - Suspect’s Age Group.
25) SUSP_RACE: 
   - Suspect’s Race Description.
26) SUSP_SEX: 
   - Suspect’s Sex Description.
27) TRANSIT_DISTRICT: 
   - Transit district in which the offense occurred.
28) VIC_AGE_GROUP: 
   - Victim’s Age Group.
29) VIC_RACE: 
   - Victim’s Race Description.
30) VIC_SEX: 
   - Victim’s Sex Description.
31) X_COORD_CD: 
   - X-coordinate for New York State Plane Coordinate System, Long Island Zone, NAD 83, units feet (FIPS 3104).
32) Y_COORD_CD: 
   - Y-coordinate for New York State Plane Coordinate System, Long Island Zone, NAD 83, units feet (FIPS 3104).
33) Latitude: 
   - Midblock Latitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326).
34) Longitude: 
   - Midblock Longitude coordinate for Global Coordinate System, WGS 1984, decimal degrees (EPSG 4326).
35) Lat_Lon: 
   - Combined latitude and longitude.
36) New Georeferenced Column: 
   - New georeferenced column combining latitude and longitude.


Index(['CMPLNT_NUM', 'ADDR_PCT_CD', 'BORO_NM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM',
       'CMPLNT_TO_DT', 'CMPLNT_TO_TM', 'CRM_ATPT_CPTD_CD', 'HADEVELOPT',
       'HOUSING_PSA', 'JURISDICTION_CODE', 'JURIS_DESC', 'KY_CD', 'LAW_CAT_CD',
       'LOC_OF_OCCUR_DESC', 'OFNS_DESC', 'PARKS_NM', 'PATROL_BORO', 'PD_CD',
       'PD_DESC', 'PREM_TYP_DESC', 'RPT_DT', 'STATION_NAME', 'SUSP_AGE_GROUP',
       'SUSP_RACE', 'SUSP_SEX', 'TRANSIT_DISTRICT', 'VIC_AGE_GROUP',
       'VIC_RACE', 'VIC_SEX', 'X_COORD_CD', 'Y_COORD_CD', 'Latitude',
       'Longitude', 'Lat_Lon', 'New Georeferenced Column'],
      dtype='object')
'''


# Columns to drop
columns_to_drop = [
    'CMPLNT_NUM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'CMPLNT_TO_DT', 'CMPLNT_TO_TM',
    'HADEVELOPT', 'HOUSING_PSA', 'JURISDICTION_CODE', 'JURIS_DESC', 'KY_CD',
    'LOC_OF_OCCUR_DESC', 'OFNS_DESC', 'PARKS_NM', 'PATROL_BORO', 'PD_DESC',
    'PREM_TYP_DESC', 'TRANSIT_DISTRICT'
]


ny_crime = ny_crime.drop(columns=columns_to_drop)


ny_crime['CRM_ATPT_CPTD_CD'] = ny_crime['CRM_ATPT_CPTD_CD'].map({'Completed': 1, 'Attempted': 0})


law_cat_mapping = {'MISDEMEANOR': 0, 'FELONY': 1, 'VIOLATION': 2}
ny_crime['LAW_CAT_CD'] = ny_crime['LAW_CAT_CD'].map(law_cat_mapping)

ny_crime = pd.get_dummies(ny_crime, columns=['SUSP_SEX'], prefix='SUSP_SEX')


ny_crime.head(), ny_crime.describe(), ny_crime.columns.tolist()


#%%

merged_census.to_excel('merged_census.xlsx', index=False)
ny_project_filtered.to_excel('ny_project_filtered.xlsx', index=False)
ny_build_filtered.to_excel('ny_build_filtered.to_excel.xlsx', index=False)
ny_value.to_excel('ny_value.xlsx', index=False)
ny_crime.to_csv('ny_crime.csv', index= False)


merged_census = pd.read_excel('merged_census.xlsx')
ny_build_filtered = pd.read_excel('ny_build_filtered.to_excel.xlsx')
ny_project_filtered = pd.read_excel('ny_project_filtered.xlsx')
ny_value = pd.read_excel('ny-home_values.xlsx')


ny_crime = pd.read_excel('ny_crime.to_excel.xlsx')

#%%

merged_census
ny_project_filtered
ny_build_filtered
ny_value
ny_crime



#%% MERGE PROCESS

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
import concurrent.futures
import os
import pickle

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Function to get zip code from latitude and longitude with caching
cache_file = 'geocode_cache.pkl'
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        geocode_cache = pickle.load(f)
else:
    geocode_cache = {}

def lat_lon_to_zip(lat, lon):
    key = (lat, lon)
    if key in geocode_cache:
        return geocode_cache[key]
    try:
        location = geocode((lat, lon), language='en')
        if location:
            address = location.raw.get('address', {})
            zip_code = address.get('postcode')
            geocode_cache[key] = zip_code
            return zip_code
    except Exception as e:
        geocode_cache[key] = None
        return None

# Save cache periodically
def save_cache():
    with open(cache_file, 'wb') as f:
        pickle.dump(geocode_cache, f)

# Load your datasets
merged_census = pd.read_excel('/mnt/data/merged_census.xlsx')
ny_project_filtered = pd.read_excel('/mnt/data/ny_project_filtered.xlsx')
ny_build_filtered = pd.read_excel('/mnt/data/ny_build_filtered.to_excel.xlsx')
ny_value = pd.read_excel('/mnt/data/ny_value.xlsx')

# Rename Postcode to ZipCode in ny_build_filtered
ny_build_filtered.rename(columns={'Postcode': 'ZipCode'}, inplace=True)

# Merge ny_project_filtered with ny_build_filtered on 'Project ID' to get ZipCode
ny_project_with_zip = pd.merge(ny_project_filtered, ny_build_filtered[['Project ID', 'ZipCode']], on='Project ID', how='left')

# Ensure ZipCode columns are consistent for merging
ny_build_filtered['ZipCode'] = ny_build_filtered['ZipCode'].astype(str).str.split('.').str[0]
ny_project_with_zip['ZipCode'] = ny_project_with_zip['ZipCode'].astype(str).str.split('.').str[0]
ny_value['Zip Code'] = ny_value['Zip Code'].astype(str).str.split('.').str[0]

# Rename 'Zip Code' to 'ZipCode' in ny_value
ny_value.rename(columns={'Zip Code': 'ZipCode'}, inplace=True)

# Function to process a single dataframe and add ZipCode column
def process_dataframe(df, lat_col, lon_col):
    df['ZipCode'] = df.apply(lambda row: lat_lon_to_zip(row[lat_col], row[lon_col]), axis=1)
    return df

# Process merged_census dataframe to add ZipCode
merged_census = process_dataframe(merged_census, 'Latitude', 'Longitude')

# Save the cache
save_cache()
# Export it to save it 

merged_census = pd.read_excel('merged_census.xlsx')


# Merge ny_build_filtered and ny_project_with_zip on 'Project ID' using an outer join
build_project_merged_df = pd.merge(ny_build_filtered, ny_project_with_zip, on='Project ID', how='outer', suffixes=('_build', '_project'))


# Remove '_project' suffix from column names for merging
build_project_merged_df.columns = [col.replace('_project', '') for col in build_project_merged_df.columns]

build_project_merged_df.to_excel('build_project_merged.xlsx', index=False)

# Now merge build_project_merged_df with merged_census on 'ZipCode'
final_merged_df = pd.merge(build_project_merged_df, merged_census, on='ZipCode', how='left')

# Finally, merge with ny_value on 'ZipCode'
final_merged_df = pd.merge(final_merged_df, ny_value, on='ZipCode', how='outer')

# Display the resulting dataframe
print("Final Merged DataFrame:")
print(final_merged_df.head())


ny_merge = final_merged_df.copy()
ny_merge.to_excel('ny_merge.xlsx', index=False)


ny_merge.columns

print(ny_merge.isnull().sum())

#%% Clean build project before the merge

build_project_merged_df


# Ensure ZipCode column is of the same data type (string)
build_project_merged_df['ZipCode'] = build_project_merged_df['ZipCode'].astype(str)

# Function to count non-zero values in a row
def count_non_zero(row):
    return (row != 0).sum()

# Apply the function to each row and create a new column for the count of non-zero values
build_project_merged_df['non_zero_count'] = build_project_merged_df.apply(count_non_zero, axis=1)

# Sort the dataframe by Project Name_build and non_zero_count in descending order
build_project_merged_df = build_project_merged_df.sort_values(by=['Project Name_build', 'non_zero_count'], ascending=[True, False])

# Drop duplicates, keeping only the row with the highest non-zero count for each Project Name_build
build_project_merged_df = build_project_merged_df.drop_duplicates(subset=['Project Name_build'])

# Drop the auxiliary column used for counting non-zero values
build_project_merged_df = build_project_merged_df.drop(columns=['non_zero_count'])

# Save the cleaned dataframe
build_project_merged_df.to_excel('build_project_merged_cleaned.xlsx', index=False)

# Display the resulting dataframe
print("Cleaned Build Project Merged DataFrame:")
print(build_project_merged_df.head())

build_project_merged_df.to_excel('build_project_merged.xlsx', index=False)

#%%

merged_census['ZipCode'] = merged_census['ZipCode'].astype(str).str.replace('.0', '')

#%%

merged_census.to_excel('merged_census.xlsx', index= False)

# Drop non-numerical columns except for ZipCode
non_numerical_columns = merged_census.select_dtypes(include=['object']).columns
columns_to_keep = ['ZipCode'] + [col for col in merged_census.columns if col not in non_numerical_columns]
merged_census = merged_census[columns_to_keep]

# Drop specific columns
columns_to_drop = ['County', 'Borough', 'CensusTract']
merged_census = merged_census.drop(columns=columns_to_drop, errors='ignore')
columns_to_drop = ['Latitude', 'Longitude']
merged_census = merged_census.drop(columns=columns_to_drop, errors='ignore')
#
merged_census_grouped = merged_census.groupby('ZipCode').mean().reset_index()

#
ny_value['ZipCode'] = ny_value['ZipCode'].astype(str)
ny_value_numerical = ny_value.select_dtypes(include=['number'])
ny_value_aggregated = ny_value_numerical.groupby(ny_value['ZipCode']).mean().reset_index()
ny_value_aggregated['ZipCode'] = ny_value['ZipCode']

# Save the cleaned and aggregated dataframe
merged_census_grouped.to_excel('merged_census_grouped.xlsx', index=False)
build_project_merged_df.to_excel('build_project_merged_df.xlsx', index=False)
ny_value_aggregated.to_excel('ny_value_aggregated.xlsx', index=False)

#%%




# Ensure ZipCode columns are of the same data type (string)
build_project_merged_df['ZipCode'] = build_project_merged_df['ZipCode'].astype(str)
merged_census_grouped['ZipCode'] = merged_census_grouped['ZipCode'].astype(str)
ny_value_aggregated['ZipCode'] = ny_value_aggregated['ZipCode'].astype(str)

# Perform the first merge with merged_census_grouped
merged_build_census = pd.merge(build_project_merged_df, merged_census_grouped, on='ZipCode', how='outer')

# Perform the second merge with ny_value_aggregated
final_merged_df = pd.merge(merged_build_census, ny_value_aggregated, on='ZipCode', how='outer')

# Display the resulting dataframe
print("Final Merged DataFrame:")
print(final_merged_df.head())

# Save the final merged dataframe to an Excel file
final_merged_df.to_excel('ny_merge_final.xlsx', index=False)

# I remove Nan Values

final_merged_cleaned = final_merged_df.dropna(subset=['Project Name_build'])

final_merged_cleaned = final_merged_cleaned.drop(columns=['Project Name_build', 'ZipCode_build'])



#%% Now let's do 2 datasets

# One dataset for ML

final_merged_cleaned.to_excel('ny_merge_final.xlsx', index=False)


#%%


'''

Non Numerical : Project ID, ZipCode
Income: Extremely Low Income Units_build	Low Income Units_build	Moderate Income Units_build	Middle Income Units_build	Other Income Units_build, Extremely Low Income Units	Low Income Units	Moderate Income Units	Middle Income Units	Other Income Units	Total Units	Extended Affordability Only_Yes	Prevailing Wage Status_Prevailing Wage, IncomeErr	IncomePerCap	IncomePerCapErr	Poverty	ChildPoverty

Professional Job: Professional	Service	Office	Construction	Production	Drive	Carpool	Transit	Walk	OtherTransp	WorkAtHome	MeanCommute	Employed	PrivateWork	PublicWork	SelfEmployed	FamilyWork	Unemployment	Median Home Value
Units size: Studio Units	1-BR Units	2-BR Units	3-BR Units	4-BR Units	5-BR Units	6-BR+ Units	Unknown-BR Units	Total Units_build
Program: Program Group_Multifamily Finance Program	Program Group_Multifamily Incentives Program	Program Group_Small Homes Program	Program Group_nan	Reporting Construction Type_Preservation	Extended Affordability Only_Yes_build	Prevailing Wage Status_Prevailing Wage_build

Population Size and Race: TotalPop	Men	Women	Hispanic	White	Black	Native	Asian	Citizen


HE HECHO 800.000 MIL intentos, esto es lo mejor que he conseguido sorry.

'''


#%% Income Analysis - XGBoost Classification


import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.decomposition import PCA
import xgboost as xgb
import matplotlib.pyplot as plt


almost_final_ML = final_merged_cleaned.copy()

# Quantiles
quantiles = almost_final_ML['Income'].quantile([0.33, 0.66])
def income_level(income):
    if income <= quantiles[0.33]:
        return 'Low'
    elif income <= quantiles[0.66]:
        return 'Medium'
    else:
        return 'High'

almost_final_ML['Income Level'] = almost_final_ML['Income'].apply(income_level)

# Features
selected_features = [
    'Extremely Low Income Units_build', 'Low Income Units_build', 'Moderate Income Units_build',
    'Middle Income Units_build', 'Other Income Units_build', 'Extremely Low Income Units',
    'Low Income Units', 'Moderate Income Units', 'Middle Income Units', 'Other Income Units',
    'Total Units', 'Extended Affordability Only_Yes', 'Prevailing Wage Status_Prevailing Wage',
    'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty', 'ChildPoverty', 'TotalPop',
    'Citizen', 'Program Group_Multifamily Finance Program', 'Program Group_Multifamily Incentives Program',
    'Program Group_Small Homes Program', 'Program Group_nan', 'Reporting Construction Type_Preservation',
    'Extended Affordability Only_Yes_build', 'Prevailing Wage Status_Prevailing Wage_build',
    'Professional', 'Service', 'Office', 'Construction', 'Production', 'Drive', 'Carpool', 
    'Transit', 'Walk', 'OtherTransp', 'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 
    'PublicWork', 'SelfEmployed', 'FamilyWork', 'Unemployment', 'Median Home Value',
    'Studio Units', '1-BR Units', '2-BR Units', '3-BR Units', '4-BR Units', '5-BR Units',
    '6-BR+ Units', 'Unknown-BR Units', 'Total Units_build'
]

# Drop 
almost_final_ML = almost_final_ML[selected_features + ['Income Level']]
almost_final_ML = almost_final_ML.dropna()

# Encode the target variable
label_encoder = LabelEncoder()
almost_final_ML['Income Level'] = label_encoder.fit_transform(almost_final_ML['Income Level'])

# Split the data into features and target
X = almost_final_ML.drop(columns=['Income Level'])
y = almost_final_ML['Income Level']

# Standardize the data
numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# PCA
pca = PCA(n_components=0.95)  # Retain 95% of variance
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Check the explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
print(f"Explained Variance Ratio: {explained_variance_ratio}")

# XGBoost
xgb_model = xgb.XGBClassifier(
    max_depth=4,
    n_estimators=100,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=1,  # I increased the regularization parameter
    reg_lambda=2,  # I increased the regularization parameter
    use_label_encoder=False,
    eval_metric='mlogloss'
)

# Train the model
xgb_model.fit(X_train_pca, y_train)

# Predict on the test set
y_pred = xgb_model.predict(X_test_pca)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}") # Accuracy: 0.9386281588447654

# Detailed classification report
print(classification_report(y_test, y_pred))

'''
print(classification_report(y_test, y_pred))
              precision    recall  f1-score   support

           0       0.98      0.93      0.96       107
           1       0.92      0.97      0.95        75
           2       0.91      0.92      0.91        95

    accuracy                           0.94       277
   macro avg       0.94      0.94      0.94       277
weighted avg       0.94      0.94      0.94       277

Accuracy:

The model achieved an accuracy of 0.9386 (93.86%). This is a strong indication that the model performs well overall in classifying the income levels.
Classification Report:

Precision:
Class 0 (Low): 0.98
Class 1 (Medium): 0.92
Class 2 (High): 0.91
Recall:
Class 0 (Low): 0.93
Class 1 (Medium): 0.97
Class 2 (High): 0.92
F1-Score:
Class 0 (Low): 0.96
Class 1 (Medium): 0.95
Class 2 (High): 0.91
The precision, recall, and F1-scores for all classes are high, indicating that the model is good at both identifying positive instances and minimizing false positives and false negatives.
The macro and weighted averages for precision, recall, and F1-score are all 0.94, which is consistent with the high overall accuracy and indicates balanced performance across the classes.


'''


# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(conf_matrix)

'''
[[100   0   7]
 [  0  73   2]
 [  2   6  87]]

Class 0 (Low):
True Positives (correctly predicted Low): 100
False Negatives (predicted as Medium/High): 7
Class 1 (Medium):
True Positives (correctly predicted Medium): 73
False Negatives (predicted as Low/High): 2
Class 2 (High):
True Positives (correctly predicted High): 87
False Negatives (predicted as Low/Medium): 8
The confusion matrix indicates that the model correctly classifies most instances. There are some misclassifications, particularly for class 0 (Low) and class 2 (High), but the numbers are relatively low.


'''

#%% PCA AND K MEANS - UNSUPERVISED


from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.decomposition import PCA
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


almost_final_ML = final_merged_cleaned.copy()

# Quantiles
quantiles = almost_final_ML['Income'].quantile([0.33, 0.66])
def income_level(income):
    if income <= quantiles[0.33]:
        return 'Low'
    elif income <= quantiles[0.66]:
        return 'Medium'
    else:
        return 'High'

almost_final_ML['Income Level'] = almost_final_ML['Income'].apply(income_level)

# Features
selected_features = [
    'Extremely Low Income Units_build', 'Low Income Units_build', 'Moderate Income Units_build',
    'Middle Income Units_build', 'Other Income Units_build', 'Extremely Low Income Units',
    'Low Income Units', 'Moderate Income Units', 'Middle Income Units', 'Other Income Units',
    'Total Units', 'Extended Affordability Only_Yes', 'Prevailing Wage Status_Prevailing Wage',
    'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty', 'ChildPoverty', 'TotalPop',
    'Citizen', 'Program Group_Multifamily Finance Program', 'Program Group_Multifamily Incentives Program',
    'Program Group_Small Homes Program', 'Program Group_nan', 'Reporting Construction Type_Preservation',
    'Extended Affordability Only_Yes_build', 'Prevailing Wage Status_Prevailing Wage_build',
    'Professional', 'Service', 'Office', 'Construction', 'Production', 'Drive', 'Carpool', 
    'Transit', 'Walk', 'OtherTransp', 'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 
    'PublicWork', 'SelfEmployed', 'FamilyWork', 'Unemployment', 'Median Home Value',
    'Studio Units', '1-BR Units', '2-BR Units', '3-BR Units', '4-BR Units', '5-BR Units',
    '6-BR+ Units', 'Unknown-BR Units', 'Total Units_build'
]

# Drop 
almost_final_ML = almost_final_ML[selected_features + ['Income Level']]
almost_final_ML = almost_final_ML.dropna()

# Encode the target variable
label_encoder = LabelEncoder()
almost_final_ML['Income Level'] = label_encoder.fit_transform(almost_final_ML['Income Level'])

# Split the data into features and target
X = almost_final_ML.drop(columns=['Income Level'])
y = almost_final_ML['Income Level']

# Standardize the data
numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X[numerical_columns])

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Graphing PCA
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y, palette='viridis', alpha=0.6)
plt.title('PCA of Income Levels')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Income Level')
plt.show()

# KMeans Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_pca)

# Silhouette Score
silhouette_avg = silhouette_score(X_pca, labels)
print(f'Silhouette Score: {silhouette_avg}')

# Plotting the clustering result
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels, palette='viridis', alpha=0.6)
plt.title('KMeans Clustering of Income Levels')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title='Cluster')
plt.show()


'''
Silhouette Score: 0.4560338078654233

'''


#%% EXTRA MAP with GEOPANDAS


import geopandas as gpd
import folium
from folium import Choropleth

# Load the MODZCTA GeoJSON file
zcta_url = "https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?method=export&format=GeoJSON"
zcta_geo = gpd.read_file(zcta_url)


zcta_geo = zcta_geo.to_crs(epsg=4326)


final_merged_cleaned['ZipCode'] = final_merged_cleaned['ZipCode'].astype(str)


income_by_zip = final_merged_cleaned.groupby('ZipCode')['Income'].mean().reset_index()
income_by_zip.rename(columns={'ZipCode': 'modzcta', 'Income': 'average_income'}, inplace=True)

zcta_geo = zcta_geo.merge(income_by_zip, on='modzcta', how='left')

m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)


Choropleth(
    geo_data=zcta_geo,
    data=zcta_geo,
    columns=['modzcta', 'average_income'],
    key_on='feature.properties.modzcta',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Income'
).add_to(m)


m.save('nyc_income_by_zip_map.html')
m

