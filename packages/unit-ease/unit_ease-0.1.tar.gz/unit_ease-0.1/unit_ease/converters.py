# unit_ease/converters.py

# Length Conversions
def meters_to_feet(meters):
    return meters * 3.28084

def feet_to_meters(feet):
    return feet / 3.28084

def kilometers_to_miles(kilometers):
    return kilometers * 0.621371

def miles_to_kilometers(miles):
    return miles / 0.621371

def centimeters_to_inches(centimeters):
    return centimeters * 0.393701

def inches_to_centimeters(inches):
    return inches / 0.393701

def millimeters_to_inches(millimeters):
    return millimeters * 0.0393701

def inches_to_millimeters(inches):
    return inches / 0.0393701

# Temperature Conversions
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Weight Conversions
def kilograms_to_pounds(kilograms):
    return kilograms * 2.20462

def pounds_to_kilograms(pounds):
    return pounds / 2.20462

def grams_to_ounces(grams):
    return grams * 0.035274

def ounces_to_grams(ounces):
    return ounces / 0.035274

def stones_to_kilograms(stones):
    return stones * 6.35029

def kilograms_to_stones(kilograms):
    return kilograms / 6.35029

# Volume Conversions
def liters_to_gallons(liters):
    return liters * 0.264172

def gallons_to_liters(gallons):
    return gallons / 0.264172

def milliliters_to_ounces(milliliters):
    return milliliters * 0.033814

def ounces_to_milliliters(ounces):
    return ounces / 0.033814

def cups_to_liters(cups):
    return cups * 0.236588

def liters_to_cups(liters):
    return liters / 0.236588
