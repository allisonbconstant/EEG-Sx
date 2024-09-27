import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Paths to your saved PHQ-9 and QIDS group data
base_path = '/Users/allisonbeers/Desktop/EEG-Sx/new/clinical_only/'

# Groups to process
groups = ['none', 'mild', 'moderate', 'severe']

# Set the style of the plots
sns.set(style="whitegrid")

# Function to plot clinical trajectories for PHQ-9 and QIDS in subplots
def plot_clinical_trajectories_combined(var_prefix, var, y_label, y_max, file_name):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Trajectory of {y_label} by Group')

    for ax, group in zip(axes.flatten(), groups):
        # Load the data for the current group
        group_data = pd.read_csv(f'{base_path}{var_prefix}_group_{group}.csv')
        
        # Group the data by time_from_baseline_years, calculate mean, SEM, and count (n)
        grouped_data = group_data.groupby('time_from_baseline_years').agg(
            mean=(var, 'mean'),
            sem=(var, 'sem'),
            n=(var, 'count')  # Count the number of subjects at each time point
        ).reset_index()

        # Plot the mean values and error bars (SEM)
        sns.lineplot(x='time_from_baseline_years', y='mean', data=grouped_data, marker='o', ax=ax)
        ax.errorbar(grouped_data['time_from_baseline_years'], grouped_data['mean'], yerr=grouped_data['sem'], fmt='o')
        
        # Annotate with the number of subjects (n) at each time point
        for j, row in grouped_data.iterrows():
            ax.annotate(f'n={int(row["n"])}', (row['time_from_baseline_years'], row['mean']),
                         textcoords="offset points", xytext=(0, 5), ha='center', fontsize=9, color='black')

        # Set titles, labels, and limits
        ax.set_title(f"{group.capitalize()} Group")
        ax.set_xlabel('Time from Baseline (years)')
        ax.set_ylabel(y_label)
        ax.set_ylim(0, y_max)
        ax.set_xlim(left=0)
        ax.grid(True)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)

    # Save the combined figure
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f'{base_path}{file_name}')
    plt.close()

# Plot PHQ-9 trajectories with four subplots (one for each group)
plot_clinical_trajectories_combined(
    var_prefix='PHQ9',
    var='phq_score_equat',
    y_label='Average PHQ-9 Score',
    y_max=27,
    file_name='clinical_trajectories_PHQ9_combined.png'
)

# Plot QIDS trajectories with four subplots (one for each group)
plot_clinical_trajectories_combined(
    var_prefix='QIDS',
    var='qids_score_equat',
    y_label='Average QIDS Score',
    y_max=27,
    file_name='clinical_trajectories_QIDS_combined.png'
)

print("Saved combined clinical trajectories for PHQ-9 and QIDS.")



# # Function to plot EEG trajectories with error bars
# def plot_eeg_trajectories(data):
#     eeg_bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
#     fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(18, 30))

#     for i, band in enumerate(eeg_bands):
#         eeg_columns = [col for col in data.columns if col.startswith(f'Z_{band}')]
#         if eeg_columns:  # Only proceed if there are columns for the band
#             for col in eeg_columns:
#                 grouped_data = data.groupby('time_from_baseline_years')[col].agg(['mean', 'sem']).reset_index()
#                 sns.lineplot(x='time_from_baseline_years', y='mean', data=grouped_data, marker='o', ax=axes[i], label=col)
#                 axes[i].errorbar(grouped_data['time_from_baseline_years'], grouped_data['mean'], yerr=grouped_data['sem'], fmt='o')
#             axes[i].set_title(f'Trajectory of {band.capitalize()} Band')
#             axes[i].set_xlabel('Time from Baseline (years)')
#             axes[i].set_ylabel('Z-score')
#             axes[i].set_xlim(left=0)
#             axes[i].set_ylim(-0.5, 0.5)  # Set y-axis limits to -0.5 to 0.5 for EEG Z-scores
#             axes[i].grid(True)
#             plt.setp(axes[i].get_xticklabels(), rotation=45, ha='right', fontsize=10)
#             axes[i].legend(loc='upper right', fontsize='small')
#         else:
#             axes[i].set_visible(False)  # Hide the subplot if no columns are available for the band

#     plt.tight_layout()
#     plt.savefig('/Users/allisonbeers/Desktop/EEG-Sx/lme_0917/theta/theta_eeg_trajectories_y_train.png')
#     plt.close()

# Plot and save the images
#plot_eeg_trajectories(data)

print("Clinical and EEG trajectories with error bars have been saved as separate images.")
