from typing import List, Optional
from logging import Logger

from umlars_translator.core.deserialization.deserializer import ModelDeserializer
from umlars_translator.app.dtos import uml_model as pydantic_models
from umlars_translator.app.dtos.input import UmlModelDTO
from umlars_translator.app.exceptions import InputDataError
from umlars_translator.core.deserialization.exceptions import UnsupportedSourceDataTypeError


from umlars_translator.core.translator import ModelTranslator

async def translate_model(file_paths):
    model_translator = ModelTranslator()
    for file_path in file_paths:
        try:
            model_translator.deserialize(file_path=file_path)
        except Exception as ex:
            print(f"Failed to translate {file_path}")

    translated_model = model_translator.serialize()

