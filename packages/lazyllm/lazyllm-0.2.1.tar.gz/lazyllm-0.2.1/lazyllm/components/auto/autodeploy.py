import lazyllm
from lazyllm import launchers, deploy, LOG
from ..deploy.base import LazyLLMDeployBase
from .configure import get_configer
from .auto_helper import model_map, get_model_name, check_requirements
from lazyllm.components.embedding.embed import EmbeddingDeploy
from lazyllm.components.stable_diffusion.stable_diffusion3 import StableDiffusionDeploy
from lazyllm.components.speech_to_text.sense_voice import SenseVoiceDeploy
from lazyllm.components.text_to_speech.base import TTSDeploy
from ..utils.downloader import ModelManager

class AutoDeploy(LazyLLMDeployBase):
    """This class is a subclass of ``LazyLLMDeployBase`` that automatically selects the appropriate inference framework and parameters based on the input arguments for inference with large language models.

Specifically, based on the input ``base_model`` parameters, ``max_token_num``, the type and number of GPUs in ``launcher``, this class can automatically select the appropriate inference framework (such as ``Lightllm`` or ``Vllm``) and the required parameters.

Args:
    base_model (str): The base model for fine-tuning, which is required to be the name or the path to the base model. Used to provide base model information.
    source (lazyllm.config['model_source']): Specifies the model download source. This can be configured by setting the environment variable ``LAZYLLM_MODEL_SOURCE``.
    trust_remote_code (bool): Whether to allow loading of model code from remote servers, default is ``True``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    stream (bool): Whether the response is streaming, default is ``False``.
    type (str): Type parameter, default is ``None``, which corresponds to the ``llm`` type. Additionally, the ``embed`` type is also supported.
    max_token_num (int): The maximum token length for the input fine-tuning model, default is ``1024``.
    launcher (lazyllm.launcher): The launcher for fine-tuning, default is ``launchers.remote(ngpus=1)``.
    kw: Keyword arguments used to update default training parameters. Note that whether additional keyword arguments can be specified depends on the framework inferred by LazyLLM, so it is recommended to set them carefully.



Examples:
    >>> from lazyllm import deploy
    >>> deploy.auto('internlm2-chat-7b')
    <lazyllm.llm.deploy type=Lightllm> 
    """
    message_format = {}
    keys_name_handle = None
    default_headers = {'Content-Type': 'application/json'}

    def __new__(cls, base_model, source=lazyllm.config['model_source'], trust_remote_code=True, max_token_num=1024,
                launcher=launchers.remote(ngpus=1), stream=False, type=None, **kw):
        base_model = ModelManager(source).download(base_model)
        model_name = get_model_name(base_model)
        if type == 'embed' or ModelManager.get_model_type(model_name) == 'embed':
            return EmbeddingDeploy(trust_remote_code, launcher)
        elif type == 'sd' or ModelManager.get_model_type(model_name) == 'sd':
            return StableDiffusionDeploy(launcher)
        elif type == 'stt' or ModelManager.get_model_type(model_name) == 'stt':
            return SenseVoiceDeploy(launcher)
        elif type == 'tts' or ModelManager.get_model_type(model_name) == 'tts':
            return TTSDeploy(model_name, launcher=launcher)
        map_name = model_map(model_name)
        candidates = get_configer().query_deploy(lazyllm.config['gpu_type'], launcher.ngpus,
                                                 map_name, max_token_num)

        for c in candidates:
            if check_requirements(c.framework.lower()):
                deploy_cls = getattr(deploy, c.framework.lower())
            else:
                continue
            if c.tgs <= 0: LOG.warning(f"Model {model_name} may out of memory under Framework {c.framework}")
            for key, value in deploy_cls.auto_map.items():
                if value:
                    kw[value] = getattr(c, key)
            return deploy_cls(trust_remote_code=trust_remote_code, launcher=launcher, stream=stream, **kw)
        raise RuntimeError(f'No valid framework found, candidates are {[c.framework.lower() for c in candidates]}')
