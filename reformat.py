import json

# Input data as a string
input_data = """
|  8  37  38  39   5|    |  0   0   0   0   0|
|  6   7   7  72  51|    |  0   0   0   0   0|
|  7  72  50  37 136|    |  1   0   0   5   0|
| 51  37 136  38  37|    |  0   7   0   1   4|
|136  51  38  37 136|    |  0   0   1   3   0|
| 51  38  37 136 208|    |  0  20   2   0   0|
|  0   0            |    |  0   0            |
"""

# Parse the input data
instructions = []
data = []

for line in input_data.strip().split("\n"):
    # Split the line using '|' as a strict delimiter
    parts = [part.strip() for part in line.split("|") if part.strip()]
    
    if len(parts) >= 2:
        # Extract and clean the instruction and data parts
        instruction_part = parts[0]
        data_part = parts[1]

        # Debugging: Print the raw parts for verification
        print(f"Instruction part: '{instruction_part}'")
        print(f"Data part: '{data_part}'")

        # Convert the instruction part to a list of integers
        instructions.extend(
            [int(x) for x in instruction_part.split() if x.isdigit()]
        )

        # Convert the data part to a list of integers
        data.extend([int(x) for x in data_part.split() if x.isdigit()])

# Ensure the arrays have a static size of 256 elements
instructions = (instructions + [0] * 256)[:256]  # Pad with 0s or truncate
data = (data + [0] * 256)[:256]  # Pad with 0s or truncate

# Debugging: Print parsed instructions and data
print("Parsed instructions:", instructions)
print("Parsed data:", data)

# Create the JSON structure
output = {
    "instructions": instructions,
    "data": data
}

# Write the JSON to a file with arrays on a single line
output_file = "formatted_rom.json"
with open(output_file, "w") as f:
    json.dump(output, f, separators=(",", ":"), indent=None)

print(f"Data has been written to {output_file}")