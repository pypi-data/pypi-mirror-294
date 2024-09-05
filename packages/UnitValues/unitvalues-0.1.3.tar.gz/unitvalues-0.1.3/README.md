# UnitValues Package
## Introduction
The UnitValue package is designed to allow easy manipulation and conversion of numerical values associated with units. It currently supports both Imperial and Metric systems and includes commonly used units, with the flexibility to add more units as needed. It works with numpy as well, empowering you to use units in your numpy arrays and funciton calls.

This package is ideal for applications that require precise unit conversions and tracking of units alongside numerical values.

## Installation
To install the UnitValue package, you can use the following command:

```bash
pip install UnitValues
```
## Features

- Create `UnitValue` objects with specified units and values.
- Convert between different units within the same dimension (e.g., meters to kilometers).
- Support for different measurement systems (e.g., metric and imperial).
- Arithmetic operations with unit handling (addition, subtraction, multiplication, division).
- Error handling for unsupported units and invalid operations.

## Class and Methods Overview

`UnitValue`
Attributes:
- value (float): The numerical value.
- unit (str): The unit associated with the value.
- system (str): The measurement system (e.g., "METRIC", "IMPERIAL").
- dimension (str): The dimension of the unit (e.g., "LENGTH", "MASS").
Methods:
- __init__(self, value: float, unit: str): Initializes a UnitValue object.
- create_unit(cls, unit: str, value: float=0) -> 'UnitValue': Creates unit object.
- to(self, target_unit: str) -> 'UnitValue': Converts the current value to the specified unit.
- convert_base_metric(self) -> 'UnitValue': Convert the current value to it's base SI/Metric unit.
- add_custom_unitadd_custom_unit(cls, system: str, dimension:str, unit:str, conversion_factor: float) -> None: Allows you to add your own units to your instance of the package.
- available_units(cls, system: str="", dimension: str="") -> str: Get available units for the specified measurement system and dimension.
- unit_from_string(cls, unit_str:str) -> 'UnitValue': Create a UnitValue object from a formatted string (e.g., '10 m').
- from_dict(cls, data: dict) -> 'UnitValue': Create a UnitValue object from a dictionary.
- to_dict(self) -> dict: Convert the UnitValue object to a dictionary.
Properties:
 - get_unit: returns unit string.
 - get_dimension: return dimension string.
 - get_system: returns system string. 

## Supported Units and Conversions

The package supports a wide range of units, including but not limited to:

### METRIC:
    DISTANCE: ['m', 'km', 'cm', 'mm']
    PRESSURE: ['kg/ms^2', 'MPa', 'bar', 'kPa', 'hPa', 'Pa']
    MASS: ['kg', 'tonne', 'g']
    VELOCITY: ['m/s', 'km/s', 'km/h', 'cm/s', 'mm/s']
    DENSITY: ['kg/m^3', 't/m^3', 'g/m^3']
    VOLUME: ['m^3', 'L', 'cm^3', 'mL', 'mm^3']
    AREA: ['m^2', 'km^2', 'cm^2', 'mm^2']
    TEMPERATURE: ['K', 'c']
    MASS FLOW RATE: ['kg/s', 't/s', 'kg/min', 'g/s']
    ENERGY: ['kgm^2/s^2', 'MJ', 'kJ', 'Nm', 'J', 'eV']
    TIME: ['s', 'h', 'min', 'ms']
    MOMENTUM: ['kgm/s', 'Ns']
    FREQUENCY: ['/s', 'Hz']
    ACCELERATION: ['m/s^2', 'g']
    FORCE: ['kgm/s^2', 'N', 'gcm/s^2']
    ENERGY PER UNIT MASS: ['m^2/s^2']
    MASS PER LENGTH: ['kg/m', 'kg/cm', 'g/cm']
    MASS PER AREA: ['kg/m^2', 'g/cm^2']
    VOLUMETRIC FLOW RATE: ['m^3/s', 'cm^3/s']
    DYNAMIC VISCOCITY: ['kg/ms', 'g/cms']
    KINEMATIC VISCOCITY: ['m^2/s', 'cm^2/s']
    MASS FLUX: ['kg/m^2s']

### IMPERIAL:
    DISTANCE: ['in', 'mi', 'yd', 'ft']
    PRESSURE: ['psi', 'psf']
    MASS: ['lb', 'ton', 'slug', 'st', 'oz']
    VELOCITY: ['ft/s', 'mi/s', 'mph', 'in/s']
    DENSITY: ['lb/in^3', 'lb/ft^3', 'lb/yd^3']
    VOLUME: ['gal', 'yd^3', 'ft^3', 'in^3']
    AREA: ['in^2', 'mi^2', 'yd^2', 'ft^2']
    TEMPERATURE: ['f', 'R']
    MASS FLOW RATE: ['lb/s', 'ton/s', 'st/s', 'oz', 'lb/min']
    ENERGY: ['ftlb', 'kcal', 'cal']
    TIME: ['s', 'h', 'min', 'ms']
    MOMENTUM: ['slugft/s', 'lbft/s']
    FREQUENCY: ['rpm']
    ACCELERATION: ['ft/s^2']
    FORCE: ['lbf']
    ENERGY PER UNIT MASS: ['ft^2/s^2']
    MASS PER UNIT LENGTH: ['lb/ft', 'oz/in']
    MASS PER AREA: ['lb/ft^2']
    VOLUMETRIC FLOW RATE: ['ft^3/s', 'gal/s']
    DYNAMIC VISCOCITY: ['lb/fts']
    KINEMATIC VISCOCITY: ['ft^2/s']
    MASS FLUX: ['lb/ft^2s']


## Example Usage

### Creating a UnitValue

To create a `UnitValue` object, use the `create_dimensioned_quantity` function:

```python
from unitvalue import UnitValue

# Create a UnitValue object with a specified unit and value
distance = UnitValue.create_unit('meter', 100)
# Or initialize instance yourself
distance = UnitValue("METRIC", "DISTANCE", "m", 100)
# or initialize a unit from a string
distance = UnitValue.unit_from_string('100 m')
# or initialize from a dictionary
data = {'system':'METRIC', 'dimension':'DISTANCE', 'unit':'m', 'value':100}
distance = UnitValue.from_dict(data)
```

### Arithmetic Operations

`UnitValue` objects support arithmetic operations, maintaining unit consistency (The units do not even need to be in the same system or magnitude for you to perform arithmetic on them as the package will handle this). It is important to know all arithmetic operations return a value in the base metric units

### Converting Units

You can convert the unit of a `UnitValue` object using the `to` method:

```python
# Convert the distance to kilometers
distance.to(unit='kilometer')
print(distance)  # Output: 0.1 kilometer

# Convert to base metric unit (Useful for Scinetifc calculations)
distance.convert_base_metric()
print(distance)
```

### Basic Example
```python
from unitvalue import UnitValue

length1 = UnitValue.create_unit('meter', 50)
length2 = UnitValue.create_unit('meter', 30)

# Addition
total_length = length1 + length2
print(total_length)  # Output: 80 m

# Subtraction
remaining_length = length1 - length2
print(remaining_length)  # Output: 20 m

# Multiplication by a scalar
double_length = length1 * 2
print(double_length)  # Output: 100 m

# Division by a scalar
half_length = length1 / 2
print(half_length)  # Output: 25 m

# Multiplication between UnitValue Objects
area = lenght1 * length2
print(area) # Output: 150 m^2

# Divivsion between UnitValue Objects
l = area / length2
print(l) # Output: 50 m

# UnitValue object to the power
werid unit = lenght1**3.5
print(weird_unit)  # Output: 125000 m^3
```

## Contributing
Contributions are welcome! If you find any issues or have ideas for enhancements, feel free to open an issue or submit a pull request on GitHub.
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Open a Pull Request.

## License
This package is distributed under the MIT License. See LICENSE for more information.
