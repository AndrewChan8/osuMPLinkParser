import json
import os

def addToResults(new_data):
    with open('qualifiers.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []

    # Append the new data
    data.append(new_data)

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
file_path = 'data.json'
new_data = {"name": "John", "age": 30, "city": "New York"}

addToResults(new_data)
