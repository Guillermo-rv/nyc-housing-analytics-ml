# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 18:13:04 2024

@author: guill
"""

'''
Project (individual):
• 25% data preprocessing
• 25% supervised analysis
• 25% unsupervised analysis
• 25% extra analysis (complex model / model not studied in
class)
* All 4 parts of the project must be completed
❑ 10 minutes presentation + 5 min questions (July 17 & 18)
❑ The notebook or python file must be sent before the
presentation to lmelgar@faculty.ie.edu

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


ny_build = pd.read_csv('housing-new-york-units-by-building.csv')
ny_build_2 = pd.read_csv('housing-new-york-units-by-building.csv')

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
ny_project_2 = pd.read_csv('housing-new-york-units-by-project.csv')

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


#%%

# Let's Use One Hot Encoder to transform some variables into numerical variables.

#%% Numerical and categorical

# Handling missing values and encoding categorical variables for ny_build_2
numerical_features_build = ny_build_2.select_dtypes(include=['int64', 'float64']).columns
categorical_features_build = ny_build_2.select_dtypes(include=['object']).columns

# Handling missing values and encoding categorical variables for ny_project_2
numerical_features_project = ny_project_2.select_dtypes(include=['int64', 'float64']).columns
categorical_features_project = ny_project_2.select_dtypes(include=['object']).columns



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


'''
BUILDING:
    -Postcode, BBL, BIN and Council District are extremely related, no surprise in here. With Postcode it will be enough.
    -Latitude and Longitude. There are four columns for each information, with 2 of them will be enough.
    -Total Unites and all counted units are very correlated as well. And themselves with 2-BR Unites and 1-BR Unites, that gives me information about how many br tend to have this houses.

PROJECTS:
    -Counted Homeownerships Units, All counted Unites and Total Units are highly correlated.

'''

#%% MISSING VALUES

# Checking missing values
missing_build = ny_build_2.isnull().sum()
print("Missing values in ny_build_2:\n", missing_build)

# Checking missing values
missing_project = ny_project_2.isnull().sum()
print("Missing values in ny_project_2:\n", missing_project)

#%% CATEGORICAL VARIABLES - ONE HOT ENCODER


from sklearn.preprocessing import OneHotEncoder

# Initialize OneHotEncoder
encoder = OneHotEncoder(drop='first', sparse=False)

# Fit and transform the data
encoded_features = encoder.fit_transform(ny_project_2[['Extended Affordability Only', 'Prevailing Wage Status']])

# Create DataFrame with the encoded features
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Extended Affordability Only', 'Prevailing Wage Status']))

# Concatenate with the original DataFrame
ny_project_2 = pd.concat([ny_project_2, encoded_df], axis=1)

# Drop original columns
ny_project_2.drop(['Extended Affordability Only', 'Prevailing Wage Status'], axis=1, inplace=True)



#%% CLEAN THE DATA

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Handling missing values and encoding categorical variables for ny_build_2
numerical_features_build = ny_build_2.select_dtypes(include=['int64', 'float64']).columns
categorical_features_build = ny_build_2.select_dtypes(include=['object']).columns

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

# Handling missing values and encoding categorical variables for ny_project_2
numerical_features_project = ny_project_2.select_dtypes(include=['int64', 'float64']).columns
categorical_features_project = ny_project_2.select_dtypes(include=['object']).columns

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

