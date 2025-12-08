import pandas as pd
import requests
import time
import os

API_KEY = "" 

if os.path.exists("Yelp_Data.csv"):
    INPUT_FILE = "Yelp_Data.csv"
else:
    INPUT_FILE = "Yelp_Data_v2.csv"

OUTPUT_YELP_ONLY = "Yelp_Raw_Data.csv"          
OUTPUT_FULL_MERGED = "DMV_Completed_Dataset.csv" 
# =========================================

def get_yelp_data(api_key, lat, lon):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.yelp.com/v3/businesses/search"
    
    base_params = {
        "latitude": lat,
        "longitude": lon,
        "radius": 1000, 
    }
    
    try:
        params_general = base_params.copy()
        params_general.update({"term": "restaurants", "sort_by": "review_count", "limit": 50})
        
        res = requests.get(url, headers=headers, params=params_general)
        if res.status_code != 200: return 0, 0, 0, 0, 0, 0, 0, 0, 0
            
        data = res.json()
        total_rest_count = data.get("total", 0)
        businesses = data.get("businesses", [])
        
        if businesses:
            avg_rating = sum([b['rating'] for b in businesses]) / len(businesses)
            avg_review_count = sum([b['review_count'] for b in businesses]) / len(businesses)
        else:
            avg_rating = 0
            avg_review_count = 0
            
        def get_count(term=None, price=None):
            p = base_params.copy()
            if term: p['term'] = term
            if price: 
                p['term'] = "restaurants"
                p['price'] = price
            p['limit'] = 1 
            r = requests.get(url, headers=headers, params=p)
            return r.json().get('total', 0) if r.status_code == 200 else 0

        n_thai = get_count(term="Thai")
        n_coffee = get_count(term="Coffee")
        n_fast = get_count(term="Fast Food")
        n_jap = get_count(term="Japanese")
        n_ita = get_count(term="Italian")
        n_amer = get_count(term="American") 
        n_bars = get_count(term="Bars")    
        n_exp = get_count(price="4") # $$$$
        
        return total_rest_count, avg_rating, avg_review_count, n_thai, n_coffee, n_fast, n_jap, n_ita,n_amer,n_bars, n_exp
        
    except Exception as e:
        print(f" Error: {e}")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"Error {INPUT_FILE}"); exit()

    print(f"read: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # df = df.head(5) # 測試用
    
    print(f"read {len(df)} data...")
    results = []
    
    for i, row in df.iterrows():
        zipcode = row['ZipCode']
        print(f"[{i+1}/{len(df)}] find Zip: {zipcode}...", end="\r")
        
        data = get_yelp_data(API_KEY, row['Latitude'], row['Longitude'])
        
        results.append({
            "ZipCode": str(zipcode),
            "Yelp_Restaurant_Count": data[0],
            "Yelp_Avg_Rating": round(data[1], 2),
            "Yelp_Avg_Review_Count": round(data[2], 1),
            "Num_Thai": data[3],
            "Num_Coffee": data[4],
            "Num_FastFood": data[5],
            "Num_Japanese": data[6],
            "Num_Italian": data[7],
            "Num_American": data[8], 
            "Num_Bars": data[9],   
            "Num_HighEnd_Price4": data[10]
        })
        time.sleep(0.2)

    yelp_df = pd.DataFrame(results)
    yelp_df.to_csv(OUTPUT_YELP_ONLY, index=False)
    print(f"\n\n scuess: {OUTPUT_YELP_ONLY}")

    df['ZipCode'] = df['ZipCode'].astype(str)
    final_df = pd.merge(df, yelp_df, on='ZipCode', how='left')
    final_df.to_csv(OUTPUT_FULL_MERGED, index=False)
    print(f"combine {OUTPUT_FULL_MERGED}")