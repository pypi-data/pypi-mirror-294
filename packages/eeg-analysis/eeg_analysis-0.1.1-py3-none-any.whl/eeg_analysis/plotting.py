import seaborn as sns
import matplotlib.pyplot as plt
import os
import pandas as pd

# List of parameters to analyze
parameters = ['IAPF', 'Baseline Fatigue score', 'Fatigue score', 'Baseline Alpha Gravity', 'Alpha Gravity', 
                'Baseline Concentration index', 'Concentration index', 'Baseline Relaxation index', 
                'Relaxation index', 'Theta peak frequency', 'Alpha peak frequency', 'Beta peak frequency', 
                'Chill', 'Stress', 'Focus', 'Anger', 'Self-control']

def plot_median_across_bands(data, output_dir='plots'):
    """
    Plot median band power across different states for each band and save the plots.

    Parameters:
    - data: DataFrame containing the cleaned data.
    - output_dir: Directory where the plots will be saved.
    """
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Reshape the DataFrame for seaborn
    melted = data.melt(id_vars=['Subject', 'Band'], value_vars=['Before', 'During', 'After'], 
                       var_name='State', value_name='Power')
    
    # Calculate median power for each subject, band, and state
    summary = melted.groupby(['Subject', 'Band', 'State']).agg({'Power': 'median'}).reset_index()
    
    # Get the unique bands
    bands = summary['Band'].unique()
    
    for band in bands:
        # Filter data for the current band
        band_data = summary[summary['Band'] == band]
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        sns.lineplot(x='State', y='Power', hue='Subject', style='Subject', data=band_data, markers=True)
        plt.title(f'Median Power by State for {band} Band')
        plt.xticks(rotation=45)
        plt.legend(title='Subject')
        
        # Save the plot
        plot_filename = os.path.join(output_dir, f'{band}_band_median_power.png')
        plt.savefig(plot_filename)
        plt.close()

# Function to calculate the median and count for each parameter
def calculate_medians_and_counts(df, label):
    medians = {param: df[param].median() for param in parameters}
    counts = {param: df[param].count() for param in parameters}
    medians['State'] = label
    counts['State'] = label
    return medians, counts

def plot_medians_and_counts(before_path, during_path, after_path, output_dir='plots'):
    """
    Function to load datasets, calculate medians and counts, and plot the results.

    Parameters:
    - before_path: str, path to the 'before.csv' dataset.
    - during_path: str, path to the 'during.csv' dataset.
    - after_path: str, path to the 'after.csv' dataset.
    - output_dir: str, path to the directory where plots will be saved.
    """

    # Load the datasets
    before = pd.read_csv(before_path)
    during = pd.read_csv(during_path)
    after = pd.read_csv(after_path)

    # Calculate medians and counts for each state
    medians_before, counts_before = calculate_medians_and_counts(before, 'Before')
    medians_during, counts_during = calculate_medians_and_counts(during, 'During')
    medians_after, counts_after = calculate_medians_and_counts(after, 'After')

    # Combine medians and counts into separate DataFrames
    medians_df = pd.DataFrame([medians_before, medians_during, medians_after])
    counts_df = pd.DataFrame([counts_before, counts_during, counts_after])

    # Melt the DataFrames for Seaborn compatibility
    medians_melted = pd.melt(medians_df, id_vars='State', value_vars=parameters, 
                             var_name='Parameter', value_name='Median Value')

    counts_melted = pd.melt(counts_df, id_vars='State', value_vars=parameters, 
                            var_name='Parameter', value_name='Count')

    # Merge the melted DataFrames to include counts with medians
    combined_df = pd.merge(medians_melted, counts_melted, on=['State', 'Parameter'])

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Plotting using Seaborn
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='Parameter', y='Median Value', hue='State', data=medians_melted, marker='o')

    # Customize the plot
    plt.xticks(rotation=45, ha="right")
    plt.title('Median of Parameters Before, During, and After')
    plt.tight_layout()

    # Save the plot to the output directory
    plot_path = os.path.join(output_dir, 'hkm_median_plot.png')
    plt.savefig(plot_path)
    plt.close()

    print(f"Plot saved to: {plot_path}")

    # Print the DataFrame with observation counts
    print("Observation counts used for median calculations:")
    print(counts_df)
