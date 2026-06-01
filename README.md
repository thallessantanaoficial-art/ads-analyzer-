# 📊 Ads Analyzer - Google Ads & Meta Ads Metrics Tool

A lightweight, modern web application for analyzing and gaining insights from your Google Ads and Meta Ads performance data.

## Features

✨ **Key Capabilities:**
- Upload and analyze CSV files from Google Ads and Meta Ads
- Calculate 10+ key performance metrics automatically
- Generate actionable insights based on your data
- Interactive charts and data visualization
- Responsive design optimized for all devices
- SEO optimized for search engines
- Lightweight and fast (~50KB total assets)

## Metrics Calculated

📈 **Performance Metrics:**
- Total Impressions
- Total Clicks
- Click-Through Rate (CTR)
- Cost Per Click (CPC)
- Cost Per Mille (CPM)
- Total Conversions
- Conversion Rate
- Cost Per Acquisition (CPA)
- Return on Ad Spend (ROAS)
- Total Revenue
- Average Daily Spend

## Insights Generated

💡 **Smart Analysis:**
- CTR analysis with recommendations
- CPC performance evaluation
- Conversion rate assessment
- ROAS profitability analysis
- Daily spend monitoring
- Impression volume tracking

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone or navigate to the project directory:**
```bash
cd ads-analyzer
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open in your browser:**
```
http://localhost:5000
```

3. **Upload your CSV file:**
   - Click the upload area or drag and drop a CSV file
   - The app will analyze it automatically
   - View metrics, insights, and charts

### CSV File Format

Your CSV should include columns like:
```
Date,Impressions,Clicks,Cost,Conversions,Conversion Value
2024-05-01,5000,250,75.50,10,500
2024-05-02,5200,280,84.00,12,600
...
```

The app automatically detects common column names from Google Ads and Meta Ads exports.

## Project Structure

```
ads-analyzer/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   └── analyzer.py       # CSV analysis logic
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── script.js     # Frontend logic
└── uploads/              # Temporary upload folder
```

## Technical Stack

🛠️ **Backend:**
- Flask 2.3.2
- Pandas 2.0.3
- NumPy 1.24.3

🎨 **Frontend:**
- HTML5
- CSS3 (responsive design)
- Vanilla JavaScript
- Chart.js for visualizations

## Performance

⚡ **Optimizations:**
- Lightweight bundle (< 50KB assets)
- Efficient CSV parsing with Pandas
- Server-side analysis for fast results
- Responsive images and lazy loading
- Minimal dependencies
- Gzip compression ready

## SEO Features

🔍 **Search Engine Optimization:**
- Meta tags for social sharing
- Semantic HTML structure
- Open Graph protocol support
- Fast page load times
- Mobile-responsive design
- Structured data ready

## Browser Support

✅ Works on:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## File Size Limits

📁 **Upload Limits:**
- Maximum file size: 10MB
- Accepts CSV format only
- Supports up to 30 days of data display

## Troubleshooting

### File Upload Issues
- Ensure CSV format is correct
- Check file size (max 10MB)
- Verify column names include: Impressions, Clicks, Cost, etc.

### Chart Not Displaying
- Refresh the page
- Ensure JavaScript is enabled
- Check browser console for errors

### Metrics Not Calculating
- Verify CSV column names
- Ensure numeric values are properly formatted
- Check for special characters in data

## Future Enhancements

🚀 **Planned Features:**
- Historical data storage
- Custom date range selection
- Campaign comparison tools
- Export reports as PDF
- Email report scheduling
- Multi-file analysis
- Custom metric creation

## License

MIT License - Free to use and modify

## Support

For issues and questions, please check the troubleshooting section or contact support.

---

**Made with ❤️ for digital marketers**
