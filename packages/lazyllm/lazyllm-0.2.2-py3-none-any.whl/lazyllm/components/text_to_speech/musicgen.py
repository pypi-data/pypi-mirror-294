import os
import json

import lazyllm
from lazyllm import LOG
from lazyllm.thirdparty import numpy as np
from ..utils.downloader import ModelManager

class MusicGen(object):

    def __init__(self, base_path, source=None, init=False):
        source = lazyllm.config['model_source'] if not source else source
        self.base_path = ModelManager(source).download(base_path)
        self.model = None
        self.init_flag = lazyllm.once_flag()
        if init:
            lazyllm.call_once(self.init_flag, self.load_tts)

    def load_tts(self):
        from transformers import pipeline
        self.model = pipeline("text-to-speech", self.base_path, device=0)

    def __call__(self, string):
        lazyllm.call_once(self.init_flag, self.load_tts)
        speech = self.model(string, forward_params={"do_sample": True})
        speech['audio'] = (speech['audio'].flatten() * 32767).astype(np.int16).tolist()
        res = {'sounds': (speech['sampling_rate'], speech['audio'])}
        return json.dumps(res)

    @classmethod
    def rebuild(cls, base_path, init):
        return cls(base_path, init=init)

    def __reduce__(self):
        init = bool(os.getenv('LAZYLLM_ON_CLOUDPICKLE', None) == 'ON' or self.init_flag)
        return MusicGen.rebuild, (self.base_path, init)

class MusicGenDeploy(object):
    """MusicGen Model Deployment Class. This class is used to deploy the MusicGen model to a specified server for network invocation.

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
    - Input for infer: `str`.  The text corresponding to the audio to be generated.
    - Return of infer: A `str` that is the serialized form of a dictionary, with the keyword “sounds”, corresponding to a list where the first element is the sampling rate, and the second element is a list of audio data.
    - Supported models: [musicgen-small](https://huggingface.co/facebook/musicgen-small)


Examples:
    >>> from lazyllm import launchers, UrlModule
    >>> from lazyllm.components import MusicGenDeploy
    >>> deployer = MusicGenDeploy(launchers.remote())
    >>> url = deployer(base_model='musicgen-small')
    >>> model = UrlModule(url=url)
    >>> model('Symphony with flute as the main melody')
    4981065 {"sounds": [32000, [-931, -1206, -1170, -1078, -10, ...
    """
    message_format = None
    keys_name_handle = None
    default_headers = {'Content-Type': 'application/json'}

    def __init__(self, launcher=None):
        self.launcher = launcher

    def __call__(self, finetuned_model=None, base_model=None):
        if not finetuned_model:
            finetuned_model = base_model
        elif not os.path.exists(finetuned_model) or \
            not any(filename.endswith('.bin', '.safetensors')
                    for _, _, filename in os.walk(finetuned_model) if filename):
            LOG.warning(f"Note! That finetuned_model({finetuned_model}) is an invalid path, "
                        f"base_model({base_model}) will be used")
            finetuned_model = base_model
        return lazyllm.deploy.RelayServer(func=MusicGen(finetuned_model), launcher=self.launcher)()
