import pandas as pd
from scipy.stats import ttest_rel

def load_data(filepath: str) -> pd.DataFrame:
    data = pd.read_csv(filepath, header=None)
    return data

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    cleaned_data = []
    subject = None
    location = None

    for index, row in data.iterrows():
        if pd.notna(row[0]):
            subject = row[0]
        elif pd.notna(row[1]):
            location = row[1]
        elif pd.notna(row[2]):
            band = row[2]
            before = row[3]
            during = row[4]
            after = row[5]
            cleaned_data.append([subject, location, band, before, during, after])

    columns = ['Subject', 'Location', 'Band', 'Before', 'During', 'After']
    df = pd.DataFrame(cleaned_data, columns=columns)
    df['Before'] = pd.to_numeric(df['Before'], errors='coerce')
    df['During'] = pd.to_numeric(df['During'], errors='coerce')
    df['After'] = pd.to_numeric(df['After'], errors='coerce')
    
    return df

def perform_ttests(data: pd.DataFrame, band: str) -> pd.DataFrame:
    results = []
    for subject in data['Subject'].unique():
        subset = data[(data['Subject'] == subject) & (data['Band'] == band)]
        before = subset['Before'].values
        during = subset['During'].values
        after = subset['After'].values
        
        ttest_before_during = ttest_rel(before, during)
        ttest_during_after = ttest_rel(during, after)
        ttest_before_after = ttest_rel(before, after)
        
        results.append({
            'Subject': subject,
            'Comparison': 'Before-During',
            'Statistic': ttest_before_during.statistic,
            'p-value': ttest_before_during.pvalue
        })
        results.append({
            'Subject': subject,
            'Comparison': 'During-After',
            'Statistic': ttest_during_after.statistic,
            'p-value': ttest_during_after.pvalue
        })
        results.append({
            'Subject': subject,
            'Comparison': 'Before-After',
            'Statistic': ttest_before_after.statistic,
            'p-value': ttest_before_after.pvalue
        })
        
    return pd.DataFrame(results)