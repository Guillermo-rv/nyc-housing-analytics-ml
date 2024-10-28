# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 20:58:42 2024

@author: guill
"""

'''


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

ny_build = pd.read_csv('housing-new-york-units-by-building.csv')

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

ny_project = pd.read_csv('housing-new-york-units-by-project.csv')

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

'''
For your project, focusing on supervised and unsupervised analysis using the New York housing dataset, here are some ideas for classification, regression, and clustering problems:

### Supervised Analysis

#### Classification Problem
1. **Predicting Building Completion Status**:
   - **Objective**: Predict whether a building project is completed or not.
   - **Target Variable**: `Project Completion Date` (transformed to a binary variable: completed/not completed).
   - **Features**: `Borough`, `Program Group`, `Project Start Date`, `Community Board`, `Council District`, `Reporting Construction Type`, and various income unit counts (`Extremely Low Income Units`, `Very Low Income Units`, etc.).

2. **Predicting Reporting Construction Type**:
   - **Objective**: Predict whether a building is categorized as 'New Construction' or 'Preservation'.
   - **Target Variable**: `Reporting Construction Type`.
   - **Features**: `Borough`, `Program Group`, `Project Start Date`, `Community Board`, `Council District`, `Total Units`, and various income unit counts.

#### Regression Problem
1. **Predicting Total Units in a Building**:
   - **Objective**: Predict the total number of units in a building.
   - **Target Variable**: `Total Units`.
   - **Features**: `Borough`, `Program Group`, `Project Start Date`, `Community Board`, `Council District`, `Latitude`, `Longitude`, `Building Completion Date`, and various income unit counts.

2. **Predicting Completion Time for Projects**:
   - **Objective**: Predict the time taken to complete a project.
   - **Target Variable**: `Project Completion Date` - `Project Start Date` (duration in days).
   - **Features**: `Borough`, `Program Group`, `Community Board`, `Council District`, `Total Units`, `Reporting Construction Type`, and various income unit counts.

### Unsupervised Analysis

#### Clustering
1. **Clustering Buildings Based on Unit Types and Sizes**:
   - **Objective**: Identify clusters of buildings with similar unit distributions.
   - **Features**: `Studio Units`, `1-BR Units`, `2-BR Units`, `3-BR Units`, `4-BR Units`, `5-BR Units`, `6-BR+ Units`, `Unknown-BR Units`.

2. **Clustering Projects Based on Geographic and Economic Characteristics**:
   - **Objective**: Identify clusters of projects based on their geographical location and economic characteristics.
   - **Features**: `Borough`, `Latitude`, `Longitude`, `Program Group`, `Total Units`, and various income unit counts.

### Extra Analysis (Complex Model / Model Not Studied in Class)
1. **Time Series Forecasting for Project Starts or Completions**:
   - **Objective**: Forecast the number of projects starting or completing over time.
   - **Target Variable**: `Project Start Date` or `Project Completion Date` aggregated by month or year.
   - **Features**: Historical counts of project starts/completions, `Borough`, `Program Group`.

2. **Geospatial Analysis with Geographic Information Systems (GIS)**:
   - **Objective**: Analyze and visualize the geographic distribution of affordable housing units across different boroughs.
   - **Tools**: Using `geopandas` and `folium` for advanced geospatial visualizations and spatial clustering.

These ideas can be further refined based on your data exploration and specific interests. Each of these problems addresses key aspects of the dataset and offers valuable insights into housing projects in New York.

'''


#%%

# Display basic information about ny_build
print("Housing New York Units by Building (ny_build):")
print(ny_build.info())
print(ny_build.describe())
print("Missing values in ny_build:")
print(ny_build.isnull().sum())

# Display basic information about ny_project
print("\nHousing New York Units by Project (ny_project):")
print(ny_project.info())
print(ny_project.describe())
print("Missing values in ny_project:")
print(ny_project.isnull().sum())

# Basic statistics for numerical columns in ny_build
ny_build_numerical_stats = ny_build.describe()
print(ny_build_numerical_stats)

# Distribution and unique counts of categorical columns in ny_build
ny_build_categorical_distribution = ny_build.select_dtypes(include='object').apply(lambda x: x.value_counts())
print(ny_build_categorical_distribution)

# Handling missing values in ny_build
ny_build_missing_values = ny_build.isnull().sum()
print(ny_build_missing_values)

# Basic statistics for numerical columns in ny_project
ny_project_numerical_stats = ny_project.describe()
print(ny_project_numerical_stats)

# Distribution and unique counts of categorical columns in ny_project
ny_project_categorical_distribution = ny_project.select_dtypes(include='object').apply(lambda x: x.value_counts())
print(ny_project_categorical_distribution)

# Handling missing values in ny_project
ny_project_missing_values = ny_project.isnull().sum()
print(ny_project_missing_values)


#%%

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Handling missing values and encoding categorical variables for ny_build
numerical_features_build = ny_build.select_dtypes(include=['int64', 'float64']).columns
categorical_features_build = ny_build.select_dtypes(include=['object']).columns

numerical_transformer_build = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer_build = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor_build = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer_build, numerical_features_build),
        ('cat', categorical_transformer_build, categorical_features_build)
    ])

ny_build_processed = preprocessor_build.fit_transform(ny_build)

# Handling missing values and encoding categorical variables for ny_project
numerical_features_project = ny_project.select_dtypes(include=['int64', 'float64']).columns
categorical_features_project = ny_project.select_dtypes(include=['object']).columns

numerical_transformer_project = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer_project = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor_project = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer_project, numerical_features_project),
        ('cat', categorical_transformer_project, categorical_features_project)
    ])

ny_project_processed = preprocessor_project.fit_transform(ny_project)

# Displaying the shape of processed datasets
print(f"Processed ny_build shape: {ny_build_processed.shape}")
print(f"Processed ny_project shape: {ny_project_processed.shape}")


#%%

import matplotlib.pyplot as plt

# Plot histograms for numerical columns in ny_build
ny_build.select_dtypes(include='number').hist(figsize=(15, 15), bins=20, edgecolor='black')
plt.suptitle('Distributions of Numerical Columns in Housing New York Units by Building', y=1.02)
plt.show()

# Bar plots for categorical columns in ny_build
categorical_columns = ['Project Name', 'Program Group', 'Borough', 'Community Board', 'Council District', 'Census Tract', 'NTA - Neighborhood Tabulation Area', 'Reporting Construction Type', 'Extended Affordability Only', 'Prevailing Wage Status']

# Due to the large number of unique values in some columns, we will plot the top 10 most frequent values for each categorical column
for column in categorical_columns:
    plt.figure(figsize=(10, 5))
    ny_build[column].value_counts().nlargest(10).plot(kind='bar', edgecolor='black')
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()
    
# Plot histograms for numerical columns in ny_project
ny_project.select_dtypes(include='number').hist(figsize=(15, 15), bins=20, edgecolor='black')
plt.suptitle('Distributions of Numerical Columns in Housing New York Units by Project', y=1.02)
plt.show()

# Bar plots for categorical columns in ny_project
categorical_columns_project = ['Project Name', 'Extended Affordability Only', 'Prevailing Wage Status', 'Planned Tax Benefit']

# Due to the large number of unique values in some columns, we will plot the top 10 most frequent values for each categorical column
for column in categorical_columns_project:
    plt.figure(figsize=(10, 5))
    ny_project[column].value_counts().nlargest(10).plot(kind='bar', edgecolor='black')
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

#%%

import seaborn as sns

# Correlation matrix for numerical columns in ny_build
correlation_matrix_build = ny_build.select_dtypes(include='number').corr()

plt.figure(figsize=(15, 15))
plt.title('Correlation Matrix for Numerical Columns in Housing New York Units by Building')
sns.heatmap(correlation_matrix_build, annot=True, fmt='.2f', cmap='coolwarm', square=True)
plt.show()

# Correlation matrix for numerical columns in ny_project
correlation_matrix_project = ny_project.select_dtypes(include='number').corr()

plt.figure(figsize=(15, 15))
plt.title('Correlation Matrix for Numerical Columns in Housing New York Units by Project')
sns.heatmap(correlation_matrix_project, annot=True, fmt='.2f', cmap='coolwarm', square=True)
plt.show()


#%%

import pandas as pd
import geopandas as gpd
import folium

# Ensure Latitude and Longitude are numeric in ny_build
ny_build['Latitude'] = pd.to_numeric(ny_build['Latitude'], errors='coerce')
ny_build['Longitude'] = pd.to_numeric(ny_build['Longitude'], errors='coerce')

# Drop rows with missing coordinates in ny_build
ny_build_geo = ny_build.dropna(subset=['Latitude', 'Longitude'])

# Debugging: Print the first few rows to check the coordinates
print("First few rows of ny_build_geo:")
print(ny_build_geo[['Latitude', 'Longitude']].head())

# Create GeoDataFrame for ny_build
try:
    ny_build_geo = gpd.GeoDataFrame(
        ny_build_geo,
        geometry=gpd.points_from_xy(ny_build_geo.Longitude, ny_build_geo.Latitude),
        crs="EPSG:4326"
    )
    print("GeoDataFrame for ny_build created successfully")
except Exception as e:
    print(f"Error creating GeoDataFrame for ny_build: {e}")

# Merge ny_project with ny_build to get geographical information
ny_project_geo = ny_project.merge(
    ny_build[['Project ID', 'Latitude', 'Longitude']],
    on='Project ID',
    how='left'
)

# Ensure Latitude and Longitude are numeric in ny_project_geo
ny_project_geo['Latitude'] = pd.to_numeric(ny_project_geo['Latitude'], errors='coerce')
ny_project_geo['Longitude'] = pd.to_numeric(ny_project_geo['Longitude'], errors='coerce')

# Drop rows with missing coordinates in ny_project
ny_project_geo = ny_project_geo.dropna(subset=['Latitude', 'Longitude'])

# Debugging: Print the first few rows to check the coordinates
print("First few rows of ny_project_geo:")
print(ny_project_geo[['Latitude', 'Longitude']].head())

# Create GeoDataFrame for ny_project
try:
    ny_project_geo = gpd.GeoDataFrame(
        ny_project_geo,
        geometry=gpd.points_from_xy(ny_project_geo.Longitude, ny_project_geo.Latitude),
        crs="EPSG:4326"
    )
    print("GeoDataFrame for ny_project created successfully")
except Exception as e:
    print(f"Error creating GeoDataFrame for ny_project: {e}")

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add ny_build_geo points to the map
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=3,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=row['Project Name']
    ).add_to(m)

# Add ny_project_geo points to the map
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=(row['Latitude'], row['Longitude']),
        radius=3,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=row['Project Name']
    ).add_to(m)

# Save map to HTML file
m.save('nyc_housing_projects_map.html')

# Display the map
m

import pandas as pd
import geopandas as gpd
import shapely
import folium
import fiona
import pyproj
import rtree

print(f"Pandas version: {pd.__version__}")
print(f"GeoPandas version: {gpd.__version__}")
print(f"Shapely version: {shapely.__version__}")
print(f"Folium version: {folium.__version__}")
print(f"Fiona version: {fiona.__version__}")
print(f"PyProj version: {pyproj.__version__}")
print(f"RTree version: {rtree.__version__}")


#%%

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Example target variable: 'Total Units'
X = ny_build_processed
y = ny_build['Total Units']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

#%%

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Example: clustering based on numerical features in ny_build
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(ny_build_processed)

# Add cluster labels to the original dataframe
ny_build['Cluster'] = kmeans.labels_

# Visualize the clusters
plt.scatter(ny_build['Longitude'], ny_build['Latitude'], c=ny_build['Cluster'], cmap='viridis')
plt.title('KMeans Clustering of Buildings')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#%%

import geopandas as gpd
import matplotlib.pyplot as plt

# Load the New York City borough boundaries dataset
# Replace this path with the path to your local file or a URL to a dataset
ny_boroughs_url = "https://data.cityofnewyork.us/resource/7t3b-ywvw.geojson"
ny_boroughs = gpd.read_file(ny_boroughs_url)

# Inspect the first few rows
print(ny_boroughs.head())

# Plot the borough boundaries
ny_boroughs.plot(edgecolor='black', facecolor='lightgray', figsize=(10, 10))
plt.title('New York City Boroughs')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


#%% AQUÍ YA BIEN


import geopandas as gpd
import matplotlib.pyplot as plt

# Load the New York City borough boundaries dataset
ny_boroughs_url = "https://data.cityofnewyork.us/resource/7t3b-ywvw.geojson"
ny_boroughs = gpd.read_file(ny_boroughs_url)

# Plot the borough boundaries with enhanced styling
fig, ax = plt.subplots(figsize=(10, 10))
ny_boroughs.plot(ax=ax, edgecolor='black', facecolor='lightgray', linewidth=1)
plt.title('New York City Boroughs', fontsize=15)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True)
plt.show()

#%% 

# Ensure that your `ny_build` and `ny_project` GeoDataFrames are created

# Plot boroughs with custom styling and add points from `ny_build` and `ny_project`
fig, ax = plt.subplots(figsize=(10, 10))
ny_boroughs.plot(ax=ax, edgecolor='black', facecolor='lightgray', linewidth=1)

# Plot `ny_build` points
ny_build_geo.plot(ax=ax, markersize=5, color='blue', label='Building Projects')

# Plot `ny_project` points
ny_project_geo.plot(ax=ax, markersize=5, color='red', label='Project Locations')

plt.title('New York City Map with Projects', fontsize=15)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()


#%%

import seaborn as sns

# Create a heatmap of building projects
fig, ax = plt.subplots(figsize=(10, 10))
ny_boroughs.plot(ax=ax, edgecolor='black', facecolor='lightgray', linewidth=1)

# Extract coordinates
x = ny_build_geo.geometry.x
y = ny_build_geo.geometry.y

# Create the heatmap
sns.kdeplot(x, y, ax=ax, cmap='Reds', shade=True, alpha=0.6, zorder=10)

plt.title('Heatmap of Building Projects in New York City', fontsize=15)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True)
plt.show()

#%%

import matplotlib.pyplot as plt

# Assuming `ny_boroughs` has a 'population' column for demonstration purposes
ny_boroughs['population'] = [100000, 200000, 300000, 400000, 500000]  # Replace with actual data

# Plot the choropleth map
fig, ax = plt.subplots(figsize=(10, 10))
ny_boroughs.plot(column='population', ax=ax, legend=True, cmap='OrRd', edgecolor='black', linewidth=1)
plt.title('Choropleth Map of Population in New York City Boroughs', fontsize=15)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True)
plt.show()

#%%

import folium

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add borough boundaries to the map
folium.GeoJson(ny_boroughs).add_to(m)

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=row['Project Name']
    ).add_to(m)

# Add points from ny_project_geo
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=row['Project Name']
    ).add_to(m)

# Save and display the map
m.save('nyc_housing_projects_interactive_map.html')
m


#%%

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame for the coordinates
coordinates = pd.DataFrame({'x': ny_build_geo.geometry.x, 'y': ny_build_geo.geometry.y})

# Create a heatmap of building projects
fig, ax = plt.subplots(figsize=(10, 10))
ny_boroughs.plot(ax=ax, edgecolor='black', facecolor='lightgray', linewidth=1)

# Create the heatmap
sns.kdeplot(data=coordinates, x='x', y='y', ax=ax, cmap='Reds', shade=True, alpha=0.6, zorder=10)

plt.title('Heatmap of Building Projects in New York City', fontsize=15)
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True)
plt.show()

#%%

import folium

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add borough boundaries to the map
folium.GeoJson(ny_boroughs, name='Boroughs').add_to(m)

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Name: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add points from ny_project_geo
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Name: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_housing_projects_interactive_map.html')
m

#%%

print(ny_build_geo[['Latitude', 'Longitude']].head())
print(ny_project_geo[['Latitude', 'Longitude']].head())

import folium

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add borough boundaries to the map
boroughs = folium.GeoJson(ny_boroughs, name='Boroughs')
boroughs.add_to(m)

# Display the map to verify borough boundaries are plotted correctly
m.save('nyc_housing_projects_boroughs_map.html')
m

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add points from ny_project_geo
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Location: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_housing_projects_interactive_map.html')
m

#%% 



from selenium import webdriver
import time

# Path to your chromedriver
chromedriver_path = '/path/to/chromedriver'

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add borough boundaries to the map
folium.GeoJson(ny_boroughs, name='Boroughs').add_to(m)

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add points from ny_project_geo
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Location: {row['Project Name']}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
map_file = 'nyc_housing_projects_interactive_map.html'
m.save(map_file)

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--window-size=1200x800')  # Set window size

driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(f'file://{map_file}')

# Function to capture a screenshot
def capture_screenshot(filename):
    driver.save_screenshot(filename)

# Capture initial screenshot
capture_screenshot('screenshot1.png')

# Optionally, capture additional screenshots with different zoom levels or positions
# Example: Change the zoom level and capture another screenshot
driver.execute_script('map.setZoom(12);')
time.sleep(2)  # Wait for the map to re-render
capture_screenshot('screenshot2.png')

# Close the browser
driver.quit()

sudo apt-get install ffmpeg  # On Linux
brew install ffmpeg          # On MacOS

ffmpeg -framerate 1 -i screenshot%d.png -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4

#%%


import geopandas as gpd

# Load the borough boundaries
ny_boroughs_url = "https://data.cityofnewyork.us/resource/7t3b-ywvw.geojson"
ny_boroughs = gpd.read_file(ny_boroughs_url)

# Ensure both GeoDataFrames are in the same coordinate reference system
ny_boroughs = ny_boroughs.to_crs(epsg=4326)
ny_build_geo = ny_build_geo.to_crs(epsg=4326)
ny_project_geo = ny_project_geo.to_crs(epsg=4326)

# Spatial join to add borough information to ny_build_geo
ny_build_geo = gpd.sjoin(ny_build_geo, ny_boroughs, how='left', op='within')

# Spatial join to add borough information to ny_project_geo
ny_project_geo = gpd.sjoin(ny_project_geo, ny_boroughs, how='left', op='within')

# Check the new columns
print(ny_build_geo.columns)
print(ny_project_geo.columns)

# STEP2 

# Calculate the number of projects in each borough
ny_boroughs['num_projects'] = ny_boroughs.geometry.apply(
    lambda borough: ny_build_geo.within(borough).sum()
)

# Print the updated boroughs with project counts
print(ny_boroughs[['boro_name', 'num_projects']])

# Define the coordinates of a central point (e.g., Manhattan)
from shapely.geometry import Point
central_point = Point(-73.9712, 40.7831)  # Central Park, Manhattan

# Calculate the distance from each project to the central point
ny_build_geo['distance_to_central'] = ny_build_geo.geometry.apply(lambda x: x.distance(central_point))
ny_project_geo['distance_to_central'] = ny_project_geo.geometry.apply(lambda x: x.distance(central_point))

# Normalize the distances
ny_build_geo['distance_to_central_normalized'] = (ny_build_geo['distance_to_central'] - ny_build_geo['distance_to_central'].min()) / (ny_build_geo['distance_to_central'].max() - ny_build_geo['distance_to_central'].min())
ny_project_geo['distance_to_central_normalized'] = (ny_project_geo['distance_to_central'] - ny_project_geo['distance_to_central'].min()) / (ny_project_geo['distance_to_central'].max() - ny_project_geo['distance_to_central'].min())

# Example weights for combining factors
weight_num_projects = 0.5
weight_distance = 0.5

# Create the investment potential score
ny_build_geo = ny_build_geo.join(ny_boroughs.set_index('boro_name')['num_projects'], on='boro_name')
ny_build_geo['investment_potential'] = (weight_num_projects * ny_build_geo['num_projects'] + 
                                        weight_distance * (1 - ny_build_geo['distance_to_central_normalized']))

ny_project_geo = ny_project_geo.join(ny_boroughs.set_index('boro_name')['num_projects'], on='boro_name')
ny_project_geo['investment_potential'] = (weight_num_projects * ny_project_geo['num_projects'] + 
                                          weight_distance * (1 - ny_project_geo['distance_to_central_normalized']))

# Print the new column to verify
print(ny_build_geo[['Project Name', 'investment_potential']].head())
print(ny_project_geo[['Project Name', 'investment_potential']].head())

# STEP 3

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Features and target variable
X = ny_build_geo[['Latitude', 'Longitude', 'distance_to_central_normalized']]
y = ny_build_geo['investment_potential']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# STEP 4

import folium
from folium import Choropleth

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add borough boundaries to the map
folium.GeoJson(ny_boroughs, name='Boroughs').add_to(m)

# Add points from ny_build_geo with investment potential
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=f"{row['Project Name']}: {row['investment_potential']:.2f}"
    ).add_to(m)

# Add points from ny_project_geo with investment potential
for idx, row in ny_project_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Location: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=f"{row['Project Name']}: {row['investment_potential']:.2f}"
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_map.html')
m


#%%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the MODZCTA CSV file
modzcta = pd.read_csv('Modified_Zip_Code_Tabulation_Areas__MODZCTA__20240630.csv')

# Display the first few rows to understand its structure
print(modzcta.head())


# Create a GeoDataFrame
geometry = [Point(xy) for xy in zip(modzcta['Longitude'], modzcta['Latitude'])]
modzcta_geo = gpd.GeoDataFrame(modzcta, geometry=geometry)

# Ensure the CRS matches
modzcta_geo = modzcta_geo.set_crs(epsg=4326)

# Display the GeoDataFrame
print(modzcta_geo.head())

#%%

import geopandas as gpd
import folium

# Load the MODZCTA GeoJSON file
modzcta_url = 'https://data.cityofnewyork.us/resource/pri4-ifjk.geojson'
modzcta = gpd.read_file(modzcta_url)

# Ensure the CRS matches
modzcta = modzcta.to_crs(epsg=4326)
ny_build_geo = ny_build_geo.to_crs(epsg=4326)
ny_project_geo = ny_project_geo.to_crs(epsg=4326)

# Display the GeoDataFrame
print(modzcta.head())

#%%

import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point

# Load the ZCTA (ZIP Code Tabulation Areas) data
zcta_url = "https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?method=export&format=GeoJSON"
zcta_geo = gpd.read_file(zcta_url)

# Ensure the ZCTA GeoDataFrame is in the correct CRS
zcta_geo = zcta_geo.to_crs(epsg=4326)

# Load the existing datasets
ny_build = pd.read_csv('housing-new-york-units-by-building.csv')
ny_project = pd.read_csv('housing-new-york-units-by-project.csv')

# Convert the existing datasets to GeoDataFrames
ny_build_geo = gpd.GeoDataFrame(
    ny_build,
    geometry=gpd.points_from_xy(ny_build.Longitude, ny_build.Latitude),
    crs="EPSG:4326"
)

# Join the building data with ZCTA data to get ZIP codes
ny_build_geo = gpd.sjoin(ny_build_geo, zcta_geo[['modzcta', 'geometry']], how='left', op='within')

# Calculate the number of projects in each ZIP code
zcta_geo['num_projects'] = zcta_geo.apply(
    lambda row: ny_build_geo[ny_build_geo['modzcta'] == row['modzcta']].shape[0], axis=1
)

# Define the coordinates of a central point (e.g., Central Park, Manhattan)
central_point = Point(-73.9712, 40.7831)

# Calculate the distance from each project to the central point
ny_build_geo['distance_to_central'] = ny_build_geo.geometry.apply(lambda x: x.distance(central_point))

# Normalize the distances
ny_build_geo['distance_to_central_normalized'] = (ny_build_geo['distance_to_central'] - ny_build_geo['distance_to_central'].min()) / (ny_build_geo['distance_to_central'].max() - ny_build_geo['distance_to_central'].min())

# Calculate the investment potential score
weight_num_projects = 0.7
weight_distance_to_central = 0.3

ny_build_geo['investment_potential'] = (weight_num_projects * ny_build_geo['num_projects'] + weight_distance_to_central * (1 - ny_build_geo['distance_to_central_normalized']))

# Create a map to visualize the investment potential
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add ZCTA boundaries to the map
folium.GeoJson(zcta_geo, name='ZIP Codes').add_to(m)

# Add points from ny_build_geo with investment potential
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Project Name: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_map.html')
m

#%% FINAL FUNCIONA GENIAL

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load the housing datasets
ny_build = pd.read_csv('/mnt/data/housing-new-york-units-by-building.csv')
ny_project = pd.read_csv('/mnt/data/housing-new-york-units-by-project.csv')

# Clean and preprocess the data
ny_build['Latitude'] = pd.to_numeric(ny_build['Latitude'], errors='coerce')
ny_build['Longitude'] = pd.to_numeric(ny_build['Longitude'], errors='coerce')
ny_build = ny_build.dropna(subset=['Latitude', 'Longitude'])

ny_project['Project Start Date'] = pd.to_datetime(ny_project['Project Start Date'])
ny_project['Project Completion Date'] = pd.to_datetime(ny_project['Project Completion Date'], errors='coerce')

# Ensure unique identifiers for merging
ny_build['Project ID'] = ny_build['Project ID'].astype(int)
ny_project['Project ID'] = ny_project['Project ID'].astype(int)

#STEP 2
# Load the MODZCTA GeoJSON file
zcta_url = "https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?method=export&format=GeoJSON"
zcta_geo = gpd.read_file(zcta_url)

# Ensure the ZCTA GeoDataFrame is in the correct CRS
zcta_geo = zcta_geo.to_crs(epsg=4326)

# Create GeoDataFrame for ny_build
ny_build_geo = gpd.GeoDataFrame(
    ny_build,
    geometry=gpd.points_from_xy(ny_build.Longitude, ny_build.Latitude),
    crs="EPSG:4326"
)

# Spatial join to get the zip code for each building
ny_build_geo = gpd.sjoin(ny_build_geo, zcta_geo[['modzcta', 'geometry']], how='left', op='within')

#STEP 3

# Calculate the number of projects in each ZIP code
zcta_project_counts = ny_build_geo.groupby('modzcta').size().reset_index(name='num_projects')

# Merge this information back to the ny_build_geo GeoDataFrame
ny_build_geo = ny_build_geo.merge(zcta_project_counts, on='modzcta', how='left')

# STEP 4

# Define the coordinates of a central point (e.g., Central Park, Manhattan)
central_point = Point(-73.9712, 40.7831)

# Calculate the distance from each project to the central point
ny_build_geo['distance_to_central'] = ny_build_geo.geometry.apply(lambda x: x.distance(central_point))

# Normalize the distances
ny_build_geo['distance_to_central_normalized'] = (ny_build_geo['distance_to_central'] - ny_build_geo['distance_to_central'].min()) / (ny_build_geo['distance_to_central'].max() - ny_build_geo['distance_to_central'].min())

# STEP 5

# Example weights for combining factors
weight_num_projects = 0.7
weight_distance_to_central = 0.3

# Create the investment potential score
ny_build_geo['investment_potential'] = (weight_num_projects * ny_build_geo['num_projects'] +
                                        weight_distance_to_central * (1 - ny_build_geo['distance_to_central_normalized']))

# Print the new column to verify
print(ny_build_geo[['Project Name', 'investment_potential']].head())

# STEP 6

import folium

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add MODZCTA boundaries to the map
folium.GeoJson(zcta_geo, name='ZIP Codes').add_to(m)

# Add points from ny_build_geo with investment potential
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_map.html')
m

# Heatmap
import folium
from folium.plugins import HeatMap

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add MODZCTA boundaries to the map
folium.GeoJson(zcta_geo, name='ZIP Codes').add_to(m)

# Add points from ny_build_geo with investment potential
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Prepare data for the heatmap
heat_data = [[row['Latitude'], row['Longitude'], row['investment_potential']] for index, row in ny_build_geo.iterrows()]

# Add heatmap layer
HeatMap(heat_data, radius=15, blur=10).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_heatmap.html')
m

#%% HOME VALUES DATA

home_values = {
    '10001': 595119, '10002': 741081, '10003': 974174, '10004': 1609370, '10005': 1399537,
    '10006': 937889, '10007': 2000001, '10009': 614907, '10010': 1002005, '10011': 1028447,
    '10012': 1692582, '10013': 2000001, '10014': 1265169, '10016': 889414, '10017': 802031,
    '10018': 669003, '10019': 876389, '10021': 1534396, '10022': 1059881, '10023': 1354744,
    '10024': 1631854, '10025': 1036547, '10026': 942611, '10027': 796538, '10028': 1403429,
    '10029': 559102, '10031': 532201, '10033': 616807, '10034': 425584, '10035': 637362,
    '10036': 1215522, '10037': 183332, '10038': 800285, '10039': 494810, '10040': 417461,
    '10044': 966347, '10065': 1279631, '10069': 1895326, '10075': 1102100, '10128': 1178137,
    '10280': 846150, '10301': 560236, '10302': 457418, '10303': 379690, '10304': 563088,
    '10305': 543037, '10306': 586474, '10307': 762582, '10308': 591055, '10309': 625525,
    '10310': 560265, '10312': 602853, '10314': 585903, '10453': 492427, '10456': 394515,
    '10458': 432607, '10459': 482720, '10460': 490637, '10461': 529312, '10462': 394749,
    '10463': 319313, '10464': 527389, '10465': 535795, '10466': 496034, '10467': 326265,
    '10468': 241157, '10469': 519873, '10470': 500614, '10471': 375162, '10472': 546453,
    '10473': 468947, '10474': 304911, '10475': 79612, '11001': 610323, '11004': 547073,
    '11005': 655877, '11101': 967206, '11102': 762607, '11103': 925316, '11104': 528147,
    '11105': 934617, '11106': 596918, '11201': 1034844, '11203': 541029, '11204': 968833,
    '11205': 811437, '11206': 803137, '11207': 546514, '11208': 549761, '11209': 820894,
    '11210': 724473, '11211': 1003101, '11212': 458230, '11213': 899994, '11214': 831544,
    '11215': 1448428, '11216': 1195924, '11217': 1390350, '11218': 820555, '11219': 965633,
    '11220': 849100, '11221': 945181, '11222': 1183646, '11223': 927077, '11224': 459485,
    '11225': 1057129, '11226': 675822, '11228': 990893, '11229': 702628, '11230': 775239,
    '11231': 1470549, '11232': 809286, '11233': 936902, '11234': 641396, '11235': 609460,
    '11236': 600089, '11237': 918023, '11238': 1028046, '11239': 477906, '11354': 529896,
    '11355': 624967, '11356': 737219, '11357': 819469, '11358': 859340, '11360': 607074,
    '11361': 765249, '11362': 505712, '11363': 840144, '11364': 672962, '11365': 784347,
    '11366': 833383, '11367': 541840, '11368': 655706, '11369': 570575, '11370': 760551,
    '11372': 383746, '11373': 611430, '11374': 441326, '11375': 495863, '11377': 581711,
    '11378': 711948, '11379': 772984, '11385': 715264, '11411': 487537, '11412': 509318,
    '11413': 528972, '11414': 526515, '11415': 309426, '11416': 622160, '11417': 613491,
    '11418': 625441, '11419': 600486, '11420': 588961, '11421': 597916, '11422': 514115,
    '11423': 602872, '11426': 595833, '11427': 589180, '11428': 593526, '11429': 519989,
    '11432': 673520, '11433': 489837, '11434': 458331, '11435': 447268, '11436': 498700,
    '11691': 559031, '11692': 471562, '11693': 403836, '11694': 704329, '11697': 612345
}


# Add home value data to the GeoDataFrame
ny_build_geo['home_value'] = ny_build_geo['modzcta'].map(home_values)
ny_build_geo['home_value'].fillna(ny_build_geo['home_value'].mean(), inplace=True)

# Verify the addition
print(ny_build_geo[['modzcta', 'home_value']].head())

# Adjust weights for combining factors
weight_num_projects = 0.5
weight_distance_to_central = 0.2
weight_home_value = 0.3

# Recalculate the investment potential score
ny_build_geo['investment_potential'] = (weight_num_projects * ny_build_geo['num_projects'] +
                                        weight_distance_to_central * (1 - ny_build_geo['distance_to_central_normalized']) +
                                        weight_home_value * ny_build_geo['home_value'])

# Verify the new investment potential scores
print(ny_build_geo[['Project Name', 'investment_potential']].head())

import folium
from folium.plugins import HeatMap

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add MODZCTA boundaries to the map
folium.GeoJson(zcta_geo, name='ZIP Codes').add_to(m)

# Add points from ny_build_geo with investment potential
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Prepare data for the heatmap
heat_data = [[row['Latitude'], row['Longitude'], row['investment_potential']] for index, row in ny_build_geo.iterrows()]

# Add heatmap layer
HeatMap(heat_data, radius=15, blur=10).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to


#%% HEATMAP COLOREADO  POR ZONAS 


import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium import Choropleth

# Load the housing datasets
ny_build = pd.read_csv('/mnt/data/housing-new-york-units-by-building.csv')
ny_project = pd.read_csv('/mnt/data/housing-new-york-units-by-project.csv')

# Load the MODZCTA GeoJSON file
zcta_url = "https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?method=export&format=GeoJSON"
zcta_geo = gpd.read_file(zcta_url)

# Ensure the ZCTA GeoDataFrame is in the correct CRS
zcta_geo = zcta_geo.to_crs(epsg=4326)

# Clean and preprocess the ny_build data
ny_build['Latitude'] = pd.to_numeric(ny_build['Latitude'], errors='coerce')
ny_build['Longitude'] = pd.to_numeric(ny_build['Longitude'], errors='coerce')
ny_build = ny_build.dropna(subset=['Latitude', 'Longitude'])

# Create GeoDataFrame for ny_build
ny_build_geo = gpd.GeoDataFrame(
    ny_build,
    geometry=gpd.points_from_xy(ny_build.Longitude, ny_build.Latitude),
    crs="EPSG:4326"
)

# Spatial join to get the zip code for each building
ny_build_geo = gpd.sjoin(ny_build_geo, zcta_geo[['modzcta', 'geometry']], how='left', predicate='within')

# Calculate the number of projects in each ZIP code and add it to ny_build_geo
zcta_project_counts = ny_build_geo.groupby('modzcta').size().reset_index(name='num_projects')
ny_build_geo = ny_build_geo.merge(zcta_project_counts, on='modzcta', how='left')

# STEP 2

# Define the coordinates of a central point (e.g., Central Park, Manhattan)
central_point = Point(-73.9712, 40.7831)

# Calculate the distance from each project to the central point
ny_build_geo['distance_to_central'] = ny_build_geo.geometry.apply(lambda x: x.distance(central_point))

# Normalize the distances
ny_build_geo['distance_to_central_normalized'] = (ny_build_geo['distance_to_central'] - ny_build_geo['distance_to_central'].min()) / (ny_build_geo['distance_to_central'].max() - ny_build_geo['distance_to_central'].min())

# Example home values dictionary
home_values = {
    '10001': 595119, '10002': 741081, '10003': 974174, '10004': 1609370, '10005': 1399537,
    '10006': 937889, '10007': 2000001, '10009': 614907, '10010': 1002005, '10011': 1028447,
    '10012': 1692582, '10013': 2000001, '10014': 1265169, '10016': 889414, '10017': 802031,
    '10018': 669003, '10019': 876389, '10021': 1534396, '10022': 1059881, '10023': 1354744,
    '10024': 1631854, '10025': 1036547, '10026': 942611, '10027': 796538, '10028': 1403429,
    '10029': 559102, '10031': 532201, '10033': 616807, '10034': 425584, '10035': 637362,
    '10036': 1215522, '10037': 183332, '10038': 800285, '10039': 494810, '10040': 417461,
    '10044': 966347, '10065': 1279631, '10069': 1895326, '10075': 1102100, '10128': 1178137,
    '10280': 846150, '10301': 560236, '10302': 457418, '10303': 379690, '10304': 563088,
    '10305': 543037, '10306': 586474, '10307': 762582, '10308': 591055, '10309': 625525,
    '10310': 560265, '10312': 602853, '10314': 585903, '10453': 492427, '10456': 394515,
    '10458': 432607, '10459': 482720, '10460': 490637, '10461': 529312, '10462': 394749,
    '10463': 319313, '10464': 527389, '10465': 535795, '10466': 496034, '10467': 326265,
    '10468': 241157, '10469': 519873, '10470': 500614, '10471': 375162, '10472': 546453,
    '10473': 468947, '10474': 304911, '10475': 79612, '11001': 610323, '11004': 547073,
    '11005': 655877, '11101': 967206, '11102': 762607, '11103': 925316, '11104': 528147,
    '11105': 934617, '11106': 596918, '11201': 1034844, '11203': 541029, '11204': 968833,
    '11205': 811437, '11206': 803137, '11207': 546514, '11208': 549761, '11209': 820894,
    '11210': 724473, '11211': 1003101, '11212': 458230, '11213': 899994, '11214': 831544,
    '11215': 1448428, '11216': 1195924, '11217': 1390350, '11218': 820555, '11219': 965633,
    '11220': 849100, '11221': 945181, '11222': 1183646, '11223': 927077, '11224': 459485,
    '11225': 1057129, '11226': 675822, '11228': 990893, '11229': 702628, '11230': 775239,
    '11231': 1470549, '11232': 809286, '11233': 936902, '11234': 641396, '11235': 609460,
    '11236': 600089, '11237': 918023, '11238': 1028046, '11239': 477906, '11354': 529896,
    '11355': 624967, '11356': 737219, '11357': 819469, '11358': 859340, '11360': 607074,
    '11361': 765249, '11362': 505712, '11363': 840144, '11364': 672962, '11365': 784347,
    '11366': 833383, '11367': 541840, '11368': 655706, '11369': 570575, '11370': 760551,
    '11372': 383746, '11373': 611430, '11374': 441326, '11375': 495863, '11377': 581711,
    '11378': 711948, '11379': 772984, '11385': 715264, '11411': 487537, '11412': 509318,
    '11413': 528972, '11414': 526515, '11415': 309426, '11416': 622160, '11417': 613491,
    '11418': 625441, '11419': 600486, '11420': 588961, '11421': 597916, '11422': 514115,
    '11423': 602872, '11426': 595833, '11427': 589180, '11428': 593526, '11429': 519989,
    '11432': 673520, '11433': 489837, '11434': 458331, '11435': 447268, '11436': 498700,
    '11691': 559031, '11692': 471562, '11693': 403836, '11694': 704329, '11697': 612345
}

# Add home value data to the GeoDataFrame
ny_build_geo['home_value'] = ny_build_geo['modzcta'].map(home_values)

# Fill missing home values with the mean home value
ny_build_geo['home_value'].fillna(ny_build_geo['home_value'].mean(), inplace=True)

# Adjust weights for combining factors
weight_num_projects = 0.5
weight_distance_to_central = 0.2
weight_home_value = 0.3

# Create the investment potential score for each building
ny_build_geo['investment_potential'] = (weight_num_projects * ny_build_geo['num_projects'] +
                                        weight_distance_to_central * (1 - ny_build_geo['distance_to_central_normalized']) +
                                        weight_home_value * ny_build_geo['home_value'])

# Aggregate the investment potential by ZIP code
zcta_investment_potential = ny_build_geo.groupby('modzcta')['investment_potential'].mean().reset_index(name='investment_potential')

# Merge this information back to the zcta_geo GeoDataFrame
zcta_geo = zcta_geo.merge(zcta_investment_potential, on='modzcta', how='left')


# STEP 2

import folium
from folium import Choropleth

# Create a base map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add a choropleth layer
Choropleth(
    geo_data=zcta_geo,
    data=zcta_geo,
    columns=['modzcta', 'investment_potential'],
    key_on='feature.properties.modzcta',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Investment Potential'
).add_to(m)

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_choropleth_map.html')
m


#%% RANK

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load datasets
ny_build = pd.read_csv('/mnt/data/housing-new-york-units-by-building.csv')
ny_project = pd.read_csv('/mnt/data/housing-new-york-units-by-project.csv')

# Load the MODZCTA GeoJSON file
zcta_url = "https://data.cityofnewyork.us/api/geospatial/pri4-ifjk?method=export&format=GeoJSON"
zcta_geo = gpd.read_file(zcta_url)

# Ensure the ZCTA GeoDataFrame is in the correct CRS
zcta_geo = zcta_geo.to_crs(epsg=4326)

# Clean and preprocess the ny_build data
ny_build['Latitude'] = pd.to_numeric(ny_build['Latitude'], errors='coerce')
ny_build['Longitude'] = pd.to_numeric(ny_build['Longitude'], errors='coerce')
ny_build = ny_build.dropna(subset=['Latitude', 'Longitude'])

# Create GeoDataFrame for ny_build
ny_build_geo = gpd.GeoDataFrame(
    ny_build,
    geometry=gpd.points_from_xy(ny_build.Longitude, ny_build.Latitude),
    crs="EPSG:4326"
)

# Spatial join to get the zip code for each building
ny_build_geo = gpd.sjoin(ny_build_geo, zcta_geo[['modzcta', 'geometry']], how='left', predicate='within')

# Calculate the number of projects in each ZIP code
zcta_project_counts = ny_build_geo.groupby('modzcta').size().reset_index(name='num_projects')

# Merge this information back to the zcta_geo GeoDataFrame
zcta_geo = zcta_geo.merge(zcta_project_counts, on='modzcta', how='left')

# Define the coordinates of a central point (e.g., Central Park, Manhattan)
central_point = Point(-73.9712, 40.7831)

# Calculate the distance from each project to the central point
ny_build_geo['distance_to_central'] = ny_build_geo.geometry.apply(lambda x: x.distance(central_point))

# Normalize the distances
ny_build_geo['distance_to_central_normalized'] = (ny_build_geo['distance_to_central'] - ny_build_geo['distance_to_central'].min()) / (ny_build_geo['distance_to_central'].max() - ny_build_geo['distance_to_central'].min())

# Example home values dictionary
home_values = {
    '10001': 595119, '10002': 741081, '10003': 974174, '10004': 1609370, '10005': 1399537,
    '10006': 937889, '10007': 2000001, '10009': 614907, '10010': 1002005, '10011': 1028447,
    '10012': 1692582, '10013': 2000001, '10014': 1265169, '10016': 889414, '10017': 802031,
    '10018': 669003, '10019': 876389, '10021': 1534396, '10022': 1059881, '10023': 1354744,
    '10024': 1631854, '10025': 1036547, '10026': 942611, '10027': 796538, '10028': 1403429,
    '10029': 559102, '10031': 532201, '10033': 616807, '10034': 425584, '10035': 637362,
    '10036': 1215522, '10037': 183332, '10038': 800285, '10039': 494810, '10040': 417461,
    '10044': 966347, '10065': 1279631, '10069': 1895326, '10075': 1102100, '10128': 1178137,
    '10280': 846150, '10301': 560236, '10302': 457418, '10303': 379690, '10304': 563088,
    '10305': 543037, '10306': 586474, '10307': 762582, '10308': 591055, '10309': 625525,
    '10310': 560265, '10312': 602853, '10314': 585903, '10453': 492427, '10456': 394515,
    '10458': 432607, '10459': 482720, '10460': 490637, '10461': 529312, '10462': 394749,
    '10463': 319313, '10464': 527389, '10465': 535795, '10466': 496034, '10467': 326265,
    '10468': 241157, '10469': 519873, '10470': 500614, '10471': 375162, '10472': 546453,
    '10473': 468947, '10474': 304911, '10475': 79612, '11001': 610323, '11004': 547073,
    '11005': 655877, '11101': 967206, '11102': 762607, '11103': 925316, '11104': 528147,
    '11105': 934617, '11106': 596918, '11201': 1034844, '11203': 541029, '11204': 968833,
    '11205': 811437, '11206': 803137, '11207': 546514, '11208': 549761, '11209': 820894,
    '11210': 724473, '11211': 1003101, '11212': 458230, '11213': 899994, '11214': 831544,
    '11215': 1448428, '11216': 1195924, '11217': 1390350, '11218': 820555, '11219': 965633,
    '11220': 849100, '11221': 945181, '11222': 1183646, '11223': 927077, '11224': 459485,
    '11225': 1057129, '11226': 675822, '11228': 990893, '11229': 702628, '11230': 775239,
    '11231': 1470549, '11232': 809286, '11233': 936902, '11234': 641396, '11235': 609460,
    '11236': 600089, '11237': 918023, '11238': 1028046, '11239': 477906, '11354': 529896,
    '11355': 624967, '11356': 737219, '11357': 819469, '11358': 859340, '11360': 607074,
    '11361': 765249, '11362': 505712, '11363': 840144, '11364': 672962, '11365': 784347,
    '11366': 833383, '11367': 541840, '11368': 655706, '11369': 570575, '11370': 760551,
    '11372': 383746, '11373': 611430, '11374': 441326, '11375': 495863, '11377': 581711,
    '11378': 711948, '11379': 772984, '11385': 715264, '11411': 487537, '11412': 509318,
    '11413': 528972, '11414': 526515, '11415': 309426, '11416': 622160, '11417': 613491,
    '11418': 625441, '11419': 600486, '11420': 588961, '11421': 597916, '11422': 514115,
    '11423': 602872, '11426': 595833, '11427': 589180, '11428': 593526, '11429': 519989,
    '11432': 673520, '11433': 489837, '11434': 458331, '11435': 447268, '11436': 498700,
    '11691': 559031, '11692': 471562, '11693': 403836, '11694': 704329, '11697': 612345
}

# Add home value data to the GeoDataFrame
ny_build_geo['home_value'] = ny_build_geo['modzcta'].map(home_values)

# Fill missing home values with the mean home value
ny_build_geo['home_value'].fillna(ny_build_geo['home_value'].mean(), inplace=True)

# Adjust weights for combining factors
weight_distance_to_central = 0.5
weight_home_value = 0.5

# Create the investment potential score for each building
ny_build_geo['investment_potential'] = (weight_distance_to_central * (1 - ny_build_geo['distance_to_central_normalized']) +
                                        weight_home_value * ny_build_geo['home_value'])

# Aggregate the investment potential by ZIP code
zcta_investment_potential = ny_build_geo.groupby('modzcta')['investment_potential'].mean().reset_index(name='investment_potential')

# Merge this information back to the zcta_geo GeoDataFrame
zcta_geo = zcta_geo.merge(zcta_investment_potential, on='modzcta', how='left')

# Generate a choropleth map to visualize the investment potential by ZIP code
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

Choropleth(
    geo_data=zcta_geo,
    data=zcta_geo,
    columns=['modzcta', 'investment_potential'],
    key_on='feature.properties.modzcta',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Investment Potential'
).add_to(m)

# Add points from ny_build_geo
for idx, row in ny_build_geo.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=folium.Popup(f"Building Project: {row['Project Name']}<br>Investment Potential: {row['investment_potential']:.2f}", parse_html=True),
        tooltip=row['Project Name']
    ).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save and display the map
m.save('nyc_investment_potential_choropleth_map.html')

# Identify the top 5 places to invest per borough
# Merge the investment potential information back to ny_build_geo to include borough data
ny_build_geo = ny_build_geo.merge(ny_build[['Project ID', 'Borough']], on='Project ID', how='left')

# Calculate the mean investment potential per borough
borough_investment_potential = ny_build_geo.groupby(['Borough', 'modzcta'])['investment_potential'].mean().reset_index()

# Rank the ZIP codes within each borough by investment potential
borough_investment_potential['rank'] = borough_investment_potential.groupby('Borough')['investment_potential'].rank(ascending=False)

# Get the top 5 ZIP codes per borough
top_investment_areas = borough_investment_potential[borough_investment_potential['rank'] <= 5].sort_values(by=['Borough', 'rank'])

# Display the top 5 investment areas per borough
for borough in top_investment_areas['Borough'].unique():
    print(f"\nTop 5 investment areas in {borough}:")
    top_areas = top_investment_areas[top_investment_areas['Borough'] == borough]
    for index, row in top_areas.iterrows():
        print(f"  ZIP Code: {row['modzcta']} - Investment Potential: {row['investment_potential']:.2f}")



