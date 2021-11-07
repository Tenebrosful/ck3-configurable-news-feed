import os
import pathlib
import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

non_english_languages = [
    'french',
    'german',
    'korean',
    'russian',
    'simp_chinese',
    'spanish',
]

def get_all_localization(language):
    localization = {}

    for root, dirs, files in os.walk(os.path.join('.', 'localization', language)):
        for filename in files:
            if filename == f"newsfeed_generated_l_{language}.yml":
                continue

            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8-sig') as file:
                yaml = ruamel.yaml.YAML()
                doc = yaml.load(file)
                localization.update(doc[f"l_{language}"])

    return localization

def generate_localization():
    english_loc = get_all_localization('english')

    for language in non_english_languages:
        missing_keys = []

        language_loc = get_all_localization(language)
        missing_keys = [key for key in english_loc.keys() if key not in language_loc]

        if missing_keys:
            generated_dict = {f"l_{language}": {key: DoubleQuotedScalarString(english_loc[key]) for key in missing_keys}}

            language_dir = os.path.join('.', 'localization', language)
            pathlib.Path(language_dir).mkdir(parents=True, exist_ok=True)
            filepath = os.path.join(language_dir, f"newsfeed_generated_l_{language}.yml")

            with open(filepath, 'w', encoding='utf-8-sig') as file:
                yaml = ruamel.yaml.YAML()
                yaml.width = 4096
                yaml.dump(generated_dict, file)

generate_localization()