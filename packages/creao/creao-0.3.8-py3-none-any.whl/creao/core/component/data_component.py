from typing import Dict, List
from creao.core.component.util import creao_component
from datasets import load_dataset

@creao_component
class HFDataComponent:
    def __init__(self, hf_dataset_path: str, **kwargs):
        """
        Initialize the HFDataComponent by setting the path to the Hugging Face dataset.

        Args:
            hf_dataset_path (str): Path to the Hugging Face dataset (e.g., 'imdb').
            **kwargs: Additional keyword arguments, if needed for future extensions.
        """
        self.hf_path = hf_dataset_path  # Store the path to the dataset

    def _convert_to_dict_list(self, dataset) -> List[Dict[str, str]]:
        """
        Convert the Hugging Face dataset into a list of dictionaries with string values.

        Args:
            dataset: The dataset to convert, typically a split from Hugging Face.

        Returns:
            List[Dict[str, str]]: A list of dictionaries where each key-value pair 
                                  in the original dataset is converted to a string.
        """
        return [
            {key: str(value) for key, value in example.items()} for example in dataset
        ]

    def run(self, chained_input: List[Dict[str, str]]) -> List[Dict[str, List[str]]]:
        """
        Download the dataset, apply global mappings, and return the processed data.

        Args:
            chained_input (List[Dict[str, str]]): Input data passed from the previous 
                                                  component in the pipeline.

        Returns:
            List[Dict[str, List[str]]]: A list of dictionaries representing the processed 
                                        dataset with keys possibly remapped according to 
                                        the global dataset map.
        """
        # Log the beginning of the dataset download process
        print(f"Downloading dataset from {self.hf_path}...")

        # Load the specified split of the dataset (defaulting to 'train')
        dataset = load_dataset(self.hf_path, split="train")

        # Initialize a list to hold the processed dataset
        list_res = []

        # Retrieve the global dataset mapping, which is assumed to be defined during the pipeline setup
        global_dataset_map = self.global_dataset_map  # This map remaps dataset keys

        # Iterate over each item in the dataset
        for item in dataset:
            # For each key in the global dataset map, replace the key in the item with its mapped key
            for key in global_dataset_map:
                if key in item:
                    value = item[key]  # Retrieve the value associated with the current key
                    mapped_key = global_dataset_map[key]  # Get the mapped key from the global map

                    # Remove the original key-value pair from the item
                    item.pop(key)

                    # Add the new key-value pair to the item using the mapped key
                    item[mapped_key] = value

            # Append the processed item to the results list
            list_res.append(item)

        # Return the list of processed items
        return list_res
