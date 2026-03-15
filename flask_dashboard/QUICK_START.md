# Quick Start Guide - Flask Dashboard

## 🚀 Start in 3 Steps

### Step 1: Install Dependencies
```bash
cd flask_dashboard
pip install -r requirements.txt
```

### Step 2: Run the Flask App
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

---

## 📊 What You Get

A **professional property investment analysis dashboard** with:

✅ **4 Interactive Sliders Groups**
- Property Configuration
- Loan Parameters  
- Growth Assumptions
- Analysis Horizon

✅ **Real-Time Calculations**
- Monthly EMI computation
- Down payment breakdown
- Breakeven year analysis

✅ **3 Beautiful Charts**
- Cost Comparison (Buy vs Rent over time)
- Net Worth Growth trajectories
- Final Net Worth comparison

✅ **Smart KPI Cards**
- Monthly EMI obligation
- Initial investment amount
- Breakeven year indicator
- Intelligent Buy vs Rent verdict

---

## 🎨 Design Features

- **Vercel-Like UI**: Clean, minimal, modern aesthetic
- **Dark Mode Support**: Automatically follows system preference
- **Fully Responsive**: Works perfectly on mobile, tablet, desktop
- **Professional Charts**: Interactive and animated using Chart.js
- **Real-Time Updates**: Instant feedback on slider changes

---

## 📁 Project Structure

```
flask_dashboard/
├── app.py                     # Flask backend + API
├── requirements.txt           # Dependencies
├── QUICK_START.md            # This file
├── README.md                 # Full documentation
├── templates/
│   └── index.html            # Main dashboard
└── static/
    ├── css/
    │   └── style.css         # Vercel-style design
    └── js/
        └── main.js           # Interactive functionality
```

---

## 🔄 How It Works

1. **Adjust sliders** in the left panel
2. **Click "Calculate Analysis"** button
3. **View results** with KPI cards and charts
4. **Analyze insights** to make investment decision

---

## 💡 Example Scenarios

### Scenario 1: Conservative Investor
- Property: ₹1 Cr
- Monthly Rent: ₹40K
- Down Payment: 30%
- Loan Rate: 7.5%
- Tenure: 25 years

### Scenario 2: Optimistic Investor
- Property: ₹2.5 Cr
- Monthly Rent: ₹75K
- Down Payment: 20%
- Loan Rate: 8.5%
- Tenure: 20 years

### Scenario 3: Short Term Analysis
- Same property details
- Analysis Horizon: 5 years
- Check if buying makes sense short-term

---

## 🔧 Troubleshooting

**Port already in use?**
```bash
# Edit app.py and change:
app.run(debug=True, port=8080)  # Use 8080 instead of 5000
```

**No charts showing?**
- Check your internet (Chart.js needs CDN)
- Hard refresh browser (Ctrl+Shift+R)

**Calculations seem wrong?**
- Verify slider ranges
- Check browser console for errors
- Ensure all values are reasonable

---

## 📈 Next Steps

1. Experiment with different scenarios
2. Compare Buy vs Rent verdicts
3. Identify breakeven years
4. Use insights for real estate decisions

---

## 📞 Support

Refer to **README.md** for:
- Detailed API documentation
- Configuration reference
- Customization guide
- Full troubleshooting guide

Enjoy analyzing! 🏠💰
