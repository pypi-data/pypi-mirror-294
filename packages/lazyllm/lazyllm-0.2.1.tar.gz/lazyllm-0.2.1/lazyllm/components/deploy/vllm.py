import os
import json
import random
import sys

import lazyllm
from lazyllm import launchers, LazyLLMCMD, ArgsDict, LOG
from .base import LazyLLMDeployBase, verify_fastapi_func


class Vllm(LazyLLMDeployBase):
    """This class is a subclass of ``LazyLLMDeployBase``, based on the inference capabilities provided by the [VLLM](https://github.com/vllm-project/vllm) framework, used for inference with large language models.

Args:
    trust_remote_code (bool): Whether to allow loading of model code from remote servers, default is ``True``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    stream (bool): Whether the response is streaming, default is ``False``.
    kw: Keyword arguments used to update default training parameters. Note that not any additional keyword arguments can be specified here.

The keyword arguments and their default values for this class are as follows:

Keyword Args: 
    tensor-parallel-size (int): Tensor parallelism parameter, default is ``1``.
    dtype (str): Data type for model weights and activations, default is ``auto``. Other options include: ``half``, ``float16``, ``bfloat16``, ``float``, ``float32``.
    kv-cache-dtype (str): Data type for the key-value cache storage, default is ``auto``. Other options include: ``fp8``, ``fp8_e5m2``, ``fp8_e4m3``.
    device (str): Backend hardware type supported by VLLM, default is ``auto``. Other options include: ``cuda``, ``neuron``, ``cpu``.
    block-size (int): Sets the size of the token block, default is ``16``.
    port (int): Service port number, default is ``auto``.
    host (str): Service IP address, default is ``0.0.0.0``.
    seed (int): Random number seed, default is ``0``.
    tokenizer_mode (str): Tokenizer loading mode, default is ``auto``.
    max-num-seqs (int): Maximum number of parallel requests for the inference engine, default is ``256``.



Examples:
    >>> from lazyllm import deploy
    >>> infer = deploy.vllm()
    """
    keys_name_handle = {
        'inputs': 'prompt',
        'stop': 'stop'
    }
    default_headers = {'Content-Type': 'application/json'}
    message_format = {
        'prompt': 'Who are you ?',
        'stream': False,
        'stop': ['<|im_end|>', '<|im_start|>', '</s>', '<|assistant|>', '<|user|>', '<|system|>', '<eos>'],
        'skip_special_tokens': False,
        'temperature': 0.01,
        'top_p': 0.8,
        'max_tokens': 1024
    }
    auto_map = {'tp': 'tensor-parallel-size'}

    def __init__(self,
                 trust_remote_code=True,
                 launcher=launchers.remote(ngpus=1),
                 stream=False,
                 **kw,
                 ):
        super().__init__(launcher=launcher)
        self.kw = ArgsDict({
            'dtype': 'auto',
            'kv-cache-dtype': 'auto',
            'tokenizer-mode': 'auto',
            'device': 'auto',
            'block-size': 16,
            'tensor-parallel-size': 1,
            'seed': 0,
            'port': 'auto',
            'host': '0.0.0.0',
            'max-num-seqs': 256,
        })
        self.trust_remote_code = trust_remote_code
        self.kw.check_and_update(kw)
        self.random_port = False if 'port' in kw and kw['port'] and kw['port'] != 'auto' else True

    def cmd(self, finetuned_model=None, base_model=None):
        if not os.path.exists(finetuned_model) or \
            not any(filename.endswith('.bin') or filename.endswith('.safetensors')
                    for filename in os.listdir(finetuned_model)):
            if not finetuned_model:
                LOG.warning(f"Note! That finetuned_model({finetuned_model}) is an invalid path, "
                            f"base_model({base_model}) will be used")
            finetuned_model = base_model

        def impl():
            if self.random_port:
                self.kw['port'] = random.randint(30000, 40000)

            cmd = f'{sys.executable} -m vllm.entrypoints.api_server --model {finetuned_model} '
            cmd += self.kw.parse_kwargs()
            if self.trust_remote_code:
                cmd += ' --trust-remote-code '
            return cmd

        return LazyLLMCMD(cmd=impl, return_value=self.geturl, checkf=verify_fastapi_func)

    def geturl(self, job=None):
        if job is None:
            job = self.job
        if lazyllm.config['mode'] == lazyllm.Mode.Display:
            return 'http://{ip}:{port}/generate'
        else:
            return f'http://{job.get_jobip()}:{self.kw["port"]}/generate'

    @staticmethod
    def extract_result(x):
        return json.loads(x)['text'][0]

    @staticmethod
    def stream_parse_parameters():
        return {"decode_unicode": False, "delimiter": b"\0"}

    @staticmethod
    def stream_url_suffix():
        return ''
