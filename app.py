import uvicorn
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="ads optimization engine api")
model_pipeline=joblib.load("ad_campaign_pipeline.pkl")

class AdCampaignInput(BaseModel):
    bid_cpc: float
    historical_impressions: int
    ad_format: str
    device_os: str
    app_category: str

@app.post("/predict")
async def predict_ctr_endpoint(payload:AdCampaignInput):
    input_dic=payload.model_dump()
    input_df=pd.DataFrame([input_dic])

    prediction=model_pipeline.predict(input_df)[0]

    return {
            "status": "success",
            "predicted_click_through_rate_percentage": float(round(prediction, 4))
        }

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
