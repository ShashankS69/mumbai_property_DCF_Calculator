# Property DCF Calculator - Flask Dashboard

A modern, Vercel-inspired Flask application for **Buy vs Rent Financial Analysis** with dynamic sliders and real-time DCF (Discounted Cash Flow) calculations.

## Features

✨ **Modern UI Design**
- Clean, minimal Vercel-like interface
- Dark mode support (follows system preference)
- Responsive layout (desktop & mobile)
- Professional typography and spacing

🎯 **Dynamic Dashboard**
- Real-time slider adjustments
- KPI cards showing key metrics
- Interactive charts (Chart.js)
- Cost comparison visualization
- Net worth projections

💰 **Complete DCF Analysis**
- Property price & rent configuration
- Loan parameters (interest rate, tenure, down payment)
- Growth assumptions (property appreciation, rent inflation)
- Investment return calculations
- Breakeven year analysis
- Buy vs Rent verdict

## Project Structure

```
flask_dashboard/
├── app.py                      # Flask backend with DCF calculations
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Main HTML template
└── static/
    ├── css/
    │   └── style.css          # Vercel-like styling
    └── js/
        └── main.js            # Client-side interactivity & charts
```

## Installation

### 1. Navigate to the Flask Dashboard Directory

```bash
cd flask_dashboard
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask Server

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## How to Use

### 1. **Adjust Parameters**
   - Use the left panel sliders to configure:
     - **Property Details**: Property price, equivalent monthly rent
     - **Loan Configuration**: Down payment %, interest rate, tenure
     - **Growth Assumptions**: Property appreciation, rent increase, investment returns
     - **Analysis Horizon**: Years to analyze (1-30)

### 2. **View Results**
   - **KPI Cards** display:
     - Monthly EMI obligation
     - Initial down payment amount
     - Breakeven year (when buying becomes cheaper than renting)
     - Recommendation (BUY vs RENT)

### 3. **Analyze Charts**
   - **Cost Comparison**: Shows cumulative equivalent costs over time
   - **Net Worth Projection**: Visualizes wealth accumulation for both scenarios
   - **Final Net Worth**: Bar chart comparing end-of-horizon values

### 4. **Make Decisions**
   - Green lines indicate buying scenario
   - Orange lines indicate renting scenario
   - The verdict helps you decide based on financial projections

## API Endpoints

### Calculate DCF Analysis
```http
POST /api/calculate
Content-Type: application/json

{
  "prop_price": 200000000,
  "monthly_rent_input": 50000,
  "dp_pct": 20,
  "loan_rate": 8.5,
  "tenure": 20,
  "prop_appr": 5.0,
  "rent_appr": 5.0,
  "inv_ret": 10.0,
  "horizon": 10
}
```

**Response:**
```json
{
  "emi": 1000000,
  "dp_amount": 40000000,
  "loan_principal": 160000000,
  "years": [1, 2, 3, ...],
  "buy_costs": [...],
  "rent_costs": [...],
  "buy_nw": [...],
  "rent_nw": [...],
  "breakeven_yr": 15,
  "final_buy_nw": 500000000,
  "final_rent_nw": 450000000,
  "verdict": "BUYING"
}
```

### Get Default Parameters
```http
GET /api/defaults
```

## Configuration Reference

### Property Details
| Parameter | Range | Default | Unit |
|-----------|-------|---------|------|
| Property Price | 5 Cr - 100 Cr | 2 Cr | ₹ |
| Monthly Rent | ₹10K - ₹500K | ₹50K | ₹ |

### Loan Configuration
| Parameter | Range | Default | Unit |
|-----------|-------|---------|------|
| Down Payment | 10% - 40% | 20% | % |
| Interest Rate | 6% - 14% | 8.5% | % p.a. |
| Tenure | 5 - 30 | 20 | years |

### Growth Assumptions
| Parameter | Range | Default | Unit |
|-----------|-------|---------|------|
| Property Appreciation | 0% - 15% | 5% | % p.a. |
| Rent Increase | 0% - 10% | 5% | % p.a. |
| Investment Return | 4% - 15% | 10% | % p.a. |
| Analysis Horizon | 1 - 30 | 10 | years |

## Understanding the Analysis

### What is Breakeven Year?
The breakeven year is when the cumulative cost of buying (inclusive of down payment + EMI - home equity) becomes LESS than the cumulative cost of renting (rent paid - investment value). 

**Green Verdict (BUYING):** If breakeven occurs within your horizon, buying becomes financially superior.

**Amber Verdict (RENTING):** If no breakeven within horizon, renting remains optimal based on your assumptions.

### EMI Calculation
EMI is calculated using the standard formula:
```
EMI = P × r × (1 + r)^n / ((1 + r)^n - 1)

Where:
- P = Loan Principal
- r = Monthly Interest Rate
- n = Total Monthly Payments
```

### Net Worth Projection
- **Buying NW** = Current Property Value - Remaining Loan Balance
- **Renting NW** = Down Payment (if renting) + Investment Growth from savings difference

## Customization

### Change Color Scheme
Edit `static/css/style.css`:
```css
:root {
  --accent-color: #3b82f6;     /* Primary blue */
  --success-color: #10b981;    /* Green for buy */
  --warning-color: #f59e0b;    /* Orange for rent */
}
```

### Adjust Range Limits
Edit `templates/index.html` - modify the `min`, `max`, and `step` attributes on range inputs:
```html
<input type="range" id="prop_price" min="50000000" max="1000000000" step="10000000">
```

### Modify Chart Styling
Edit `static/js/main.js` and adjust the Chart.js configuration objects.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (responsive)

## Dependencies

- **Flask 2.3.3**: Web framework
- **Chart.js**: Interactive charts (CDN)
- **Vanilla JavaScript**: No frontend framework required

## Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
gunicorn --bind 0.0.0.0:8000 app:app
# Or modify app.py:
app.run(debug=True, port=8080)
```

### Chart Not Rendering
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Try hard-refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Calculation Issues
- Verify all slider values are within valid ranges
- Check Flask server logs for errors
- Inspect network requests in browser DevTools

## License

This project is part of the Mumbai Property Market Intelligence application suite.

## Support

For issues or feature requests, check the main repository documentation.
