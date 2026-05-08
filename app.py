# import streamlit as st
# import pandas as pd
# import re
# from datetime import datetime
# import io

# # --- AAPKA ORIGINAL LOGIC (NO CHANGES) ---
# CRM_FIELDS = [
#     'Campaign', 'CustomerType', 'customerName', 'CustomerSubtype',
#     'ContactNumber', 'City', 'Location', 'SubLocation', 'Area',
#     'Address', 'Email', 'Facilities', 'ReferenceId', 'CustomerId',
#     'ClientId', 'CustomerDate', 'CustomerYear', 'Other', 'Description',
#     'Video', 'GoogleMap', 'Price', 'LeadType', 'URL', 'isFavourite', 'Verified'
# ]

# JAIPUR_AREAS = [
#     'Vaishali Nagar', 'Mansarovar', 'Jagatpura', 'Malviya Nagar', 'Tonk Road',
#     'Ajmer Road', 'Sanganer', 'Bani Park', 'C Scheme', 'Raja Park', 'Jhotwara',
#     'Kalwar Road', 'Pratap Nagar', 'Gopalpura', 'Sikar Road', 'Sitapura'
# ]

# def extract_area_and_bhk(text):
#     if not isinstance(text, str): return "N/A"
#     bhk_matches = re.findall(r'\b\d+\s*BHK\b', text, re.IGNORECASE)
#     sqft_pattern = r'\d+\s*(?:sq\s*ft|sqft|square\s*feet)'
#     sqft_matches = re.findall(sqft_pattern, text, re.IGNORECASE)
#     yard_pattern = r'\d+\s*(?:sq\s*yard|sq\s*yd|sq\s*yards)'
#     yard_matches = re.findall(yard_pattern, text, re.IGNORECASE)
#     all_found = bhk_matches + sqft_matches + yard_matches
#     return " ".join([item.strip() for item in all_found]) if all_found else "N/A"

# def extract_clean_prices(text):
#     if not isinstance(text, str): return "N/A"
#     anchor_pattern = r'(?:Rent|Price|Security|₹|Rs\.?)\s*[:=]?\s*[\d,.]+(?:\s*(?:k|/-|Lakh|Lac|Cr|Crore|thousand))?'
#     matches = re.findall(anchor_pattern, text, re.IGNORECASE)
#     if not matches: return "N/A"
#     cleaned_results = []
#     for m in matches:
#         value_part = re.search(r'(₹?[\d,.]+(?:\s*(?:k|Lakh|Lac|Cr|Crore))?)', m, re.IGNORECASE)
#         if value_part:
#             val = value_part.group(1).replace('₹', '').strip()
#             if re.search(r'[\dk]', val, re.IGNORECASE):
#                 cleaned_results.append(val)
#     return "-".join(cleaned_results) if cleaned_results else "N/A"

# def extract_geo_data(text):
#     text_str = str(text)
#     found_loc = "N/A"
#     for area in JAIPUR_AREAS:
#         if area.lower() in text_str.lower():
#             found_loc = area
#             break
#     if found_loc == "N/A":
#         loc_match = re.search(r'(?:in|at|near|location:|address:)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text_str)
#         if loc_match: found_loc = loc_match.group(1).strip()
#     address = text_str.split('\n')[0][:100].strip() if text_str != "nan" else "N/A"
#     return found_loc, found_loc, address

# def extract_indian_mobile(text):
#     if pd.isna(text) or str(text).strip() == "": return "1010101010"
#     clean_text = re.sub(r'[\s\-\(\)\.\/]', '', str(text))
#     matches = re.findall(r'(?:(?<=^)|(?<=\D))([6-9]\d{9})(?=\D|$)', clean_text)
#     if not matches:
#         twelve_digit = re.findall(r'91([6-9]\d{9})', clean_text)
#         if twelve_digit: matches = twelve_digit
#     return matches[0] if matches else "1010101010"

# def get_customer_type_and_subtype(text):
#     t = text.lower()
#     c_type, c_subtype = "Other", "N/A"
#     bhk_num_match = re.search(r'(\d+)\s*bhk', t)
#     if bhk_num_match or 'flat' in t or 'apartment' in t:
#         c_type = "Flat"
#         if bhk_num_match:
#             num = int(bhk_num_match.group(1))
#             if num == 1: c_subtype = "1 BHK"
#             elif num == 2: c_subtype = "2 BHK"
#             elif num >= 3: c_subtype = "3 BHK and above"
#         elif any(x in t for x in ['3+1', '3+study', '4 bhk', '5 bhk']):
#             c_subtype = "3 BHK and above"
#     elif any(x in t for x in ['house', 'independent makaan', 'duplex', 'makaan']):
#         c_type, c_subtype = "House", "Independent Makaan/Duplex"
#     elif any(x in t for x in ['villa', 'bungalow', 'kothi']):
#         c_type, c_subtype = "Villa", "Villa/Bungalow"
#     elif any(x in t for x in ['room', 'single room', 'portion']):
#         c_type, c_subtype = "Room", "Single Room/Portion"
#     elif any(x in t for x in ['shop', 'office', 'warehouse', 'showroom', 'basement', 'commercial']):
#         c_type, c_subtype = "Commercial Space", "Shop/Office/Commercial"
#     elif any(x in t for x in ['plot', 'jda approved']):
#         c_type, c_subtype = "Residential Plot", "Plot/JDA Plot"
#     elif 'farm house' in t:
#         c_type, c_subtype = "Farm House", "Farm House"
#     elif any(x in t for x in ['bigha', 'kheti', 'agricultural']):
#         c_type, c_subtype = "Agricultural Land", "Bigha/Kheti Land"
#     return c_type, c_subtype

# # --- INTERFACE DESIGN ---
# st.set_page_config(page_title="FB Real Estate Miner", page_icon="🏢")

# st.title("🏢 Real Estate Data Miner")
# st.info("Bss Excel file drop karein aur processed CSV payein.")

# uploaded_file = st.file_uploader("Upload Facebook Excel (Sheet name 'Data' honi chahiye)", type=["xlsx"])

# if uploaded_file:
#     try:
#         df_raw = pd.read_excel(uploaded_file, sheet_name='Data')
#         st.success(f"File Load Ho Gayi! Total {len(df_raw)} records mile.")

#         if st.button("Mining Shuru Karein 🚀"):
#             current_date = datetime.now().strftime('%d-%m-%Y')
#             rows = []
#             bar = st.progress(0)

#             for i, (_, row) in enumerate(df_raw.iterrows()):
#                 raw_text = str(row.get('text', "")).strip()
#                 if raw_text == "" or raw_text.lower() == 'nan': continue

#                 entry = {field: "N/A" for field in CRM_FIELDS}
#                 entry.update({
#                     'ContactNumber': extract_indian_mobile(raw_text),
#                     'Description': raw_text,
#                     'Area': extract_area_and_bhk(raw_text),
#                     'Price': extract_clean_prices(raw_text),
#                     'City': 'Jaipur',
#                     'CustomerDate': current_date,
#                     'ReferenceId': 'facebook'
#                 })

#                 c_type, c_subtype = get_customer_type_and_subtype(raw_text)
#                 entry['CustomerType'], entry['CustomerSubtype'] = c_type, c_subtype

#                 loc, sub_loc, addr = extract_geo_data(raw_text)
#                 entry['Location'], entry['SubLocation'], entry['Address'] = loc, sub_loc, addr

#                 lower_text = raw_text.lower()
#                 if 'rent' in lower_text: entry['Campaign'] = 'Rentout'
#                 elif any(x in lower_text for x in ['sale', 'sell']): entry['Campaign'] = 'Seller'
#                 elif any(x in lower_text for x in ['buy', 'looking for']): entry['Campaign'] = 'Buyer'

#                 rows.append(entry)
#                 bar.progress((i + 1) / len(df_raw))

#             df_final = pd.DataFrame(rows)
#             st.write("### Data Preview (Top 10):")
#             st.dataframe(df_final.head(10))

#             # Download Option
#             csv = df_final.to_csv(index=False).encode('utf-8')
#             st.download_button("Download Processed CSV 📥", csv, f"Processed_{current_date}.csv", "text/csv")

#     except Exception as e:
#         st.error(f"Opps! Error: {e}")

import streamlit as st
import pandas as pd
import re
from datetime import datetime
import io
from openpyxl import load_workbook

# ============================================================
# CRM FIELD LIST
# ============================================================
CRM_FIELDS = [
    'Campaign', 'CustomerType', 'customerName', 'CustomerSubtype',
    'ContactNumber', 'City', 'Location', 'SubLocation', 'Area',
    'Address', 'Email', 'Facilities', 'ReferenceId', 'CustomerId',
    'ClientId', 'CustomerDate', 'CustomerYear', 'Other', 'Description',
    'Video', 'GoogleMap', 'Price', 'LeadType', 'URL', 'isFavourite', 'Verified'
]

# ============================================================
# JAIPUR KE POPULAR AREAS KI LIST
# ============================================================
JAIPUR_AREAS = [
    'Vaishali Nagar', 'Mansarovar', 'Jagatpura', 'Malviya Nagar', 'Tonk Road',
    'Ajmer Road', 'Sanganer', 'Bani Park', 'C Scheme', 'Raja Park', 'Jhotwara',
    'Kalwar Road', 'Pratap Nagar', 'Gopalpura', 'Sikar Road', 'Sitapura'
]

# ============================================================
# FUNCTIONS
# ============================================================

def extract_area_and_bhk(text):
    if not isinstance(text, str): return "N/A"
    bhk_matches = re.findall(r'\b\d+\s*BHK\b', text, re.IGNORECASE)
    sqft_pattern = r'\d+\s*(?:sq\s*ft|sqft|square\s*feet)'
    sqft_matches = re.findall(sqft_pattern, text, re.IGNORECASE)
    yard_pattern = r'\d+\s*(?:sq\s*yard|sq\s*yd|sq\s*yards)'
    yard_matches = re.findall(yard_pattern, text, re.IGNORECASE)
    all_found = bhk_matches + sqft_matches + yard_matches
    return " ".join([item.strip() for item in all_found]) if all_found else "N/A"

def extract_clean_prices(text):
    if not isinstance(text, str): return "N/A"
    anchor_pattern = r'(?:Rent|Price|Security|₹|Rs\.?)\s*[:=]?\s*[\d,.]+(?:\s*(?:k|/-|Lakh|Lac|Cr|Crore|thousand))?'
    matches = re.findall(anchor_pattern, text, re.IGNORECASE)
    if not matches: return "N/A"
    cleaned_results = []
    for m in matches:
        value_part = re.search(r'(₹?[\d,.]+(?:\s*(?:k|Lakh|Lac|Cr|Crore))?)', m, re.IGNORECASE)
        if value_part:
            val = value_part.group(1).replace('₹', '').strip()
            if re.search(r'[\dk]', val, re.IGNORECASE):
                cleaned_results.append(val)
    return "-".join(cleaned_results) if cleaned_results else "N/A"

def extract_geo_data(text):
    text_str = str(text)
    found_loc = "N/A"
    for area in JAIPUR_AREAS:
        if area.lower() in text_str.lower():
            found_loc = area
            break
    if found_loc == "N/A":
        loc_match = re.search(r'(?:in|at|near|location:|address:)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', text_str)
        if loc_match:
            found_loc = loc_match.group(1).strip()
    address = text_str.split('\n')[0][:100].strip() if text_str != "nan" else "N/A"
    return found_loc, found_loc, address

def extract_indian_mobile(text):
    if pd.isna(text) or str(text).strip() == "": return "1010101010"
    clean_text = re.sub(r'[\s\-\(\)\.\/]', '', str(text))
    matches = re.findall(r'(?:(?<=^)|(?<=\D))([6-9]\d{9})(?=\D|$)', clean_text)
    if not matches:
        twelve_digit = re.findall(r'91([6-9]\d{9})', clean_text)
        if twelve_digit:
            matches = twelve_digit
    return matches[0] if matches else "1010101010"

def get_customer_type_and_subtype(text):
    t = text.lower()
    c_type, c_subtype = "Other", "N/A"
    bhk_num_match = re.search(r'(\d+)\s*bhk', t)
    if bhk_num_match or 'flat' in t or 'apartment' in t:
        c_type = "Flat"
        if bhk_num_match:
            num = int(bhk_num_match.group(1))
            if num == 1: c_subtype = "1 BHK"
            elif num == 2: c_subtype = "2 BHK"
            elif num >= 3: c_subtype = "3 BHK and above"
        elif any(x in t for x in ['3+1', '3+study', '4 bhk', '5 bhk']):
            c_subtype = "3 BHK and above"
    elif any(x in t for x in ['house', 'independent makaan', 'duplex', 'makaan']):
        c_type, c_subtype = "House", "Independent Makaan/Duplex"
    elif any(x in t for x in ['villa', 'bungalow', 'kothi']):
        c_type, c_subtype = "Villa", "Villa/Bungalow"
    elif any(x in t for x in ['room', 'single room', 'portion']):
        c_type, c_subtype = "Room", "Single Room/Portion"
    elif any(x in t for x in ['shop', 'office', 'warehouse', 'showroom', 'basement', 'commercial']):
        c_type, c_subtype = "Commercial Space", "Shop/Office/Commercial"
    elif any(x in t for x in ['plot', 'jda approved']):
        c_type, c_subtype = "Residential Plot", "Plot/JDA Plot"
    elif 'farm house' in t:
        c_type, c_subtype = "Farm House", "Farm House"
    elif any(x in t for x in ['bigha', 'kheti', 'agricultural']):
        c_type, c_subtype = "Agricultural Land", "Bigha/Kheti Land"
    return c_type, c_subtype

# ============================================================
# STREAMLIT UI
# ============================================================
st.set_page_config(page_title="Real Estate Miner", page_icon="🏢")
st.title("🏢 Real Estate Data Miner")
st.info("Excel upload karein. Agar 'caption' column hai toh Instagram mana jayega, aur 'text' hai toh Facebook.")

uploaded_file = st.file_uploader("Upload Excel File (Data sheet zaroori hai)", type=["xlsx"])

# ============================================================
# MAIN PROCESSING
# ============================================================
if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, sheet_name='Data')
        st.success(f"File Load Ho Gayi! Total {len(df_raw)} records mile.")

        if st.button("Mining Shuru Karein 🚀"):
            current_date = datetime.now().strftime('%d-%m-%Y')
            rows = []
            bar = st.progress(0)

            # Check columns to decide source
            has_caption = 'caption' in df_raw.columns
            has_text = 'text' in df_raw.columns

            for i, (_, row) in enumerate(df_raw.iterrows()):
                # Logic to select source text and ReferenceId
                if has_caption:
                    raw_text = str(row.get('caption', "")).strip()
                    ref_id = 'instagram'
                elif has_text:
                    raw_text = str(row.get('text', "")).strip()
                    ref_id = 'facebook'
                else:
                    st.error("Excel mein na 'text' column mila na 'caption'! Mining rok di gayi.")
                    st.stop()

                if raw_text == "" or raw_text.lower() == 'nan':
                    continue

                entry = {field: "N/A" for field in CRM_FIELDS}

                entry.update({
                    'ContactNumber': str(extract_indian_mobile(raw_text)),
                    'Description': raw_text,
                    'Area': extract_area_and_bhk(raw_text),
                    'Price': extract_clean_prices(raw_text),
                    'City': 'Jaipur',
                    'CustomerDate': str(current_date),
                    'ReferenceId': ref_id  # Automatic Switch
                })

                c_type, c_subtype = get_customer_type_and_subtype(raw_text)
                entry['CustomerType'] = c_type
                entry['CustomerSubtype'] = c_subtype

                loc, sub_loc, addr = extract_geo_data(raw_text)
                entry['Location'] = loc
                entry['SubLocation'] = sub_loc
                entry['Address'] = addr

                lower_text = raw_text.lower()
                if 'rent' in lower_text:
                    entry['Campaign'] = 'Rentout'
                elif any(x in lower_text for x in ['sale', 'sell']):
                    entry['Campaign'] = 'Seller'
                elif any(x in lower_text for x in ['buy', 'looking for']):
                    entry['Campaign'] = 'Buyer'

                rows.append(entry)
                bar.progress((i + 1) / len(df_raw))

            df_final = pd.DataFrame(rows)
            st.write(f"### Data Preview (Detected Source: {ref_id.capitalize()}):")
            st.dataframe(df_final.head(10))

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False, sheet_name='ProcessedData')
                workbook = writer.book
                worksheet = writer.sheets['ProcessedData']
                headers = [cell.value for cell in worksheet[1]]

                # Number format fix for Excel
                for col_name in ['ContactNumber', 'CustomerDate']:
                    if col_name in headers:
                        col_idx = headers.index(col_name) + 1
                        for row_cells in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=col_idx, max_col=col_idx):
                            for cell in row_cells: cell.number_format = '@'

            output.seek(0)
            st.download_button(
                label="Download Processed Excel 📥",
                data=output,
                file_name=f"Processed_{ref_id}_{current_date}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error: {e}")
