import pandas as pd

def wrangling():
    df = pd.read_csv('data/raw/ds_salaries.csv')

    # Data Wrangling
    iso3166_to_continent = {
        'DE': 'Europe',
        'JP': 'Asia',
        'GB': 'Europe',
        'HN': 'North America',
        'US': 'North America',
        'HU': 'Europe',
        'NZ': 'Oceania',
        'FR': 'Europe',
        'IN': 'Asia',
        'PK': 'Asia',
        'CN': 'Asia',
        'GR': 'Europe',
        'AE': 'Asia',
        'NL': 'Europe',
        'MX': 'North America',
        'CA': 'North America',
        'AT': 'Europe',
        'NG': 'Africa',
        'ES': 'Europe',
        'PT': 'Europe',
        'DK': 'Europe',
        'IT': 'Europe',
        'HR': 'Europe',
        'LU': 'Europe',
        'PL': 'Europe',
        'SG': 'Asia',
        'RO': 'Europe',
        'IQ': 'Asia',
        'BR': 'South America',
        'BE': 'Europe',
        'UA': 'Europe',
        'IL': 'Asia',
        'RU': 'Europe',
        'MT': 'Europe',
        'CL': 'South America',
        'IR': 'Asia',
        'CO': 'South America',
        'MD': 'Europe',
        'KE': 'Africa',
        'SI': 'Europe',
        'CH': 'Europe',
        'VN': 'Asia',
        'AS': 'Oceania',
        'TR': 'Asia',
        'CZ': 'Europe',
        'DZ': 'Africa',
        'EE': 'Europe',
        'MY': 'Asia',
        'AU': 'Oceania',
        'IE': 'Europe'
    }

    df['Continent'] = df['company_location'].map(iso3166_to_continent)

    def data_mapping_replace(df, col_name, dict):
        df[col_name] = df[col_name].replace(dict)

    data_mapping_replace(df, "remote_ratio", {100: 'Full-Remote', 50: 'Hybrid', 0:'In-Person'})
    data_mapping_replace(df, "experience_level", {'EN': 'Entry-Level', 'SE': 'Lower-Middle', 'MI':'Mid-Level', 'EX': 'Executive-Level'})
    data_mapping_replace(df, "employment_type", {'FT': 'Full-Time', 'PT': 'Part-Time', "FL":'Freelance', "CT": "Contract"})
    data_mapping_replace(df, "company_size", {'L': 'Large', 'M': 'Medium', "S":'Small'})

    return df