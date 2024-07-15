import json
from collections import defaultdict


class LabelManager:
    def __init__(self, json_file_path):
        self.data = self._read_json(json_file_path)
        self.label_dict = {file["filename"]: file for file in self.data["label"]}
        self.label_count = self._calculate_label_count()

    def _read_json(self, json_file_path):
        with open(json_file_path, "r") as f:
            return json.load(f)

    def _calculate_label_count(self):
        label_count = defaultdict(int)
        for file in self.data["label"]:
            label_count[file["label"]] += 1
        return label_count

    def filter_files(self, **kwargs) -> list:
        """
        Example:
        filter_files(label='benignware', CPUArchitecture='ARM')
        filter_files(tags='test')
        """
        filtered_files = self.data["label"]
        for key, value in kwargs.items():
            filtered_files = [file for file in filtered_files if file.get(key) == value]
        return [file["filename"] for file in filtered_files]

    def get_file_info(self, file_name: str, info_key: str) -> str:
        file = self.label_dict.get(file_name)
        if file:
            return file.get(info_key, None)
        return None

    def get_labels_count(self, labels: list) -> tuple:
        return tuple(self.label_count.get(label, 0) for label in labels)
