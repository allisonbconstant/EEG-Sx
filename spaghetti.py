import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Paths to your saved PHQ-9 and QIDS group data
base_path = '/Users/allisonbeers/Desktop/EEG-Sx/new/clinical_only/'

# Groups to process
groups = ['none', 'mild', 'moderate', 'severe']

# Set the number of random subjects to display
n_random_subjects = 10

# Plot PHQ-9 trajectories by group
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('PHQ-9 Score Trajectories by Group')

for ax, group in zip(axs.flatten(), groups):
    # Load the data for the current group
    group_data = pd.read_csv(f'{base_path}PHQ9_group_{group}.csv')
    
    # Count the number of unique subjects
    unique_subjects = group_data['Subject'].nunique()
    print(f'PHQ-9 group {group}: {unique_subjects} unique subjects')

    # Randomly select up to 10 subjects for each group
    selected_subjects = group_data['Subject'].drop_duplicates().sample(n=min(n_random_subjects, unique_subjects), random_state=42)

    # Plot each selected subject's data for the current group
    for subject in selected_subjects:
        subject_data = group_data[group_data['Subject'] == subject]
        ax.plot(subject_data['time_from_baseline_years'], subject_data['phq_score_equat'], alpha=0.7)
        ax.scatter(subject_data['time_from_baseline_years'], subject_data['phq_score_equat'], alpha=0.7)
    
    # Set title and labels, and annotate with the number of unique subjects
    ax.set_title(f'PHQ-9: {group.capitalize()} Group (n={unique_subjects})')
    ax.set_xlabel('Time from Baseline (years)')
    ax.set_ylim(0, 27)
    ax.set_ylabel('PHQ-9 Score')

# Save the PHQ-9 plots to a file
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'{base_path}PHQ9_trajectories_limited.png')
plt.close()

# Plot QIDS trajectories by group
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('QIDS Score Trajectories by Group')

for ax, group in zip(axs.flatten(), groups):
    # Load the data for the current group
    group_data = pd.read_csv(f'{base_path}QIDS_group_{group}.csv')
    
    # Count the number of unique subjects
    unique_subjects = group_data['Subject'].nunique()
    print(f'QIDS group {group}: {unique_subjects} unique subjects')

    # Randomly select up to 10 subjects for each group
    selected_subjects = group_data['Subject'].drop_duplicates().sample(n=min(n_random_subjects, unique_subjects), random_state=42)

    # Plot each selected subject's data for the current group
    for subject in selected_subjects:
        subject_data = group_data[group_data['Subject'] == subject]
        ax.plot(subject_data['time_from_baseline_years'], subject_data['qids_score_equat'], alpha=0.7)
        ax.scatter(subject_data['time_from_baseline_years'], subject_data['qids_score_equat'], alpha=0.7)
    
    # Set title and labels, and annotate with the number of unique subjects
    ax.set_title(f'QIDS: {group.capitalize()} Group (n={unique_subjects})')
    ax.set_xlabel('Time from Baseline (years)')
    ax.set_ylim(0, 27)
    ax.set_ylabel('QIDS Score')

# Save the QIDS plots to a file
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f'{base_path}QIDS_trajectories_limited.png')
plt.close()
