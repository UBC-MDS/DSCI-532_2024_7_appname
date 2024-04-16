import pandas as pd
import json

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

    df['continent'] = df['company_location'].map(iso3166_to_continent)

    def data_mapping_replace(df, col_name, dict):
        df[col_name] = df[col_name].replace(dict)

    data_mapping_replace(df, "remote_ratio", {100: 'Full-Remote', 50: 'Hybrid', 0:'In-Person'})
    data_mapping_replace(df, "experience_level", {'EN': 'Entry-Level', 'SE': 'Senior-Level', 'MI': 'Mid-Level', 'EX': 'Executive-Level'})
    data_mapping_replace(df, "employment_type", {'FT': 'Full-Time', 'PT': 'Part-Time', "FL":'Freelance', "CT": "Contract"})
    data_mapping_replace(df, "company_size", {'L': 'Large', 'M': 'Medium', "S":'Small'})

    country_dict = {
        'DE': 'Germany', 'JP': 'Japan', 'GB': 'United Kingdom', 'HN': 'Honduras',
        'US': 'United States of America', 'HU': 'Hungary', 'NZ': 'New Zealand', 'FR': 'France',
        'IN': 'India', 'PK': 'Pakistan', 'CN': 'China', 'GR': 'Greece',
        'AE': 'United Arab Emirates', 'NL': 'Netherlands', 'MX': 'Mexico', 'CA': 'Canada',
        'AT': 'Austria', 'NG': 'Nigeria', 'ES': 'Spain', 'PT': 'Portugal',
        'DK': 'Denmark', 'IT': 'Italy', 'HR': 'Croatia', 'LU': 'Luxembourg',
        'PL': 'Poland', 'SG': 'Singapore', 'RO': 'Romania', 'IQ': 'Iraq',
        'BR': 'Brazil', 'BE': 'Belgium', 'UA': 'Ukraine', 'IL': 'Israel',
        'RU': 'Russia', 'MT': 'Malta', 'CL': 'Chile', 'IR': 'Iran',
        'CO': 'Colombia', 'MD': 'Moldova', 'KE': 'Kenya', 'SI': 'Slovenia',
        'CH': 'Switzerland', 'VN': 'Vietnam', 'AS': 'American Samoa', 'TR': 'Turkey',
        'CZ': 'Czech Republic', 'DZ': 'Algeria', 'EE': 'Estonia', 'MY': 'Malaysia',
        'AU': 'Australia', 'IE': 'Ireland'
    }
    df['company_location'] = df['company_location'].map(country_dict)

    df = df[['job_title', 'employment_type', 'experience_level', 
            'salary_in_usd', 'remote_ratio', 'company_size', 
            'company_location', 'continent']]
    df = df.rename(columns={
        'salary_in_usd': 'salary'
    })

    # Write the DataFrame to CSV files
    #df.to_csv('data/raw/ds_salaries_cleaned.csv', index=False)
    #df.to_csv('data/clean/ds_salaries.csv', index=False)

    #Abbreviate the really long names for bottom right bar chart
    df['job_title'] = df['job_title'].str.replace("Machine Learning", "ML")
    df['job_title'] = df['job_title'].str.replace("Computer Vision", "CV")
    df['job_title'] = df['job_title'].str.replace("Engineer", "Engr.")
    df['job_title'] = df['job_title'].str.replace("Scientist", "Sci.")

    return df

df = wrangling()

with open('data/countries.geojson') as f:
    geojson = json.load(f)