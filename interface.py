import streamlit as st
import requests

# ==============================================================================
# 1. PAGE CONFIGURATION & LAYOUT SETUP
# ==============================================================================
st.set_page_config(
    page_title=" AdOps Optimizer", 
    page_icon="📊", 
    layout="centered"
)

st.title("📊  AdOps Optimization Engine")
st.markdown("### Client-Facing Real-Time Bidding Yield Optimization Dashboard")
st.write("This frontend dashboard communicates directly with our decoupled FastAPI ML service layer.")
st.write("---")

# ==============================================================================
# 2. INTERACTIVE INPUT FORMS & SLIDERS
# ==============================================================================
st.subheader("🛠️ Campaign Adjustments & Targeting Matrix")

# Split inputs into two clean visual columns
col1, col2 = st.columns(2)

with col1:
    bid_cpc = st.slider("Bid Pricing (CPC $)", min_value=0.10, max_value=5.00, value=1.00, step=0.05)
    historical_impressions = st.number_input("Target Impressions Limit", min_value=1000, max_value=500000, value=50000, step=1000)

with col2:
    ad_format = st.selectbox("Creative Format Selection", ["Banner", "Video", "Interstitial"])
    device_os = st.selectbox("Target Operating System", ["iOS", "Android"])
    app_category = st.selectbox("App Inventory Category", ["Gaming", "Finance", "Social", "Utility"])

st.write("---")

# ==============================================================================
# 3. FASTAPI NETWORK CONNECTION & EXECUTION LOOP
# ==============================================================================
# Define the local gateway address where your FastAPI is actively listening
FASTAPI_URL = "http://127.0.0.1:8000/predict"

# Trigger the prediction via a Network Request when the button is clicked
if st.button("🚀 Run Performance Forecast", use_container_width=True):
    
    # Pack the slider variables into the exact JSON template your Pydantic schema expects
    payload = {
        "bid_cpc": float(bid_cpc),
        "historical_impressions": int(historical_impressions),
        "ad_format": ad_format,
        "device_os": device_os,
        "app_category": app_category
    }
    
    # Show a sleek loading spinner while the network port is communicating
    with st.spinner("Transmitting parameters to local ML microservice cluster..."):
        try:
            # Send the data payload over port 8000 to FastAPI
            response = requests.post(FASTAPI_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                predicted_ctr = result["predicted_click_through_rate_percentage"]
                
                # Render the final prediction result beautifully on screen
                st.success("Analysis Complete!")
                st.metric(label="Predicted Click-Through Rate (CTR)", value=f"{predicted_ctr}%")
            else:
                st.error(f"❌ Server Error: Received HTTP status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Refused: Is your FastAPI backend app.py actively running on port 8000?")