from typing import List
from promptflow import tool, log_metric
import numpy as np

@tool
def aggregate_variants_results(results: List[dict], metrics: List[str]):
    # Initialize an empty dictionary to store the aggregated results
    aggregate_results = {}

    # Loop through each result in the results list
    for result in results:
        # Loop through each key-value pair in the result dictionary
        for name, value in result.items():
            # If the name is in the first element of the metrics list
            if name in metrics[0]:
                # If the name is not already a key in the aggregate_results dictionary, add it
                if name not in aggregate_results.keys():
                    aggregate_results[name] = []
                # Try to convert the value to a float
                try:
                    float_val = float(value)
                # If the conversion fails, assign NaN to float_val
                except Exception:
                    float_val = np.nan
                # Append the float value to the list of values for the current name in the aggregate_results dictionary
                aggregate_results[name].append(float_val)

    # Loop through each key-value pair in the aggregate_results dictionary
    for name, value in aggregate_results.items():
        # If the name is in the first element of the metrics list
        if name in metrics[0]:
            # Calculate the mean of the values, ignoring NaNs, and assign it to the current name in the aggregate_results dictionary
            aggregate_results[name] = np.nanmean(value)
            # Round the mean value to 2 decimal places
            aggregate_results[name] = round(aggregate_results[name], 2)
            # Log the metric with its name and value
            log_metric(name, aggregate_results[name])

    # Return the aggregate_results dictionary
    return aggregate_results