from langchain import PromptTemplate
from . import functions
import requests


with open('./utils/template_ayumi.txt', 'r') as f:
    template = functions.convert_to_multiline_string(f.read())


class OobaBoogaModel:
    """Class with only class methods"""

    # Class variable for the model pipeline
    prompt = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.prompt is None:
            cls.prompt = PromptTemplate(template=template, input_variables=["history",
                                                                            "examples",
                                                                            "last_interactions",
                                                                            "input"])

    @classmethod
    def predict(cls, history: str, examples: str, last_interactions: str, text: str):

        # Make sure the model is loaded
        cls.load()

        # get the formatted prompt - input
        prompt = cls.prompt.format(history=history,
                                   examples=examples,
                                   last_interactions=last_interactions,
                                   input=text)


        request = {
            'prompt': prompt,
            'max_new_tokens': 250,
            # Generation params. If 'preset' is set to different than 'None', the values
            # in presets/preset-name.yaml are used instead of the individual numbers.
            'preset': 'None',
            'do_sample': True,
            'temperature': 0.9,
            'top_p': 0.95,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'tfs': 1,
            'top_a': 0,
            'repetition_penalty': 1.15,
            'repetition_penalty_range': 0,
            'top_k': 50,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,

            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        HOST = 'localhost:6868'
        URI = f'http://{HOST}/api/v1/generate'

        generated_text = requests.post(URI, json=request).json()['results'][0]['text']

        # Create the custom prediction object.
        return {"answer": generated_text}
