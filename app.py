"""
UAE Promo Pulse - COMPLETE ENHANCED Dashboard
With custom dataset upload, error filtering, and comprehensive logging
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from simulator import PromoSimulator
import numpy as np
import io
import sys
import os
import time
import logging
from datetime import datetime
from typing import Tuple, Dict, Optional, List
import warnings
import json

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.streamlit'))

# Page config
st.set_page_config(
    page_title="UAE Promo Pulse Dashboard",
    page_icon="🇦🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for error logs
if 'error_logs' not in st.session_state:
    st.session_state.error_logs = []

if 'data_quality_report' not in st.session_state:
    st.session_state.data_quality_report = {}

# Professional Color Palette
COLORS = {
    'primary': '#1e3a8a',
    'secondary': '#3b82f6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#06b6d4',
}

# Professional Executive Dashboard CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #faf8f3;
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1600px;
        margin: 0 auto;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.5rem !important;
        line-height: 1.2 !important;
    }
    
    h2 {
        font-size: 1.875rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        letter-spacing: -0.01em !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #334155 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    .metric-card {
        background: #bae6fd;
        padding: 1.75rem;
        border-radius: 16px;
        border: 1px solid #7dd3fc;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #38bdf8;
    }
    
    .metric-card h3 {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #0c4a6e !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 0.75rem 0 !important;
    }
    
    .metric-card h1 {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin: 0 !important;
        line-height: 1 !important;
    }
    
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        min-height: 600px;
        width: 100%;
    }
    
    .error-log-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
    }
    
    .warning-log-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
    }
    
    .success-log-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.625rem 1.5rem;
        font-weight: 600;
        font-size: 0.9375rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px 0 rgba(59, 130, 246, 0.4);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
    }
</style>
""", unsafe_allow_html=True)

def log_error(message: str, level: str = "ERROR"):
    """Add error to session state logs"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        'timestamp': timestamp,
        'level': level,
        'message': message
    }
    st.session_state.error_logs.append(log_entry)
    
    # Also log to logger
    if level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)
    else:
        logger.info(message)

def clean_dataframe(df: pd.DataFrame, df_name: str) -> Tuple[pd.DataFrame, Dict]:
    """Clean DataFrame by removing rows with errors and tracking issues"""
    cleaning_report = {
        'original_rows': len(df),
        'cleaned_rows': 0,
        'removed_rows': 0,
        'errors_found': [],
        'columns_cleaned': []
    }
    
    df_cleaned = df.copy()
    initial_len = len(df_cleaned)
    
    # Remove duplicates
    duplicates_before = df_cleaned.duplicated().sum()
    if duplicates_before > 0:
        df_cleaned = df_cleaned.drop_duplicates()
        cleaning_report['errors_found'].append(f"Removed {duplicates_before} duplicate rows")
        log_error(f"{df_name}: Removed {duplicates_before} duplicate rows", "WARNING")
    
    # Handle missing values
    missing_before = df_cleaned.isnull().sum().sum()
    if missing_before > 0:
        # For numeric columns, fill with median
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_cleaned[col].isnull().any():
                median_val = df_cleaned[col].median()
                df_cleaned[col].fillna(median_val, inplace=True)
                cleaning_report['columns_cleaned'].append(f"{col} (filled with median: {median_val})")
        
        # For categorical columns, fill with mode or 'Unknown'
        cat_cols = df_cleaned.select_dtypes(include=['object']).columns
        for col in cat_cols:
            if df_cleaned[col].isnull().any():
                mode_val = df_cleaned[col].mode()[0] if len(df_cleaned[col].mode()) > 0 else 'Unknown'
                df_cleaned[col].fillna(mode_val, inplace=True)
                cleaning_report['columns_cleaned'].append(f"{col} (filled with: {mode_val})")
        
        cleaning_report['errors_found'].append(f"Fixed {missing_before} missing values")
        log_error(f"{df_name}: Fixed {missing_before} missing values", "WARNING")
    
    # Remove rows with negative quantities (if qty column exists)
    if 'qty' in df_cleaned.columns:
        negative_qty = (df_cleaned['qty'] < 0).sum()
        if negative_qty > 0:
            df_cleaned = df_cleaned[df_cleaned['qty'] >= 0]
            cleaning_report['errors_found'].append(f"Removed {negative_qty} rows with negative quantities")
            log_error(f"{df_name}: Removed {negative_qty} rows with negative quantities", "WARNING")
    
    # Remove rows with negative prices (if price columns exist)
    price_cols = [col for col in df_cleaned.columns if 'price' in col.lower() or 'cost' in col.lower()]
    for col in price_cols:
        if col in df_cleaned.columns:
            negative_prices = (df_cleaned[col] < 0).sum()
            if negative_prices > 0:
                df_cleaned = df_cleaned[df_cleaned[col] >= 0]
                cleaning_report['errors_found'].append(f"Removed {negative_prices} rows with negative {col}")
                log_error(f"{df_name}: Removed {negative_prices} rows with negative {col}", "WARNING")
    
    # Validate date columns
    date_cols = [col for col in df_cleaned.columns if 'date' in col.lower() or 'time' in col.lower()]
    for col in date_cols:
        if col in df_cleaned.columns:
            try:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
                invalid_dates = df_cleaned[col].isnull().sum()
                if invalid_dates > 0:
                    df_cleaned = df_cleaned.dropna(subset=[col])
                    cleaning_report['errors_found'].append(f"Removed {invalid_dates} rows with invalid {col}")
                    log_error(f"{df_name}: Removed {invalid_dates} rows with invalid {col}", "WARNING")
            except Exception as e:
                log_error(f"{df_name}: Could not parse date column {col}: {str(e)}", "ERROR")
    
    cleaning_report['cleaned_rows'] = len(df_cleaned)
    cleaning_report['removed_rows'] = initial_len - len(df_cleaned)
    
    return df_cleaned, cleaning_report

def validate_dataframe(df: pd.DataFrame, required_cols: List[str], df_name: str = "DataFrame") -> Tuple[bool, List[str]]:
    """Validate DataFrame has required columns and return missing columns"""
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        error_msg = f"{df_name} missing required columns: {', '.join(missing_cols)}"
        log_error(error_msg, "ERROR")
        return False, missing_cols
    
    if len(df) == 0:
        error_msg = f"{df_name} is empty after cleaning"
        log_error(error_msg, "ERROR")
        return False, []
    
    log_error(f"{df_name} validation passed: {len(df)} rows, {len(df.columns)} columns", "INFO")
    return True, []

def load_custom_datasets(products_file, stores_file, sales_file, inventory_file, issues_file=None) -> Optional[Tuple]:
    """Load and clean custom datasets from uploaded files with comprehensive validation"""
    try:
        start_time = time.time()
        log_error("Starting custom dataset upload process", "INFO")
        
        # Clear previous error logs
        st.session_state.error_logs = []
        st.session_state.data_quality_report = {}
        
        # Load raw data
        with st.spinner("📂 Loading files..."):
            products = pd.read_csv(products_file)
            stores = pd.read_csv(stores_file)
            sales = pd.read_csv(sales_file)
            inventory = pd.read_csv(inventory_file)
            
            if issues_file:
                issues = pd.read_csv(issues_file)
            else:
                issues = pd.DataFrame({'issue_type': []})
                log_error("No issues file provided, using empty DataFrame", "INFO")
        
        log_error(f"Raw data loaded - Products: {len(products)}, Stores: {len(stores)}, Sales: {len(sales)}, Inventory: {len(inventory)}", "INFO")
        
        # Clean each DataFrame
        with st.spinner("🧹 Cleaning data..."):
            products_clean, products_report = clean_dataframe(products, "Products")
            stores_clean, stores_report = clean_dataframe(stores, "Stores")
            sales_clean, sales_report = clean_dataframe(sales, "Sales")
            inventory_clean, inventory_report = clean_dataframe(inventory, "Inventory")
            issues_clean, issues_report = clean_dataframe(issues, "Issues")
        
        # Store cleaning reports
        st.session_state.data_quality_report = {
            'products': products_report,
            'stores': stores_report,
            'sales': sales_report,
            'inventory': inventory_report,
            'issues': issues_report
        }
        
        # Validate required columns
        required_products = ['product_id', 'category', 'brand', 'unit_cost_aed']
        required_stores = ['store_id', 'city', 'channel']
        required_sales = ['order_id', 'product_id', 'store_id', 'qty', 'selling_price_aed']
        required_inventory = ['product_id', 'store_id', 'stock_on_hand']
        
        validation_errors = []
        
        valid_products, missing_prod = validate_dataframe(products_clean, required_products, "Products")
        if not valid_products:
            validation_errors.append(f"Products: Missing columns {missing_prod}")
        
        valid_stores, missing_stores = validate_dataframe(stores_clean, required_stores, "Stores")
        if not valid_stores:
            validation_errors.append(f"Stores: Missing columns {missing_stores}")
        
        valid_sales, missing_sales = validate_dataframe(sales_clean, required_sales, "Sales")
        if not valid_sales:
            validation_errors.append(f"Sales: Missing columns {missing_sales}")
        
        valid_inventory, missing_inv = validate_dataframe(inventory_clean, required_inventory, "Inventory")
        if not valid_inventory:
            validation_errors.append(f"Inventory: Missing columns {missing_inv}")
        
        if validation_errors:
            st.error("❌ Validation errors in uploaded files:")
            for error in validation_errors:
                st.write(f"• {error}")
            return None
        
        # Final validation - check if data is meaningful
        if len(sales_clean) == 0:
            st.error("❌ Sales data is empty after cleaning")
            log_error("Sales data is empty after cleaning", "ERROR")
            return None
        
        if len(products_clean) == 0:
            st.error("❌ Products data is empty after cleaning")
            log_error("Products data is empty after cleaning", "ERROR")
            return None
        
        elapsed = time.time() - start_time
        success_msg = f"Custom data loaded and cleaned successfully in {elapsed:.2f}s"
        st.success(f"✅ {success_msg}")
        log_error(success_msg, "INFO")
        
        # Summary of cleaning
        total_removed = (products_report['removed_rows'] + stores_report['removed_rows'] + 
                        sales_report['removed_rows'] + inventory_report['removed_rows'])
        
        if total_removed > 0:
            st.warning(f"⚠️ Cleaned data: Removed {total_removed} problematic rows across all datasets")
        
        return (products_clean, stores_clean, sales_clean, inventory_clean, issues_clean)
    
    except pd.errors.ParserError as e:
        error_msg = f"CSV format error: {str(e)}"
        st.error(f"❌ {error_msg}")
        log_error(error_msg, "ERROR")
        st.info("Please ensure all files are valid CSV format")
        return None
    
    except Exception as e:
        error_msg = f"Error loading custom data: {str(e)}"
        st.error(f"❌ {error_msg}")
        log_error(error_msg, "ERROR")
        logger.exception("Custom data loading failed")
        return None

@st.cache_data
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all cleaned datasets with comprehensive error handling"""
    try:
        start_time = time.time()
        log_error("Loading pre-built datasets", "INFO")
        
        data_files = {
            'products': 'products_clean.csv',
            'stores': 'stores_clean.csv',
            'sales': 'sales_clean.csv',
            'inventory': 'inventory_clean.csv',
            'issues': 'issues.csv'
        }
        
        loaded_data = {}
        missing_files = []
        
        for name, filepath in data_files.items():
            try:
                if os.path.exists(filepath):
                    loaded_data[name] = pd.read_csv(filepath)
                    log_error(f"Loaded {name}: {len(loaded_data[name])} rows", "INFO")
                else:
                    missing_files.append(filepath)
            except Exception as e:
                logger.error(f"Error loading {filepath}: {str(e)}")
                missing_files.append(filepath)
        
        if missing_files:
            raise FileNotFoundError(f"Missing files: {', '.join(missing_files)}")
        
        if len(loaded_data['sales']) == 0:
            raise ValueError("Sales data is empty")
        if len(loaded_data['products']) == 0:
            raise ValueError("Products data is empty")
            
        elapsed = time.time() - start_time
        log_error(f"Pre-built data loaded successfully in {elapsed:.2f}s", "INFO")
        
        return (loaded_data['products'], loaded_data['stores'], 
                loaded_data['sales'], loaded_data['inventory'], loaded_data['issues'])
        
    except FileNotFoundError as e:
        st.error(f"❌ Data file error: {e}")
        st.info("📋 Please run:\n```bash\npython data_generator.py\npython cleaner.py\n```")
        st.stop()
    except ValueError as e:
        st.error(f"❌ Data validation error: {e}")
        st.info("Data appears to be corrupted or empty. Please regenerate it.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected error loading data: {str(e)}")
        logger.exception("Data loading failed")
        st.stop()

@st.cache_resource
def initialize_simulator(_products, _stores, _sales, _inventory):
    """Initialize simulator"""
    return PromoSimulator(_products, _stores, _sales, _inventory)

def calculate_advanced_kpis(sales: pd.DataFrame, products: pd.DataFrame, stores: pd.DataFrame, 
                           inventory: pd.DataFrame) -> Dict[str, float]:
    """Calculate comprehensive KPIs with caching"""
    try:
        net_revenue = (sales['selling_price_aed'] * sales['qty']).sum()
        total_cost = (sales['qty'] * products.set_index('product_id').loc[sales['product_id'].values, 'unit_cost_aed']).sum()
        gross_profit = net_revenue - total_cost
        gross_margin_pct = (gross_profit / net_revenue * 100) if net_revenue > 0 else 0
        
        returns = sales[sales['qty'] < 0]['qty'].abs().sum()
        total_qty = sales[sales['qty'] > 0]['qty'].sum()
        return_rate_pct = (returns / total_qty * 100) if total_qty > 0 else 0
        
        if 'channel' in sales.columns:
            channel_revenue = sales.groupby('channel')['selling_price_aed'].sum()
        else:
            channel_revenue = {}
        
        return {
            'net_revenue': net_revenue,
            'gross_profit': gross_profit,
            'gross_margin_pct': gross_margin_pct,
            'return_rate_pct': return_rate_pct,
            'total_transactions': len(sales),
            'avg_transaction_value': net_revenue / len(sales) if len(sales) > 0 else 0,
            'channel_revenue': channel_revenue
        }
    except Exception as e:
        logger.error(f"Error calculating KPIs: {str(e)}")
        return {}

def create_scenario_comparison(sim, city, channel, category, budget, margin_floor, days):
    """Compare multiple scenarios"""
    scenarios = []
    discount_levels = [10, 15, 20, 25, 30, 35]
    
    for disc in discount_levels:
        try:
            _, violations, s_kpis = sim.simulate_promo(
                city, channel, category, disc, budget, margin_floor, days
            )
            scenarios.append({
                'Discount %': disc,
                'Revenue (AED)': s_kpis['simulated_revenue'],
                'Margin %': s_kpis['simulated_margin_pct'],
                'Profit (AED)': s_kpis['profit_proxy'],
                'Budget Use %': s_kpis['budget_utilization_pct'],
                'Stockout Risk %': s_kpis['stockout_risk_pct'],
                'Status': '✅ Valid' if not any([violations['budget_exceeded'], violations['margin_below_floor']]) else '❌ Violated'
            })
        except Exception as e:
            st.warning(f"Scenario {disc}% failed: {str(e)}")
    
    return pd.DataFrame(scenarios) if scenarios else pd.DataFrame()

def create_product_matrix(sales_enriched):
    """BCG-style matrix"""
    product_perf = sales_enriched[sales_enriched['payment_status'] == 'Paid'].copy()
    product_perf['revenue'] = product_perf['qty'] * product_perf['selling_price_aed']
    product_perf['cogs'] = product_perf['qty'] * product_perf['unit_cost_aed']
    product_perf['margin'] = product_perf['revenue'] - product_perf['cogs']
    
    perf = product_perf.groupby('category').agg({
        'revenue': 'sum',
        'margin': 'sum',
        'qty': 'sum'
    }).reset_index()
    
    perf['margin_pct'] = (perf['margin'] / perf['revenue'] * 100).fillna(0)
    
    return perf

def create_revenue_margin_chart(sales_data):
    """Create enhanced Revenue vs Margin Trend chart"""
    sales_data = sales_data.copy()
    sales_data['order_time'] = pd.to_datetime(sales_data['order_time'], errors='coerce')
    
    sales_data = sales_data[
        (sales_data['order_time'].dt.year == 2024) &
        (sales_data['order_time'].dt.month >= 5) &
        (sales_data['order_time'].dt.month <= 9)
    ].copy()
    
    if len(sales_data) == 0:
        st.warning("No data available for May-September 2024")
        return None
    
    sales_data['week_start'] = sales_data['order_time'].dt.to_period('W').apply(lambda r: r.start_time)
    sales_data['week_label'] = sales_data['week_start'].dt.strftime('%b %d')
    
    sales_data['revenue'] = sales_data['qty'] * sales_data['selling_price_aed']
    sales_data['cogs'] = sales_data['qty'] * sales_data['unit_cost_aed']
    sales_data['margin'] = sales_data['revenue'] - sales_data['cogs']
    
    weekly_data = sales_data.groupby('week_start').agg({
        'revenue': 'sum',
        'margin': 'sum',
        'qty': 'sum'
    }).reset_index()
    
    weekly_data['margin_pct'] = (weekly_data['margin'] / weekly_data['revenue'] * 100).fillna(0)
    weekly_data['week_label'] = weekly_data['week_start'].dt.strftime('%b %d, %Y')
    
    avg_revenue = weekly_data['revenue'].mean()
    avg_margin = weekly_data['margin_pct'].mean()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=weekly_data['week_start'],
            y=weekly_data['revenue'],
            name="Revenue (AED)",
            marker=dict(color='#667eea'),
            hovertemplate='<b>Week of %{x|%b %d, %Y}</b><br>Revenue: AED %{y:,.0f}<extra></extra>',
            opacity=0.7
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=weekly_data['week_start'],
            y=weekly_data['margin_pct'],
            name="Margin %",
            mode='lines+markers',
            line=dict(color='#f093fb', width=3),
            marker=dict(size=8, color='#f093fb'),
            hovertemplate='<b>Week of %{x|%b %d, %Y}</b><br>Margin: %{y:.1f}%<extra></extra>',
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="📊 Revenue vs Margin Trend Analysis (May - September 2024)",
        hovermode='x unified',
        height=600,
        showlegend=True
    )
    
    fig.update_yaxes(title_text="<b>Revenue (AED)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Margin (%)</b>", secondary_y=True)
    
    return fig, weekly_data, avg_revenue, avg_margin

def display_error_logs():
    """Display error logs in an expander"""
    if len(st.session_state.error_logs) > 0:
        with st.expander(f"📋 Error Logs ({len(st.session_state.error_logs)} entries)", expanded=False):
            
            # Filter options
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                level_filter = st.multiselect(
                    "Filter by level:",
                    options=['INFO', 'WARNING', 'ERROR'],
                    default=['INFO', 'WARNING', 'ERROR']
                )
            
            with col2:
                search_term = st.text_input("Search logs:", "")
            
            with col3:
                if st.button("🗑️ Clear Logs"):
                    st.session_state.error_logs = []
                    st.rerun()
            
            # Display filtered logs
            filtered_logs = [
                log for log in st.session_state.error_logs 
                if log['level'] in level_filter and (not search_term or search_term.lower() in log['message'].lower())
            ]
            
            if len(filtered_logs) == 0:
                st.info("No logs match the current filters")
            else:
                for log in reversed(filtered_logs):  # Most recent first
                    css_class = "error-log-box" if log['level'] == "ERROR" else \
                                "warning-log-box" if log['level'] == "WARNING" else \
                                "success-log-box"
                    
                    icon = "❌" if log['level'] == "ERROR" else \
                           "⚠️" if log['level'] == "WARNING" else \
                           "ℹ️"
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <strong>{icon} [{log['timestamp']}] {log['level']}</strong><br>
                        {log['message']}
                    </div>
                    """, unsafe_allow_html=True)

def display_data_quality_report():
    """Display data quality report"""
    if st.session_state.data_quality_report:
        with st.expander("📊 Data Quality Report", expanded=True):
            for dataset_name, report in st.session_state.data_quality_report.items():
                st.markdown(f"### {dataset_name.title()}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Original Rows", report['original_rows'])
                with col2:
                    st.metric("Cleaned Rows", report['cleaned_rows'])
                with col3:
                    removed = report['removed_rows']
                    st.metric("Removed Rows", removed, delta=f"-{removed}" if removed > 0 else "0")
                
                if report['errors_found']:
                    st.markdown("**Issues Found & Fixed:**")
                    for error in report['errors_found']:
                        st.write(f"• {error}")
                
                if report['columns_cleaned']:
                    with st.expander(f"🔧 Columns Cleaned ({len(report['columns_cleaned'])})"):
                        for col_info in report['columns_cleaned']:
                            st.write(f"• {col_info}")
                
                st.markdown("---")

def main():
    # Data Source Selection
    st.sidebar.header("📊 Data Source")
    data_source = st.sidebar.radio(
        "Select Data Source:",
        ["📁 Pre-Built Dataset", "📤 Upload Custom Data"],
        index=0
    )
    
    # Load data based on selection
    if data_source == "📁 Pre-Built Dataset":
        try:
            products, stores, sales, inventory, issues = load_data()
            st.sidebar.success("✅ Pre-built data loaded")
        except Exception as e:
            st.sidebar.error(f"Error loading pre-built data: {e}")
            st.stop()
    else:
        # Custom data upload
        st.sidebar.markdown("### Upload Required Files:")
        st.sidebar.info("Upload CSV files for: Products, Stores, Sales, and Inventory")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            products_file = st.file_uploader("📦 Products CSV", type="csv", key="products_upload")
            sales_file = st.file_uploader("🛍️ Sales CSV", type="csv", key="sales_upload")
        
        with col2:
            stores_file = st.file_uploader("🏪 Stores CSV", type="csv", key="stores_upload")
            inventory_file = st.file_uploader("📊 Inventory CSV", type="csv", key="inventory_upload")
        
        issues_file = st.file_uploader("📋 Issues CSV (Optional)", type="csv", key="issues_upload")
        
        # Validate and load uploaded files
        if products_file and stores_file and sales_file and inventory_file:
            result = load_custom_datasets(
                products_file, stores_file, sales_file, inventory_file, issues_file
            )
            
            if result is None:
                st.sidebar.error("❌ Failed to load custom data. Check error messages above.")
                
                # Display error logs immediately after failed upload
                display_error_logs()
                display_data_quality_report()
                
                st.stop()
            else:
                products, stores, sales, inventory, issues = result
                st.sidebar.success("✅ Custom data loaded successfully!")
                
                # Display data quality report
                display_data_quality_report()
        else:
            st.sidebar.warning("⚠️ Please upload all required files (Products, Stores, Sales, Inventory)")
            
            # Show example of expected format
            with st.sidebar.expander("ℹ️ Expected File Formats"):
                st.markdown("""
                **Products CSV must have:**
                - product_id
                - category
                - brand
                - unit_cost_aed
                
                **Stores CSV must have:**
                - store_id
                - city
                - channel
                
                **Sales CSV must have:**
                - order_id
                - product_id
                - store_id
                - qty
                - selling_price_aed
                
                **Inventory CSV must have:**
                - product_id
                - store_id
                - stock_on_hand
                """)
            
            st.stop()
    
    # Show error logs section (always visible after loading data)
    display_error_logs()
    
    # Initialize simulator
    sim = initialize_simulator(products, stores, sales, inventory)
    
    # Professional Executive Header
    st.markdown("""
    <div style="background: #e0f2fe; 
                padding: 2.5rem 2rem; 
                border-radius: 16px; 
                margin-bottom: 2rem;
                border: 1px solid #bae6fd;">
        <h1 style="color: #0c4a6e; font-size: 2.5rem; font-weight: 800; margin: 0;">
            🇦🇪 UAE Promo Pulse Dashboard
        </h1>
        <p style="color: #075985; font-size: 1.125rem; margin: 0.5rem 0 0 0; font-weight: 500;">
            Executive Business Intelligence Platform  •  Real-Time Analytics & Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dataset Overview
    with st.expander("📊 Dataset Overview", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📦 Products", f"{len(products):,}")
        with col2:
            st.metric("🏪 Stores", f"{len(stores):,}")
        with col3:
            st.metric("🛍️ Transactions", f"{len(sales):,}")
        with col4:
            st.metric("📋 Inventory Records", f"{len(inventory):,}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📅 Data Period**")
            if 'order_time' in sales.columns:
                sales['order_time'] = pd.to_datetime(sales['order_time'])
                min_date = sales['order_time'].min().date()
                max_date = sales['order_time'].max().date()
                st.info(f"From **{min_date}** to **{max_date}**")
            else:
                st.info("Date information not available")
        
        with col2:
            st.markdown("**📂 Data Source**")
            source_label = "Pre-built Dataset" if data_source == "📁 Pre-Built Dataset" else "Custom Uploaded Dataset"
            st.info(f"**{source_label}**")
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("---")
        st.header("🎛️ Control Panel")
        
        # Quick Presets
        st.subheader("⚡ Quick Presets")
        preset = st.selectbox(
            "Apply Preset Filter",
            ["Custom", "Dubai Electronics", "All Marketplaces", "Fashion App"]
        )
        
        if preset == "Custom":
            sales['order_time'] = pd.to_datetime(sales['order_time'])
            min_date = sales['order_time'].min().date()
            max_date = sales['order_time'].max().date()
            
            st.subheader("📅 Time Period")
            date_range = st.date_input(
                "Select Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            st.subheader("🗺️ Geography & Channel")
            city_filter = st.selectbox("City", ['All'] + sorted(stores['city'].unique().tolist()))
            channel_filter = st.selectbox("Channel", ['All'] + sorted(stores['channel'].unique().tolist()))
            
            st.subheader("🏷️ Product Filters")
            category_filter = st.selectbox("Category", ['All'] + sorted(products['category'].unique().tolist()))
            brand_filter = st.selectbox("Brand", ['All'] + sorted(products['brand'].unique().tolist()))
        else:
            if preset == "Dubai Electronics":
                city_filter, category_filter, channel_filter = "Dubai", "Electronics", "All"
            elif preset == "All Marketplaces":
                city_filter, category_filter, channel_filter = "All", "All", "Marketplace"
            elif preset == "Fashion App":
                city_filter, category_filter, channel_filter = "All", "Fashion", "App"
            else:
                city_filter, category_filter, channel_filter = "All", "All", "All"
            
            date_range = None
            brand_filter = "All"
        
        st.markdown("---")
        st.header("🎯 Simulation Lab")
        
        with st.expander("📊 Scenario Settings", expanded=True):
            sim_city = st.selectbox("Target City", ['All'] + sorted(stores['city'].unique().tolist()), key='sim_city')
            sim_channel = st.selectbox("Target Channel", ['All'] + sorted(stores['channel'].unique().tolist()), key='sim_channel')
            sim_category = st.selectbox("Target Category", ['All'] + sorted(products['category'].unique().tolist()), key='sim_category')
            
            discount_pct = st.slider("💰 Discount %", 0, 50, 20, 5)
            promo_budget = st.number_input("💵 Budget (AED)", 10000, 200000, 50000, 5000)
            margin_floor = st.slider("📉 Margin Floor %", 0, 30, 10, 5)
            sim_days = st.selectbox("⏱️ Duration (days)", [7, 14], index=1)
        
        run_sim = st.button("🚀 Launch Simulation", type="primary", use_container_width=True)
        
        if run_sim:
            with st.spinner("🔄 Running simulation..."):
                try:
                    if discount_pct < 0 or discount_pct > 100:
                        st.error("❌ Discount must be between 0-100%")
                    elif promo_budget <= 0:
                        st.error("❌ Budget must be positive")
                    else:
                        start_time = time.time()
                        simulated, violations, sim_kpis = sim.simulate_promo(
                            sim_city, sim_channel, sim_category,
                            discount_pct, promo_budget, margin_floor, sim_days
                        )
                        elapsed = time.time() - start_time
                        
                        if simulated is None or len(simulated) == 0:
                            raise ValueError("Simulation returned no results")
                        
                        st.session_state['sim_results'] = (simulated, violations, sim_kpis)
                        st.success(f"✅ Simulation Complete! ({elapsed:.2f}s)")
                        log_error(f"Simulation completed successfully in {elapsed:.2f}s", "INFO")
                        
                        if violations:
                            violation_messages = []
                            if violations.get('budget_exceeded'):
                                violation_messages.append("⚠️ Budget exceeded")
                            if violations.get('margin_below_floor'):
                                violation_messages.append("⚠️ Margin below floor")
                            if violations.get('stockouts_exist'):
                                violation_messages.append("⚠️ Stockout risk detected")
                            
                            if violation_messages:
                                st.warning("Constraint Violations: " + ", ".join(violation_messages))
                
                except ValueError as e:
                    st.error(f"❌ Validation error: {str(e)}")
                    log_error(f"Simulation validation error: {str(e)}", "ERROR")
                except Exception as e:
                    st.error(f"❌ Simulation error: {str(e)}")
                    st.info("💡 Tips: Try adjusting discount %, budget, or other parameters")
                    log_error(f"Simulation execution failed: {str(e)}", "ERROR")
    
    # Apply filters
    try:
        filtered_sales = sales.copy()
        
        if preset == "Custom" and date_range and len(date_range) == 2:
            filtered_sales = filtered_sales[
                (filtered_sales['order_time'].dt.date >= date_range[0]) &
                (filtered_sales['order_time'].dt.date <= date_range[1])
            ]
        
        filtered_sales = filtered_sales.merge(
            products[['product_id', 'category', 'brand', 'unit_cost_aed']], 
            on='product_id',
            how='left'
        )
        filtered_sales = filtered_sales.merge(
            stores[['store_id', 'city', 'channel', 'fulfillment_type']], 
            on='store_id',
            how='left'
        )

        if city_filter != 'All':
            filtered_sales = filtered_sales[filtered_sales['city'] == city_filter]
        if channel_filter != 'All':
            filtered_sales = filtered_sales[filtered_sales['channel'] == channel_filter]
        if category_filter != 'All':
            filtered_sales = filtered_sales[filtered_sales['category'] == category_filter]
        if preset == "Custom" and brand_filter != 'All':
            filtered_sales = filtered_sales[filtered_sales['brand'] == brand_filter]
    
    except Exception as e:
        st.error(f"❌ Error during data preparation: {str(e)}")
        log_error(f"Data preparation error: {str(e)}", "ERROR")
    
    # Calculate KPIs
    try:
        kpis = sim.compute_kpis(filtered_sales)
        if not kpis or len(kpis) == 0:
            raise ValueError("KPI calculation returned empty results")
    except Exception as e:
        log_error(f"Error calculating KPIs: {str(e)}", "ERROR")
        kpis = {
            'net_revenue': 0,
            'gross_profit': 0,
            'gross_margin_pct': 0,
            'return_rate_pct': 0,
            'total_transactions': 0,
            'avg_transaction_value': 0
        }
    
    # View Toggle
    st.markdown("---")
    view_mode = st.radio(
        "**Select Dashboard View:**",
        ["💼 Executive Suite", "⚙️ Operations Command Center"],
        horizontal=True
    )
    st.markdown("---")
    
    # EXECUTIVE VIEW
    if "Executive" in view_mode:
        st.markdown("## 💼 Executive Suite")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>NET REVENUE</h3>
                <h1>AED {kpis['net_revenue']:,.0f}</h1>
                <p>Gross: AED {kpis['gross_revenue']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>GROSS MARGIN</h3>
                <h1>{kpis['gross_margin_pct']:.1f}%</h1>
                <p>Amount: AED {kpis['gross_margin_aed']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if 'sim_results' in st.session_state:
                _, _, sim_kpis = st.session_state['sim_results']
                st.markdown(f"""
                <div class="metric-card">
                    <h3>PROFIT PROXY (SIM)</h3>
                    <h1>AED {sim_kpis['profit_proxy']:,.0f}</h1>
                    <p>Margin: {sim_kpis['simulated_margin_pct']:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Run simulation")
        
        with col4:
            if 'sim_results' in st.session_state:
                _, _, sim_kpis = st.session_state['sim_results']
                color = "green" if sim_kpis['budget_utilization_pct'] <= 100 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>BUDGET USAGE</h3>
                    <h1 style="color:{color};">{sim_kpis['budget_utilization_pct']:.1f}%</h1>
                    <p>{sim_kpis['promo_spend']:,.0f} AED spent</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Run simulation")
        
        st.divider()
        
        # Revenue vs Margin Chart
        st.markdown("### 📈 Revenue vs Margin Trend")
        chart_result = create_revenue_margin_chart(filtered_sales)
        
        if chart_result:
            fig, weekly_data, avg_revenue, avg_margin = chart_result
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📈 Avg Revenue", f"AED {avg_revenue:,.0f}")
            with col2:
                st.metric("💰 Avg Margin", f"{avg_margin:.1f}%")
            with col3:
                st.metric("📊 Weeks Tracked", len(weekly_data))
            with col4:
                total_revenue = weekly_data['revenue'].sum()
                st.metric("💵 Total Revenue", f"AED {total_revenue:,.0f}")
        
        st.divider()
        
        # BCG Matrix
        st.markdown("### 🎯 Product Performance Matrix (BCG)")
        perf_matrix = create_product_matrix(filtered_sales)
        
        fig = px.scatter(
            perf_matrix, x='revenue', y='margin_pct', size='qty', color='category',
            title='Product Performance Matrix', size_max=60
        )
        
        avg_revenue_bcg = perf_matrix['revenue'].median()
        avg_margin_bcg = perf_matrix['margin_pct'].median()
        
        fig.add_hline(y=avg_margin_bcg, line_dash="dash", line_color="gray")
        fig.add_vline(x=avg_revenue_bcg, line_dash="dash", line_color="gray")
        fig.update_layout(height=600)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Scenario Comparison
        if 'sim_results' in st.session_state:
            st.divider()
            st.markdown("### 🎯 Scenario Comparison")
            
            scenario_df = create_scenario_comparison(
                sim, sim_city, sim_channel, sim_category,
                promo_budget, margin_floor, sim_days
            )
            
            if not scenario_df.empty:
                st.dataframe(
                    scenario_df.style.highlight_max(subset=['Profit (AED)'], color='lightgreen')
                                    .format({
                                        'Revenue (AED)': '{:,.0f}',
                                        'Margin %': '{:.1f}',
                                        'Profit (AED)': '{:,.0f}',
                                        'Budget Use %': '{:.1f}',
                                        'Stockout Risk %': '{:.1f}'
                                    }),
                    use_container_width=True,
                    hide_index=True
                )
    
    # OPERATIONS VIEW
    else:
        st.markdown("## ⚙️ Operations Command Center")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'sim_results' in st.session_state:
                _, _, sim_kpis = st.session_state['sim_results']
                risk_color = "red" if sim_kpis['stockout_risk_pct'] > 20 else "orange" if sim_kpis['stockout_risk_pct'] > 10 else "green"
                st.markdown(f"""
                <div class="metric-card">
                    <h3>STOCKOUT RISK</h3>
                    <h1 style="color:{risk_color};">{sim_kpis['stockout_risk_pct']:.1f}%</h1>
                    <p>{sim_kpis['high_risk_skus']} SKUs at risk</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Run simulation")
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>RETURN RATE</h3>
                <h1>{kpis['return_rate_pct']:.1f}%</h1>
                <p>Target: < 5%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>PAYMENT FAILURES</h3>
                <h1>{kpis['payment_failure_rate_pct']:.1f}%</h1>
                <p>Target: < 10%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>DATA QUALITY</h3>
                <h1>{len(issues)}</h1>
                <p>Issues Resolved</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📦 Inventory Distribution")
        
        latest_inv = inventory.sort_values('snapshot_date').groupby('product_id').last().reset_index()
        fig = px.histogram(
            latest_inv, x='stock_on_hand', nbins=40,
            title='Inventory Distribution', marginal='box'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    # Download Section
    st.markdown("---")
    st.subheader("💾 Download & Export")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            "📊 Sales Data", 
            sales.to_csv(index=False).encode('utf-8'),
            f"sales_{datetime.now().strftime('%Y%m%d')}.csv", 
            "text/csv", 
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            "📋 Issues Log", 
            issues.to_csv(index=False).encode('utf-8'),
            f"issues_{datetime.now().strftime('%Y%m%d')}.csv", 
            "text/csv", 
            use_container_width=True
        )
    
    with col3:
        if 'sim_results' in st.session_state:
            simulated, _, _ = st.session_state['sim_results']
            st.download_button(
                "🎯 Simulation", 
                simulated.to_csv(index=False).encode('utf-8'),
                f"simulation_{datetime.now().strftime('%Y%m%d')}.csv", 
                "text/csv", 
                use_container_width=True
            )
    
    with col4:
        # Export error logs
        if st.session_state.error_logs:
            logs_df = pd.DataFrame(st.session_state.error_logs)
            st.download_button(
                "📝 Error Logs",
                logs_df.to_csv(index=False).encode('utf-8'),
                f"error_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
