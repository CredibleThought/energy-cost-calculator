import streamlit as st
import pandas as pd
import plotly.express as px
from decimal import Decimal
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="Energy Usage Calculator", layout="wide")

st.title("Energy Usage Calculator")

# Initialize session state for devices and rates
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'rate_peak' not in st.session_state:
    st.session_state.rate_peak = 0.292
if 'rate_low' not in st.session_state:
    st.session_state.rate_low = 0.07

# Sidebar - Buy Me a Coffee
# Sidebar - Buy Me a Coffee
with st.sidebar:
    components.html(
        """<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="stevefernandes" data-color="#FFDD00" data-emoji="☕"  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>""",
        height=70
    )

# Sidebar - Data Management
st.sidebar.header("Data Management")

# Save
if st.session_state.devices:
    # Embed rates into the CSV
    save_df = pd.DataFrame(st.session_state.devices)
    save_df['Rate Peak'] = st.session_state.get('rate_peak', 0.30) # Access state safely or use widget var if defined? 
    # Actually, widget vars are defined later now. So stick to session state or define defaults.
    # To be safe: use st.session_state.get() since we haven't rendered widgets yet.
    # Or cleaner: Just define defaults for fallback.
    save_df['Rate Low'] = st.session_state.get('rate_low', 0.10)
    
    csv_data = save_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Save List to CSV",
        data=csv_data,
        file_name="devices.csv",
        mime="text/csv"
    )

# Load
uploaded_file = st.sidebar.file_uploader("Load Devices CSV", type="csv")
if uploaded_file is not None:
    if st.sidebar.button("Load List from CSV"):
        try:
            loaded_df = pd.read_csv(uploaded_file)
            
            # Extract rates if present
            if 'Rate Peak' in loaded_df.columns and 'Rate Low' in loaded_df.columns:
                # Update session state for rates BEFORE widgets are created
                st.session_state.rate_peak = float(loaded_df.iloc[0]['Rate Peak'])
                st.session_state.rate_low = float(loaded_df.iloc[0]['Rate Low'])
                
                # Drop the columns so they don't pollute the device list
                loaded_df = loaded_df.drop(columns=['Rate Peak', 'Rate Low'])
            
            st.session_state.devices = loaded_df.to_dict('records')
            st.sidebar.success("Loaded devices and rates successfully!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")

st.sidebar.markdown("---")

# Sidebar for global settings (Rates)
st.sidebar.header("Electricity Rates (£/kWh)")
# Use keys to allow updating from load logic. Defaults set in session_state above.
cost_peak = st.sidebar.number_input("Peak Cost", min_value=0.0, format="%.4f", step=0.01, key="rate_peak")
cost_low = st.sidebar.number_input("Off-Peak Cost", min_value=0.0, format="%.4f", step=0.01, key="rate_low")


# Main Interface
st.header("Add New Device")

# Custom CSS for the form
st.markdown("""
<style>
    [data-testid="stForm"] {
        background-color: #cccccc;
        border: 1px solid #888;
        padding: 20px;
        border-radius: 10px;
    }
    [data-testid="stForm"] [data-testid="stWidgetLabel"] p,
    [data-testid="stForm"] [data-testid="stMarkdown"] p,
    [data-testid="stForm"] [data-testid="stMarkdown"] h1,
    [data-testid="stForm"] [data-testid="stMarkdown"] h2,
    [data-testid="stForm"] [data-testid="stMarkdown"] h3 {
        font-weight: bold;
        color: #000; /* Force black in light mode for max contrast */
    }
    /* Dark mode support check */
    @media (prefers-color-scheme: dark) {
        [data-testid="stForm"] {
            background-color: #666666; 
            border: 1px solid #aaa;
        }
        [data-testid="stForm"] [data-testid="stWidgetLabel"] p,
        [data-testid="stForm"] [data-testid="stMarkdown"] p,
        [data-testid="stForm"] [data-testid="stMarkdown"] h1,
        [data-testid="stForm"] [data-testid="stMarkdown"] h2,
        [data-testid="stForm"] [data-testid="stMarkdown"] h3 {
            color: #ffffff; /* Force white in dark mode for max contrast */
        }
    }
    
    /* Make table headers bold - Aggressive targeting */
    [data-testid="stDataFrame"] th,
    [data-testid="stDataEditor"] th,
    [data-testid="stDataFrame"] [role="columnheader"],
    [data-testid="stDataEditor"] [role="columnheader"],
    [data-testid="stDataFrame"] div[class*="header"],
    [data-testid="stDataEditor"] div[class*="header"] {
        font-weight: 900 !important;
        font-family: sans-serif !important;
        color: black !important; /* ensure visibility in light mode */
    }
    
    /* Dark mode override for headers */
    @media (prefers-color-scheme: dark) {
        [data-testid="stDataFrame"] th,
        [data-testid="stDataEditor"] th,
        [data-testid="stDataFrame"] [role="columnheader"],
        [data-testid="stDataEditor"] [role="columnheader"] {
             color: white !important;
        }
    }
</style>
""", unsafe_allow_html=True)

with st.form("new_device"):
    name = st.text_input("Device Name")
    
    st.subheader("Usage Profile (Load)")
    c1, c2 = st.columns(2)
    power_heavy = c1.number_input("Heavy Load (W)", min_value=0.0, value=100.0, step=1.0, format="%.2f")
    power_light = c2.number_input("Regular Load (W)", min_value=0.0, value=10.0, step=1.0, format="%.2f")
    
    st.subheader("Time Allocation in each state")
    c3, c4 = st.columns(2)
    alloc_heavy = c3.number_input("Heavy Load %", min_value=0.0, max_value=100.0, value=100.0, step=1.0)
    alloc_light = c4.number_input("Regular Load %", min_value=0.0, max_value=100.0, value=100.0 - alloc_heavy, step=1.0)
    
    st.subheader("Time Profile (Per Day at each Rate)")
    t1, t2 = st.columns(2)
    # Total hours can be up to 24.
    hours_peak = t1.number_input("Hours @ Peak Rate", min_value=0.0, max_value=24.0, value=0.0, step=0.1, format="%.2f")
    hours_low = t2.number_input("Hours @ Off-Peak Rate", min_value=0.0, max_value=24.0, value=0.0, step=0.1, format="%.2f")

    submitted = st.form_submit_button("Add Device")
    if submitted:
        if not name:
            st.error("Please enter a device name.")
        elif abs((alloc_heavy + alloc_light) - 100.0) > 0.01:
            st.error(f"Load allocations must sum to 100%. Current sum: {alloc_heavy + alloc_light}%")
        elif (hours_peak + hours_low) > 24.0:
             st.error(f"Total hours cannot exceed 24. Current total: {hours_peak + hours_low}")
        else:
            st.session_state.devices.append({
                "Name": name,
                "Power Heavy": power_heavy,
                "Power Light": power_light,
                "Alloc Heavy": alloc_heavy,
                "Alloc Light": alloc_light,
                "Hours Peak": hours_peak,
                "Hours Low": hours_low
            })
            st.success(f"Added {name}")

# Display and Edit Devices
if st.session_state.devices:
    st.subheader("Device List & Costs")
    
    df = pd.DataFrame(st.session_state.devices)
    
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Device Name"),
            "Power Heavy": st.column_config.NumberColumn("Heavy Load (W)", min_value=0.0, format="%.2f"),
            "Power Light": st.column_config.NumberColumn("Regular Load (W)", min_value=0.0, format="%.2f"),
            "Alloc Heavy": st.column_config.NumberColumn("Heavy Load %", min_value=0.0, max_value=100.0, format="%.2f"),
            "Alloc Light": st.column_config.NumberColumn("Regular Load %", min_value=0.0, max_value=100.0, format="%.2f"),
            "Hours Peak": st.column_config.NumberColumn("Hours @ Peak Rate", min_value=0.0, max_value=24.0, step=0.1, format="%.2f"),
            "Hours Low": st.column_config.NumberColumn("Hours @ Off-Peak Rate", min_value=0.0, max_value=24.0, step=0.1, format="%.2f"),
        },
        key="device_editor"
    )
    
    current_devices = edited_df.to_dict('records')
    if current_devices != st.session_state.devices:
        st.session_state.devices = current_devices
        st.rerun()

    # Validation: Ensure allocations sum to 100%
    if not edited_df.empty:
        has_errors = False
        for index, row in edited_df.iterrows():
            try:
                a_heavy = float(row.get('Alloc Heavy', 0))
                a_light = float(row.get('Alloc Light', 0))
                if abs((a_heavy + a_light) - 100.0) > 0.1:
                    st.error(f"Device '{row.get('Name', 'Unknown')}': Heavy ({a_heavy}%) + Regular ({a_light}%) must sum to 100%.")
                    has_errors = True
            except Exception:
                pass # Conversion issues handled in calc
        
        if has_errors:
            st.stop()

    # Calculate Costs
    if not edited_df.empty:
        results = []
        for index, row in edited_df.iterrows():
            try:
                # Load Profile
                p_heavy = Decimal(str(row['Power Heavy']))
                p_light = Decimal(str(row['Power Light']))
                a_heavy = Decimal(str(row['Alloc Heavy'])) / Decimal("100")
                a_light = Decimal(str(row['Alloc Light'])) / Decimal("100")
                
                # Calculate Average Power in kW
                # Avg Watts = (Heavy * %) + (Light * %)
                avg_watts = (p_heavy * a_heavy) + (p_light * a_light)
                avg_kw = avg_watts / Decimal("1000")
                
                # Time Profile
                h_peak = Decimal(str(row['Hours Peak']))
                h_low = Decimal(str(row['Hours Low']))
                
                # Rates (£)
                r_peak = Decimal(str(cost_peak))
                r_low = Decimal(str(cost_low))
                
                # Cost Calculation
                daily_kwh = (h_peak * avg_kw) + (h_low * avg_kw)
                
                cost_peak_period = h_peak * avg_kw * r_peak
                cost_low_period = h_low * avg_kw * r_low
                
                daily_cost = cost_peak_period + cost_low_period
                monthly_cost = daily_cost * Decimal("30.4167")
                annual_cost = daily_cost * Decimal("365")
                
                results.append({
                    "Daily Cost": daily_cost,
                    "Monthly Cost": monthly_cost,
                    "Annual Cost": annual_cost,
                    "Daily kWh": daily_kwh
                })
            except Exception as e:
                # st.error(f"Error calculating row {index}: {e}") # Suppress individual row errors to avoid clutter
                results.append({"Daily Cost": Decimal(0), "Monthly Cost": Decimal(0), "Annual Cost": Decimal(0), "Daily kWh": Decimal(0)})

        cost_df = pd.DataFrame(results)
        
        display_df = pd.concat([edited_df, cost_df], axis=1)
        
        # 1-based indexing: Reset first to ensure clean sequence
        display_df.reset_index(drop=True, inplace=True)
        display_df.index = display_df.index + 1
        


        format_mapping = {
            "Daily Cost": "£{:.2f}", 
            "Monthly Cost": "£{:.2f}", 
            "Annual Cost": "£{:.2f}",
            "Power Heavy": "{:.2f}",
            "Power Light": "{:.2f}",
            "Hours Peak": "{:.2f}",
            "Hours Low": "{:.2f}",
            "Alloc Heavy": "{:.2f}",
            "Alloc Light": "{:.2f}"
        }
        
        st.subheader("Cost Breakdown")
        st.dataframe(
            display_df.style.format(format_mapping),
            use_container_width=True
        )

        # Total Metrics
        total_daily = cost_df["Daily Cost"].sum()
        total_monthly = cost_df["Monthly Cost"].sum()
        total_annual = cost_df["Annual Cost"].sum()
        
        total_daily_kwh = cost_df["Daily kWh"].sum()
        total_monthly_kwh = total_daily_kwh * Decimal("30.4167")
        total_annual_kwh = total_daily_kwh * Decimal("365")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Daily Cost", f"£{total_daily:,.2f} ({total_daily_kwh:,.2f} kWh)")
        m2.metric("Total Monthly Cost", f"£{total_monthly:,.2f} ({total_monthly_kwh:,.2f} kWh)")
        m3.metric("Total Annual Cost", f"£{total_annual:,.2f} ({total_annual_kwh:,.2f} kWh)")
        
        with st.expander("Calculation Details (First Device)"):
            if not edited_df.empty:
                r = edited_df.iloc[0]
                
                # Extract
                p_heavy = Decimal(str(r['Power Heavy']))
                p_light = Decimal(str(r['Power Light']))
                a_heavy = Decimal(str(r['Alloc Heavy']))
                a_light = Decimal(str(r['Alloc Light']))
                h_peak = Decimal(str(r['Hours Peak']))
                h_low = Decimal(str(r['Hours Low']))
                
                # Rates
                r_peak = Decimal(str(cost_peak))
                r_low = Decimal(str(cost_low))
                
                # Avg Power
                avg_watts = (p_heavy * (a_heavy/100)) + (p_light * (a_light/100))
                avg_kw = avg_watts / Decimal("1000")
                
                st.write(f"**Device**: {r['Name']}")
                st.markdown("#### 1. Average Power (Load Profile)")
                st.write(f"- Heavy Load: {p_heavy}W ({a_heavy}%)")
                st.write(f"- Regular Load: {p_light}W ({a_light}%)")
                st.write(f"- **Average Power**: {avg_watts:.2f} W -> **{avg_kw:.4f} kW**")
                
                st.markdown("#### 2. Cost (Time Profile)")
                st.write(f"**Rates (£/kWh)**: Peak £{r_peak:.4f}, Off-Peak £{r_low:.4f}")
                st.write(f"- **Peak Period**: {h_peak} hrs * {avg_kw:.4f} kW * £{r_peak:.4f} = £{(h_peak * avg_kw * r_peak):.4f}")
                st.write(f"- **Off-Peak Period**: {h_low} hrs * {avg_kw:.4f} kW * £{r_low:.4f} = £{(h_low * avg_kw * r_low):.4f}")
                
                st.markdown("#### Total")
                st.write(f"- **Daily Cost**: £{(h_peak * avg_kw * r_peak) + (h_low * avg_kw * r_low):.4f}")
        
        # Chart
        st.markdown("---")
        st.subheader("Annual Cost Distribution")
        
        # Prepare data for Pie Chart
        # We need Device Name and Annual Cost
        pie_data = []
        for index, row in edited_df.iterrows():
            device_name = row.get('Name', f"Device {index+1}")
            try:
                # Retrieve the Annual Cost calculated earlier
                annual_cost = results[index]['Annual Cost']
            except IndexError:
                annual_cost = Decimal(0)
            
            pie_data.append({
                "Device": device_name,
                "Annual Cost (£)": float(annual_cost)
            })
            
        chart_df = pd.DataFrame(pie_data)
        
        if not chart_df.empty:
            fig = px.pie(chart_df, values="Annual Cost (£)", names="Device", 
                         title="Share of Total Annual Cost")
            st.plotly_chart(fig, use_container_width=True)


if not st.session_state.devices:
    st.info("No devices added yet.")
