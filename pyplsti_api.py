from fastapi import FastAPI, HTTPException
from subprocess import Popen, PIPE, run
# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse


import subprocess
import os
from typing import Dict, List
from pathlib import Path
# from glob import glob
# from collections import defaultdict
# import json
from pydantic import BaseModel, field_validator, Field

from pyplastimatch import register

class Inputs_register(BaseModel):
    r"""
    Purpose:
        - To define the input parameters for running image registration using pyplastimatch.
    Attributes:
        - global_params: a dictionary containing the global parameters for the registration.
        - stage_params_list: a list of dictionaries defining the parameters for each stage of the registration.
        please consult pyplastimatch.register() documentation for more information.
    """

    global_params: Dict[str, str]
    stage_params_list: List[Dict[str, str]]

app = FastAPI()

@app.post("/register")
def register(
    all_inputs: Inputs_register
    ) -> None:
    r"""
    Purpose:
        - To run image registration using pyplastimatch.
    """
    register(all_inputs.global_params, all_inputs.stage_params_list)