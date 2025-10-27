# LVNC CardioScan Pro - Streamlit Application

AI-Powered Handheld Diagnostic Tool for Predicting Left Ventricular Non-Compaction Cardiomyopathy

## About

This application implements the research from "Frugal AI-Powered Handheld Diagnostic Gun for Predicting Left Ventricular Non-Compaction Cardiomyopathy Using Echocardiographic Features" by Maxwell John Luther et al., Department of Biomedical Engineering, University of Ghana.

## Features

- 📊 Real-time cardiac parameter analysis
- 🎯 LVNC risk score calculation
- 📈 Patient history tracking
- 🔬 Machine learning-based predictions
- 📱 Responsive web interface
- 🌍 Designed for low-resource settings

## Installation

### Local Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run lvnc_app.py
```

4. Open your browser to `http://localhost:8501`

## Deployment

### Deploy to Streamlit Cloud (FREE)

1. Create a GitHub account if you don't have one

2. Create a new repository and upload these files:
   - `lvnc_app.py`
   - `requirements.txt`
   - `README.md`

3. Go to [share.streamlit.io](https://share.streamlit.io)

4. Sign in with GitHub

5. Click "New app"

6. Select your repository, branch (main), and main file (lvnc_app.py)

7. Click "Deploy"

Your app will be live in a few minutes at a URL like: `https://your-app-name.streamlit.app`

### Alternative Deployment Options

#### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku main
```

#### AWS/GCP/Azure
Deploy as a containerized application using Docker (see below)

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY lvnc_app.py .
EXPOSE 8501
CMD ["streamlit", "run", "lvnc_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t lvnc-app .
docker run -p 8501:8501 lvnc-app
```

## Usage

1. **Enter Patient Data**: Input cardiac parameters including:
   - End-Diastolic Volume (EDV)
   - End-Systolic Volume (ESV)
   - Ejection Fraction (EF)
   - Filling Rate
   - Emptying Rate
   - Trabeculation Density

2. **Calculate Risk**: Click "Start Cardiac Scan" to analyze

3. **Review Results**: 
   - Risk score (0.0 - 1.0)
   - Risk category (Low/Moderate/High)
   - Clinical recommendations
   - Detailed metrics and visualizations

## Risk Stratification

| Risk Score | Category | Action |
|------------|----------|--------|
| < 0.50 | Lower Risk | Routine monitoring |
| 0.50 - 0.60 | Moderate Risk | Follow-up with cardiologist |
| > 0.60 | High Risk | Urgent clinical evaluation |

## Model Performance

Based on 100 samples from EchoNet-Dynamic dataset:
- **Accuracy**: 95%
- **AUC**: 0.996
- **Sensitivity**: 100%
- **Specificity**: 90%

## Clinical Significance

### Key Parameters

1. **Ejection Fraction (EF)** [40% weight]
   - Normal: >50%
   - High risk: <40%

2. **Trabeculation Density** [35% weight]
   - Higher values indicate more complex trabeculation
   - Associated with LVNC pathology

3. **Volume Metrics** [25% weight]
   - Delta volume reflects cardiac contractility

## Important Notes

⚠️ **Medical Disclaimer**: This tool is for research and educational purposes only. It is designed to assist healthcare professionals and should NOT replace clinical judgment or standard diagnostic procedures.

- Always consult with qualified healthcare professionals
- Use in conjunction with standard cardiac imaging
- Intended for screening and risk stratification only
- Not FDA approved for clinical diagnosis

## About LVNC

Left Ventricular Non-Compaction Cardiomyopathy is a rare genetic disorder characterized by:
- Deep trabeculations in the left ventricle
- Spongy appearance of heart muscle
- 35-47% mortality rate in Sub-Saharan Africa

This tool aims to improve early detection in low-resource settings where cardiac MRI and advanced echocardiography are often inaccessible.

## Technology Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (Random Forest)
- **Visualization**: Plotly
- **Language**: Python 3.9+

## Contributing

This project is based on academic research. For contributions or questions, please contact:

**Department of Biomedical Engineering**  
University of Ghana  
Accra, Ghana

## License

Educational and Research Use Only

## Citation

If you use this tool in your research, please cite:

```
Luther, M.J., Anim, P.T., Rockson, M.A., Buabeng, J.A., Kuwornu, P., Yeboah, S., & Angelina, A. (2024). 
Frugal AI-Powered Handheld Diagnostic Gun for Predicting Left Ventricular Non-Compaction Cardiomyopathy 
Using Echocardiographic Features. Department of Biomedical Engineering, University of Ghana, Accra, Ghana.
```

## Support

For technical support or questions about deployment, please open an issue in the repository.

---

**Version**: 1.0  
**Last Updated**: October 2024