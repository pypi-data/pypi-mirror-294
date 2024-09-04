# suraj_datalab

[![PyPI version](https://img.shields.io/pypi/v/suraj_datalab.svg)](https://pypi.org/project/suraj_datalab/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/surajwate/DataLab/actions/workflows/publish.yml/badge.svg)](https://github.com/surajwate/DataLab/actions)

`suraj_datalab` is a Python package designed to streamline the process of analyzing and visualizing both categorical and numerical data. It also includes utilities for data cleaning and preparing datasets for machine learning models, like creating K-Folds for cross-validation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Usage](#usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Features

- **Categorical Analysis**: Effortlessly analyze and visualize categorical data in relation to target variables.
- **Numerical Analysis**: Detect, analyze, and visualize outliers in numerical data.
- **Data Cleaning**: Automatically handle rare categories in your datasets.
- **Cross-Validation Preparation**: Create K-Folds for both classification and regression tasks, including stratified K-Folds.
- **Visualization**: Built-in support for generating insightful plots with minimal code.
- **Extensible**: Designed with flexibility in mind, allowing easy extension and integration with other data processing workflows.

## Installation

### Requirements

- Python 3.12 or higher
- [pandas](https://pandas.pydata.org/)
- [seaborn](https://seaborn.pydata.org/)
- [matplotlib](https://matplotlib.org/)

### Install via pip

```bash
pip install suraj_datalab
```

## Quickstart

Here’s how you can quickly get started with `suraj_datalab`:

```python
import pandas as pd
from suraj_datalab.analysis import analyze_categorical_feature, analyze_numerical_feature

# Sample DataFrame
data = {'Feature': ['A', 'B', 'A', 'B'], 'Transported': [True, False, True, False]}
df = pd.DataFrame(data)

# Analyze categorical feature
result = analyze_categorical_feature(df, 'Feature', 'Transported')
print(result)
```

## Usage

For detailed usage instructions, please refer to the [Usage Guide](https://surajwate.com/DataLab/usage/).

## Examples

Check out the [Examples](https://surajwate.com/DataLab/examples/) section for practical examples of how to use the functions and classes provided by `suraj_datalab`.

## API Reference

For a detailed reference of all available functions and classes, see the [API Reference](https://surajwate.com/DataLab/api_reference/).

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to all contributors who have helped with this project.

## Contact

For any questions or suggestions, please contact [Suraj Wate](mailto:surajwate@gmail.com).
