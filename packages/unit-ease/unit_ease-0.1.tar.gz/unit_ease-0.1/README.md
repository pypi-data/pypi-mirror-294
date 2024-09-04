# Unit Converter

**Unit Converter** is a simple Python package that allows you to convert between various units of length, temperature, weight, and volume. This package provides straightforward functions to handle common unit conversions with ease.

## Features

- **Length Conversions**
  - Meters to Feet and Feet to Meters
  - Kilometers to Miles and Miles to Kilometers
  - Centimeters to Inches and Inches to Centimeters
  - Millimeters to Inches and Inches to Millimeters

- **Temperature Conversions**
  - Celsius to Fahrenheit and Fahrenheit to Celsius
  - Celsius to Kelvin and Kelvin to Celsius

- **Weight Conversions**
  - Kilograms to Pounds and Pounds to Kilograms
  - Grams to Ounces and Ounces to Grams
  - Stones to Kilograms and Kilograms to Stones

- **Volume Conversions**
  - Liters to Gallons and Gallons to Liters
  - Milliliters to Ounces and Ounces to Milliliters
  - Cups to Liters and Liters to Cups

## Installation

You can install the package using pip:

```bash
pip install unit_ease


>>> from unit_ease import (
    meters_to_feet, feet_to_meters,
    kilometers_to_miles, miles_to_kilometers,
    centimeters_to_inches, inches_to_centimeters,
    millimeters_to_inches, inches_to_millimeters,
    celsius_to_fahrenheit, fahrenheit_to_celsius,
    celsius_to_kelvin, kelvin_to_celsius,
    kilograms_to_pounds, pounds_to_kilograms,
    grams_to_ounces, ounces_to_grams,
    stones_to_kilograms, kilograms_to_stones,
    liters_to_gallons, gallons_to_liters,
    milliliters_to_ounces, ounces_to_milliliters,
    cups_to_liters, liters_to_cups
 )

# Length Conversions
>>> print(f"10 meters is {meters_to_feet(10)} feet.")
>>> print(f"5 miles is {miles_to_kilometers(5)} kilometers.")

# Temperature Conversions
>>> print(f"25 Celsius is {celsius_to_fahrenheit(25)} Fahrenheit.")
>>> print(f"300 Kelvin is {kelvin_to_celsius(300)} Celsius.")

# Weight Conversions
>>> print(f"70 kilograms is {kilograms_to_pounds(70)} pounds.")
>>> print(f"5 grams is {grams_to_ounces(5)} ounces.")

# Volume Conversions
>>> print(f"2 liters is {liters_to_gallons(2)} gallons.")
>>> print(f"100 milliliters is {milliliters_to_ounces(100)} ounces.")
