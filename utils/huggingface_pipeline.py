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


# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)




class HuggingFaceModel:
    """Class with only class methods"""

    # Class variable for the model pipeline
    qa_pipeline = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.qa_pipeline is None:
            # Load the model pipeline.
            # Note: Usually, this would also download the model.
            # But, we download the model into the container in the Dockerfile
            # so that it's built into the container and there's no download at
            # run time (otherwise, each time we'll download a 1.5GB model).
            # Loading still takes time, though. So, we do that here.
            # Note: You can use a GPU here if needed.
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

            cls.template = template

            prompt = PromptTemplate(template=template, input_variables=["question"])

            cls.llm_chain = LLMChain(prompt=prompt, llm=cls.llm)

            set_seed(420)
            elapsed = 1000 * (perf_counter() - t0)
            log.info("Model warm-up time: %d ms.", elapsed)

    @classmethod
    def predict(cls, text: str):

        # Make sure the model is loaded
        cls.load()

        # For the tutorial, let's create
        # a custom object from the huggingface prediction.
        # Our prediction object will include the label and score

        t0 = perf_counter()
        # pylint: disable-next=not-callable
        generated_text = cls.llm_chain.run(text)
        # generated_text = generated_text

        # added_text = generated_text[len(text):].strip()
        # elapsed = 1000 * (perf_counter() - t0)
        # log.info("Model prediction time: %d ms.", elapsed)

        # Create the custom prediction object.
        return {"answer": generated_text}
