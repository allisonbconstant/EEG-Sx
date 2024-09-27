import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv('/Users/allisonbeers/Desktop/EEG-Sx/new/merged_data_all.csv')

# Convert time_from_baseline from days to years and round to the nearest 0.25 years
data['time_from_baseline_years'] = np.round(data['time_from_baseline'] / 365.0 * 4) / 4

# Identify baseline (time_from_baseline = 0) data for group assignment
baseline_data = data[data['time_from_baseline_years'] == 0].copy()

# Assign PHQ-9 group based on baseline scores only
def assign_phq_group(score):
    if 0 <= score <= 4:
        return 'none'
    elif 5 <= score <= 9:
        return 'mild'
    elif 10 <= score <= 14:
        return 'moderate'
    else:
        return 'severe'

# Assign QIDS group based on baseline scores only
def assign_qids_group(score):
    if 0 <= score <= 5:
        return 'none'
    elif 6 <= score <= 10:
        return 'mild'
    elif 11 <= score <= 15:
        return 'moderate'
    else:
        return 'severe'

# Apply the group assignment based strictly on baseline data
baseline_data['phq_group'] = baseline_data['phq_score_equat'].apply(assign_phq_group)
baseline_data['qids_group'] = baseline_data['qids_score_equat'].apply(assign_qids_group)

# Merge the group labels back to the full dataset
data = pd.merge(data, baseline_data[['Subject', 'phq_group', 'qids_group']], on='Subject', how='left')

# Save separate CSV files for each PHQ-9 group and print number of unique subjects in each group
phq_groups = ['none', 'mild', 'moderate', 'severe']
for group in phq_groups:
    group_data = data[data['phq_group'] == group]
    unique_subjects = group_data['Subject'].nunique()  # Count unique subjects
    print(f'PHQ-9 group {group}: {unique_subjects} unique subjects')
    group_data.to_csv(f'/Users/allisonbeers/Desktop/EEG-Sx/new/clinical_only/PHQ9_group_{group}.csv', index=False)
    print(f'Saved PHQ-9 group {group} to CSV.')

# Save separate CSV files for each QIDS group and print number of unique subjects in each group
qids_groups = ['none', 'mild', 'moderate', 'severe']
for group in qids_groups:
    group_data = data[data['qids_group'] == group]
    unique_subjects = group_data['Subject'].nunique()  # Count unique subjects
    print(f'QIDS group {group}: {unique_subjects} unique subjects')
    group_data.to_csv(f'/Users/allisonbeers/Desktop/EEG-Sx/new/clinical_only/QIDS_group_{group}.csv', index=False)
    print(f'Saved QIDS group {group} to CSV.')
