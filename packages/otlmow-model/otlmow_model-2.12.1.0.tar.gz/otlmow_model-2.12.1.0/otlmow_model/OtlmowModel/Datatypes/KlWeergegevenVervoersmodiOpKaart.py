# coding=utf-8
from otlmow_model.OtlmowModel.BaseClasses.KeuzelijstField import KeuzelijstField
from otlmow_model.OtlmowModel.BaseClasses.KeuzelijstWaarde import KeuzelijstWaarde


# Generated with OTLEnumerationCreator. To modify: extend, do not edit
class KlWeergegevenVervoersmodiOpKaart(KeuzelijstField):
    """De verschillende beschikbare vervoersmodi die op de bijhorende kaart worden meegegeven."""
    naam = 'KlWeergegevenVervoersmodiOpKaart'
    label = 'Weergegeven vervoersmodi op kaart'
    objectUri = 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#KlWeergegevenVervoersmodiOpKaart'
    definition = 'De verschillende beschikbare vervoersmodi die op de bijhorende kaart worden meegegeven.'
    status = 'ingebruik'
    codelist = 'https://wegenenverkeer.data.vlaanderen.be/id/conceptscheme/KlWeergegevenVervoersmodiOpKaart'
    options = {
        'bus': KeuzelijstWaarde(invulwaarde='bus',
                                label='Bus',
                                status='ingebruik',
                                definitie='Bus',
                                objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/bus'),
        'deelauto': KeuzelijstWaarde(invulwaarde='deelauto',
                                     label='Deelauto',
                                     status='ingebruik',
                                     definitie='TODO',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelauto'),
        'deelbakfiets': KeuzelijstWaarde(invulwaarde='deelbakfiets',
                                         label='Deelbakfiets',
                                         status='ingebruik',
                                         definitie='Deelbakfiets',
                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelbakfiets'),
        'deelbolderkar': KeuzelijstWaarde(invulwaarde='deelbolderkar',
                                          label='Deelbolderkar',
                                          status='ingebruik',
                                          definitie='Deelbolderkar',
                                          objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelbolderkar'),
        'deelbuggy': KeuzelijstWaarde(invulwaarde='deelbuggy',
                                      label='Deelbuggy',
                                      status='ingebruik',
                                      definitie='Deelbuggy',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelbuggy'),
        'deelfiets': KeuzelijstWaarde(invulwaarde='deelfiets',
                                      label='Deelfiets',
                                      status='ingebruik',
                                      definitie='TODO',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelfiets'),
        'deelrolstoel': KeuzelijstWaarde(invulwaarde='deelrolstoel',
                                         label='Deelrolstoel',
                                         status='ingebruik',
                                         definitie='Deelrolstoel',
                                         objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelrolstoel'),
        'deelstep': KeuzelijstWaarde(invulwaarde='deelstep',
                                     label='Deelstep',
                                     status='ingebruik',
                                     definitie='Deelstep',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelstep'),
        'deelwagen': KeuzelijstWaarde(invulwaarde='deelwagen',
                                      label='Deelwagen',
                                      status='ingebruik',
                                      definitie='Deelwagen',
                                      objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/deelwagen'),
        'e-deelbakfiets': KeuzelijstWaarde(invulwaarde='e-deelbakfiets',
                                           label='e-deelbakfiets',
                                           status='ingebruik',
                                           definitie='e-deelbakfiets',
                                           objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/e-deelbakfiets'),
        'e-deelfiets': KeuzelijstWaarde(invulwaarde='e-deelfiets',
                                        label='e-deelfiets',
                                        status='ingebruik',
                                        definitie='e-deelfiets',
                                        objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/e-deelfiets'),
        'e-deelstep': KeuzelijstWaarde(invulwaarde='e-deelstep',
                                       label='e-deelstep',
                                       status='ingebruik',
                                       definitie='e-deelstep',
                                       objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/e-deelstep'),
        'e-deelwagen': KeuzelijstWaarde(invulwaarde='e-deelwagen',
                                        label='e-deelwagen',
                                        status='ingebruik',
                                        definitie='e-deelwagen',
                                        objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/e-deelwagen'),
        'flex': KeuzelijstWaarde(invulwaarde='flex',
                                 label='Flex',
                                 status='ingebruik',
                                 definitie='Flex',
                                 objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/flex'),
        'flex-2': KeuzelijstWaarde(invulwaarde='flex-2',
                                   label='Flex+',
                                   status='ingebruik',
                                   definitie='Flex+',
                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/flex-2'),
        'flexvervoer': KeuzelijstWaarde(invulwaarde='flexvervoer',
                                        label='Flexvervoer',
                                        status='ingebruik',
                                        definitie='TODO',
                                        objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/flexvervoer'),
        'kernnet-aanvullend-net': KeuzelijstWaarde(invulwaarde='kernnet-aanvullend-net',
                                                   label='Kernnet - aanvullend net',
                                                   status='ingebruik',
                                                   definitie='TODO',
                                                   objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/kernnet-aanvullend-net'),
        'metro': KeuzelijstWaarde(invulwaarde='metro',
                                  label='Metro',
                                  status='ingebruik',
                                  definitie='Metro',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/metro'),
        'taxi': KeuzelijstWaarde(invulwaarde='taxi',
                                 label='Taxi',
                                 status='ingebruik',
                                 definitie='Taxi',
                                 objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/taxi'),
        'tram': KeuzelijstWaarde(invulwaarde='tram',
                                 label='Tram',
                                 status='ingebruik',
                                 definitie='Tram',
                                 objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/tram'),
        'trein': KeuzelijstWaarde(invulwaarde='trein',
                                  label='Trein',
                                  status='ingebruik',
                                  definitie='Trein',
                                  objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/trein'),
        'treinnet': KeuzelijstWaarde(invulwaarde='treinnet',
                                     label='Treinnet',
                                     status='ingebruik',
                                     definitie='TODO',
                                     objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/treinnet'),
        'vast-en-semiflex': KeuzelijstWaarde(invulwaarde='vast-en-semiflex',
                                             label='Vast en semiflex',
                                             status='ingebruik',
                                             definitie='TODO',
                                             objectUri='https://wegenenverkeer.data.vlaanderen.be/id/concept/KlWeergegevenVervoersmodiOpKaart/vast-en-semiflex')
    }

    @classmethod
    def create_dummy_data(cls):
        return cls.create_dummy_data_keuzelijst(cls.options)

