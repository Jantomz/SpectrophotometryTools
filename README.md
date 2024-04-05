# Spectrophotometry Data Processing Tools

This repository contains various tools in different formats for visualizing, manipulating, and creating data related to spectrophotometry.

## Table of Contents

- [Introduction](#introduction)
- [Data Point Naming Scheme](#data-point-naming-scheme)
- [Mineral Indexes](#mineral-indexes)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

This repository is created for the Ottawa Regional Science Fair and aims to provide a collection of tools that can be used for processing spectrophotometry data. The tools included in this repository are designed to help visualize, manipulate, and create data in various formats.

## Data Point Naming Scheme

The data point naming scheme used in this repository follows the format: `rock_[magnification]_[version]_[sample-num]`. This naming convention helps to organize and identify different data points based on their magnification, version, and sample number.

magnification: a multiplier value to increase variation in data
version: a version of the dataset that is randomly varied
sample-num: the index of the data within the dataset

## Mineral Indexes

The minerals are each given an index as their classification, this is based off alphabetical order:

0 - Biotite

1 - Calcite

2 - Fluorite

3 - Galena

4 - Hematite

5 - Quartz

## Tools

To use the tools in this repository, follow these steps:

1. Clone the repository to your local machine.
2. Navigate to the specific tool you want to use.
3. Follow the specific instructions of each tool:

- [Model Tester](#model-tester)
  - Tool to test tensorflow keras spectrophotometry machine learning models with mineral spectral signatures
- [Tensorflow Model Creator](#tensorflow-model-creator)
  - Tool to create tensorflow keras spectrophotometry machine learning models with mineral spectral signatures
- [HTML Graphers](#html-graphers)
  - Tool to visualize mass spectral signature data from csv files to compare different minerals

## Model Tester

To test a specific model, open up the jupyter notebook in your local environment and select the proper model to be loaded by replacing `your_keras_model` with the file path to your model.

```
model = load_model("your_keras_model")
```

Then replace `your_data` with the file path to the file containing your data in csv format.

```
dataObj = manipulator("your_data")
```

Then just run all blocks of code in order and you can test the accuracy of your model!

## Tensorflow Model Creator

To create a tensorflow model just follow the lines of code in the tool, replacing `your_data` with the file path to the file containing your data in csv format.

```
dataObj = manipulator("your_data")
```

Then just run all blocks of code in order and you can create a tensorflow model to identify and classify mineral spectral signatures!

## HTML Graphers

Open the Server file in your terminal and type `npm start` to open the server on your local machine.

Then, open the HTML file that you would like to use and simply input your csv file to create and download the respective graphs!

## Contributing

Contributions to this repository are welcome. If you have any ideas, suggestions, or improvements, please feel free to open an issue or submit a pull request.
