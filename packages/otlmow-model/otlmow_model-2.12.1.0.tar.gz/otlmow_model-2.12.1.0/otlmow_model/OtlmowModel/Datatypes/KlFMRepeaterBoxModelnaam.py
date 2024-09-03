# coding=utf-8
from otlmow_model.OtlmowModel.BaseClasses.KeuzelijstField import KeuzelijstField


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlFMRepeaterBoxModelnaam(KeuzelijstField):
    """De modelnaam van de FM repeaterbox module."""
    naam = 'KlFMRepeaterBoxModelnaam'
    label = 'FM repeaterbox modelnaam'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlFMRepeaterBoxModelnaam'
    definition = 'De modelnaam van de FM repeaterbox module.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlFMRepeaterBoxModelnaam'
    options = {
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

