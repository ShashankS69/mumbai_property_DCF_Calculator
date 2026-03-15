from flask import Flask, render_template, request, jsonify
import json
import math

app = Flask(__name__)


def calculate_dcf(params):
    """
    Calculate Buy vs Rent DCF Analysis
    """
    prop_price = params.get('prop_price', 2_00_00_000)
    monthly_rent_input = params.get('monthly_rent_input', 50_000)
    dp_pct = params.get('dp_pct', 20)
    loan_rate = params.get('loan_rate', 8.5)
    tenure = params.get('tenure', 20)
    prop_appr = params.get('prop_appr', 5.0)
    rent_appr = params.get('rent_appr', 5.0)
    inv_ret = params.get('inv_ret', 10.0)
    horizon = params.get('horizon', 10)

    # EMI Calculation
    dp_amount = prop_price * (dp_pct / 100)
    loan_principal = prop_price - dp_amount
    monthly_rate = loan_rate / 100 / 12
    total_months = tenure * 12

    if monthly_rate > 0:
        emi = loan_principal * monthly_rate * ((1 + monthly_rate)**total_months) / (((1 + monthly_rate)**total_months) - 1)
    else:
        emi = loan_principal / total_months

    # Simulation
    annual_prop_rate = prop_appr / 100
    annual_rent_rate = rent_appr / 100
    monthly_inv_rate = inv_ret / 100 / 12
    sim_months = horizon * 12
    portfolio_val = dp_amount
    current_rent_val = monthly_rent_input
    rem_loan_bal = loan_principal
    years, buy_costs, rent_costs, buy_nw, rent_nw = [], [], [], [], []
    cum_out_of_pocket = dp_amount

    for m in range(1, sim_months + 1):
        is_emi_paid = m <= total_months
        pmt = emi if is_emi_paid else 0
        if is_emi_paid:
            interest_paid = rem_loan_bal * monthly_rate
            principal_paid = pmt - interest_paid
            rem_loan_bal -= principal_paid
            if rem_loan_bal < 0:
                rem_loan_bal = 0
        cum_out_of_pocket += pmt
        portfolio_growth = portfolio_val * monthly_inv_rate
        investment_contrib = pmt - current_rent_val
        portfolio_val = portfolio_val + portfolio_growth + investment_contrib
        if m % 12 == 0:
            y = m // 12
            years.append(y)
            curr_prop_val = prop_price * ((1 + annual_prop_rate)**y)
            home_equity = curr_prop_val - rem_loan_bal
            buy_costs.append(cum_out_of_pocket - home_equity)
            rent_costs.append(cum_out_of_pocket - portfolio_val)
            buy_nw.append(home_equity)
            rent_nw.append(portfolio_val)
            current_rent_val *= (1 + annual_rent_rate)

    # Determine breakeven
    breakeven_yr = None
    for y, bc, rc in zip(years, buy_costs, rent_costs):
        if bc < rc:
            breakeven_yr = y
            break

    final_buy_nw = buy_nw[-1] if buy_nw else 0
    final_rent_nw = rent_nw[-1] if rent_nw else 0

    return {
        'emi': round(emi, 2),
        'dp_amount': round(dp_amount, 2),
        'loan_principal': round(loan_principal, 2),
        'years': years,
        'buy_costs': [round(x, 2) for x in buy_costs],
        'rent_costs': [round(x, 2) for x in rent_costs],
        'buy_nw': [round(x, 2) for x in buy_nw],
        'rent_nw': [round(x, 2) for x in rent_nw],
        'breakeven_yr': breakeven_yr,
        'final_buy_nw': round(final_buy_nw, 2),
        'final_rent_nw': round(final_rent_nw, 2),
        'verdict': 'BUYING' if breakeven_yr else 'RENTING'
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    result = calculate_dcf(data)
    return jsonify(result)


@app.route('/api/defaults', methods=['GET'])
def api_defaults():
    defaults = {
        'prop_price': 2_00_00_000,
        'monthly_rent_input': 50_000,
        'dp_pct': 20,
        'loan_rate': 8.5,
        'tenure': 20,
        'prop_appr': 5.0,
        'rent_appr': 5.0,
        'inv_ret': 10.0,
        'horizon': 10
    }
    return jsonify(defaults)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
