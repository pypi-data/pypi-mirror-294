from typing import List, Optional
from logging import Logger

from kink import inject

from src.umlars_translator.core.translator import ModelTranslator
from src.umlars_translator.core.deserialization.deserializer import ModelDeserializer
from src.umlars_translator.app.dtos import uml_model as pydantic_models
from src.umlars_translator.app.dtos.input import UmlModelDTO
from src.umlars_translator.app.exceptions import InputDataError
from src.umlars_translator.core.deserialization.exceptions import UnsupportedSourceDataTypeError


@inject
async def translate_service(uml_model: UmlModelDTO, app_logger: Optional[Logger] = None) -> pydantic_models.UmlModel:
    model_translator = ModelTranslator(model_deseializer=ModelDeserializer())
    try:
        for uml_file in uml_model.source_files:
            app_logger.info(f"Processing file: {uml_file.filename}")
            try:
                model_translator.deserialize(data_sources=[uml_file.to_data_source()], clear_builder_afterwards=False, model_id=uml_model.id)
                app_logger.info(f"File {uml_file.filename} was successfully deserialized")
            except Exception as ex:
                error_message = f"Failed to deserialize file {uml_file.filename}: {ex}"
                app_logger.error(error_message)

    except UnsupportedSourceDataTypeError as ex:
        error_message = f"Failed to deserialize model: {ex}"
        app_logger.error(error_message)
        raise InputDataError(error_message) from ex
    except Exception as ex:
        error_message = f"Failed to translate model: {ex}"
        app_logger.error(error_message)
        raise InputDataError(error_message) from ex

    app_logger.info("Serializing translated model")
    translated_model = model_translator.serialize(to_string=False)
    model_translator.clear()
    app_logger.info(f"Model {uml_model.id} saved and translator state cleared")

    app_logger.info(f"Successfully translated model: {translated_model.id}")
    return translated_model
