import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Streamlit Page Configuration
st.set_page_config(page_title="CrimePulse India", layout="wide")
st.title("CrimePulse India: State-Wise Crime Prediction (2001-2012)")
st.write("Analyze and predict crime trends across Indian states.")

# Load data
data_path = r"C:\Users\kspra\OneDrive\Desktop\CRIME ANALYSIS\data\newtrial - Sheet 1 - 01_District_wise_crim 2.csv"
df = pd.read_csv(data_path)

# Dropdowns
states = sorted(df['STATE/UT'].unique())
years = list(range(2001, 2013))

state = st.selectbox("Select State/UT", states)
year = st.selectbox("Select Year", years)

# Prediction Button
if st.button("Predict Crime Trend"):
    payload = {'state': state, 'year': year}
    try:
        response = requests.post("http://localhost:5000/predict", json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()['predicted_crime']
            st.success(f"Predicted Dominant Crime in {state} ({year}): {result}")
        else:
            st.error(f"Server returned status code {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Flask server at http://localhost:5000. Ensure 'app.py' is running.")
    except requests.exceptions.Timeout:
        st.error("Request timed out. Check if the Flask server is responding.")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

# Separator
st.markdown("---")

# Crime Heatmap
st.subheader("State-Year Crime Heatmap")

# Select crime type
numeric_columns = df.select_dtypes(include='number').columns.tolist()
if numeric_columns:
    selected_crime = st.selectbox("Select Crime Type for Heatmap", numeric_columns)
    
    # Grouping and pivoting for heatmap
    heatmap_data = df.groupby(['STATE/UT', 'YEAR']).sum(numeric_only=True).reset_index()
    pivot_table = heatmap_data.pivot(index='STATE/UT', columns='YEAR', values=selected_crime)

    # Plotting with Plotly
    fig = px.imshow(
        pivot_table,
        labels=dict(x="Year", y="State/UT", color=f"{selected_crime} Cases"),
        x=pivot_table.columns,
        y=pivot_table.index,
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No numeric crime columns available in the dataset to plot a heatmap.")

# Footer
st.markdown("---")
st.write("Built for analyzing Indian crime data | CrimePulse India")
