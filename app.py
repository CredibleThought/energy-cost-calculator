import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.express as px
from decimal import Decimal, getcontext
import streamlit.components.v1 as components

# Set page config
st.set_page_config(page_title="Energy Usage Calculator", layout="wide")

st.title("Energy Usage Calculator")

# Default Device Profiles
DEVICE_DEFAULTS = {
    "Other": {
        "Power Heavy": 100.0, "Power Light": 10.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 0.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (LED) 32 inch": {
        "Power Heavy": 45.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (LED) 55 inch": {
        "Power Heavy": 80.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (LED) 65 inch": {
        "Power Heavy": 110.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (LED) 75 inch": {
        "Power Heavy": 145.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (OLED) 32 inch": {
        "Power Heavy": 55.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (OLED) 55 inch": {
        "Power Heavy": 100.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (OLED) 65 inch": {
        "Power Heavy": 160.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (OLED) 75 inch": {
        "Power Heavy": 220.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (Micro LED) 32 inch": {
        "Power Heavy": 50.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (Micro LED) 55 inch": {
        "Power Heavy": 90.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (Micro LED) 65 inch": {
        "Power Heavy": 140.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Television (Micro LED) 75 inch": {
        "Power Heavy": 190.0, "Power Light": 1.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 3.0, "Hours Low": 1.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Computer (Gaming)": {
        "Power Heavy": 400.0, "Power Light": 50.0,
        "Alloc Heavy": 80.0, "Alloc Light": 20.0,
        "Hours Peak": 8.0, "Hours Low": 1.0,
        "Days": 5.0, "Weeks": 52.0
    },
    "Computer (Mac Mini M4)": {
        "Power Heavy": 30.0, "Power Light": 5.0,
        "Alloc Heavy": 10.0, "Alloc Light": 90.0,
        "Hours Peak": 8.0, "Hours Low": 1.0,
        "Days": 5.0, "Weeks": 52.0
    },
    "Computer (Desktop)": {
        "Power Heavy": 200.0, "Power Light": 50.0,
        "Alloc Heavy": 10.0, "Alloc Light": 90.0,
        "Hours Peak": 8.0, "Hours Low": 1.0,
        "Days": 5.0, "Weeks": 52.0
    },
    "Light (Incandescent)": {
        "Power Heavy": 60.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 5.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Light (Halogen)": {
        "Power Heavy": 45.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 5.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Light (LED Spotlight)": {
        "Power Heavy": 5.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 5.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Light (LED Bulb)": {
        "Power Heavy": 9.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 5.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Light (LED ceiling light)": {
        "Power Heavy": 18.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 5.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Electric Radiator": {
        "Power Heavy": 1500.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 4.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 26.0
    },
    "Fan Heater": {
        "Power Heavy": 2000.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 2.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 20.0
    },
    "Air Conditioner (Heating)": {
        "Power Heavy": 1200.0, "Power Light": 10.0,
        "Alloc Heavy": 80.0, "Alloc Light": 20.0,
        "Hours Peak": 4.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 20.0
    },
    "Air Conditioner (Cooling)": {
        "Power Heavy": 1200.0, "Power Light": 10.0,
        "Alloc Heavy": 80.0, "Alloc Light": 20.0,
        "Hours Peak": 4.0, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 12.0
    },
    "Sky Q box": {
        "Power Heavy": 21.0, "Power Light": 17.0,
        "Alloc Heavy": 40.0, "Alloc Light": 60.0,
        "Hours Peak": 5.0, "Hours Low": 19.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Sky Q mini": {
        "Power Heavy": 11.0, "Power Light": 4.0,
        "Alloc Heavy": 40.0, "Alloc Light": 60.0,
        "Hours Peak": 5.0, "Hours Low": 19.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Sky Stream Puck": {
        "Power Heavy": 4.0, "Power Light": 0.5,
        "Alloc Heavy": 40.0, "Alloc Light": 60.0,
        "Hours Peak": 5.0, "Hours Low": 19.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Virgin Media 360 Box": {
        "Power Heavy": 12.0, "Power Light": 1.6,
        "Alloc Heavy": 40.0, "Alloc Light": 60.0,
        "Hours Peak": 5.0, "Hours Low": 19.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Apple TV": {
        "Power Heavy": 5.0, "Power Light": 0.5,
        "Alloc Heavy": 40.0, "Alloc Light": 60.0,
        "Hours Peak": 4.0, "Hours Low": 20.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Induction Hob": {
        "Power Heavy": 2000.0, "Power Light": 0.0,
        "Alloc Heavy": 100.0, "Alloc Light": 0.0,
        "Hours Peak": 0.5, "Hours Low": 0.0,
        "Days": 7.0, "Weeks": 52.0
    },
    "Electric Oven (Fan)": {
        "Power Heavy": 2500.0, "Power Light": 0.0,
        "Alloc Heavy": 30.0, "Alloc Light": 70.0,
        "Hours Peak": 0.7, "Hours Low": 0.0,
        "Days": 5.0, "Weeks": 52.0
    },
    "Electric Oven (Conventional)": {
        "Power Heavy": 2500.0, "Power Light": 0.0,
        "Alloc Heavy": 45.0, "Alloc Light": 55.0,
        "Hours Peak": 0.8, "Hours Low": 0,
        "Days": 5.0, "Weeks": 52.0
    },
    "Washing Machine": {
        "Power Heavy": 2000.0, "Power Light": 200.0,
        "Alloc Heavy": 20.0, "Alloc Light": 80.0,
        "Hours Peak": 0.5, "Hours Low": 0.5,
        "Days": 3.0, "Weeks": 52.0
    },
    "Tumble Dryer": {
        "Power Heavy": 2500.0, "Power Light": 200.0,
        "Alloc Heavy": 90.0, "Alloc Light": 10.0,
        "Hours Peak": 1.0, "Hours Low": 0.0,
        "Days": 3.0, "Weeks": 40.0
    },
    "Dishwasher": {
        "Power Heavy": 1800.0, "Power Light": 100.0,
        "Alloc Heavy": 30.0, "Alloc Light": 70.0,
        "Hours Peak": 0.0, "Hours Low": 1.5,
        "Days": 5.0, "Weeks": 52.0
    }
}

# Initialize session state for devices and rates
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'rate_peak' not in st.session_state:
    st.session_state.rate_peak = 0.2361
if 'rate_low' not in st.session_state:
    st.session_state.rate_low = 0.07

# Sidebar - Buy Me a Coffee
# Sidebar - Buy Me a Coffee
with st.sidebar:
    components.html(
        """
        <div style="transform: scale(0.9); transform-origin: top left;">
            <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="stevefernandes" data-color="#FFDD00" data-emoji="☕"  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
        </div>
        """,
        height=60
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
# Custom CSS for the form
st.markdown("""
<style>
    /* 1. Target ONLY the inner vertical block using direct child combinator */
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) {
        background-color: #cccccc !important;
        border: 1px solid #888 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-top: 5px !important; /* Small gap from header */
    }
    
    /* Make the inner content wrapper transparent so the grey shows through */
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) > div {
        background-color: transparent !important;
    }

    /* Ensure label colors are correct in the box */
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stWidgetLabel"] p,
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] p,
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h1,
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h2,
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h3 {
        font-weight: bold;
        color: #000 !important;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) {
            background-color: #666666 !important; 
            border: 1px solid #aaa !important;
        }
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) > div {
            background-color: transparent !important;
        }
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stWidgetLabel"] p,
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] p,
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h1,
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h2,
        div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) [data-testid="stMarkdown"] h3 {
            color: #ffffff !important;
        }
    }
    
    /* REMOVE SPACING BETWEEN HEADER AND BOX - Adjusted for cleaner look */
    /* Remove bottom padding from header but keep margin */
    div:has(> h2#add-new-device) {
        padding-bottom: 0 !important;
    }
    h2#add-new-device {
        padding-bottom: 0 !important;
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
    
    /* Plotly Legend Scrollbar Fix */
    g.scrollbar rect.scrollbar-glyph {
        fill: #888 !important;
        fill-opacity: 0.8 !important;
    }
    g.scrollbar rect.scrollbar-channel {
        fill: #eee !important;
        fill-opacity: 0.1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for the button - Injected specifically to override Streamlit defaults
st.markdown("""
<style>
    /* Target the submit button within the container */
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) .stButton button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }
    
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) .stButton button:hover {
        background-color: #0056b3 !important;
        color: white !important;
    }

    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) .stButton button:active {
           background-color: #004494 !important;
           color: white !important;
    }
    
    /* Ensure text color is white in both light and dark modes for this button */
    div[data-testid="stVerticalBlock"]:has(> [data-testid="stElementContainer"] .device-box-fix) .stButton button p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper to look up device defaults
def get_device_default(device_type):
    return DEVICE_DEFAULTS.get(device_type, DEVICE_DEFAULTS["Other"])

# Callback for dropdown
def on_device_type_change():
    selected = st.session_state.device_type_selector
    data = get_device_default(selected)
    
    st.session_state.new_device_name = selected if selected != "Other" else ""
    st.session_state.new_device_power_heavy = float(data["Power Heavy"])
    st.session_state.new_device_power_light = float(data["Power Light"])
    st.session_state.new_device_alloc_heavy = float(data["Alloc Heavy"])
    st.session_state.new_device_alloc_light = float(data["Alloc Light"])
    h_peak = float(data["Hours Peak"])
    h_low = float(data["Hours Low"])
    
    st.session_state.new_device_time_peak = float_to_time(h_peak)
    st.session_state.new_device_time_low = float_to_time(h_low)
    st.session_state.new_device_days = int(data["Days"])
    st.session_state.new_device_weeks = int(data["Weeks"])

# Helper functions for time conversion
def float_to_time(h_float):
    h = int(h_float)
    m = int(round((h_float - h) * 60))
    if h >= 24: return time(23, 59)
    if m == 60:
        h += 1
        m = 0
    if h >= 24: return time(23, 59)
    return time(h, m)

def time_to_float(t):
    return t.hour + (t.minute / 60.0)

# Initialize session state for form inputs if not present
if 'new_device_name' not in st.session_state:
    st.session_state.new_device_name = ""
if 'new_device_power_heavy' not in st.session_state:
    st.session_state.new_device_power_heavy = 100.0
if 'new_device_power_light' not in st.session_state:
    st.session_state.new_device_power_light = 10.0
if 'new_device_alloc_heavy' not in st.session_state:
    st.session_state.new_device_alloc_heavy = 100.0
if 'new_device_alloc_light' not in st.session_state:
    st.session_state.new_device_alloc_light = 0.0
if 'new_device_time_peak' not in st.session_state:
    st.session_state.new_device_time_peak = time(0, 0)
if 'new_device_time_low' not in st.session_state:
    st.session_state.new_device_time_low = time(0, 0)
if 'new_device_days' not in st.session_state:
    st.session_state.new_device_days = 7
if 'new_device_weeks' not in st.session_state:
    st.session_state.new_device_weeks = 52

# Container for "Add New Device" to group inputs visually
st.header("Add New Device")
with st.container(border=True):
    # Marker for CSS targeting
    st.markdown('<div class="device-box-fix"></div>', unsafe_allow_html=True)
    
    
    # Top Row: Device Type and Quantity
    row1_col1, row1_col2 = st.columns([3, 1])
    
    # Device Type Dropdown
    device_types = sorted([k for k in DEVICE_DEFAULTS.keys() if k != "Other"]) + ["Other"]
    row1_col1.selectbox("Device Type", options=device_types, index=device_types.index("Other"), key="device_type_selector", on_change=on_device_type_change)
    
    # Quantity
    quantity = row1_col2.number_input("Quantity", min_value=1, value=1, step=1, format="%d")

    name = st.text_input("Device Name", key="new_device_name")
    
    st.subheader("Usage Profile (Load)")
    c1, c2 = st.columns(2)
    power_heavy = c1.number_input("High Power (W)", min_value=0.0, step=1.0, format="%.2f", key="new_device_power_heavy")
    power_light = c2.number_input("Low Power (W)", min_value=0.0, step=1.0, format="%.2f", key="new_device_power_light")
    
    st.subheader("Time Allocation in each state")
    c3, c4 = st.columns(2)
    alloc_heavy = c3.number_input("High Power %", min_value=0.0, max_value=100.0, step=1.0, key="new_device_alloc_heavy")
    alloc_light = c4.number_input("Low Power %", min_value=0.0, max_value=100.0, step=1.0, key="new_device_alloc_light")
    
    st.subheader("Hours Per Day")
    # Peak
    p1, p2 = st.columns([1, 1])
    # Use time_input for cleaner UI (HH:MM)
    time_peak = p1.time_input("Peak Hours", key="new_device_time_peak")
    
    # Off-Peak
    time_low = p2.time_input("Off-Peak Hours", key="new_device_time_low")
    
    st.subheader("Frequency")
    f1, f2 = st.columns(2)
    days_per_week = f1.number_input("Days per Week", min_value=0, max_value=7, step=1, format="%d", key="new_device_days")
    weeks_per_year = f2.number_input("Weeks per Year", min_value=0, max_value=52, step=1, format="%d", key="new_device_weeks")

    # Button is now outside a form, so it triggers a rerun immediately
    submitted = st.button("Add Device")
    if submitted:
        # Reconstruct decimal hours from time objects
        hours_peak = time_peak.hour + (time_peak.minute / 60.0)
        hours_low = time_low.hour + (time_low.minute / 60.0)
        
        if not name:
            st.error("Please enter a device name.")
        elif abs((alloc_heavy + alloc_light) - 100.0) > 0.01:
            st.error(f"Load allocations must sum to 100%. Current sum: {alloc_heavy + alloc_light}%")
        elif (hours_peak + hours_low) > 24.0:
             st.error(f"Total hours cannot exceed 24. Current total: {hours_peak + hours_low:.2f}")
        else:
            # Store unscaled hours and separate frequency data
            # Scaling will happen at calculation time
            
            # Add single entry with Count
            st.session_state.devices.append({
                "Name": name,
                "Count": int(quantity),
                "Power Heavy": power_heavy,
                "Power Light": power_light,
                "Alloc Heavy": alloc_heavy,
                "Alloc Light": alloc_light,
                "Hours Peak": hours_peak,     # Stored unscaled
                "Hours Low": hours_low,       # Stored unscaled
                "Days": days_per_week,        # Store frequency
                "Weeks": weeks_per_year,      # Store frequency
                "Include": True
            })
            
            st.success(f"Added {name} (x{quantity})")

# Display and Edit Devices
if st.session_state.devices:
    if st.session_state.devices:
        st.subheader("Device List")
        
        df = pd.DataFrame(st.session_state.devices)
        if "Include" not in df.columns:
            df["Include"] = True
        if "Count" not in df.columns:
            df["Count"] = 1
        if "Days" not in df.columns:
            df["Days"] = 7.0
        if "Weeks" not in df.columns:
            df["Weeks"] = 52.0
            
        # Add temporary Time columns for display/editing
        # We use apply to convert the float hours to datetime.time objects
        if "Hours Peak" in df.columns:
            df["Time Peak"] = df["Hours Peak"].apply(float_to_time)
        if "Hours Low" in df.columns:
            df["Time Low"] = df["Hours Low"].apply(float_to_time)
    
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Name": st.column_config.TextColumn("Device Name"),
            "Count": st.column_config.NumberColumn("Count", min_value=1, step=1, format="%d"),
            "Power Heavy": st.column_config.NumberColumn("High Power (W)", min_value=0.0, format="%.2f"),
            "Power Light": st.column_config.NumberColumn("Low Power (W)", min_value=0.0, format="%.2f"),
            "Alloc Heavy": st.column_config.NumberColumn("High Power %", min_value=0.0, max_value=100.0, format="%.2f"),
            "Alloc Light": st.column_config.NumberColumn("Low Power %", min_value=0.0, max_value=100.0, format="%.2f"),
            "Time Peak": st.column_config.TimeColumn("Peak Hours", format="HH:mm", step=60),
            "Time Low": st.column_config.TimeColumn("Off-Peak Hours", format="HH:mm", step=60),
            "Days": st.column_config.NumberColumn("Days/Week", min_value=0, max_value=7, step=1, format="%d"),
            "Weeks": st.column_config.NumberColumn("Weeks/Year", min_value=0, max_value=52, step=1, format="%d"),
            "Hours Peak": None, # Hide original float column
            "Hours Low": None,  # Hide original float column
            "Include": st.column_config.CheckboxColumn("Include", default=True),
        },
        key="device_editor"
    )
    
    # Process updates: Convert Time objects back to float hours for storage/calculation
    if edited_df is not None:
        # Recalculate floats from the edited Time columns
        if "Time Peak" in edited_df.columns:
            edited_df["Hours Peak"] = edited_df["Time Peak"].apply(lambda t: time_to_float(t) if t else 0.0)
        if "Time Low" in edited_df.columns:
            edited_df["Hours Low"] = edited_df["Time Low"].apply(lambda t: time_to_float(t) if t else 0.0)
            
        # Drop temporary columns for clean storage
        storage_df = edited_df.drop(columns=["Time Peak", "Time Low"], errors="ignore")
        
        current_devices = storage_df.to_dict('records')
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
                h_peak_raw = Decimal(str(row['Hours Peak']))
                h_low_raw = Decimal(str(row['Hours Low']))
                
                # Frequency Scaling
                days = Decimal(str(row.get('Days', 7.0)))
                weeks = Decimal(str(row.get('Weeks', 52.0)))
                scaling_factor = (days / Decimal("7.0")) * (weeks / Decimal("52.0"))
                
                # Effective Daily Hours (for cost calc only)
                h_peak = h_peak_raw * scaling_factor
                h_low = h_low_raw * scaling_factor
                
                # Count
                count = Decimal(str(row.get('Count', 1)))

                # Rates (£)
                r_peak = Decimal(str(cost_peak))
                r_low = Decimal(str(cost_low))
                
                # Cost Calculation (Per Unit)
                unit_daily_kwh = (h_peak * avg_kw) + (h_low * avg_kw)
                
                unit_cost_peak = h_peak * avg_kw * r_peak
                unit_cost_low = h_low * avg_kw * r_low
                unit_daily_cost = unit_cost_peak + unit_cost_low
                
                # Total Cost (Scaled by Count)
                daily_kwh = unit_daily_kwh * count
                daily_cost = unit_daily_cost * count
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
        # Fix index alignment: Ensure cost_df matches edited_df indices
        # If edited_df has gaps (e.g. from deletion), default RangeIndex of cost_df causes concat errors.
        if not cost_df.empty:
            cost_df.index = edited_df.index
        
        display_df = pd.concat([edited_df, cost_df], axis=1)
        
        # 1-based indexing: Reset first to ensure clean sequence
        display_df.reset_index(drop=True, inplace=True)
        display_df.index = display_df.index + 1
        
        # Format Hours columns to HH:MM strings for display
        def format_display_time(val):
            try:
                t = float_to_time(float(val))
                return t.strftime("%H:%M")
            except:
                return str(val)

        if "Hours Peak" in display_df.columns:
             display_df.drop(columns=["Hours Peak"], inplace=True)
        if "Hours Low" in display_df.columns:
             display_df.drop(columns=["Hours Low"], inplace=True)
            
        # Rename columns for display
        display_df = display_df.rename(columns={
            "Power Heavy": "High Power (W)",
            "Power Light": "Low Power (W)",
            "Alloc Heavy": "High Power %",
            "Alloc Light": "Low Power %",
        })
        


        format_mapping = {
            "Daily Cost": "£{:.2f}", 
            "Monthly Cost": "£{:.2f}", 
            "Annual Cost": "£{:.2f}",
            "High Power (W)": "{:.2f}",
            "Low Power (W)": "{:.2f}",
            "High Power %": "{:.2f}",
            "Low Power %": "{:.2f}",
            "Daily kWh": "{:.3f}"
        }
        
        st.subheader("Cost Breakdown")
        st.dataframe(
            display_df.style.format(format_mapping),
            use_container_width=True
        )

        # Total Metrics - Filter by Include
        # Align indices just in case, though they should match
        active_mask = edited_df["Include"].fillna(True).astype(bool)
        active_cost_df = cost_df[active_mask]
        
        total_daily = active_cost_df["Daily Cost"].sum()
        total_monthly = active_cost_df["Monthly Cost"].sum()
        total_annual = active_cost_df["Annual Cost"].sum()
        
        total_daily_kwh = active_cost_df["Daily kWh"].sum()
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
                
                count_val = int(Decimal(str(r.get('Count', 1))))

                st.write(f"**Device**: {r['Name']} (Count: {count_val})")
                st.markdown("#### 1. Average Power (Load Profile)")
                st.write(f"- Heavy Load: {p_heavy}W ({a_heavy}%)")
                st.write(f"- Regular Load: {p_light}W ({a_light}%)")
                st.write(f"- **Average Power**: {avg_watts:.2f} W -> **{avg_kw:.4f} kW**")
                
                st.markdown("#### 2. Cost (Time Profile)")
                st.write(f"**Rates (£/kWh)**: Peak £{r_peak:.4f}, Off-Peak £{r_low:.4f}")
                st.write(f"- **Peak Period**: {h_peak} hrs * {avg_kw:.4f} kW * £{r_peak:.4f} = £{(h_peak * avg_kw * r_peak):.4f}")
                st.write(f"- **Off-Peak Period**: {h_low} hrs * {avg_kw:.4f} kW * £{r_low:.4f} = £{(h_low * avg_kw * r_low):.4f}")
                
                st.markdown("#### Total")
                unit_daily = (h_peak * avg_kw * r_peak) + (h_low * avg_kw * r_low)
                total_daily = unit_daily * count_val
                st.write(f"- **Unit Daily Cost**: £{unit_daily:.4f}")
                if count_val > 1:
                     st.write(f"- **Total Daily Cost** (x{count_val}): £{total_daily:.4f}")
        
        # Chart
        st.markdown("---")
        st.subheader("Annual Cost Distribution")
        
        # Prepare data for Pie Chart
        # Use display_df which contains all the correct aligned data
        # Filter for included devices
        chart_df = display_df[display_df["Include"].fillna(True).astype(bool)].copy()
        chart_df = chart_df[["Name", "Annual Cost"]]
        chart_df["Annual Cost"] = chart_df["Annual Cost"].astype(float)
        
        if not chart_df.empty:
            fig = px.pie(chart_df, values="Annual Cost", names="Name", 
                         title="Share of Total Annual Cost")
            fig.update_layout(height=900)
            st.plotly_chart(fig, use_container_width=True)


if not st.session_state.devices:
    st.info("No devices added yet.")
