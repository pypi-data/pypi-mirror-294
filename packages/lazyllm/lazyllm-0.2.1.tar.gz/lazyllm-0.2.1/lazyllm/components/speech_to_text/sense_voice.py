import os
from urllib.parse import urlparse

import lazyllm
from lazyllm import LOG
from ..utils.downloader import ModelManager
from lazyllm.thirdparty import funasr


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_valid_path(path):
    return os.path.isfile(path)

class SenseVoice(object):
    def __init__(self, base_path, source=None, init=False):
        source = lazyllm.config['model_source'] if not source else source
        self.base_path = ModelManager(source).download(base_path)
        self.model = None
        self.init_flag = lazyllm.once_flag()
        if init:
            lazyllm.call_once(self.init_flag, self.load_stt)

    def load_stt(self):
        self.model = funasr.AutoModel(
            model=self.base_path,
            trust_remote_code=False,
            vad_model="fsmn-vad",
            vad_kwargs={"max_single_segment_time": 30000},
            device="cuda:0",
        )

    def __call__(self, string):
        lazyllm.call_once(self.init_flag, self.load_stt)
        if isinstance(string, dict):
            if string['audio']:
                string = string['audio'][0] if isinstance(string['audio'], list) else string['audio']
            else:
                string = string['inputs']
        assert isinstance(string, str)
        string = string.strip()
        if not string.endswith(('.mp3', '.wav')):
            return "Only '.mp3' and '.wav' formats in the form of file paths or URLs are supported."
        if not is_valid_path(string) and not is_valid_url(string):
            return f"This {string} is not a valid URL or file path. Please check."
        res = self.model.generate(
            input=string,
            cache={},
            language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,
            merge_length_s=15,
        )
        text = funasr.utils.postprocess_utils.rich_transcription_postprocess(res[0]["text"])
        return text

    @classmethod
    def rebuild(cls, base_path, init):
        return cls(base_path, init=init)

    def __reduce__(self):
        init = bool(os.getenv('LAZYLLM_ON_CLOUDPICKLE', None) == 'ON' or self.init_flag)
        return SenseVoice.rebuild, (self.base_path, init)

class SenseVoiceDeploy(object):
    """SenseVoice Model Deployment Class. This class is used to deploy the SenseVoice model to a specified server for network invocation.

`__init__(self, launcher=None)`
Constructor, initializes the deployment class.

Args:
    launcher (lazyllm.launcher): An instance of the launcher used to start the remote service.

`__call__(self, finetuned_model=None, base_model=None)`
Deploys the model and returns the remote service address.

Args:
    finetuned_model (str): If provided, this model will be used for deployment; if not provided or the path is invalid, `base_model` will be used.
    base_model (str): The default model, which will be used for deployment if `finetuned_model` is invalid.
    Return (str): The URL address of the remote service.

Notes:
    - Input for infer: `str`. The audio path or link.
    - Return of infer: `str`. The recognized content.
    - Supported models: [SenseVoiceSmall](https://huggingface.co/FunAudioLLM/SenseVoiceSmall)


Examples:
    >>> import os
    >>> import lazyllm
    >>> from lazyllm import launchers, UrlModule
    >>> from lazyllm.components import SenseVoiceDeploy
    >>> deployer = SenseVoiceDeploy(launchers.remote())
    >>> url = deployer(base_model='SenseVoiceSmall')
    >>> model = UrlModule(url=url)
    >>> model('path/to/audio') # support format: .mp3, .wav
    ... xxxxxxxxxxxxxxxx
    """
    keys_name_handle = {
        'inputs': 'inputs',
        'audio': 'audio',
    }
    message_format = {
        'inputs': 'Who are you ?',
        'audio': None,
    }
    default_headers = {'Content-Type': 'application/json'}

    def __init__(self, launcher=None):
        self.launcher = launcher

    def __call__(self, finetuned_model=None, base_model=None):
        if not finetuned_model:
            finetuned_model = base_model
        elif not os.path.exists(finetuned_model) or \
            not any(filename.endswith('.pt', '.bin', '.safetensors')
                    for _, _, filename in os.walk(finetuned_model) if filename):
            LOG.warning(f"Note! That finetuned_model({finetuned_model}) is an invalid path, "
                        f"base_model({base_model}) will be used")
            finetuned_model = base_model
        return lazyllm.deploy.RelayServer(func=SenseVoice(finetuned_model), launcher=self.launcher)()
