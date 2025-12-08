import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

INPUT_FILE = "./urburn_dataset/DMV_Yelp_Dataset.csv"
OUTPUT_FULL = "./urburn_dataset/Final_Project_Data_With_Scores.csv"
OUTPUT_SCORES_ONLY = "./urburn_dataset/Livability_Scores_Only.csv"
# =========================================
if not os.path.exists(INPUT_FILE):
    print(f"Error: {INPUT_FILE}")
    exit()

df = pd.read_csv(INPUT_FILE)
print(f"Get {len(df)} data")

# fill out misdata
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(0)

scaler = MinMaxScaler()

# Transport Score)
df['Log_Metro_Dist'] = np.log1p(df['MetroDistanceMeters'])
df['Log_DC_Dist'] = np.log1p(df['DistanceToDC_Meters'])

norm_metro = 1 - scaler.fit_transform(df[['Log_Metro_Dist']])
norm_dc = 1 - scaler.fit_transform(df[['Log_DC_Dist']])
df['Score_Transport'] = (0.7 * norm_metro) + (0.3 * norm_dc)

# Food Score
df['Log_Rest_Count'] = np.log1p(df['Yelp_Restaurant_Count'])

norm_rest_count = scaler.fit_transform(df[['Log_Rest_Count']])
norm_rating = scaler.fit_transform(df[['Yelp_Avg_Rating']])

df['Score_Food'] = (0.6 * norm_rest_count) + (0.4 * norm_rating)

# Lifestyle Score
for col in ['Num_Bars', 'Num_American', 'Num_Thai', 'Num_Japanese', 'Num_Italian', 'Num_Coffee', 'Num_HighEnd_Price4']:
    if col not in df.columns:
        df[col] = 0

# metrics
df['Diversity_Count'] = df['Num_Thai'] + df['Num_Japanese'] + df['Num_Italian'] + df['Num_American']

norm_coffee = scaler.fit_transform(df[['Num_Coffee']])
norm_bars = scaler.fit_transform(df[['Num_Bars']])
norm_diversity = scaler.fit_transform(df[['Diversity_Count']])
norm_high_end = scaler.fit_transform(df[['Num_HighEnd_Price4']])

df['Score_Lifestyle'] = (0.3 * norm_diversity) + \
                        (0.3 * norm_coffee) + \
                        (0.2 * norm_bars) + \
                        (0.2 * norm_high_end)

# Final Livability Index
df['Livability_Score'] = (0.4 * df['Score_Transport']) + \
                         (0.3 * df['Score_Food']) + \
                         (0.3 * df['Score_Lifestyle'])

# turn to 0-100 score
df['Livability_Score'] = round(df['Livability_Score'] * 100, 1)

cols_to_drop = ['Log_Metro_Dist', 'Log_DC_Dist', 'Log_Rest_Count', 'Diversity_Count']
df_final = df.drop(columns=cols_to_drop)



df_final.to_csv(OUTPUT_FULL, index=False)
print(f"save for all data: {OUTPUT_FULL}")

# Scores Only
score_cols = [
    'ZipCode', 'City', 'State', 'MedianPrice', 
    'Livability_Score', 'Score_Transport', 'Score_Food', 'Score_Lifestyle'
]

existing_cols = [c for c in score_cols if c in df_final.columns]
df_scores = df_final[existing_cols]

df_scores.to_csv(OUTPUT_SCORES_ONLY, index=False)
print(f"score only: {OUTPUT_SCORES_ONLY}")

print("="*30)
print("check:")
print(df_scores.head())