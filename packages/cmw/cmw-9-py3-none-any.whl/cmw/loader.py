import yaml

class DotDict(dict):
    """A dictionary subclass that allows dot notation access to dictionary keys."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]

# Function to load YAML into a DotDict
def load_yaml_with_dot_access(path):
    with path.open("r") as file:
        data = yaml.safe_load(file)
    return convert_to_dotdict(data)

# Recursively convert a dictionary to DotDict
def convert_to_dotdict(data):
    if isinstance(data, dict):
        return DotDict({k: convert_to_dotdict(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [convert_to_dotdict(i) for i in data]
    else:
        return data
