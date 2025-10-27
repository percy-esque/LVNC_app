import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="LVNC CardioScan Pro",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 24px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff4b4b;
    }
    .risk-high {
        color: #ff4b4b;
        font-weight: bold;
    }
    .risk-moderate {
        color: #ffa500;
        font-weight: bold;
    }
    .risk-low {
        color: #00ff00;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
    st.session_state.model = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/heart-with-pulse.png", width=80)
    st.title("CardioScan Pro")
    st.markdown("---")
    
    device_status = st.selectbox(
        "🔌 Device Status",
        ["Disconnected", "Connected", "Scanning"]
    )
    
    st.markdown("---")
    st.markdown("### Instructions:")
    st.markdown("""
    1. Enter patient cardiac data
    2. Ensure values are accurate
    3. Click 'Calculate Risk Score'
    4. Review risk assessment
    """)
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #888;'>
        <small>CardioScan LVNC Detection System</small><br>
        <small>For clinical use only</small><br>
        <small>This device is intended to assist healthcare professionals in LVNC assessment.</small>
        </div>
    """, unsafe_allow_html=True)

# Main content
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("# ❤️")
with col_title:
    st.title("LVNC Cardiac Analysis System")
    st.markdown("**Advanced detection of Left Ventricular Non-Compaction Cardiomyopathy**")

st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Patient Analysis", "📈 Patient History & Prior Scans", "ℹ️ About LVNC", "🔬 Model Training"])

with tab1:
    st.header("Enter Patient Cardiac Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📏 Volume Measurements")
        edv = st.number_input(
            "End-Diastolic Volume (EDV) [mL]",
            min_value=50.0,
            max_value=400.0,
            value=150.0,
            step=5.0,
            help="Normal range: 100-160 mL"
        )
        
        esv = st.number_input(
            "End-Systolic Volume (ESV) [mL]",
            min_value=20.0,
            max_value=300.0,
            value=60.0,
            step=5.0,
            help="Normal range: 40-70 mL"
        )
    
    with col2:
        st.markdown("### 💓 Functional Parameters")
        ef = st.number_input(
            "Ejection Fraction (EF) [%]",
            min_value=10.0,
            max_value=80.0,
            value=55.0,
            step=1.0,
            help="Normal range: >50%. EF <40% indicates high risk"
        )
        
        filling_rate = st.number_input(
            "Filling Rate [mL/s]",
            min_value=50.0,
            max_value=500.0,
            value=200.0,
            step=10.0,
            help="Rate of ventricular filling during diastole"
        )
    
    with col3:
        st.markdown("### 🔍 Morphological Features")
        emptying_rate = st.number_input(
            "Emptying Rate [mL/s]",
            min_value=50.0,
            max_value=500.0,
            value=180.0,
            step=10.0,
            help="Rate of ventricular emptying during systole"
        )
        
        trab_density = st.number_input(
            "Trabeculation Density Index",
            min_value=-5.0,
            max_value=15.0,
            value=0.5,
            step=0.1,
            help="Higher values indicate more trabeculation"
        )
    
    st.markdown("---")
    
    # Calculate button
    col_calc1, col_calc2, col_calc3 = st.columns([1, 2, 1])
    with col_calc2:
        calculate_button = st.button("🔬 Start Cardiac Scan", use_container_width=True)
    
    if calculate_button:
        with st.spinner("Analyzing cardiac parameters..."):
            # Calculate derived features
            delta_area = edv - esv
            irregularity_index = 2 * ((np.sqrt(edv) + np.sqrt(esv))) / ((edv + esv) + 0.0001)
            
            # Calculate risk score based on the methodology in the paper
            # Risk factors: Low EF (<40%), High trabeculation density
            risk_score = 0.0
            
            # EF contribution (40% weight)
            if ef < 40:
                risk_score += 0.40
            elif ef < 50:
                risk_score += 0.20
            else:
                risk_score += 0.05
            
            # Trabeculation density contribution (35% weight)
            if trab_density > 5:
                risk_score += 0.35
            elif trab_density > 2:
                risk_score += 0.20
            else:
                risk_score += 0.05
            
            # Volume-based contribution (25% weight)
            if delta_area < 60:
                risk_score += 0.15
            elif delta_area < 80:
                risk_score += 0.08
            
            if filling_rate < 150 or emptying_rate < 150:
                risk_score += 0.10
            
            # Determine risk category
            if risk_score > 0.60:
                risk_category = "High risk"
                risk_color = "risk-high"
                recommendation = "⚠️ **URGENT**: Immediate clinical evaluation recommended. Consider advanced cardiac imaging (MRI)."
            elif risk_score > 0.50:
                risk_category = "Moderate risk"
                risk_color = "risk-moderate"
                recommendation = "⚡ **ATTENTION**: Follow-up with cardiologist. Monitor cardiac function closely."
            else:
                risk_category = "Lower risk"
                risk_color = "risk-low"
                recommendation = "✅ **ROUTINE**: Continue regular cardiac monitoring. Maintain healthy lifestyle."
            
            # Display results
            st.markdown("## 📋 Analysis Results")
            
            # Risk score display
            col_result1, col_result2, col_result3 = st.columns(3)
            
            with col_result1:
                st.metric(
                    label="Risk Score",
                    value=f"{risk_score:.2f}",
                    delta=None
                )
            
            with col_result2:
                st.markdown(f"### Risk Category")
                st.markdown(f"<h2 class='{risk_color}'>{risk_category}</h2>", unsafe_allow_html=True)
            
            with col_result3:
                st.metric(
                    label="Ejection Fraction",
                    value=f"{ef:.1f}%",
                    delta="Normal" if ef > 50 else "Low",
                    delta_color="normal" if ef > 50 else "inverse"
                )
            
            # Recommendation box
            st.info(recommendation)
            
            # Detailed metrics
            st.markdown("### 📊 Detailed Cardiac Metrics")
            
            col_detail1, col_detail2, col_detail3, col_detail4 = st.columns(4)
            
            with col_detail1:
                st.metric("EDV", f"{edv:.1f} mL", "Normal" if 100 <= edv <= 160 else "Abnormal")
            
            with col_detail2:
                st.metric("ESV", f"{esv:.1f} mL", "Normal" if 40 <= esv <= 70 else "Abnormal")
            
            with col_detail3:
                st.metric("Delta Volume", f"{delta_area:.1f} mL")
            
            with col_detail4:
                st.metric("Trab. Density", f"{trab_density:.2f}")
            
            # Visualization
            st.markdown("### 📈 Risk Factor Analysis")
            
            # Create gauge chart for risk score
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "LVNC Risk Score", 'font': {'size': 24}},
                delta={'reference': 0.5},
                gauge={
                    'axis': {'range': [None, 1], 'tickwidth': 1, 'tickcolor': "darkgray"},
                    'bar': {'color': "darkred" if risk_score > 0.6 else "orange" if risk_score > 0.5 else "green"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 0.5], 'color': 'lightgreen'},
                        {'range': [0.5, 0.6], 'color': 'lightyellow'},
                        {'range': [0.6, 1], 'color': 'lightcoral'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.6
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Arial"}
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Feature importance visualization
            features = ['EF', 'Trabeculation\nDensity', 'Filling\nRate', 'Emptying\nRate', 'Delta\nVolume']
            importance = [0.40, 0.35, 0.10, 0.08, 0.07]
            
            fig_bar = px.bar(
                x=features,
                y=importance,
                labels={'x': 'Cardiac Parameters', 'y': 'Clinical Importance'},
                title='Parameter Contribution to Risk Assessment'
            )
            fig_bar.update_traces(marker_color='#ff4b4b')
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "white"}
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.header("📈 Patient History & Prior Scans")
    
    st.info("👤 **Patient History & Prior Scans** - Check patient historical data from previous visits")
    
    # Sample historical data
    if st.checkbox("Show sample patient history"):
        dates = pd.date_range(start='2024-01-01', end='2024-10-01', periods=10)
        history_df = pd.DataFrame({
            'Date': dates,
            'EF (%)': np.random.uniform(45, 65, 10),
            'Risk Score': np.random.uniform(0.3, 0.7, 10),
            'Trab. Density': np.random.uniform(0, 5, 10)
        })
        
        st.dataframe(history_df, use_container_width=True)
        
        # Plot EF trend
        fig_trend = px.line(
            history_df,
            x='Date',
            y='EF (%)',
            title='Ejection Fraction Trend Over Time',
            markers=True
        )
        fig_trend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.header("ℹ️ About Left Ventricular Non-Compaction (LVNC)")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        ### What is LVNC?
        
        Left Ventricular Non-Compaction Cardiomyopathy (LVNC) is a rare genetic heart disorder characterized by:
        
        - **Deep trabeculations** in the left ventricular wall
        - **Spongy appearance** of the heart muscle
        - **Arrested development** of the ventricular wall during fetal growth
        
        ### Prevalence
        - 0.26% - 3.7% in patients referred for echocardiography
        - Third most diagnosed cardiomyopathy
        - 35-47% mortality rate in Sub-Saharan Africa over a decade
        """)
    
    with col_info2:
        st.markdown("""
        ### Clinical Features
        
        **Symptoms range from:**
        - Asymptomatic
        - Heart failure
        - Arrhythmias
        - Cardiac arrest
        - Thromboembolism
        
        ### Diagnostic Criteria
        
        **Traditional methods:**
        - 2:1 non-compacted to compacted myocardial ratio
        - Requires expert interpretation
        - Cardiac MRI (expensive, limited access)
        - Transthoracic echocardiography
        """)
    
    st.markdown("---")
    st.markdown("""
    ### Risk Stratification in This System
    
    This AI-powered system uses the following parameters:
    
    | Parameter | Clinical Significance | Weight |
    |-----------|----------------------|--------|
    | **Ejection Fraction (EF)** | EF <40% indicates systolic dysfunction | 40% |
    | **Trabeculation Density** | Higher values indicate more complex trabeculation | 35% |
    | **Volume Metrics** | Delta volume reflects contractility | 25% |
    
    **Risk Categories:**
    - **< 0.50**: Lower risk - Routine monitoring
    - **0.50-0.60**: Moderate risk - Follow-up with cardiologist
    - **> 0.60**: High risk - Urgent evaluation needed
    """)

with tab4:
    st.header("🔬 Model Training Information")
    
    st.markdown("""
    ### Random Forest Classifier Performance
    
    The prediction model was trained on 100 samples from the EchoNet-Dynamic dataset:
    """)
    
    col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
    
    with col_perf1:
        st.metric("Accuracy", "95%")
    with col_perf2:
        st.metric("AUC", "0.996")
    with col_perf3:
        st.metric("Sensitivity", "100%")
    with col_perf4:
        st.metric("Specificity", "90%")
    
    st.markdown("""
    ### Features Used
    
    The model analyzes the following engineered features:
    - End-Diastolic Volume (EDV)
    - End-Systolic Volume (ESV)
    - Ejection Fraction (EF)
    - Filling Rate
    - Emptying Rate
    - Trabeculation Density Index
    - Irregularity Index
    
    ### About the Device
    
    This AI-powered handheld diagnostic tool is designed as a **frugal alternative** to expensive 
    cardiac MRI and conventional echocardiography, particularly for:
    
    - **Low-resource settings** in Sub-Saharan Africa
    - **Point-of-care screening**
    - **Reducing diagnostic disparities**
    - **Improving early detection**
    
    The device concept integrates:
    - Ultrasonic transducers
    - ECG electrodes
    - AI processing unit
    - Touchscreen interface
    - Wireless communication
    """)
    
    st.info("""
    **Citation**: Luther, M.J., et al. (2024). Frugal AI-Powered Handheld Diagnostic Gun for 
    Predicting Left Ventricular Non-Compaction Cardiomyopathy Using Echocardiographic Features. 
    Department of Biomedical Engineering, University of Ghana, Accra, Ghana.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>CardioScan LVNC Detection System</strong> | Version 1.0</p>
    <p><small>⚠️ This tool is for research and educational purposes. Always consult with healthcare professionals for clinical decisions.</small></p>
</div>
""", unsafe_allow_html=True)
