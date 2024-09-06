from sonusai.utils import ASRData
from sonusai.utils import ASRResult


def aixplain_whisper(data: ASRData) -> ASRResult:
    import tempfile
    from os import getenv
    from os.path import join

    from aixplain.factories.model_factory import ModelFactory
    from sonusai import SonusAIError
    from sonusai.utils import float_to_int16
    from sonusai.utils import write_audio

    whisper_model = data.whisper_model
    if whisper_model is None:
        envvar = 'AIXP_WHISPER_' + data.whisper_model_name.upper()
        modelkey = getenv(envvar)
        if modelkey is None:
            raise SonusAIError(f'{envvar} environment variable does not exist')

        whisper_model = ModelFactory.get(modelkey)

    with tempfile.TemporaryDirectory() as tmp:
        file = join(tmp, 'asr.wav')
        write_audio(name=file, audio=float_to_int16(data.audio))

        retry = 5
        count = 0
        while True:
            try:
                results = whisper_model.run(file)
                return ASRResult(text=results['data'], confidence=results['confidence'])
            except Exception as e:
                count += 1
                print(f'Warning: aiXplain exception: {e}')
                if count >= retry:
                    raise SonusAIError(f'Whisper exception: {e.args}')


"""
aiXplain Whisper results:
{
  'completed': True,
  'data': 'The birch canoe slid on the smooth planks.',
  'usedCredits': 3.194770833333333e-05,
  'runTime': 114.029,
  'confidence': None,
  'details': [],
  'rawData': {
    'predictions': [
      ' The birch canoe slid on the smooth planks.'
    ]
  },
  'status': 'SUCCESS'
}
"""
