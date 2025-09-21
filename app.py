import streamlit as st
import pandas as pd

# Sidebar navigation
st.sidebar.title("Civil Engineering Toolkit")
page = st.sidebar.radio("Go to:", ["Home", "Estimator", "DSR Dashboard"])

if page == "Home":
	st.title("Civil Engineering Resource Hub")
	st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80", use_column_width=True)
	st.header("What is Estimation in Civil Engineering?")
	st.write("""
	Estimation is the process of forecasting the probable cost, quantities, and resources required for a construction project. It is crucial for:
	- Planning and budgeting
	- Tendering and contracts
	- Resource allocation
	- Avoiding cost overruns
	- Ensuring project feasibility
	""")
	st.header("Key Civil Engineering Works")
	st.markdown("""
	- Building Construction
	- Road & Highway Projects
	- Water Supply & Sanitation
	- Bridges & Flyovers
	- Irrigation & Dams
	- Surveying & Land Development
	- Structural Design
	- Project Management
	- Quantity Surveying & Estimation
	- Maintenance & Repairs
	""")
	st.info("Use the sidebar to explore the Estimator and DSR Dashboard.")

elif page == "DSR Dashboard":
	st.title("District Schedule Rates (DSR) Dashboard")
	st.write("""
	DSR (District Schedule Rates) are government-published rates for construction materials, labor, and works. They are used for public works estimation and contracts.
	""")
	st.subheader("Important DSR Points:")
	dsr_points = [
		"Rates are updated annually by CPWD/PWD.",
		"Include material, labor, machinery, and overheads.",
		"Vary by district/region.",
		"Used for government tenders and estimates.",
		"Include standard specifications for each item.",
		"GST and royalty may be extra.",
		"Non-schedule items (NS items) are quoted separately."
	]
	for pt in dsr_points:
		st.markdown(f"- {pt}")
	st.subheader("Sample DSR Table (2025)")
	dsr_data = pd.DataFrame({
		"Item": ["Cement (OPC 43)", "Steel (TMT)", "Sand (River)", "Bricks (1st class)", "Labour (Mason)", "Tiles (Ceramic)"],
		"Unit": ["Bag", "Kg", "Cum", "1000 Nos", "Day", "Sq.ft"],
		"DSR Rate (₹)": [420, 65, 1600, 8000, 600, 90]
	})
	st.dataframe(dsr_data)
	st.caption("Refer to your local PWD/CPWD DSR book for full details.")

else:
	st.title("🏠 Construction Project Estimator (with Plan Dimensions)")
	st.write("Enter your plan dimensions below. The app will estimate material quantities using standard thumb rules, then let you adjust rates and see the BOQ.")
	# Step 1: Collect Plan Dimensions
	st.header("1. Enter Plan Dimensions")
	col1, col2 = st.columns(2)
	with col1:
		length = st.number_input("Length of apartment (ft)", min_value=0.0, value=40.0, step=1.0)
		floors = st.number_input("Number of floors", min_value=1, value=1, step=1)
	with col2:
		breadth = st.number_input("Breadth of apartment (ft)", min_value=0.0, value=25.0, step=1.0)
		wall_height = st.number_input("Wall height (ft)", min_value=8.0, value=10.0, step=0.5)
	area = length * breadth * floors
	st.markdown(f"**Total Built-up Area:** {area:.0f} sq.ft")
	# Step 2: Estimate Quantities (Thumb Rules)
	st.header("2. Estimated Material Quantities (Editable)")
	qty_cement = st.number_input("Cement (bags, ~1.5 per sq.ft)", min_value=0.0, value=area*1.5, step=1.0)
	qty_steel = st.number_input("Steel (kg, ~3.5 per sq.ft)", min_value=0.0, value=area*3.5, step=1.0)
	qty_sand = st.number_input("Sand (brass, ~0.05 per sq.ft)", min_value=0.0, value=area*0.05, step=0.1)
	qty_tiles = st.number_input("Flooring (tiles, sq.ft)", min_value=0.0, value=area, step=1.0)
	qty_labour = st.number_input("Labour (sq.ft)", min_value=0.0, value=area, step=1.0)
	# Step 3: Enter Rates and Calculate BOQ
	st.header("3. Bill of Quantities (BOQ)")
	rate_cement = st.number_input("Cement rate per bag (₹)", min_value=0.0, value=400.0, step=1.0)
	rate_steel = st.number_input("Steel rate per kg (₹)", min_value=0.0, value=60.0, step=1.0)
	rate_sand = st.number_input("Sand rate per brass (₹)", min_value=0.0, value=1200.0, step=1.0)
	rate_tiles = st.number_input("Tiles rate per sq.ft (₹)", min_value=0.0, value=80.0, step=1.0)
	rate_labour = st.number_input("Labour rate per sq.ft (₹)", min_value=0.0, value=350.0, step=1.0)
	boq = [
		{"Item": "Cement", "Unit": "Bag", "Quantity": qty_cement, "Rate (₹)": rate_cement, "Amount (₹)": qty_cement*rate_cement},
		{"Item": "Steel", "Unit": "Kg", "Quantity": qty_steel, "Rate (₹)": rate_steel, "Amount (₹)": qty_steel*rate_steel},
		{"Item": "Sand", "Unit": "Brass", "Quantity": qty_sand, "Rate (₹)": rate_sand, "Amount (₹)": qty_sand*rate_sand},
		{"Item": "Flooring (Tiles)", "Unit": "Sq.ft", "Quantity": qty_tiles, "Rate (₹)": rate_tiles, "Amount (₹)": qty_tiles*rate_tiles},
		{"Item": "Labour", "Unit": "Sq.ft", "Quantity": qty_labour, "Rate (₹)": rate_labour, "Amount (₹)": qty_labour*rate_labour},
	]
	total = sum(item["Amount (₹)"] for item in boq)
	boq_df = pd.DataFrame(boq)
	st.dataframe(boq_df.style.format({"Quantity": "{:.0f}", "Rate (₹)": "₹{:.0f}", "Amount (₹)": "₹{:,.0f}"}), use_container_width=True)
	st.markdown(f"**Subtotal:** ₹{total:,.0f}")
	# Step 4: Add finishing and contingency
	st.header("4. Add Finishing & Contingency")
	finishing_pct = st.slider("Finishing/Overheads (%)", 0, 20, 12)
	contingency_pct = st.slider("Contingency (%)", 0, 10, 5)
	finishing_amt = total * finishing_pct / 100
	contingency_amt = total * contingency_pct / 100
	final_total = total + finishing_amt + contingency_amt
	st.markdown(f"**Finishing/Overheads:** ₹{finishing_amt:,.0f}")
	st.markdown(f"**Contingency:** ₹{contingency_amt:,.0f}")
	st.markdown(f"## Final Estimated Cost: ₹{final_total:,.0f}")
	st.caption("Tip: Adjust dimensions, quantities, and rates as per your project. This is a quick estimation tool, not a substitute for a detailed engineering estimate.")
