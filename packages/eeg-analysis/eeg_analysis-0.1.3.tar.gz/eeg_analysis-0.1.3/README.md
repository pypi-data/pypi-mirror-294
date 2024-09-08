# EEG Analysis

This Library provides functions to process and plot EEG data, specifically focusing on the effects of different states (Before, During, After) on various EEG frequency bands.

## Installation

To install the library, use pip:

```bash
pip install eeg_analysis
```

## Usage

### Loading the Data

First, load the data from a CSV file. The CSV file should be structured with columns for subject, location, band, and power measurements for three states (Before, During, After).

```python
import pandas as pd
from eeg_analysis import load_data

# Load the data
data = load_data('path/to/your/data.csv')
```

### Cleaning the Data

Once the data is loaded, it needs to be cleaned and structured into a more usable format. The `clean_data` function organizes the data into a DataFrame with appropriate columns.

```python
from eeg_analysis import clean_data

# Clean and structure the data
df = clean_data(data)

# Optionally, save the cleaned data to a new CSV file
df.to_csv('cleaned_data.csv', index=False)
print(df.head())
```

### Performing Paired T-Tests

The library includes a function to perform paired t-tests between the different states for a specified frequency band. This can help determine if there are statistically significant differences in power between the states.

```python
from eeg_analysis import perform_ttests

# Perform t-tests for a specific band (e.g., 'Delta')
ttest_results_df = perform_ttests(df, 'Delta')

# Display the results
print(ttest_results_df)
```

### Plotting Median Power Across Bands

The library provides a function to plot the median power across different states for each frequency band. This can help visualize the changes in power for different subjects and states.

```python
from my_pypi_library import plot_median_across_bands

# Plot the median power across bands
plot_median_across_bands(df)
```

### Example Workflow

Here's a complete example that demonstrates the typical workflow using the library:

```python
import pandas as pd
from eeg_analysis import load_data, clean_data, perform_ttests, plot_median_across_bands

# Step 1: Load the data
data = load_data('path/to/your/data.csv')

# Step 2: Clean and structure the data
df = clean_data(data)

# Step 3: Perform t-tests for a specific band (e.g., 'Delta')
ttest_results_df = perform_ttests(df, 'Delta')
print(ttest_results_df)

# Step 4: Plot the median power across bands
plot_median_across_bands(df)
```

## API Reference

### `load_data(filepath: str) -> pd.DataFrame`

Load the data from a CSV file.

- **Parameters:**
  - `filepath` (str): The path to the CSV file containing the data.

- **Returns:**
  - `pd.DataFrame`: A DataFrame containing the loaded data.

### `clean_data(data: pd.DataFrame) -> pd.DataFrame`

Clean and structure the data into a usable format.

- **Parameters:**
  - `data` (pd.DataFrame): The raw data DataFrame.

- **Returns:**
  - `pd.DataFrame`: A cleaned and structured DataFrame.

### `perform_ttests(data: pd.DataFrame, band: str) -> pd.DataFrame`

Perform paired t-tests for a given frequency band.

- **Parameters:**
  - `data` (pd.DataFrame): The cleaned data DataFrame.
  - `band` (str): The frequency band to analyze (e.g., 'Delta').

- **Returns:**
  - `pd.DataFrame`: A DataFrame containing the t-test results for each subject and comparison.

### `plot_median_across_bands(data: pd.DataFrame)`

Plot the median power across different states for each frequency band.

- **Parameters:**
  - `data` (pd.DataFrame): The cleaned data DataFrame.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request on [GitHub](https://github.com/KarthikDani/BCI-Internship/tree/main/eeg_analysis).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.