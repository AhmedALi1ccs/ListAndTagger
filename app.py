import streamlit as st
import pandas as pd
import io
import os

# Define the column mappings
column_list_mapping = {
    'HIDDENGEMS': 'Base List',
    'ABSENTEE': 'Base List',
    'HIGH EQUITY': 'Base List',
    'DOWNSIZING': 'Downsizing',
    'PRE-FORECLOSURE': 'Foreclosure',
    'VACANT': 'Base List',
    '55+': 'Base List',
    'ESTATE': 'Base List',
    'INTER FAMILY TRANSFER': 'Interfamily Transfer',
    'DIVORCE': 'Divorce - Propstream',
    'TAXES': 'Base List',
    'PROBATE': 'Probate',
    'LOW CREDIT': 'Base List',
    'CODE VIOLATIONS': 'Code Violations',
    'BANKRUPTCY': 'Bankruptcy',
    'LIENS CITY/COUNTY': 'Liens-Recorder',
    'LIENS OTHER': 'Liens-Recorder',
    'LIENS UTILITY': 'Special Assessments',
    'LIENS HOA': 'Special Assessments',
    'LIENS MECHANIC': 'Special Assessments',
    'POOR CONDITION': 'Driving For Dollars',
    'EVICTION': 'Evictions',
    '30-60 DAYS': 'Late Mortgage',
    'JUDGEMENT': 'Base List',
    'DEBT COLLECTION': 'Base List'
}

column_abbreviation_mapping = {
    'HIDDENGEMS': '8020 Hidden Gems List',
    'ABSENTEE': '8020 Absentee List',
    'HIGH EQUITY': '8020 High Equity List',
    'DOWNSIZING': '8020 Downsizing List',
    'PRE-FORECLOSURE': '8020 Pre-Foreclosure List',
    'VACANT': '8020 Vacant List',
    '55+': '8020 55+ List',
    'ESTATE': '8020 Estate List',
    'INTER FAMILY TRANSFER': '8020 Inter-family Transfer List',
    'DIVORCE': '8020 Divorce List',
    'TAXES': '8020 Taxes List',
    'PROBATE': '8020 Probate List',
    'LOW CREDIT': 'Base List',
    'CODE VIOLATIONS': '8020 Code Violations List',
    'BANKRUPTCY': '8020 Bankruptcy List',
    'LIENS CITY/COUNTY': '8020 Liens List',
    'LIENS OTHER': '8020 Liens List',
    'LIENS UTILITY': '8020 Liens List',
    'LIENS HOA': '8020 Liens List',
    'LIENS MECHANIC': '8020 Liens List',
    'POOR CONDITION': '8020 Poor Conditions List',
    'EVICTION': '8020 Evictions List',
    '30-60 DAYS': '8020 30-60 days List',
    'JUDGEMENT': '8020 Judgement List',
    'DEBT COLLECTION': '8020 Debt Collection List'
}

def process_file(file):
    # Load the file based on its extension
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        st.error('Unsupported file type. Please upload an Excel or CSV file.')
        return None

    # Process the 'LISTS' column
    if 'LISTS' not in df.columns:
        df['LISTS'] = ''
    df['LISTS'] = df['LISTS'].fillna('')
    
    for index, row in df.iterrows():
        selected_abbreviations = set(
            column_list_mapping[col] for col in column_list_mapping
            if col in df.columns and row[col] == 1
        )
    
        new_list = ', '.join(sorted(selected_abbreviations))
        if df.at[index, 'LISTS']:
            df.at[index, 'LISTS'] = df.at[index, 'LISTS'] + ', ' + new_list
        else:
            df.at[index, 'LISTS'] = new_list

    # Process the 'TAGS' column
    if 'TAGS' not in df.columns:
        df['TAGS'] = ''
    df['TAGS'] = df['TAGS'].fillna('')
    
    for index, row in df.iterrows():
        selected_abbreviations = set(
            column_abbreviation_mapping[col] for col in column_abbreviation_mapping
            if col in df.columns and row[col] == 1
        )
        new_list = ', '.join(sorted(selected_abbreviations))
        if df.at[index, 'TAGS']:
            df.at[index, 'TAGS'] = df.at[index, 'TAGS'] + ', ' + new_list
        else:
            df.at[index, 'TAGS'] = new_list

    return df

st.title('List and Tags Processor')

uploaded_file = st.file_uploader("Choose an Excel or CSV file", type=['xlsx', 'csv'])
if uploaded_file:
    st.write("Processing your file...")
    processed_df = process_file(uploaded_file)
    if processed_df is not None:
        st.write("File processed successfully.")
        
        # Construct the output filename
        base, ext = os.path.splitext(uploaded_file.name)
        output_filename = f"{base}_ListsandTagsAdjusted.csv"
        
        # Save the processed DataFrame to a BytesIO object
        buffer = io.BytesIO()
        if uploaded_file.name.endswith('.xlsx'):
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                processed_df.to_excel(writer, index=False, sheet_name='Sheet1')
        else:
            processed_df.to_csv(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
            label="Download processed file",
            data=buffer,
            file_name=output_filename,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if uploaded_file.name.endswith('.xlsx') else 'text/csv'
        )
