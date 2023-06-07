import sys
from transformers import pipeline, set_seed
from typing import List
import numpy as np
from time import perf_counter
import logging
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import os
import warnings
from utils.functions import *


# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

with open('./utils/template_ayumi.txt', 'r') as f:
    template = convert_to_multiline_string(f.read())


class HuggingFaceModel:
    """Class with only class methods"""

    # Class variable for the model pipeline
    qa_pipeline = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.qa_pipeline is None:
            # Load the model pipeline.
            t0 = perf_counter()
            quantized_model_dir = [x for x in os.listdir() if '-GPTQ' in x][0]

            model_basename = [x.split('.safetensors')[0] for x in os.listdir(quantized_model_dir) if x.endswith('safetensors')][0]
            use_triton = False

            cls.tokenizer = AutoTokenizer.from_pretrained(quantized_model_dir, use_fast=True)
            cls.model = AutoGPTQForCausalLM.from_quantized(quantized_model_dir,
                                                       use_safetensors=True,
                                                       model_basename=model_basename,
                                                       device="cuda:0",
                                                       use_triton=use_triton,
                                                       quantize_config=None)
            cls.qa_pipeline = pipeline(
                "text-generation",
                model=cls.model,
                tokenizer=cls.tokenizer,
                max_new_tokens=240,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.15)
            cls.llm = HuggingFacePipeline(pipeline=cls.qa_pipeline)

            cls.prompt = PromptTemplate(template=template, input_variables=["history", "input"])
            cls.llm_chain = LLMChain(prompt=cls.prompt, llm=cls.llm)

            set_seed(420)
            elapsed = 1000 * (perf_counter() - t0)
            log.info("Model warm-up time: %d ms.", elapsed)

    @classmethod
    def predict(cls, history: str, text: str):

        # Make sure the model is loaded
        cls.load()

        t0 = perf_counter()

        # run the predictions using the llm chain
        generated_text = cls.llm_chain.predict(history=history, input=text)
        elapsed = 1000 * (perf_counter() - t0)
        log.info("Model prediction time: %d ms.", elapsed)

        # Create the custom prediction object.
        return {"answer": generated_text}
