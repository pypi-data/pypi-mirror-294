import pandas as pd
import dataframe_image as dfi
import os
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta
import calendar
import time

warnings.filterwarnings("ignore", category=FutureWarning)

def bound_conditions(x, rule = 0):
    if rule == 0:
        x = round(float(x) * 100, 0)
        if x>500:
            x = "Unlimited"
        else:
            x = str(x) + "%"
        return x
    elif rule == 1:
        x = int(x)
        if x>500000000:
            x = "Unlimited"
        return str(x)

def crop_df(new_df, granularity):
    if granularity == []:
        return new_df
    unlimited_index = len(new_df)

    try:
        unlimited_index = new_df[new_df[granularity[1]] == 'Unlimited'].index[0]
    except:
        pass
    if unlimited_index == len(new_df):
        try:
            unlimited_index = new_df[(new_df[granularity[1]] == '0.0%') & (new_df[granularity[0]] == '0.0%')].index[0]
            unlimited_index -= 1
        except:
            pass
    new_df = new_df.loc[:unlimited_index]
    try:
        new_df = new_df[new_df['Tier'] != 'All Tiers']
    except:
        pass
    return new_df

def add_all_objectives(df):
    d = {}
    l1,l2 = [],[]
    for i in df['s01.07.01 Tiered % Rate Table'].unique():
        for j in range(1,11):
            l1.append(i)
            l2.append('Objective ' + str(j))
    df1 = pd.DataFrame()
    df1['s01.07.01 Tiered % Rate Table'] = l1
    df1['Objective'] = l2
    df.rename(columns = {'Tier' : 'Objective'}, inplace = True)

    return df1.merge(df, on = ['s01.07.01 Tiered % Rate Table','Objective'], how = 'left')

def delete_objectives(df,column_name):
    rows_to_delete = []
    for index in range(len(df) - 1, -1, -1):
        if df.at[index, column_name] == 0:
            rows_to_delete.append(index)
        else:
            break
    # Drop the identified rows
    df.drop(rows_to_delete, inplace=True)

    # Reset the index if needed
    df.reset_index(drop=True, inplace=True)
    return df



def get_previous_month_year():
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime("%B %Y")

# Function to get the correct suffix for a day
def get_day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

# Function to get today's date in the desired format
def get_todays_date():
    today = datetime.today()
    day = today.day
    suffix = get_day_suffix(day)
    return today.strftime(f"%d{suffix} %B")

def create_rate_table_images():
    folder_path = os.getcwd()
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    for source_file in csv_files:
        df = pd.read_csv(source_file)
        source_file = source_file.lower()
        df.rename(columns = {"Unnamed: 0" : 's01.07.01 Tiered % Rate Table', "Unnamed: 1":"Tier"}, inplace = True)
        for field in df["s01.07.01 Tiered % Rate Table"].unique():
            new_df = df[df["s01.07.01 Tiered % Rate Table"] == field].copy()
            new_df.fillna(0, inplace = True)

            if ('m01.14' in source_file) or ('type 1' in source_file):
                new_df = new_df[['Tier', 'Lower Bound(In %)','Upper Bound(In %)', 'Accelerator(In x)']]

                new_df['Lower Bound(In %)'] = new_df['Lower Bound(In %)'].apply(bound_conditions)
                new_df['Upper Bound(In %)'] = new_df['Upper Bound(In %)'].apply(bound_conditions)
                new_df['Accelerator(In x)'] = new_df['Accelerator(In x)'].apply(lambda x: str(x) + "x")
                granularity = ['Lower Bound(In %)','Upper Bound(In %)']

            elif ('m01.15' in source_file) or ('type 2' in source_file):
                new_df = new_df[['Tier', 'Lower Bound (In $)','Upper Bound (In $)', "Payout %"]]

                new_df['Lower Bound (In $)'] = new_df['Lower Bound (In $)'].apply(lambda x: bound_conditions(x, rule = 1))
                new_df['Upper Bound (In $)'] = new_df['Upper Bound (In $)'].apply(lambda x: bound_conditions(x, rule = 1))
                new_df["Payout %"] = new_df["Payout %"].apply(lambda x: str(round(x * 100, 2)) + "%")
                granularity = ['Lower Bound (In $)','Upper Bound (In $)']

            elif ('m01.16' in source_file) or ('type 3' in source_file):
                new_df = new_df[[ "Tier",'Attainment %',"Percentage Payout"]]

                new_df['Attainment %'] = new_df['Attainment %'].apply(bound_conditions)
                new_df['Percentage Payout'] = new_df['Percentage Payout'].apply(bound_conditions)
                granularity = ['Attainment %',"Percentage Payout"]

            elif ('m01.25' in source_file) or ('type 4' in source_file):
                new_df = new_df[['Tier', 'Lower Bound (In %)','Upper Bound (In %)', 'Accelerator (In x)']]

                new_df['Lower Bound (In %)'] = new_df['Lower Bound (In %)'].apply(bound_conditions)
                new_df['Upper Bound (In %)'] = new_df['Upper Bound (In %)'].apply(bound_conditions)
                new_df['Accelerator (In x)'] = new_df['Accelerator (In x)'].apply(lambda x: str(x) + "x")
                granularity = ['Lower Bound (In %)','Upper Bound (In %)']

            elif ('m01.17' in source_file) or ('type 5' in source_file):
                new_df.rename(columns = {'Tier' : 'Range'}, inplace = True)
                new_df = new_df[['Range', 'Lower Bound(In %)','Upper Bound(In %)', 'Payout Percentage', 'Quarterly Payout Amount']]

                new_df['Lower Bound(In %)'] = new_df['Lower Bound(In %)'].apply(bound_conditions)
                new_df['Upper Bound(In %)'] = new_df['Upper Bound(In %)'].apply(bound_conditions)
                new_df['Payout Percentage'] = new_df['Payout Percentage'].apply(bound_conditions)
                new_df['Quarterly Payout Amount'] = new_df['Quarterly Payout Amount'].apply(lambda x: str(round(x,1)))
                granularity = []
                new_df["Range"] = new_df["Range"].apply(lambda x: int(x.split()[1]))
                new_df = new_df.sort_values(by='Range')
                new_df["Range"] = new_df["Range"].apply(lambda x: "Range " + str(x))

            elif ('m01.18' in source_file) or ('type 6' in source_file):
                new_df = add_all_objectives(new_df)
                new_df.rename(columns = {'Tier' : 'Objective'}, inplace = True)
                new_df = new_df[['Objective', 'Payment(In $)']]
                new_df.fillna(0, inplace = True)
                new_df['Payment(In $)'] = new_df['Payment(In $)'].apply(lambda x: int(x))
                new_df["Objective"] = new_df["Objective"].apply(lambda x: int(x.split()[1]))
                new_df = new_df.sort_values(by='Objective')
                new_df["Objective"] = new_df["Objective"].apply(lambda x: "Objective " + str(x))
                new_df = delete_objectives(new_df,'Payment(In $)')
                granularity = []

            elif ('m01.19' in source_file) or ('type 7' in source_file):
                new_df.rename(columns = {'Tier' : 'Objective'}, inplace = True)
                new_df = new_df[['Objective', 'Percentage Input']]
                new_df = delete_objectives(new_df,'Percentage Input')
                new_df['Percentage Input'] = new_df['Percentage Input'].apply(bound_conditions)
                granularity = []

            elif ('m01.20' in source_file) or ('type 8' in source_file):
                new_df = new_df[['Tier', 'Lower Bound(In %)','Upper Bound(In %)', 'Commission rate(In %)']]

                new_df['Lower Bound(In %)'] = new_df['Lower Bound(In %)'].apply(bound_conditions)
                new_df['Upper Bound(In %)'] = new_df['Upper Bound(In %)'].apply(bound_conditions)
                new_df['Commission rate(In %)'] = new_df['Commission rate(In %)'].apply(lambda x: str(round(float(x) * 100, 2)) + "%")
                granularity = ['Lower Bound(In %)','Upper Bound(In %)']

            elif ('m01.21' in source_file) or ('type 9' in source_file):
                new_df = new_df[['Tier', 'Lower Bound(In %)','Upper Bound(In %)', 'Payment % of Target Incentive']]

                new_df['Lower Bound(In %)'] = new_df['Lower Bound(In %)'].apply(bound_conditions)
                new_df['Upper Bound(In %)'] = new_df['Upper Bound(In %)'].apply(bound_conditions)
                new_df['Payment % of Target Incentive'] = new_df['Payment % of Target Incentive'].apply(lambda x: str(round(x * 100, 2)) + "%")
                granularity = ['Lower Bound(In %)','Upper Bound(In %)']
            else:
                print('Please enter the file name correctly.')

            new_df = crop_df(new_df, granularity) 
            path = get_todays_date() + '_' + source_file[:-4]
            os.makedirs(path, exist_ok = True)
            path = path + '\\' + field.replace(" ", "").replace("|", "_").replace(".", ",") + '.png'

            if len(new_df) != 0: 

                dfi.export(new_df.style.hide(axis='index'),path,table_conversion='matplotlib')

def main():
    start = time.time()

    create_rate_table_images()
    end = time.time()
    print("Execution Time : ",int(end-start) , "s")