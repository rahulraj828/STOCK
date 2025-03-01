# Indian Stock Market Analytics Dashboard

A comprehensive Streamlit-based stock data visualization tool focused on Indian stock markets (NSE and BSE), providing real-time data fetching and interactive analysis capabilities.

## 🌟 Features

- Real-time stock data from NSE and BSE
- Interactive candlestick charts
- Key market metrics visualization
- Financial information display
- Drag-and-drop customizable dashboard
- CSV data export functionality

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository and main.py as the main file
6. Click "Deploy"

Your app will be live at `https://share.streamlit.io/yourusername/repository-name/main/main.py`

## 📦 Dependencies

The project requires the following Python packages:
```
streamlit>=1.24.0
pandas
yfinance
plotly
nsetools
streamlit-elements
beautifulsoup4
requests
trafilatura
```

## 💻 Local Development

1. Clone the repository:
```bash
git clone <your-repository-url>
cd indian-stock-analytics
```
2. Install dependencies:
```bash
pip install streamlit pandas yfinance plotly nsetools streamlit-elements beautifulsoup4 requests trafilatura
```
3. Run the app:
```bash
streamlit run main.py
```

## 📝 Note

This project is designed to work with Indian stock market data. Make sure you have proper internet connectivity to fetch real-time stock information.

## 🔗 Important Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Deploying Streamlit Apps](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app)