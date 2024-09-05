from ...common import LazyLLMRegisterMetaClass

def is_number(s: str):
    try:
        int(s)
        return True
    except ValueError:
        if s == "None" or len(s) == 0:
            return False
        else:
            raise ValueError("Invalid number: " + s + ". You can enter an integer, None or an empyt string.")

class LazyLLMFormatterBase(metaclass=LazyLLMRegisterMetaClass):
    """This class is the base class of the formatter. The formatter is the formatter of the model output result. Users can customize the formatter or use the formatter provided by LazyLLM.
Main methods: _parse_formatter: parse the index content. _load: Parse the str object, and the part containing Python objects is parsed out, such as list, dict and other objects. _parse_py_data_by_formatter: format the python object according to the custom formatter and index. format: format the passed content. If the content is a string type, convert the string into a python object first, and then format it. If the content is a python object, format it directly.


Examples:
    >>> from lazyllm.components.formatter import FormatterBase
    >>> class MyFormatter(FormatterBase):
    ...     def __init__(self, formatter: str = None):
    ...         self._formatter = formatter
    ...         if self._formatter:
    ...             self._parse_formatter()
    ...         else:
    ...             self._slices = None
    ...     def _parse_formatter(self):
    ...         slice_str = self._formatter.strip()[1:-1]
    ...         slices = []
    ...         parts = slice_str.split(":")
    ...         start = int(parts[0]) if parts[0] else None
    ...         end = int(parts[1]) if len(parts) > 1 and parts[1] else None
    ...         step = int(parts[2]) if len(parts) > 2 and parts[2] else None
    ...         slices.append(slice(start, end, step))
    ...         self._slices = slices
    ...     def _load(self, data):
    ...         return [int(x) for x in data.strip('[]').split(',')]
    ...     def _parse_py_data_by_formatter(self, data):
    ...         if self._slices is not None:
    ...             result = []
    ...             for s in self._slices:
    ...                 if isinstance(s, slice):
    ...                     result.extend(data[s])
    ...                 else:
    ...                     result.append(data[int(s)])
    ...             return result
    ...         else:
    ...             return data
    ...
    >>> fmt = MyFormatter("[1:3]")
    >>> res = fmt.format("[1,2,3,4,5]")
    >>> print(res)
    [2, 3]
    """
    def _load(self, msg: str):
        return msg

    def _parse_py_data_by_formatter(self, py_data):
        raise NotImplementedError("This data parse function is not implemented.")

    def format(self, msg):
        if isinstance(msg, str): msg = self._load(msg)
        return self._parse_py_data_by_formatter(msg)

    def __call__(self, msg):
        return self.format(msg)


class JsonLikeFormatter(LazyLLMFormatterBase):
    def __init__(self, formatter: str = None):
        self._formatter = formatter
        if self._formatter:
            self._parse_formatter()
        else:
            self._slices = None

    def _parse_formatter(self):
        # Remove the surrounding brackets
        slice_str = self._formatter.strip()[1:-1]
        dimensions = slice_str.split(",")
        slices = []

        for dim in dimensions:
            if ":" in dim:
                parts = dim.split(":")
                start = int(parts[0]) if is_number(parts[0]) else None
                end = int(parts[1]) if len(parts) > 1 and is_number(parts[1]) else None
                step = int(parts[2]) if len(parts) > 2 and is_number(parts[2]) else None
                slices.append(slice(start, end, step))
            else:
                slices.append(dim.strip())
        self._slices = slices

    def _parse_py_data_by_formatter(self, data, *, slices=None):
        def _impl(data, slice):
            if isinstance(data, (tuple, list)) and isinstance(slice, str):
                return data[int(slice)]
            return data[slice]

        if slices is None: slices = self._slices
        if not slices: return data
        if isinstance(slices[0], slice): return [self._parse_py_data_by_formatter(d, slices=slices[1:])
                                                 for d in _impl(data, slices[0])]
        else: return self._parse_py_data_by_formatter(_impl(data, slices[0]), slices=slices[1:])


class EmptyFormatter(LazyLLMFormatterBase):
    """This type is the system default formatter. When the user does not specify anything or does not want to format the model output, this type is selected. The model output will be in the same format.


Examples:
    >>> import lazyllm
    >>> from lazyllm.components import EmptyFormatter
    >>> toc_prompt='''
    ... You are now an intelligent assistant. Your task is to understand the user's input and convert the outline into a list of nested dictionaries. Each dictionary contains a `title` and a `describe`, where the `title` should clearly indicate the level using Markdown format, and the `describe` is a description and writing guide for that section.
    ... 
    ... Please generate the corresponding list of nested dictionaries based on the following user input:
    ... 
    ... Example output:
    ... [
    ...     {
    ...         "title": "# Level 1 Title",
    ...         "describe": "Please provide a detailed description of the content under this title, offering background information and core viewpoints."
    ...     },
    ...     {
    ...         "title": "## Level 2 Title",
    ...         "describe": "Please provide a detailed description of the content under this title, giving specific details and examples to support the viewpoints of the Level 1 title."
    ...     },
    ...     {
    ...         "title": "### Level 3 Title",
    ...         "describe": "Please provide a detailed description of the content under this title, deeply analyzing and providing more details and data support."
    ...     }
    ... ]
    ... User input is as follows:
    ... '''
    >>> query = "Please help me write an article about the application of artificial intelligence in the medical field."
    >>> m = lazyllm.TrainableModule("internlm2-chat-20b").prompt(toc_prompt).start()  # the model output without specifying a formatter
    >>> ret = m(query, max_new_tokens=2048)
    >>> print(f"ret: {ret!r}")
    'Based on your user input, here is the corresponding list of nested dictionaries:
    [
        {
            "title": "# Application of Artificial Intelligence in the Medical Field",
            "describe": "Please provide a detailed description of the application of artificial intelligence in the medical field, including its benefits, challenges, and future prospects."
        },
        {
            "title": "## AI in Medical Diagnosis",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical diagnosis, including specific examples of AI-based diagnostic tools and their impact on patient outcomes."
        },
        {
            "title": "### AI in Medical Imaging",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical imaging, including the advantages of AI-based image analysis and its applications in various medical specialties."
        },
        {
            "title": "### AI in Drug Discovery and Development",
            "describe": "Please provide a detailed description of how artificial intelligence is used in drug discovery and development, including the role of AI in identifying potential drug candidates and streamlining the drug development process."
        },
        {
            "title": "## AI in Medical Research",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical research, including its applications in genomics, epidemiology, and clinical trials."
        },
        {
            "title": "### AI in Genomics and Precision Medicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in genomics and precision medicine, including the role of AI in analyzing large-scale genomic data and tailoring treatments to individual patients."
        },
        {
            "title": "### AI in Epidemiology and Public Health",
            "describe": "Please provide a detailed description of how artificial intelligence is used in epidemiology and public health, including its applications in disease surveillance, outbreak prediction, and resource allocation."
        },
        {
            "title": "### AI in Clinical Trials",
            "describe": "Please provide a detailed description of how artificial intelligence is used in clinical trials, including its role in patient recruitment, trial design, and data analysis."
        },
        {
            "title": "## AI in Medical Practice",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical practice, including its applications in patient monitoring, personalized medicine, and telemedicine."
        },
        {
            "title": "### AI in Patient Monitoring",
            "describe": "Please provide a detailed description of how artificial intelligence is used in patient monitoring, including its role in real-time monitoring of vital signs and early detection of health issues."
        },
        {
            "title": "### AI in Personalized Medicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in personalized medicine, including its role in analyzing patient data to tailor treatments and predict outcomes."
        },
        {
            "title": "### AI in Telemedicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in telemedicine, including its applications in remote consultations, virtual diagnoses, and digital health records."
        },
        {
            "title": "## AI in Medical Ethics and Policy",
            "describe": "Please provide a detailed description of the ethical and policy considerations surrounding the use of artificial intelligence in the medical field, including issues related to data privacy, bias, and accountability."
        }
    ]'
    >>> m = lazyllm.TrainableModule("internlm2-chat-20b").formatter(EmptyFormatter()).prompt(toc_prompt).start()  # the model output of the specified formatter
    >>> ret = m(query, max_new_tokens=2048)
    >>> print(f"ret: {ret!r}")
    'Based on your user input, here is the corresponding list of nested dictionaries:
    [
        {
            "title": "# Application of Artificial Intelligence in the Medical Field",
            "describe": "Please provide a detailed description of the application of artificial intelligence in the medical field, including its benefits, challenges, and future prospects."
        },
        {
            "title": "## AI in Medical Diagnosis",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical diagnosis, including specific examples of AI-based diagnostic tools and their impact on patient outcomes."
        },
        {
            "title": "### AI in Medical Imaging",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical imaging, including the advantages of AI-based image analysis and its applications in various medical specialties."
        },
        {
            "title": "### AI in Drug Discovery and Development",
            "describe": "Please provide a detailed description of how artificial intelligence is used in drug discovery and development, including the role of AI in identifying potential drug candidates and streamlining the drug development process."
        },
        {
            "title": "## AI in Medical Research",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical research, including its applications in genomics, epidemiology, and clinical trials."
        },
        {
            "title": "### AI in Genomics and Precision Medicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in genomics and precision medicine, including the role of AI in analyzing large-scale genomic data and tailoring treatments to individual patients."
        },
        {
            "title": "### AI in Epidemiology and Public Health",
            "describe": "Please provide a detailed description of how artificial intelligence is used in epidemiology and public health, including its applications in disease surveillance, outbreak prediction, and resource allocation."
        },
        {
            "title": "### AI in Clinical Trials",
            "describe": "Please provide a detailed description of how artificial intelligence is used in clinical trials, including its role in patient recruitment, trial design, and data analysis."
        },
        {
            "title": "## AI in Medical Practice",
            "describe": "Please provide a detailed description of how artificial intelligence is used in medical practice, including its applications in patient monitoring, personalized medicine, and telemedicine."
        },
        {
            "title": "### AI in Patient Monitoring",
            "describe": "Please provide a detailed description of how artificial intelligence is used in patient monitoring, including its role in real-time monitoring of vital signs and early detection of health issues."
        },
        {
            "title": "### AI in Personalized Medicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in personalized medicine, including its role in analyzing patient data to tailor treatments and predict outcomes."
        },
        {
            "title": "### AI in Telemedicine",
            "describe": "Please provide a detailed description of how artificial intelligence is used in telemedicine, including its applications in remote consultations, virtual diagnoses, and digital health records."
        },
        {
            "title": "## AI in Medical Ethics and Policy",
            "describe": "Please provide a detailed description of the ethical and policy considerations surrounding the use of artificial intelligence in the medical field, including issues related to data privacy, bias, and accountability."
        }
    ]'
    """
    def _parse_py_data_by_formatter(self, msg: str):
        return msg
