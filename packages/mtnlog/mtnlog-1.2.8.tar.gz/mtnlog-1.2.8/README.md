# mtnlog - A simple multinode performance logger for Python

## Introduction

mtnlog is a simple multinode performance logger for Python. It is designed to be used in a similar way to Python's built-in logging module, but with a focus on performance logging. It provides a simple API for logging performance data, including start and end times, and allows for easy integration with other logging systems.

## Installation

You can install mtnlog using pip:

```bash
pip install mtnlog
```

## Usage

To use mtnlog, you have two features: `JSONLogger` and `PerformanceLogger` and `PerformancePlotter`.

### JSONLogger

The `JSONLogger` class is a simple logger that writes performance data to a JSON file. You can create a new `JSONLogger` instance by passing a file path to the constructor:

```python
from mtnlog import JSONLogger

logger = JSONLogger(log_dir='logs') # logs is the directory where the log file will be saved
```

You can then use the `log` method to log performance data:

```python
logger.log('<your_dict>', filename='log') # your_dict is a dictionary with the data you want to log / filename is the name of the file
```

`your_dict` is a dictionary with the data you want to log.
`filename` is the name of the file where the data will be saved

### PerformanceLogger

The `PerformanceLogger` class is a logger for system performance data. It logs the the time taken to execute the block, as well as the CPU, memory, and GPU usage. You can create a new `PerformanceLogger` instance by passing a file path to the constructor:

```python
from mtnlog import PerformanceLogger

collector = PerformanceLogger(log_dir="<your_log_dir>", log_node="<current_node>")
```

`your_log_dir` is the directory where the log file will be saved.
`current_node` is the number of the node you are logging.

You can then use the `change_tag` method to change the tag of the log:

```python
collector.change_tag("<new_tag>")
```

`new_tag` is the new tag you want to use.

To stop logging, you can use the `stop` method:

```python
collector.stop()
```

### PerformancePlotter

The `PerformancePlotter` class is a plotter for system performance data. It plots the time taken to execute the block, as well as the CPU, memory, GPU, and network usage. You can create a new `PerformancePlotter` instance by passing a file path to the constructor:

```python
from mtnlog import PerformancePlotter

plotter = PerformancePlotter(base_dir="<your_base_dir>", log_node="<current_node>")

```

`your_base_dir` is the base directory where the log file will be saved.
`current_node` is the number of the node you are logging.

You can then use the `plot` method to plot the data:

```python

plotter.plot()

```

## Example

Here is an example of how to use mtnlog:

```python
from mtnlog import JSONLogger, PerformanceLogger, PerformancePlotter

# Create a JSONLogger instance

logger = JSONLogger(log_dir='logs')

# Log some data

logger.log({'message': 'Hello, world!'}, filename='log')

# Create a PerformanceLogger instance

collector = PerformanceLogger(log_dir='logs', log_node="0")

# Change the tag

collector.change_tag('new_tag')

# Stop logging

collector.stop()

# Create a PerformancePlotter instance

plotter = PerformancePlotter(base_dir='logs', log_node="0")

# Plot the data

plotter.plot()

```
