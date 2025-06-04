
![Mapa de inversión NYC](nyc_investment_potential_heatmap.gif)
![NYC Income by Zip Map](nyc_income_by_zip_map.html.gif)
---

# NYC Housing & Census Analysis by ZIP Code

This repository contains an exploratory data analysis and machine learning project focused on **New York City** housing data, ZIP Code boundaries, census statistics, and additional datasets (such as crime data and home values). The main objective is to understand housing characteristics across different NYC ZIP Codes, integrate census information, and use machine learning techniques to uncover insights about income levels, housing unit distributions, and investment potential.

---

## 1. Datasets Used

1. **Housing New York Units by Building (`ny_build`)**  
   - Source: [NYC Open Data](https://data.cityofnewyork.us/Housing-Development/Housing-New-York-Units-by-Building/8x5j-irr2)  
   - Contains building-level details: number of affordable units, bedrooms, location (latitude/longitude), etc.

2. **Housing New York Units by Project (`ny_project`)**  
   - Source: [NYC Open Data](https://data.cityofnewyork.us/Housing-Development/Housing-New-York-Units-by-Project/hyij-8hr7)  
   - Contains project-level details: total units, affordability programs, start/completion dates, etc.

3. **NYPD Complaint Data (`ny_crime`)**  
   - Source: [NYC Open Data](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Current-Year-To-Date-/qgea-i56i)  
   - Used primarily to demonstrate geospatial merging and potential correlation with housing.  

4. **NYC Census Data (`ny_census`)**  
   - Source: Various Census datasets aggregated for NYC tracts.  
   - Contains demographic and socioeconomic variables (population, median income, poverty rate, etc.).

5. **NYC Home Values (`ny_value`)**  
   - Source: Additional dataset or aggregated data about median home values by ZIP Code.

6. **NYC Modified ZIP Code Tabulation Areas (MODZCTA)**  
   - GeoJSON file from [NYC Open Data](https://data.cityofnewyork.us/Business/ZIP-Code-Boundaries-Map/i8iw-xf4u) or [ZCTA GeoData](https://data.cityofnewyork.us/api/geospatial/pri4-ifjk).  
   - Used for mapping ZIP Codes and merging location data.

---

## 2. Project Structure

```
.
├── data/
│   ├── housing-new-york-units-by-building.csv
│   ├── housing-new-york-units-by-project.csv
│   ├── NYPD_Complaint_Data_Current_Year_To_Date.csv
│   ├── nyc_census_tracts.csv
│   ├── ny-home_values.xlsx
│   ├── ...
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_data_merging.ipynb
│   ├── 03_eda_and_visualizations.ipynb
│   ├── 04_ml_and_clustering.ipynb
│   └── ...
├── output/
│   ├── ny_merge_final.xlsx
│   ├── nyc_investment_potential_map.html
│   ├── nyc_income_by_zip_map.html
│   └── ...
├── environment.yml (or requirements.txt)
└── README.md
```

1. **data/**: Contains all original CSV/Excel datasets.  
2. **notebooks/**: Jupyter notebooks for cleaning, merging, EDA, and modeling.  
3. **output/**: Contains final merged datasets, generated maps (HTML files), and model outputs.  
4. **environment.yml / requirements.txt**: Lists all required Python libraries and versions.

---

## 3. Installation & Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/nyc-zip-analysis.git
   cd nyc-zip-analysis
   ```

2. **Create a new conda environment (recommended)**:
   ```bash
   conda create -n nyc-analysis python=3.9
   conda activate nyc-analysis
   ```

3. **Install required packages** (via `environment.yml` or manually):
   ```bash
   conda install -c conda-forge geopandas folium plotly shapely fiona pyproj rtree
   conda install -c conda-forge xgboost scikit-learn
   pip install pandas seaborn matplotlib
   ```

4. **Open the notebooks**:
   ```bash
   jupyter notebook
   ```
   Then navigate to the `notebooks/` directory and open the desired notebook.

---

## 4. Data Cleaning & Merging

- **Housing Data**:  
  - Filtered out unnecessary columns (e.g., `Building ID`, `Street`, etc.).  
  - Encoded categorical variables (e.g., `Reporting Construction Type`, `Extended Affordability Only`) using **OneHotEncoder**.
  - Merged **Building**-level and **Project**-level data on `Project ID`.

- **Census Data**:  
  - Used census tract data, aggregated key variables (e.g., `TotalPop`, `Income`, `Poverty`) to the ZIP Code level.
  - Merged with **MODZCTA** GeoJSON to link lat/long coordinates to ZIP Codes.

- **Home Values**:  
  - Created a dictionary/Excel file for approximate median home values by ZIP Code.
  - Joined to the main dataframe on the `ZipCode` column.

- **Crime Data** (Optional):  
  - Demonstrates how to incorporate geospatial points (crime incidents) into a broader analysis.  
  - Filtered columns to keep essential features (e.g., `BORO_NM`, `LAW_CAT_CD`, `Latitude`, `Longitude`).

- **Final Merge**:  
  - All data consolidated into a single `DataFrame` (`ny_merge_final.xlsx`) containing aggregated metrics by ZIP Code, plus building-level and project-level attributes.

---

## 5. Exploratory Data Analysis (EDA)

1. **Summary Statistics**:  
   - Checked missing values, duplicates, and outliers.
   - Computed correlation matrices to identify relationships among variables (e.g., `Income`, `Total Units`, `Poverty Rate`).

2. **Visualization**:  
   - Created histograms, bar plots, and scatter plots to explore distributions (e.g., bedroom counts, income).
   - Mapped ZIP Codes using **GeoPandas** + **Folium** to visualize variables like average income, housing units, or investment potential.

3. **Geospatial Plots**:  
   - Used **folium.Choropleth** to color ZIP Codes by average income or by aggregated unit counts.
   - Placed circle markers for building locations to see spatial clustering of developments.

---

## 6. Machine Learning & Clustering

1. **Supervised Learning (XGBoost)**  
   - Target: **Income Level** (Low, Medium, High) derived from quantiles.  
   - Features: Housing unit counts, census stats, program types, etc.  
   - Achieved high accuracy (~93%+) on a 3-class classification task.  
   - Assessed performance via **confusion matrix** and **classification report**.

2. **Unsupervised Learning (K-Means)**  
   - Performed **PCA** to reduce dimensions.  
   - Clustering on principal components gave an overall **silhouette score** of ~0.45.  
   - Provided insights into how different ZIP Codes (and building projects) group together by socioeconomic and housing features.

---

## 7. Geospatial “Investment Potential” (Optional Demo)

- Computed a heuristic score using:  
  - **Distance to Manhattan’s Central Point** (e.g., Central Park).  
  - **Median Home Value** by ZIP Code.  
  - **Number of Projects** in an area.  
- Visualized the result as a **choropleth map** in Folium to highlight ZIP Codes with potentially higher or lower investment appeal.

---

## 8. Key Findings

1. **Income Distribution**:  
   - Strong correlation between census income measures and home values by ZIP Code.
   - Areas with higher `Income` also showed higher `Median Home Value` and lower `Poverty` rates.

2. **Housing Unit Types**:  
   - ZIP Codes with many **extremely low** or **low-income** units tended to have higher poverty rates, consistent with policy targeting.

3. **Clustering & Classification**:  
   - XGBoost classifier reliably distinguishes Low/Medium/High income levels using building-level, census, and project-level features.
   - Clusters identified by K-Means reflect distinct socioeconomic profiles across the city.

4. **Geospatial Insights**:  
   - Visual maps highlight clear borough-based patterns in income and housing developments (e.g., Manhattan vs. Bronx, etc.).

---

## 9. Future Work


- **Time-Series Analysis**: Investigate how completion dates correlate with changing neighborhood demographics.
- **Detailed Crime Correlation**: More robust geospatial joins to measure if certain housing projects correlate with changes in crime rates.
- **Deep-Dive into Neighborhoods**: Use the `NTA - Neighborhood Tabulation Area` or finer census tract merges for more granular analysis.
- One idea worth exploring would be integrating **time-aware models** (e.g., Time Series Forecasting or Spatial-Temporal Graph Networks) to analyze how investment trends evolve and affect income or migration over time. 
---

## 10. Contributing

Contributions are welcome! If you have suggestions or want to add new features, feel free to open an issue or submit a pull request.

---

## 11. License

This project is licensed under the [MIT License](LICENSE). Data sources belong to their respective owners (NYC Open Data, etc.) and may have separate usage terms.

---
