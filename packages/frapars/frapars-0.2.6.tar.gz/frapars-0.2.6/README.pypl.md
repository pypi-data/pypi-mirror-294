# FRAPARS (France-parse-addresses)

Simple script that permits to parse addresses in France format.

## Install

To install the package from pypl use the command

`pip install frapars`

or with Poetry:
`poetry add frapars`


## Example of usage
The package can be used to process multiple or single addresses. Here few example.

Use this to import the library:
```
from frapars.functions.addresses import parse_from_address, parse_all_parallel
```

Then, for single usage:
```python
address = "3 Rue Industrie (De l')"
result = parse_from_address(address)
print(result)
```
Obtaining
```terminal
[{'raw': 'Jaures (128, Avenue Jean)', 'urba_names': ['avenue'], 'city': [], 'address_num': ['128'], 'department': [], 'street_name': ['jaures', 'jean'], 'formatted': '128 Avenue Jaures Jean'}, {'raw': 'Ferdinand Buisson (42, Rue)', 'urba_names': ['rue'], 'city': ['buisson'], 'address_num': ['42'], 'department': [], 'street_name': ['ferdinand'], 'formatted': '42 Rue Ferdinand Buisson'}]
```

Use the fields `.raw` and `.formatted` and `.details` to retrieve the specifica value that you need.

For List of addresses:
```python
adresses_list = ["Hommelet (31, rue de l'), 59512, ROUBAIX", ' Allée Combes (Des)', " 3 Rue Industrie (De l')", ' Route Départementale 49', ' 02210 Rozet Saint Albin', ' Pont Romain, 12, Rue Du', ' Chaussée (11, Rue de la )', ' Jaures (128, Avenue Jean) et Ferdinand Buisson (42, Rue)', ' Jacquart (50, 52 Rue) ', ' Lecat (50, Rue)', ' Deguise Olivier (3, Rue)   Rd360', " Lieu Dit 'L'Italie"]

parsed_addresses = parse_all_parallel(adresses_list)
for entry in result:
    print(f"Raw: {entry.raw} --> Formatted: {entry.formatted}")
```

This will print something like:
```terminal
Raw: Hommelet (31, rue de l'), 59512, ROUBAIX --> Formatted: 31 Rue De L Hommelet Roubaix 59512
Raw:  Allée Combes (Des) --> Formatted: Allée Des Combes
Raw:  3 Rue Industrie (De l') --> Formatted: 3 Rue De L Industrie
Raw:  Route Départementale 49 --> Formatted: 49 Route Départementale
Raw:  02210 Rozet Saint Albin --> Formatted: Rozet Saint Albin 02210
Raw:  Pont Romain, 12, Rue Du --> Formatted: 12 Rue Du Pont Romain
Raw:  Chaussée (11, Rue de la ) --> Formatted: 11 Rue De La Chaussée
Raw:  Jaures (128, Avenue Jean) et Ferdinand Buisson (42, Rue) --> Formatted: 128 Avenue Jaures Jean et 42 Rue Ferdinand Buisson
Raw:  Jacquart (50, 52 Rue)  --> Formatted: 50-52 Rue Jacquart
Raw:  Lecat (50, Rue) --> Formatted: 50 Rue Lecat
Raw:  Deguise Olivier (3, Rue)   Rd360 --> Formatted: 3 Rue Deguise Olivier
Raw:  Lieu Dit 'L'Italie --> Formatted: Lieu Dit L Italie
```

In case you want a specific format template there is a Format() object to do so.
```python
from frapars.helper.formatter import Formatter, AddressFields

address = "Jaures (128, Avenue Jean) 10141, France, FR"
result = parse_from_address(address, Formatter(
    template=f"{AddressFields.ADDRESS_NUM.value} - {AddressFields.CITY.value} - {AddressFields.POSTCODE.value}"
))
print(result.formatted)
print('/n')
print(result)
```

Returning:
```shell
42 - Ferdinand - Buisson

[{'raw': 'Jaures (128, Avenue Jean)', 'urba_names': ['avenue'], 'city': [], 'address_num': ['128'], 'department': [], 'street_name': ['jaures', 'jean'], 'formatted': '128 - Jaures Jean -'}, {'raw': 'Ferdinand Buisson (42, Rue)', 'urba_names': ['rue'], 'city': ['buisson'], 'address_num': ['42'], 'department': [], 'street_name': ['ferdinand'], 'formatted': '42 - Ferdinand - Buisson'}]
```


## To-Do List

- [ ] Write junit tests
- [ ] More example
- [ ] Update insee file - create a task that do it 

Enjoy and Rate!!
