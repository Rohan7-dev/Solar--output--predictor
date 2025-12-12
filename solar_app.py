
import streamlit as st
import requests
import pandas as pd
import altair as alt

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="Solar Smart: Engineering & ROI", page_icon="☀️", layout="centered")

# --- 🎨 CSS STYLING (The Professional Look) ---
st.markdown("""
    <style>
    /* Main Title */
    h1 {
        text-align: center; color: #FFA500; font-family: 'Helvetica', sans-serif;
        font-size: 3rem !important; margin-bottom: 1rem;
    }
    /* Input Styling */
    div[data-testid="stTextInput"] label, div[data-testid="stNumberInput"] label { 
        font-size: 1.1rem !important; color: #ddd; 
    }
    div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input { 
        font-size: 1.1rem !important; height: 3rem !important; 
    }
    /* Button Styling */
    div[data-testid="stButton"] button {
        width: 100%; height: 3.5rem; font-size: 1.3rem !important;
        background-color: #FFA500; color: black; border: none; border-radius: 8px; font-weight: bold; margin-top: 10px;
    }
    div[data-testid="stButton"] button:hover { background-color: #FFD700; color: black; }
    /* Section Headers */
    h3 { font-size: 1.6rem !important; border-bottom: 2px solid #444; padding-bottom: 10px; margin-top: 40px !important; }
    /* Metrics */
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00CC99; }
    </style>
    """, unsafe_allow_html=True)

# 2. Hero Section
st.title("Solar Smart: Engineering & ROI ☀️")
st.image("https://images.unsplash.com/photo-1509391366360-2e959784a276?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80", caption="Comprehensive PV System Analysis", use_container_width=True)

# 3. User Inputs (Grouped for clarity)
st.info("📝 **Configure Your System**")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📍 Location & System**")
    city = st.text_input("City Name", "London")
    panel_power = st.number_input("System Size (kW)", value=5.0, step=0.5)

with col2:
    st.markdown("**💰 Consumption & Tariff**")
    monthly_usage = st.number_input("Monthly Usage (kWh)", value=350, step=10)
    tariff = st.number_input("Electricity Rate (Price/Unit)", value=8.0, step=0.5)

# 4. The Logic Core
if st.button("Run Full Analysis", use_container_width=True):
    
    # 🔐 API KEY SECTION
    api_key = st.secrets["OPENWEATHER_KEY"]
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            # --- A. DATA MINING (Physics) ---
            clouds = data["clouds"]["all"]
            temp_k = data["main"]["temp"]
            temp_c = temp_k - 273.15
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            
            # --- B. ENGINEERING CALCULATIONS ---
            # 1. Efficiency Factors
            cloud_efficiency = 1 - (clouds / 100 * 0.8) # 80% loss at full cloud
            heat_loss = max(0, (temp_c - 25) * 0.005)   # 0.5% loss per °C > 25°C
            temp_efficiency = 1 - heat_loss
            
            # 2. Power & Energy
            actual_power = panel_power * cloud_efficiency * temp_efficiency
            daily_production = actual_power * 5  # 5 Peak Sun Hours assumption
            monthly_production = daily_production * 30
            
            # --- C. FINANCIAL CALCULATIONS ---
            old_bill = monthly_usage * tariff
            net_usage = max(0, monthly_usage - monthly_production)
            new_bill = net_usage * tariff
            savings = old_bill - new_bill
            
            # ==========================================
            #           VISUAL DASHBOARD START
            # ==========================================
            
            # SECTION 1: ENVIRONMENTAL ANALYSIS 🌍
            st.subheader(f"1. Environmental Analysis for {city}")
            
            # Map & Metrics
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=10)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("☁️ Cloud Cover", f"{clouds}%")
            c2.metric("🌡️ Temperature", f"{temp_c:.1f}°C")
            c3.metric("⚡ Real-Time Output", f"{actual_power:.2f} kW", delta=f"{actual_power - panel_power:.2f} kW")

            # SECTION 2: SYSTEM PERFORMANCE ⚙️
            st.subheader("2. System Performance (Rated vs Actual)")
            
            # Horizontal Bar Chart (The one we fixed earlier)
            chart_data = pd.DataFrame({
                "Power Type": ["Rated Max Power (Lab)", "Actual Output (Now)"],
                "Power (kW)": [panel_power, actual_power]
            })
            
            chart_power = alt.Chart(chart_data).mark_bar(size=40).encode(
                x=alt.X('Power (kW)', title='Power Output (Kilowatts)'),
                y=alt.Y('Power Type', title=None),
                color=alt.Color('Power Type', legend=None),
                tooltip=['Power Type', 'Power (kW)']
            ).properties(height=200)
            
            st.altair_chart(chart_power, use_container_width=True)
            
            # Engineering Glossary (Restored!)
            with st.expander("ℹ️ Click to understand the Engineering Math"):
                st.markdown(f"""
                **Why is the output lower?**
                * **Rated Power** is measured at $25^\circ C$. Today it is **{temp_c:.1f}^\circ C**.
                * **Thermal Loss:** Because of the heat, you are losing **{heat_loss*100:.1f}%** efficiency.
                * **Cloud Loss:** Clouds are blocking **{clouds}%** of the sky, reducing irradiance.
                """)

            # SECTION 3: FINANCIAL ROI 💰
            st.subheader("3. Financial Impact Analysis")
            
            # Bill Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Current Monthly Bill", f"{old_bill:.0f}", help="Without Solar")
            m2.metric("New Bill", f"{new_bill:.0f}", delta=f"-{savings:.0f} drop", delta_color="inverse", help="With Solar")
            m3.metric("Est. Monthly Savings", f"{savings:.0f}", help="Cash in pocket")
            
            # Bill Comparison Chart (Vertical)
            bill_data = pd.DataFrame({
                "Scenario": ["Current Bill", "With Solar"],
                "Cost": [old_bill, new_bill]
            })
            
            chart_bill = alt.Chart(bill_data).mark_bar(size=50).encode(
                x=alt.X('Scenario', sort=None),
                y='Cost',
                color=alt.Color('Scenario', scale=alt.Scale(domain=['Current Bill', 'With Solar'], range=['#ff4b4b', '#00CC99'])),
                tooltip=['Scenario', 'Cost']
            ).properties(height=300)
            
            st.altair_chart(chart_bill, use_container_width=True)
            
            if savings > 0:
                st.success(f"🎉 Success! This system covers {min(100, (monthly_production/monthly_usage)*100):.0f}% of your energy needs.")
            
        else:
            st.error("❌ City not found! Please check spelling.")

    except Exception as e:

        st.error(f"❌ Connection Error: {e}")
