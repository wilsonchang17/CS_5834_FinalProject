# Multimodal Framework for Urban Livability Assessment and Residential Value Discovery

**Final Project for CS5834 Urban Computing**
**Virginia Tech, Fall 2025**

This repository implements a framework for assessing urban livability and identifying undervalued residential areas in the Washington D.C. metropolitan area (DMV). By fusing structured geographic data with unstructured user-generated content, this project aims to surface "hidden gem" neighborhoods that offer high quality of life relative to their cost.

## Overview

Traditional rental platforms often prioritize hard constraints like price and subway distance while overlooking the "soft" aspects of livability found in user narratives. Our framework addresses this gap through three core modules:

1.  **Multimodal Livability Index**
    * Constructs a unified score at the ZIP code level by synthesizing transit accessibility, amenity diversity, and review-based sentiment.
2.  **Lifestyle Clustering**
    * Applies unsupervised clustering to multimodal feature vectors to reveal distinct neighborhood profiles based on price, density, and perceived experience.
3.  **Residual-Based Value Discovery**
    * Trains a housing price prediction model and analyzes the residuals to identify locations where actual market prices are significantly lower than predicted values.

## Authors

* **Chen-Wei Chang** (wilsonchang@vt.edu)
* **Yun-En Tsai** (yunen@vt.edu)
* **Pin Chang** (ben0426@vt.edu)

## Data Sources

The repository contains processed datasets derived from **four primary raw sources**. We performed spatial alignment and feature engineering on these inputs to construct the final analytical files:

* **Zillow Housing Records:** Provides listing prices, transaction amounts, and historical rental estimates.
* **Metro Transit Data:** Sourced from the Metro API to locate stations and compute connectivity metrics.
* **ZIP Code Boundaries:** Geospatial shapefiles used to aggregate all metrics into common spatial units (ZCTAs).
* **Yelp Places Data:** Collected via Yelp API to estimate amenity density, cuisine diversity, and neighborhood sentiment.

These sources are processed into the following datasets found in the `data/` folder:
* `DMV_House_Price_Data.csv`: Aggregated housing and transit metrics.
* `Yelp_Data.csv`: Raw amenity and review features.
* `DMV_Yelp_Dataset.csv`: The final consolidated dataset merging all features for analysis.