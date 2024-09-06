# Drift Package

## Overview

The RefractMLMonitor Package is designed to monitor and detect data drift in machine learning models. It helps in identifying changes in the input data distribution over time, which can affect the performance of the model.

## Features

- **Feature Drift Detection**: Detects changes in the input feature's data distribution.
- **Label Drift Detection**: Identifies changes in the distribution of the labels.
- **Prediction Drift Detection**: Monitors changes in the distribution of the model predictions.
- **Performance Drift Detection**: Tracks changes in the performance metrics of the model.
- **Alert Generation**: Generates alerts when significant drift is detected.
- **Report Generation**: Provides detailed reports on the detected drift.
- **Integration with Snowflake**: Stores drift data and alerts in Snowflake tables.

## Installation

To install the Drift Package, use the following command:

```bash
pip install RefractMLMonitor
```