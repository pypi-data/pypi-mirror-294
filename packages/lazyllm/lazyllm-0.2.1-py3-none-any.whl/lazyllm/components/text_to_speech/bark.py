import os
import json

import lazyllm
from lazyllm import LOG
from lazyllm.thirdparty import torch
from lazyllm.thirdparty import transformers as tf
from ..utils.downloader import ModelManager

class Bark(object):

    def __init__(self, base_path, source=None, trust_remote_code=True, init=False):
        source = lazyllm.config['model_source'] if not source else source
        self.base_path = ModelManager(source).download(base_path)
        self.trust_remote_code = trust_remote_code
        self.processor, self.bark = None, None
        self.init_flag = lazyllm.once_flag()
        self.device = 'cpu'
        if init:
            lazyllm.call_once(self.init_flag, self.load_bark)

    def load_bark(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = tf.AutoProcessor.from_pretrained(self.base_path)
        self.processor.speaker_embeddings['repo_or_path'] = self.base_path
        self.bark = tf.BarkModel.from_pretrained(self.base_path,
                                                 torch_dtype=torch.float16,
                                                 attn_implementation="flash_attention_2").to(self.device)

    def __call__(self, string):
        lazyllm.call_once(self.init_flag, self.load_bark)
        if isinstance(string, str):
            query = string
            voice_preset = "v2/zh_speaker_9"
        elif isinstance(string, dict):
            query = string['inputs']
            voice_preset = string['voice_preset']
        else:
            raise TypeError(f"Not support input type:{type(string)}, requires str or dict.")
        inputs = self.processor(query, voice_preset=voice_preset).to(self.device)
        speech = self.bark.generate(**inputs) * 32767
        res = {'sounds': (
            self.bark.generation_config.sample_rate,
            speech.cpu().numpy().squeeze().tolist()
        )}
        return json.dumps(res)

    @classmethod
    def rebuild(cls, base_path, init):
        return cls(base_path, init=init)

    def __reduce__(self):
        init = bool(os.getenv('LAZYLLM_ON_CLOUDPICKLE', None) == 'ON' or self.init_flag)
        return Bark.rebuild, (self.base_path, init)

class BarkDeploy(object):
    """Bark Model Deployment Class. This class is used to deploy the Bark model to a specified server for network invocation.

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
    - Supported models: [bark](https://huggingface.co/suno/bark)


Examples:
    >>> from lazyllm import launchers, UrlModule
    >>> from lazyllm.components import BarkDeploy
    >>> deployer = BarkDeploy(launchers.remote())
    >>> url = deployer(base_model='bark')
    >>> model = UrlModule(url=url)
    >>> res = model('Hello World!')
    >>> print(len(res), res[:50])
    ... 373843 {"sounds": [24000, [-66.9375, -62.0625, -60.5, -60
    """
    keys_name_handle = {
        'inputs': 'inputs',
    }
    message_format = {
        'inputs': 'Who are you ?',
        'voice_preset': None,
    }
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
        return lazyllm.deploy.RelayServer(func=Bark(finetuned_model), launcher=self.launcher)()
