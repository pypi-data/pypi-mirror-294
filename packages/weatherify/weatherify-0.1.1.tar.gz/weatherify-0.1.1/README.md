# Weatherify

A simple command-line weather forecasting tool.

## Installation

```
pip install weatherify
```

## Usage

```
weatherify [location]
```

If no location is provided, it will attempt to use your current location based on your IP address.

Example:
```
weatherify New York
weatherify "Los Angeles, CA"
weatherify
```

## Features

- Current weather conditions with ASCII art representation
- 3-day weather forecast
- Automatic geolocation if no location is specified