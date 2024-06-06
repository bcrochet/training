import json
from argparse import ArgumentParser
import json
import random

def to_jsonl(path_to_data):
    print(f"Preprocessing data to jsonl format...")
    output_path = f"{path_to_data.split('.')[0]}-output.jsonl"
    with open(path_to_data, "r") as f, open(output_path, "w") as g:
        for line in f:
            line = json.loads(line)
            input = line["user"]
            output = line["assistant"]
            g.write(
                json.dumps(
                    {"input": input, "output": output}
                )
                + "\n"
            )
    print(f"Data was successfully preprocessed and saved by {output_path} .")

    return output_path

def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to jsonl dataset you want to prepare.",
    )
    args = parser.parse_args()

    return args

def split_nemo(nemo_train_data):
    input_file = nemo_train_data
    training_output_file = "training.jsonl"
    validation_output_file = "validation.jsonl"
    test_output_file = "test.jsonl"
    
    # Specify the proportion of data for training and validation
    train_proportion = 0.80
    validation_proportion = 0.15
    
    # Read the JSONL file and shuffle the JSON objects
    with open(input_file, "r") as f:
        lines = f.readlines()
        random.shuffle(lines)
    
    # Calculate split indices
    total_lines = len(lines)
    train_index = int(total_lines * train_proportion)
    val_index = int(total_lines * validation_proportion)
    
    # Distribute JSON objects into training and validation sets
    train_data = lines[:train_index]
    validation_data = lines[train_index:train_index+val_index]
    test_data = lines[train_index+val_index:]
    
    # Write JSON objects to training file
    with open(training_output_file, "w") as f:
        for line in train_data:
            f.write(line.strip() + "\n")
    
    # Write JSON objects to validation file
    with open(validation_output_file, "w") as f:
        for line in validation_data:
            f.write(line.strip() + "\n")
    
    # Write JSON objects to training file
    with open(test_output_file, "w") as f:
        for line in test_data:
            f.write(line.strip() + "\n")
    
def main():
    args = get_args()
    path_to_data = args.input
    nemo_data = to_jsonl(path_to_data)
    split_nemo(nemo_data)


if __name__ == "__main__":
    main()
