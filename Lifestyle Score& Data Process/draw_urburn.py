import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
import matplotlib.ticker as ticker

sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

INPUT_FILE = "./urburn_dataset/Final_Project_Data_With_Scores.csv"
try:
    df = pd.read_csv(INPUT_FILE)
    print(f"sucess: {len(df)} 筆")
except:
    print("please check file name is correct")
    exit()

def plot_value_matrix(df):
    plt.figure(figsize=(10, 8))
    
    avg_price = df['MedianPrice'].mean()
    avg_score = df['Livability_Score'].mean()
    
    scatter = sns.scatterplot(
        data=df, 
        x='MedianPrice', 
        y='Livability_Score', 
        size='Score_Transport',
        hue='State',           
        alpha=0.7,
        palette='viridis',
        sizes=(20, 200)
    )
    
    plt.axvline(avg_price, color='red', linestyle='--', alpha=0.5, label='Avg Price')
    plt.axhline(avg_score, color='blue', linestyle='--', alpha=0.5, label='Avg Score')
    
    gems = df[(df['Livability_Score'] > avg_score) & (df['MedianPrice'] < avg_price)]
    top_gems = gems.sort_values('Livability_Score', ascending=False).head(5)
    
    for i, row in top_gems.iterrows():
        plt.text(row['MedianPrice'], row['Livability_Score']+1, row['City'], 
                 fontsize=9, fontweight='bold', color='black')

    plt.title('Residential Value Discovery Matrix\n(Top-Left Quadrant = Undervalued/High-Value Areas)', fontsize=14)
    plt.xlabel('Median Housing Price ($)', fontsize=12)
    plt.ylabel('Livability Score (0-100)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('chart_value_matrix.png', dpi=300)
    print("圖表 1 完成: chart_value_matrix.png")

# Chart 2
def plot_radar_chart(df):
    df_sorted = df.sort_values('Livability_Score', ascending=False)
    targets = pd.concat([df_sorted.head(3), df_sorted.iloc[[50]]]) # Top 3 + Rank 50
    
    categories = ['Transport', 'Food', 'Lifestyle']
    N = len(categories)
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    
    plt.xticks(angles[:-1], categories, color='black', size=12)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.50", "0.75"], color="grey", size=10)
    plt.ylim(0, 1)
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for idx, (i, row) in enumerate(targets.iterrows()):
        values = [row['Score_Transport'], row['Score_Food'], row['Score_Lifestyle']]
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f"{row['City']} ({row['ZipCode']})")
        ax.fill(angles, values, colors[idx], alpha=0.1)
        
    plt.title('Livability Profile Comparison', size=15, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    plt.tight_layout()
    plt.savefig('chart_radar_profile.png', dpi=300)
    print("圖表 2 完成: chart_radar_profile.png")

# Spatial Heatmap
def plot_spatial_heatmap_fixed(df):
    plt.figure(figsize=(12, 8))
    
    scatter = plt.scatter(
        df['Longitude'], 
        df['Latitude'], 
        c=df['Livability_Score'], 
        cmap='RdYlGn', 
        s=df['MedianPrice']/5000, 
        alpha=0.7,
        edgecolors='white',
        linewidth=0.5
    )
    
    plt.colorbar(label='Livability Score (Green=High, Red=Low)')
    
    def lon_formatter(x, pos):
        return f'{abs(x):.1f}°W'
    
    def lat_formatter(y, pos):
        return f'{y:.1f}°N'

    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lon_formatter))
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lat_formatter))
    # -------------------------------------
    landmarks = {
        'DC Core': (-77.0369, 38.9072),
        'Dulles Airport': (-77.4565, 38.9531),
        'Alexandria': (-77.0469, 38.8048)
    }
    
    for name, (lon, lat) in landmarks.items():
        plt.annotate(name, (lon, lat), xytext=(5, 5), textcoords='offset points', 
                     fontsize=9, fontweight='bold', color='black',
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

    plt.title('Spatial Distribution of Livability Scores in DMV Area', fontsize=15)
    plt.xlabel('Longitude (West)')
    plt.ylabel('Latitude (North)')
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('chart_spatial_map_fixed.png', dpi=300)
    print("圖表 3 (修正版) 完成: chart_spatial_map_fixed.png")

plot_spatial_heatmap_fixed(df)

# Correlation Matrix
def plot_correlation(df):
    plt.figure(figsize=(10, 8))
    
    cols = ['Livability_Score', 'Score_Transport', 'Score_Food', 'Score_Lifestyle', 
            'MedianPrice', 'DistanceToDC_Meters', 'Growth_5Y']
    
    corr = df[cols].corr()
    
    sns.heatmap(
        corr, 
        annot=True, 
        cmap='coolwarm', 
        fmt=".2f", 
        linewidths=0.5,
        vmin=-1, vmax=1
    )
    
    plt.title('Correlation Matrix of Key Indicators', fontsize=14)
    plt.tight_layout()
    plt.savefig('chart_correlation.png', dpi=300)
    print("圖表 4 完成: chart_correlation.png")

# Price vs Value Zones
def plot_price_value_zones(df):
    plt.figure(figsize=(10, 8))
    
    avg_price = df['MedianPrice'].mean()
    avg_score = df['Livability_Score'].mean()
    
    ax = sns.scatterplot(
        data=df, 
        x='MedianPrice', 
        y='Livability_Score', 
        hue='State', 
        s=100, 
        palette='deep',
        edgecolor='black'
    )
    
    def currency_formatter(x, pos):
        if x >= 1000000:
            return f'${x/1000000:.1f}M' 
        else:
            return f'${x/1000:.0f}k'   
            
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
    # -------------------------------------
    
    plt.axvline(avg_price, color='gray', linestyle='--')
    plt.axhline(avg_score, color='gray', linestyle='--')
    
    # Label Zones
    plt.text(df['MedianPrice'].min(), df['Livability_Score'].max(), 
             'HIDDEN GEMS\n(High Value)', fontsize=12, color='green', ha='left', va='top', fontweight='bold')
    plt.text(df['MedianPrice'].max(), df['Livability_Score'].max(), 
             'LUXURY\n(Quality)', fontsize=12, color='blue', ha='right', va='top', fontweight='bold')
    plt.text(df['MedianPrice'].max(), df['Livability_Score'].min(), 
             'OVERPRICED\n(Low Value)', fontsize=12, color='red', ha='right', va='bottom', fontweight='bold')
    plt.text(df['MedianPrice'].min(), df['Livability_Score'].min(), 
             'ECONOMY\n(Basic)', fontsize=12, color='orange', ha='left', va='bottom', fontweight='bold')

    df['Value_Ratio'] = df['Livability_Score'] / df['MedianPrice']
    best_value = df.sort_values('Value_Ratio', ascending=False).head(3)
    
    for i, row in best_value.iterrows():
        plt.text(row['MedianPrice'], row['Livability_Score']+1, row['City'], fontsize=9, fontweight='bold')

    plt.title('Strategic Housing Matrix: Price vs. Livability', fontsize=14)
    plt.xlabel('Median Housing Price', fontsize=12)
    plt.ylabel('Livability Score (0-100)', fontsize=12)
    plt.tight_layout()
    
    plt.savefig('chart_price_zones_fixed.png', dpi=300)

plot_price_value_zones(df)

if __name__ == "__main__":
    plot_value_matrix(df)
    plot_radar_chart(df)
    plot_spatial_heatmap(df)
    plot_correlation(df)