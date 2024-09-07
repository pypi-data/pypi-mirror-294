from abc import ABC, abstractmethod
import csv
from typing import Dict, List
from datasets import load_dataset
from creao.core.component.util import creao_component

class BaseDataComponent(ABC):
    def __init__(self, **kwargs):
        """
        Initialize the base data component, possibly with additional keyword arguments
        for future extensions.
        
        Args:
            **kwargs: Additional keyword arguments for future use.
        """
        self.global_dataset_map = kwargs.get('global_dataset_map', {})

    @abstractmethod
    def load_data(self) -> List[Dict[str, str]]:
        """
        Abstract method for loading data that must be implemented by subclasses.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded data.
        """
        pass

    def _remap_keys(self, dataset: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Apply the global dataset mapping to remap keys in the dataset.

        Args:
            dataset (List[Dict[str, str]]): The dataset to process.

        Returns:
            List[Dict[str, str]]: The dataset with keys remapped according to global_dataset_map.
        """
        remapped_data = []

        for item in dataset:
            # Create a copy of the item so that the original is not modified
            remapped_item = item.copy()
            # Iterate over each key in the global dataset map and remap it
            for key in self.global_dataset_map:
                if key in remapped_item:
                    value = remapped_item.pop(key)
                    mapped_key = self.global_dataset_map[key]
                    remapped_item[mapped_key] = value

            remapped_data.append(remapped_item)

        return remapped_data

    def run(self, chained_input: List[Dict[str, str]] = None) -> List[Dict[str, str]]:
        """
        Load the data, apply global mappings, and return the processed data.

        Args:
            chained_input (List[Dict[str, str]], optional): Input data passed from the previous 
                                                            component in the pipeline.

        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the processed dataset 
                                  with keys remapped according to the global dataset map.
        """
        # Load the data using the subclass-specific method
        dataset = self.load_data()

        # Apply global dataset mapping to the loaded data
        return self._remap_keys(dataset)
    

@creao_component
class HFDataComponent(BaseDataComponent):
    def __init__(self, hf_dataset_path: str, **kwargs):
        """
        Initialize the HFDataComponent by setting the path to the Hugging Face dataset.
        
        Args:
            hf_dataset_path (str): Path to the Hugging Face dataset (e.g., 'imdb').
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.hf_path = hf_dataset_path

    def load_data(self) -> List[Dict[str, str]]:
        """
        Load data from the specified Hugging Face dataset and convert it to a list of dictionaries.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded dataset.
        """
        # Log the beginning of the dataset download process
        print(f"Downloading dataset from {self.hf_path}...")

        # Load the dataset split (defaulting to 'train')
        dataset = load_dataset(self.hf_path, split="train")
        
        # Convert the dataset to a list of dictionaries with string values
        return [{key: str(value) for key, value in example.items()} for example in dataset]


@creao_component
class CSVDataComponent(BaseDataComponent):
    def __init__(self, file_path: str, **kwargs):
        """
        Initialize the CSVDataComponent by setting the path to the CSV file.

        Args:
            csv_file_path (str): Path to the CSV file.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.csv_path = file_path

    def load_data(self) -> List[Dict[str, str]]:
        """
        Load data from the specified CSV file and convert it to a list of dictionaries.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries representing the loaded CSV data.
        """
        # Log the beginning of the CSV file loading process
        print(f"Loading CSV data from {self.csv_path}...")

        # Read the CSV file and convert it to a list of dictionaries
        data_list = []
        with open(self.csv_path, mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data_list.append({key: str(value) for key, value in row.items()})
        
        return data_list