import os
import shutil
import lazyllm
from .model_mapping import model_name_mapping, model_provider, model_groups

lazyllm.config.add('model_source', str, 'modelscope', 'MODEL_SOURCE')
lazyllm.config.add('model_cache_dir', str, os.path.join(os.path.expanduser('~'), '.lazyllm', 'model'),
                   'MODEL_CACHE_DIR')
lazyllm.config.add('model_path', str, '', 'MODEL_PATH')
lazyllm.config.add('model_source_token', str, '', 'MODEL_SOURCE_TOKEN')
lazyllm.config.add('data_path', str, '', 'DATA_PATH')


class ModelManager():
    """ModelManager is a utility class provided by LazyLLM for developers to automatically download models.
Currently, it supports search for models from local directories, as well as automatically downloading model from
huggingface or modelscope. Before using ModelManager, the following environment variables need to be set:

- LAZYLLM_MODEL_SOURCE: The source for model downloads, which can be set to ``huggingface`` or ``modelscope`` .
- LAZYLLM_MODEL_SOURCE_TOKEN: The token provided by ``huggingface`` or ``modelscope`` for private model download.
- LAZYLLM_MODEL_PATH: A colon-separated ``:`` list of local absolute paths for model search.
- LAZYLLM_MODEL_CACHE_DIR: Directory for downloaded models.

Keyword Args: 
    model_source (str, optional): The source for model downloads, currently only supports ``huggingface`` or ``modelscope`` .
        If necessary, ModelManager downloads model data from the source. If not provided, LAZYLLM_MODEL_SOURCE
        environment variable would be used, and if LAZYLLM_MODEL_SOURCE is not set, ModelManager will not download
        any model.
    token (str, optional): The token provided by ``huggingface`` or ``modelscope`` . If the token is present, ModelManager uses
        the token to download model. If not provided, LAZYLLM_MODEL_SOURCE_TOKEN environment variable would be used.
        and if LAZYLLM_MODEL_SOURCE_TOKEN is not set, ModelManager will not download private models, only public ones.
    model_path (str, optional): A colon-separated list of absolute paths. Before actually start to download model,
        ModelManager trys to find the target model in the directories in this list. If not provided,
        LAZYLLM_MODEL_PATH environment variable would be used, and LAZYLLM_MODEL_PATH is not set, ModelManager skips
        looking for models from model_path.
    cache_dir (str, optional): An absolute path of a directory to save downloaded models. If not provided,
        LAZYLLM_MODEL_CACHE_DIR environment variable would be used, and if LAZYLLM_MODEL_PATH is not set, the default
        value is ~/.lazyllm/model.

<span style="font-size: 20px;">&ensp;**`ModelManager.download(model) -> str`**</span>

Download models from model_source. The function first searches for the target model in directories listed in the
model_path parameter of ModelManager class. If not found, it searches under cache_dir. If still not found,
it downloads the model from model_source and stores it under cache_dir.

Args:
    model (str): The name of the target model. The function uses this name to download the model from model_source.
    To further simplify use of the function, LazyLLM provides a mapping dict from abbreviated model names to original
    names on the download source for popular models, such as ``Llama-3-8B`` , ``GLM3-6B`` or ``Qwen1.5-7B``. For more details,
    please refer to the file ``lazyllm/module/utils/downloader/model_mapping.py`` . The model argument can be either
    an abbreviated name or one from the download source.


Examples:
    >>> from lazyllm.components import ModelManager
    >>> downloader = ModelManager(model_source='modelscope')
    >>> downloader.download('chatglm3-6b')
    """
    def __init__(self, model_source=lazyllm.config['model_source'],
                 token=lazyllm.config['model_source_token'],
                 cache_dir=lazyllm.config['model_cache_dir'],
                 model_path=lazyllm.config['model_path']):
        self.model_source = model_source
        self.token = token
        self.cache_dir = cache_dir
        self.model_pathes = model_path.split(":") if len(model_path) > 0 else []

    @classmethod
    def get_model_type(cls, model) -> str:
        assert isinstance(model, str) and len(model) > 0, "model name should be a non-empty string"
        for name, info in model_name_mapping.items():
            if 'type' not in info: continue

            model_name_set = {name.casefold()}
            for source in info['source']:
                model_name_set.add(info['source'][source].split('/')[-1].casefold())

            if model.split(os.sep)[-1].casefold() in model_name_set:
                return info['type']
        return 'llm'

    @classmethod
    def get_model_name(cls, model) -> str:
        search_string = os.path.basename(model)
        for model_name, sources in model_name_mapping.items():
            if model_name.lower() == search_string.lower() or any(
                os.path.basename(source_file).lower() == search_string.lower()
                for source_file in sources["source"].values()
            ):
                return model_name
        return ""

    @classmethod
    def get_model_prompt_keys(cls, model) -> dict:
        model_name = cls.get_model_name(model)
        if model_name and "prompt_keys" in model_name_mapping[model_name.lower()]:
            return model_name_mapping[model_name.lower()]["prompt_keys"]
        else:
            return dict()

    def _try_add_mapping(self, model):
        model_base = os.path.basename(model)
        model = model_base.lower()
        if model in model_name_mapping.keys():
            return
        matched_model_prefix = next((key for key in model_provider if model.startswith(key)), None)
        if matched_model_prefix and self.model_source in model_provider[matched_model_prefix]:
            matching_keys = [key for key in model_groups.keys() if key in model]
            if matching_keys:
                matched_groups = max(matching_keys, key=len)
                model_name_mapping[model] = {
                    "prompt_keys": model_groups[matched_groups]["prompt_keys"],
                    "source": {k: v + '/' + model_base for k, v in model_provider[matched_model_prefix].items()}
                }

    def download(self, model=''):
        assert isinstance(model, str), "model name should be a string."
        self._try_add_mapping(model)
        if len(model) == 0 or model[0] in (os.sep, '.', '~'): return model  # Dummy or local model.

        model_at_path = self._model_exists_at_path(model)
        if model_at_path: return model_at_path

        if self.model_source == '' or self.model_source not in ('huggingface', 'modelscope'):
            print("[WARNING] model automatic downloads only support Huggingface and Modelscope currently.")
            return model

        if model.lower() in model_name_mapping.keys() and \
                self.model_source in model_name_mapping[model.lower()]['source'].keys():
            full_model_dir = os.path.join(self.cache_dir, model)
            if self._is_model_valid(full_model_dir):
                print(f"[INFO] model link found at {full_model_dir}")
                return full_model_dir
            else:
                self._unlink_or_remove_model(full_model_dir)

            mapped_model_name = model_name_mapping[model.lower()]['source'][self.model_source]
            model_save_dir = self._do_download(mapped_model_name)
            if model_save_dir:
                # The code safely creates a symbolic link by removing any existing target.
                if os.path.exists(full_model_dir):
                    os.remove(full_model_dir)
                os.symlink(model_save_dir, full_model_dir, target_is_directory=True)
                return full_model_dir
            return model  # failed to download model, keep model as it is
        else:
            model_name_for_download = model

            # Try to figure out a possible model provider
            matched_model_prefix = next((key for key in model_provider if model.lower().startswith(key)), None)
            if matched_model_prefix and self.model_source in model_provider[matched_model_prefix]:
                model_name_for_download = model_provider[matched_model_prefix][self.model_source] + '/' + model

            model_save_dir = self._do_download(model_name_for_download)
            return model_save_dir if model_save_dir else model

    def _model_exists_at_path(self, model_name):
        if len(self.model_pathes) == 0:
            return None
        model_dirs = []

        # For short model name, get all possible names from the mapping.
        if model_name.lower() in model_name_mapping.keys():
            for source in ('huggingface', 'modelscope'):
                if source in model_name_mapping[model_name.lower()]['source'].keys():
                    model_dirs.append(model_name_mapping[model_name.lower()]['source'][source].replace('/', os.sep))
        model_dirs.append(model_name.replace('/', os.sep))

        for model_path in self.model_pathes:
            if len(model_path) == 0: continue
            if model_path[0] != os.sep:
                print(f"[WARNING] skipping path {model_path} as only absolute pathes is accepted.")
                continue
            for model_dir in model_dirs:
                full_model_dir = os.path.join(model_path, model_dir)
                if self._is_model_valid(full_model_dir):
                    return full_model_dir
        return None

    def _is_model_valid(self, model_dir):
        if not os.path.isdir(model_dir):
            return False
        return any((True for _ in os.scandir(model_dir)))

    def _unlink_or_remove_model(self, model_dir):
        if not os.path.exists(model_dir): return
        if os.path.islink(model_dir):
            os.unlink(model_dir)
        else:
            shutil.rmtree(model_dir)

    def _do_download(self, model=''):
        model_dir = model.replace('/', os.sep)
        full_model_dir = os.path.join(self.cache_dir, model_dir)
        if self._is_model_valid(full_model_dir):
            print(f"[INFO] model found at {full_model_dir}")
            return full_model_dir
        else:
            self._unlink_or_remove_model(full_model_dir)

        if self.model_source == 'huggingface':
            return self._download_model_from_hf(model, full_model_dir)
        elif self.model_source == 'modelscope':
            return self._download_model_from_ms(model, self.cache_dir)

        return model

    def _download_model_from_hf(self, model_name='', model_dir=''):
        from huggingface_hub import snapshot_download

        try:
            # refer to https://huggingface.co/docs/huggingface_hub/v0.23.1/en/package_reference/file_download
            # #huggingface_hub.snapshot_download
            if self.token == '':
                self.token = None
            elif self.token.lower() == 'true':
                self.token = True
            # else token would be a string from the user.
            model_dir_result = snapshot_download(repo_id=model_name, local_dir=model_dir, cache_dir=model_dir,
                                                 token=self.token)

            lazyllm.LOG.info(f"model downloaded at {model_dir_result}")
            return model_dir_result
        except Exception as e:
            lazyllm.LOG.error(f"Huggingface: {e}")
            if not self.token:
                lazyllm.LOG.error('The token is found to be empty. Please set the token by '
                                  'the environment variable LAZYLLM_MODEL_SOURCE_TOKEN.')
            if os.path.isdir(model_dir):
                shutil.rmtree(model_dir)
                lazyllm.LOG.error(f"{model_dir} removed due to exceptions.")
                # so that lazyllm would not regard model_dir as a downloaded available model after.

    def _download_model_from_ms(self, model_name='', model_source_dir=''):
        from modelscope.hub.snapshot_download import snapshot_download
        # refer to https://www.modelscope.cn/docs/ModelScope%20Hub%E4%BD%BF%E7%94%A8%E6%96%87%E6%A1%A3
        try:
            if (len(self.token) > 0):
                from modelscope.hub.api import HubApi
                api = HubApi()
                api.login(self.token)
            model_dir_result = snapshot_download(model_id=model_name, cache_dir=model_source_dir)

            lazyllm.LOG.info(f"Model downloaded at {model_dir_result}")
            return model_dir_result
        except Exception as e:
            lazyllm.LOG.error(f"Modelscope:{e}")
            if not self.token:
                lazyllm.LOG.error('The token is found to be empty. Please set the token by '
                                  'the environment variable LAZYLLM_MODEL_SOURCE_TOKEN.')

            # unlike Huggingface, Modelscope adds model name as sub-dir to cache_dir.
            # so we need to figure out the exact dir of the model for clearing in case of exceptions.
            model_dir = model_name.replace('/', os.sep)
            full_model_dir = os.path.join(model_source_dir, model_dir)
            if os.path.isdir(full_model_dir):
                shutil.rmtree(full_model_dir)
                lazyllm.LOG.error(f"{full_model_dir} removed due to exceptions.")
