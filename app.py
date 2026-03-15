import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config FIRST
st.set_page_config(page_title="Mumbai Property Market", layout="wide")

# =========================================================
# GLOBAL CSS INJECTION (DARK TARGETED THEME)
# =========================================================
css_inject = """
<style>
/* 1. Global typography and background */
body, .stApp {
    background-color: #0F1923 !important;
    color: #E8EDF2 !important;
    font-family: 'Inter', 'Arial', sans-serif !important;
}
h1, h2, h3, h4, h5, h6, p, span, div, label { color: #E8EDF2; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0F1923; }
::-webkit-scrollbar-thumb { background: #2A3A4A; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #C9A84C; }
.top-header-bar {
    background-color: #0F1923;
    color: #E8EDF2;
    padding: 1rem 0;
    margin-bottom: 24px;
    border-bottom: 2px solid #C9A84C;
    font-size: 24px;
    font-weight: 700;
}
/* 2. Sidebar styling */
.stSidebar, [data-testid="stSidebar"] {
    background-color: #141E27 !important;
    border-right: 1px solid #2A3A4A !important;
}
.sidebar-logo {
    color: #FFFFFF;
    font-weight: bold;
    font-size: 13px;
    margin-bottom: 2rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.sidebar-logo::before { content: "◆ "; color: #C9A84C; }
.sidebar-section-header {
    font-size: 13px;
    font-weight: 600;
    color: #8A9BB0;
    text-transform: lowercase;
    font-variant: small-caps;
    border-left: 3px solid #C9A84C;
    padding-left: 8px;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
.sidebar-divider { border-top: 1px solid #2A3A4A; margin: 24px 0; }
.stSidebar label {
    color: #C9A84C !important;
    font-size: 11px !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-variant: small-caps;
}
[data-baseweb="select"] > div, [data-baseweb="input"] > div {
    background-color: #1A2633 !important;
    border-color: #2A3A4A !important;
    color: #E8EDF2 !important;
}
[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"] > div:focus-within { border-color: #C9A84C !important; }
[data-baseweb="popover"] > div, ul[role="listbox"] {
    background-color: #1A2633 !important;
    border-color: #2A3A4A !important;
}
ul[role="listbox"] li { background-color: transparent !important; color: #E8EDF2 !important; }
span[data-baseweb="tag"] { background-color: #1B3A5C !important; border-color: #2A3A4A !important; }
span[data-baseweb="tag"] span { color: #E8EDF2 !important; }
span[data-baseweb="tag"] button { color: #8A9BB0 !important; }
div[data-baseweb="slider"] [data-testid="stSlider"] div div div div { background: #C9A84C !important; }
div[data-baseweb="slider"] div[role="slider"] { background: #C9A84C !important; border-color: #C9A84C !important; }
[data-testid="stSlider"] > div > div > div > div { background: #C9A84C !important; }
[data-testid="stSlider"] span { background: #C9A84C !important; border-color: #C9A84C !important; }
.stRadio div[role="radiogroup"] input:checked + div { background-color: #C9A84C !important; border-color: #C9A84C !important; }
.stRadio div[role="radiogroup"] input:checked + div::after { background-color: #0F1923 !important; }
:root { --primary-color: #C9A84C !important; }
/* 3. Section Headers */
.section-heading {
    color: #E8EDF2;
    font-size: 20px;
    font-weight: 600;
    border-left: 4px solid #C9A84C;
    padding-left: 12px;
    margin: 32px 0 16px 0;
}
hr { border-color: #2A3A4A !important; }
/* 4. Tabs */
.tab-content-container { padding-top: 24px; }
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent !important;
    gap: 32px;
    border-bottom: 1px solid #2A3A4A !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #8A9BB0 !important;
    border-bottom: 2px solid transparent !important;
    background-color: transparent !important;
    font-weight: 500 !important;
    padding: 12px 0px !important;
}
.stTabs [aria-selected="true"] {
    color: #E8EDF2 !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #C9A84C !important;
}
/* 5. KPI Cards */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { display: none; }
.kpi-card {
    background-color: #1A2633;
    border: 1px solid #2A3A4A;
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}
.kpi-label { font-size: 12px; font-weight: 600; color: #8A9BB0; text-transform: lowercase; font-variant: small-caps; letter-spacing: 0.5px; margin-bottom: 8px; }
.kpi-value { font-size: 28px; font-weight: 700; color: #E8EDF2; margin-bottom: 4px; }
.kpi-subtitle { font-size: 12px; color: #8A9BB0; }
/* 6. Chart containers */
.chart-container-wrapper {
    background-color: #1A2633;
    padding: 16px;
    border-radius: 6px;
    border: 1px solid #2A3A4A;
    margin-bottom: 24px;
}
/* 7. Listings Browser */
.pill-badge {
    background-color: #1B3A5C;
    color: #E8EDF2;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 16px;
}
[data-testid="stDataFrame"] thead tr th {
    background-color: #141E27 !important;
    color: #E8EDF2 !important;
    border-bottom: 1px solid #2A3A4A !important;
}
/* 8. Buy vs Rent */
.emi-card {
    background-color: #1A2633;
    border: 1px solid #2A3A4A;
    border-top: 3px solid #C9A84C;
    border-radius: 8px;
    padding: 24px;
    text-align: center;
}
.emi-label { font-size: 13px; font-weight: 600; color: #8A9BB0; text-transform: lowercase; font-variant: small-caps; letter-spacing: 1px; margin-bottom: 8px; }
.emi-value { font-size: 36px; font-weight: 700; color: #E8EDF2; }
.verdict-box { margin-top: 16px; padding: 16px; border-radius: 6px; font-weight: 600; font-size: 15px; background-color: #1A2633; border: 1px solid #2A3A4A; }
.verdict-buy { border-left: 4px solid #4CAF7D; color: #4CAF7D; }
.verdict-rent { border-left: 4px solid #C9A84C; color: #C9A84C; }
</style>
"""

st.markdown(css_inject, unsafe_allow_html=True)
st.markdown('<div class="top-header-bar">Mumbai Property Market Intelligence</div>', unsafe_allow_html=True)

COLOR_MAP = {
    "Bandra": "#1B3A5C",
    "Chembur": "#2E86AB",
    "Powai": "#C9A84C",
    "Andheri": "#4CAF7D",
    "Thane": "#8B6F9E"
}
FONT_FAMILY = "'Inter', 'Arial', sans-serif"
CHART_BG = "rgba(0,0,0,0)"
PAPER_BG = "#1A2633"
TICK_TXT = "#8A9BB0"
TITLE_TXT = "#E8EDF2"
GRID_COLOR = "#2A3A4A"

def apply_corporate_layout(fig):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAMILY, color=TICK_TXT),
        title=dict(font=dict(size=14, color=TITLE_TXT, family=FONT_FAMILY), y=0.95, x=0.01, xanchor='left'),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=TICK_TXT))
    )
    fig.update_xaxes(showgrid=False, zeroline=False, showline=True, linewidth=1, linecolor=GRID_COLOR, tickfont=dict(color=TICK_TXT), title_font=dict(color=TICK_TXT))
    fig.update_yaxes(showgrid=True, gridcolor=GRID_COLOR, gridwidth=1, zeroline=False, showline=False, tickfont=dict(color=TICK_TXT), title_font=dict(color=TICK_TXT))
    return fig

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_listings.csv")
    df['date_listed'] = pd.to_datetime(df['date_listed'], errors='coerce')
    df['furnishing'] = df['furnishing'].fillna('Unknown')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.markdown('<div class="sidebar-logo">Market Intel Board</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section-header">Market Filters</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="margin-bottom: 8px"></div>', unsafe_allow_html=True)

all_markets = sorted(df['micro_market'].dropna().unique())
all_beds = sorted(df['bedrooms'].dropna().unique())
all_furnishings = sorted(df['furnishing'].unique())

selected_markets = st.sidebar.multiselect("Micro Market", all_markets, default=all_markets)
selected_beds = st.sidebar.multiselect("Bedrooms (BHK)", all_beds, default=all_beds)
listing_type = st.sidebar.radio("Listing Type", ["Both", "Sale", "Rent"], index=0)
selected_furnishing = st.sidebar.multiselect("Furnishing", all_furnishings, default=all_furnishings)

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-section-header">DCF Settings</div>', unsafe_allow_html=True)

prop_price = st.sidebar.slider("Property price (₹)", 50_00_000, 10_00_00_000, 2_00_00_000, step=10_00_000)
monthly_rent_input = st.sidebar.slider("Monthly rent equivalent (₹)", 10_000, 500_000, 50_000, step=5_000)
dp_pct = st.sidebar.slider("Down payment (%)", 10, 40, 20)
loan_rate = st.sidebar.slider("Loan interest rate (%)", 6.0, 14.0, 8.5, step=0.1)
tenure = st.sidebar.slider("Loan tenure (years)", 5, 30, 20)

st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

prop_appr = st.sidebar.slider("Annual property appreciation (%)", 0.0, 15.0, 5.0, step=0.1)
rent_appr = st.sidebar.slider("Annual rent increase (%)", 0.0, 10.0, 5.0, step=0.1)
inv_ret = st.sidebar.slider("Investment return on down payment (%)", 4.0, 15.0, 10.0, step=0.1)
horizon = st.sidebar.slider("Analysis horizon (years)", 1, 30, 10)

# --- FILTER ---
filtered_df = df[
    (df['micro_market'].isin(selected_markets)) &
    (df['bedrooms'].isin(selected_beds)) &
    (df['furnishing'].isin(selected_furnishing))
].copy()

if listing_type != "Both":
    filtered_df = filtered_df[filtered_df['listing_type'] == listing_type]

filtered_df['bedrooms_str'] = filtered_df['bedrooms'].astype(str) + ' BHK'

# --- TABS ---
st.markdown('<div class="tab-content-container"></div>', unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(["Market Overview", "Trends", "Listings Browser", "Buy vs Rent DCF Calculator"])

# ------------- TAB 1 -------------
with tab1:
    if filtered_df.empty:
        st.warning("No listings match your filters.")
    else:
        st.markdown('<div class="section-heading">Key Market Metrics</div>', unsafe_allow_html=True)

        total_list = f"{len(filtered_df):,}"

        # ── FIXED: Both mode now shows values for both KPIs ──
        med_price_v = filtered_df['sale_price_cr'].median()
        med_price = f"₹{med_price_v:,.2f} Cr" if listing_type in ["Sale", "Both"] and not pd.isna(med_price_v) else "—"

        med_rent_v = filtered_df['monthly_rent_inr'].median()
        med_rent = f"₹{med_rent_v:,.0f}" if listing_type in ["Rent", "Both"] and not pd.isna(med_rent_v) else "—"

        med_psf_v = filtered_df['price_per_sqft'].median()
        med_psf = f"₹{med_psf_v:,.0f}" if not pd.isna(med_psf_v) else "—"

        kpi_html = f"""
        <div style="display: flex; gap: 16px; margin-bottom: 32px;">
            <div style="flex: 1;" class="kpi-card">
                <div class="kpi-label">Total Listings</div>
                <div class="kpi-value">{total_list}</div>
                <div class="kpi-subtitle">Matching current filters</div>
            </div>
            <div style="flex: 1;" class="kpi-card">
                <div class="kpi-label">Median Sale Price</div>
                <div class="kpi-value">{med_price}</div>
                <div class="kpi-subtitle">Across selected configs</div>
            </div>
            <div style="flex: 1;" class="kpi-card">
                <div class="kpi-label">Median Rent (Monthly)</div>
                <div class="kpi-value">{med_rent}</div>
                <div class="kpi-subtitle">Across selected configs</div>
            </div>
            <div style="flex: 1;" class="kpi-card">
                <div class="kpi-label">Median Price / SqFt</div>
                <div class="kpi-value">{med_psf}</div>
                <div class="kpi-subtitle">Based on available data</div>
            </div>
        </div>
        """
        st.markdown(kpi_html, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">Pricing Analysis</div>', unsafe_allow_html=True)
        r1_c1, r1_c2 = st.columns([1, 1], gap="large")

        with r1_c1:
            st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
            # ── FIXED: Both mode shows sale price chart ──
            if listing_type in ["Sale", "Both"]:
                grp1 = filtered_df.groupby(['micro_market', 'bedrooms_str'])['sale_price_cr'].median().reset_index()
                if not grp1.empty:
                    fig1 = px.bar(grp1, x='micro_market', y='sale_price_cr', color='bedrooms_str', barmode='group',
                                  title="Median Sale Price (Cr) by Market & BHK",
                                  labels={'micro_market': '', 'sale_price_cr': 'Median Sale Price (Cr)', 'bedrooms_str': 'BHK'},
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                    fig1 = apply_corporate_layout(fig1)
                    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Not enough data for Sale Price chart")
            else:
                grp1 = filtered_df.groupby(['micro_market', 'bedrooms_str'])['monthly_rent_inr'].median().reset_index()
                if not grp1.empty:
                    fig1 = px.bar(grp1, x='micro_market', y='monthly_rent_inr', color='bedrooms_str', barmode='group',
                                  title="Median Rent (₹) by Market & BHK",
                                  labels={'micro_market': '', 'monthly_rent_inr': 'Median Rent (₹)', 'bedrooms_str': 'BHK'},
                                  color_discrete_sequence=px.colors.qualitative.Safe)
                    fig1 = apply_corporate_layout(fig1)
                    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Not enough data for Rent chart")
            st.markdown('</div>', unsafe_allow_html=True)

        with r1_c2:
            st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
            psf_df = filtered_df.dropna(subset=['area_sqft'])
            if not psf_df.empty:
                grp2 = psf_df.groupby('micro_market')['price_per_sqft'].median().reset_index()
                fig2 = px.bar(grp2, x='micro_market', y='price_per_sqft', color='micro_market',
                              color_discrete_map=COLOR_MAP, title="Median Price / SqFt by Market",
                              labels={'micro_market': '', 'price_per_sqft': 'Median Price/SqFt (₹)'})
                fig2.update_layout(showlegend=False)
                fig2 = apply_corporate_layout(fig2)
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Not enough data for Price/SqFt chart")
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        st.markdown('<div class="section-heading">Distribution Metrics</div>', unsafe_allow_html=True)
        r2_c1, r2_c2 = st.columns([1, 1], gap="large")

        with r2_c1:
            st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
            # ── FIXED: Both mode shows sale price distribution ──
            if listing_type in ["Sale", "Both"]:
                fig3 = px.box(filtered_df, x='micro_market', y='sale_price_cr', color='micro_market',
                              color_discrete_map=COLOR_MAP, title="Sale Price Distribution by Market (Cr)",
                              labels={'micro_market': '', 'sale_price_cr': 'Sale Price (Cr)'})
                fig3.update_layout(showlegend=False)
                fig3 = apply_corporate_layout(fig3)
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            else:
                fig3 = px.box(filtered_df, x='micro_market', y='monthly_rent_inr', color='micro_market',
                              color_discrete_map=COLOR_MAP, title="Rent Distribution by Market (₹)",
                              labels={'micro_market': '', 'monthly_rent_inr': 'Monthly Rent (₹)'})
                fig3.update_layout(showlegend=False)
                fig3 = apply_corporate_layout(fig3)
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)


# ------------- TAB 2 -------------
with tab2:
    trends_df = filtered_df.dropna(subset=['date_listed']).copy()
    if trends_df.empty:
        st.warning("No listings match your filters or missing date information.")
    else:
        st.markdown('<div class="section-heading">Market Time Series</div>', unsafe_allow_html=True)
        trends_df['month'] = trends_df['date_listed'].dt.strftime('%b %Y')
        trends_df = trends_df.sort_values('date_listed')

        col_t1, col_t2 = st.columns([1, 1], gap="large")

        with col_t1:
            st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
            if listing_type in ["Sale", "Both"]:
                grp_t = trends_df.groupby(['month', 'micro_market'], sort=False)['sale_price_cr'].median().reset_index()
                fig_t1 = px.line(grp_t, x='month', y='sale_price_cr', color='micro_market',
                                 color_discrete_map=COLOR_MAP, markers=True,
                                 title="Monthly Median Sale Price Progression",
                                 labels={'month': '', 'sale_price_cr': 'Median Sale Price (Cr)'})
            else:
                grp_t = trends_df.groupby(['month', 'micro_market'], sort=False)['monthly_rent_inr'].median().reset_index()
                fig_t1 = px.line(grp_t, x='month', y='monthly_rent_inr', color='micro_market',
                                 color_discrete_map=COLOR_MAP, markers=True,
                                 title="Monthly Median Rent Progression",
                                 labels={'month': '', 'monthly_rent_inr': 'Median Rent (₹)'})
            fig_t1 = apply_corporate_layout(fig_t1)
            st.plotly_chart(fig_t1, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_t2:
            st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
            grp_vol = trends_df.groupby(['month', 'micro_market'], sort=False).size().reset_index(name='count')
            fig_t2 = px.bar(grp_vol, x='month', y='count', color='micro_market',
                            color_discrete_map=COLOR_MAP, barmode='group',
                            title="Listing Volume Inflow",
                            labels={'month': '', 'count': 'Number of Listings'})
            fig_t2 = apply_corporate_layout(fig_t2)
            st.plotly_chart(fig_t2, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)


# ------------- TAB 3 -------------
with tab3:
    if filtered_df.empty:
        st.warning("No listings match your filters.")
    else:
        st.markdown('<div class="section-heading">Listings Data Explorer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pill-badge">Showing {len(filtered_df)} of {len(df)} listings</div>', unsafe_allow_html=True)

        display_cols = ['micro_market', 'sub_locality', 'bedrooms', 'listing_type',
                        'sale_price_cr', 'monthly_rent_inr', 'area_sqft', 'price_per_sqft',
                        'furnishing', 'date_listed', 'source_url']
        display_cols = [c for c in display_cols if c in filtered_df.columns]

        def bg_color_alternating(s):
            return ['background-color: #1A2633; color: #E8EDF2' if i % 2 == 0
                    else 'background-color: #141E27; color: #E8EDF2' for i in range(len(s))]

        styled_df = filtered_df[display_cols].copy().reset_index(drop=True)
        styled_df = styled_df.style.apply(bg_color_alternating)
        styled_df = styled_df.format({
            "sale_price_cr": "₹{:,.2f} Cr",
            "monthly_rent_inr": "₹{:,.0f}",
            "price_per_sqft": "₹{:,.0f}",
            "area_sqft": "{:,.0f}"
        }, na_rep="-")

        st.dataframe(
            styled_df,
            column_config={
                "source_url": st.column_config.LinkColumn("Source URL"),
                "sale_price_cr": st.column_config.Column("Sale Price (Cr)"),
                "monthly_rent_inr": st.column_config.Column("Monthly Rent"),
                "price_per_sqft": st.column_config.Column("Price/SqFt"),
                "area_sqft": st.column_config.Column("Area (SqFt)"),
                "date_listed": st.column_config.DateColumn("Date Listed", format="YYYY-MM-DD")
            },
            hide_index=True,
            use_container_width=True
        )


# ------------- TAB 4 -------------
with tab4:
    st.markdown('<div class="section-heading">Strategic Acquisition Analysis (Buy vs Rent)</div>', unsafe_allow_html=True)

    dp_amount = prop_price * (dp_pct / 100)
    loan_principal = prop_price - dp_amount
    monthly_rate = loan_rate / 100 / 12
    total_months = tenure * 12

    if monthly_rate > 0:
        emi = loan_principal * monthly_rate * ((1 + monthly_rate)**total_months) / (((1 + monthly_rate)**total_months) - 1)
    else:
        emi = loan_principal / total_months

    st.markdown(f"""
    <div class="emi-card">
        <div class="emi-label">Calculated EMI Obligation</div>
        <div class="emi-value">₹ {emi:,.0f} <span style="font-size: 16px; font-weight: 500; color: #8A9BB0;">/ month</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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

    df_compare = pd.DataFrame({
        "Year": years,
        "Buying Cost": buy_costs,
        "Renting Cost": rent_costs,
        "Buying Net Worth": buy_nw,
        "Renting Net Worth": rent_nw
    })

    breakeven_yr = None
    for y, bc, rc in zip(years, buy_costs, rent_costs):
        if bc < rc:
            breakeven_yr = y
            break

    st.markdown('<div class="section-heading">Financial Growth Trajectory</div>', unsafe_allow_html=True)
    col_dcf1, col_dcf2 = st.columns([1, 1], gap="large")

    with col_dcf1:
        st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
        fig_dcf = px.line(df_compare, x="Year", y=["Buying Cost", "Renting Cost"],
                          title="Cumulative Equivalent Cost (Lower is Better)",
                          labels={"value": "Total Cost (₹)", "variable": "Scenario", "Year": ""},
                          color_discrete_map={"Buying Cost": "#4CAF7D", "Renting Cost": "#C9A84C"})
        fig_dcf = apply_corporate_layout(fig_dcf)
        if breakeven_yr is not None:
            fig_dcf.add_vline(x=breakeven_yr, line_dash="dash", line_color="#4CAF7D",
                              annotation_text=f"Breakeven: Yr {breakeven_yr}")
            st.markdown(f'<div class="verdict-box verdict-buy">Verdict: Acquisition outpaces renting after year {breakeven_yr}.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="verdict-box verdict-rent">Verdict: Renting remains financially optimal across the horizon.</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_dcf, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_dcf2:
        st.markdown('<div class="chart-container-wrapper">', unsafe_allow_html=True)
        final_buy_nw = buy_nw[-1] if buy_nw else 0
        final_rent_nw = rent_nw[-1] if rent_nw else 0
        fig_nw = go.Figure(data=[
            go.Bar(name='Buying', x=['Projected Horizon'], y=[final_buy_nw], marker_color='#1B3A5C'),
            go.Bar(name='Renting', x=['Projected Horizon'], y=[final_rent_nw], marker_color='#C9A84C')
        ])
        fig_nw.update_layout(title=f"Net Worth Outcome (Year {horizon})", yaxis_title="Net Worth (₹)", barmode='group')
        fig_nw = apply_corporate_layout(fig_nw)
        st.plotly_chart(fig_nw, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Yearly Amortization & Growth Data</div>', unsafe_allow_html=True)

    def bg_color_alternating_dcf(s):
        return ['background-color: #1A2633; color: #E8EDF2' if i % 2 == 0
                else 'background-color: #141E27; color: #E8EDF2' for i in range(len(s))]

    styled_df_comp = df_compare.style.apply(bg_color_alternating_dcf).format({
        "Buying Cost": "₹{:,.0f}",
        "Renting Cost": "₹{:,.0f}",
        "Buying Net Worth": "₹{:,.0f}",
        "Renting Net Worth": "₹{:,.0f}"
    })

    st.dataframe(styled_df_comp, use_container_width=True, hide_index=True)