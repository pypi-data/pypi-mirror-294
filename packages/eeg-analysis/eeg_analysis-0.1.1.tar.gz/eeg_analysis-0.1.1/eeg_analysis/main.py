from .data_processing import load_data, clean_data
from .plotting import plot_median_across_bands, plot_medians_and_counts
import pkg_resources

def load_clean_and_plot_band_data(filepath: str = None):
    if filepath is None:
        # Use default path to the data file included in the package
        filepath = pkg_resources.resource_filename('eeg_analysis', 'data/id_iskcon_data.csv')
    
    data = load_data(filepath)
    cleaned_data = clean_data(data)
    plot_median_across_bands(cleaned_data)

def plot_hkm_medians(before_data_path: str = None, during_data_path: str = None, after_data_path: str = None):
    # Use default path to the data file included in the package
    if before_data_path is None:
        before_data_path = pkg_resources.resource_filename('eeg_analysis', 'data/before.csv')
    if during_data_path is None:
        during_data_path = pkg_resources.resource_filename('eeg_analysis', 'data/during.csv')
    if after_data_path is None:
        after_data_path = pkg_resources.resource_filename('eeg_analysis', 'data/after.csv')
    
    plot_medians_and_counts(before_data_path, during_data_path, after_data_path)