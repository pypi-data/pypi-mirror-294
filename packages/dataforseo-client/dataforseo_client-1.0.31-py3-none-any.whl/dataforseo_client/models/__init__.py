import re
import importlib

def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def __getattr__(name):
    file_name = camel_to_snake(name)

    modules_to_try = [
        'dataforseo_client.models',
        'dataforseo_client.api',
        'dataforseo_client',
    ]

    for module in modules_to_try:
        try:
            module = importlib.import_module(f'{module}.{file_name}')
            model = getattr(module, name)
            globals()[name] = model
            return model
        except:
            continue
    
    raise ImportError(f"Cannot find {name} in any of the specified modules")