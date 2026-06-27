import pandas as pd
import numpy as np
np.random.seed(42)
n_samples=1000

bid_cpc=np.random.uniform(0.10,5,n_samples)
impressions=np.random.randint(1000,50000,n_samples)
ad_format=np.random.choice(["Video","banner","Interstitial"],size=n_samples,p=[0.5,0.3,0.2])
device_os = np.random.choice(["iOS", "Android"], size=n_samples, p=[0.4, 0.6])
app_categories = np.random.choice(["Gaming", "Finance", "Social", "Utility"], size=n_samples)
#formula for base_ctr
base_ctr=1.2+(bid_cpc*0.4)-(np.log1p(impressions)*0.05)


for i in range(n_samples):
    if ad_format[i] == "Video": base_ctr[i] += 1.5         
    if ad_format[i] == "Banner": base_ctr[i] -= 0.6        
    if device_os[i] == "iOS": base_ctr[i] += 0.3            
    if app_categories[i] == "Finance": base_ctr[i] += 0.5

    final_ctr = base_ctr + np.random.normal(0, 0.3, n_samples)
    final_ctr = np.clip(final_ctr, 0.1, 15.0)

    df = pd.DataFrame({
    "bid_cpc": bid_cpc,
    "historical_impressions": impressions,
    "ad_format": ad_format,
    "device_os": device_os,
    "app_category": app_categories,
    "predicted_ctr": final_ctr
})

df.to_csv("ad_campaign_data.csv", index=False)
