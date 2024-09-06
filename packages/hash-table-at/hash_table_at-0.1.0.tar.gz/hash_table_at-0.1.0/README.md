# hash-table
Custom hash table implementation that tries to replicate built-in Python dictionary.
The aim is to better understand its functioning and apply TDD framework to test core functionalities.

## Getting started
Missing

## Technical Documentation

### hash table key features

If you have any new feature, feel free to create a MR explaining this feature and I'll add that to the list

| requirement                                      | included |  
|--------------------------------------------------|---------|
| Create an empty hash table                       | ✅       |
| Insert a key-value pair                          | ✅       | 
| Accept arbitrary key type                        | ✅       |
| Get a key-value pair                             | ✅       |
| Delete a key-value pair                          | ✅       |
| Update the value associated with an existing key | ✅       |
| Hash table is iterable                           | ✅       |
| Possible to compare to hash tables               | ✅       |
| Possible to convert python dictionary            | ✅       |
| String representation                            | ✅       |
| Union operation                                  | ✅       |
| Miscellaneous (dict.clear() dict.update()        | ✅       |
| Managing Hash collision: linear probing          | ✅       |
| Managing Hash collision: separate chaining       |         |
| Dynamic resizing                                 | ✅       |
| Retain insertion order                           | ✅       |

### Features documentation
Missing

### Improve performances
At the moment the actual performances are not comparable to python built-in dictionary.
I've identified two key pain points that I want to improve in the search f a key:
1. __setitem__ uses string comparison, which is costly (O(N)). Want to move to hash comparison
2. __delitem__ has to remove key from a list in linear time  (O(N)). Want to move away from lists to improve search, without loosing the key insertion order

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.