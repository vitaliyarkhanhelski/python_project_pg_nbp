# NBP Exchange Rates Dashboard

## 📊 Project Overview

A modern, interactive web application for fetching and visualizing exchange rates and gold prices from the Polish National Bank (NBP) API. The application provides real-time data visualization with an intuitive user interface.

## 🎯 What It Does

- **Currency Exchange Rates**: Fetches and displays USD, EUR, CHF, and GBP exchange rates
- **Gold Price Tracking**: Monitors historical gold prices in PLN
- **Interactive Charts**: Beautiful, responsive line charts with date range selection
- **Data Analysis**: Provides statistics (min, max, average values)
- **Date Range Selection**: Flexible date picker with validation (max 367 days)
- **Real-time Data**: Live data from official NBP API

## 🛠️ Technologies & Libraries

### **Frontend Framework**
- **Streamlit** - Modern Python web framework for data applications
- **Custom CSS** - Professional styling with gradients and responsive design

### **Data Processing**
- **Pandas** - Data manipulation and DataFrame operations
- **Matplotlib** - Chart creation and data visualization
- **Requests** - HTTP API communication

### **API Integration**
- **NBP API** - Official Polish National Bank REST API
- **JSON Data Parsing** - Real-time data processing
- **Error Handling** - Robust API error management

### **Architecture**
- **Modular Design** - Clean separation of concerns
- **Configuration Management** - Centralized settings
- **Component-Based UI** - Reusable UI components

## 🏗️ Project Structure

```
project_nbp/
├── streamlit_app.py      # Main application entry point
├── config.py             # Configuration constants
├── nbp_api_client.py     # API communication layer
├── chart_utils.py        # Chart rendering utilities
├── ui_components.py      # UI rendering components
├── css_utils.py          # CSS styling management
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore rules
```

## ✨ Key Features

### **User Interface**
- 🎨 Modern, responsive design with custom CSS
- 📱 Mobile-friendly layout
- 🎯 Intuitive sidebar controls
- 📊 Interactive data tables
- 📈 Professional chart visualizations

### **Data Management**
- 🔄 Real-time API data fetching
- 📅 Flexible date range selection (2002-present)
- ⚡ Smart data validation
- 🎯 Error handling and user feedback
- 📊 Comprehensive statistics display

### **Technical Excellence**
- 🏗️ Modular, maintainable code architecture
- ⚙️ Centralized configuration management
- 🔧 Reusable component system
- 📝 Clean, documented code
- 🚀 Professional development practices

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access Dashboard**:
   Open `http://localhost:8501` in your browser

## 📈 Data Sources

- **NBP API**: `https://api.nbp.pl/api/`
- **Exchange Rates**: Table A rates (USD, EUR, CHF, GBP)
- **Gold Prices**: Historical gold prices in PLN
- **Data Range**: 2002-present (exchange rates), 2013-present (gold)

## 🎓 Learning Outcomes

This project demonstrates:
- **API Integration** with external data sources
- **Data Visualization** with interactive charts
- **Web Application Development** with Streamlit
- **Software Architecture** with modular design
- **User Experience Design** with responsive interfaces
- **Professional Development** with clean code practices

## 🔗 Repository

**GitHub**: [vitaliyarkhanhelski/python_project_pg_nbp](https://github.com/vitaliyarkhanhelski/python_project_pg_nbp)

---

*Built with ❤️ using Python, Streamlit, and modern web technologies*
