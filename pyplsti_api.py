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

app = FastAPI()

class Inputs_register(BaseModel):
    r"""
    ### Purpose:
        - To define the input parameters for running image registration using pyplastimatch.
    ### Attributes:
        - global_params: a dictionary containing the global parameters for the registration.
        - stage_params_list: a list of dictionaries defining the parameters for each stage of the registration.
        please consult pyplastimatch.register() documentation for more information.
    """

    global_params: Dict[str, str]
    stage_params_list: List[Dict[str, str]]
    def __init__(self, **data):
        super().__init__(**data)
        dir_temp_data = Path(__file__).parent.joinpath("temp_data")
        for key, value in self.global_params.items():
            if "temp_data/registration/" in value:
                value = value.split("temp_data/registration/")[-1]
            value = dir_temp_data.joinpath(value)
            self.global_params[key] = value

@app.post("/plastimatch_register")
def register_api(
    all_registration_inputs: Inputs_register
    ) -> None:
    r"""
    ### Purpose:
        - To run image registration using pyplastimatch.
    
    ### Inputs:
        - all_registration_inputs: an instance of Inputs_register containing the input parameters for the registration.
    """
    print(f"static image: {all_registration_inputs.global_params['fixed']}")
    print(f"moving image: {all_registration_inputs.global_params['moving']}")
    print(f"output image: {all_registration_inputs.global_params['image_out']}")
    print(f"output vf: {all_registration_inputs.global_params['vf_out']}")
    register(all_registration_inputs.global_params, all_registration_inputs.stage_params_list)

class Inputs_convert(BaseModel):
    r"""
    ### Purpose:
        - To define the input parameters for running the convert command of pyplastimatch.
    
    ### Attributes:
        - options: a dictionary containing the options for the convert command.
        - input_file: the input file for the convert command.
    """
    pth_input: Path | str = None
    pth_output: Path | str = None
    # these attributes will be filled from the options
    xf: Path | str = None

    def __init__(self, **data):
        dir_temp_data = Path(__file__).parent.joinpath("temp_data")
        for key, value in data.items():
            if isinstance(value, str):
                if "temp_data/registration/" in value:
                    value = value.split("temp_data/registration/")[-1]
                value = dir_temp_data.joinpath(value)
            data[key] = value
        super().__init__(**data)

@app.post("/plastimatch_convert")
def convert_api(
    all_convert_inputs: Inputs_convert
    ) -> None:
    r"""
    ### Purpose:
        - To run the convert command of pyplastimatch.
    ### Inputs:
        - all_convert_inputs: an instance of Inputs_convert containing the input parameters for the convert command.    
    """
    from pyplastimatch import convert
    convert(
        input=all_convert_inputs.pth_input,
        output_img=all_convert_inputs.pth_output,
        xf=all_convert_inputs.xf
    )

def test_register_api():
    pth_static = "../temp_data/static.nrrd"
    pth_moving = "../temp_data/moving.nrrd"
    pth_output = "../temp_data/registered.nrrd"
    vf_out = "../temp_data/vf.nrrd"

    global_params = {
        "fixed" : f"{pth_static}",
        "moving" : f"{pth_moving}",
        "image_out" : f"{pth_output}",
        "vf_out" : f"{vf_out}",
    }

    stage_params_list = [
        {
            "xform": "bspline"
        }
    ]
    inputs = Inputs_register(global_params=global_params, stage_params_list=stage_params_list)
    register_api(inputs)

def test_convert_api():
    pth_input = "../temp_data/moving.nrrd"
    pth_output = "../temp_data/warped.nrrd"
    xf = "../temp_data/vf.nrrd"
    inputs = Inputs_convert(pth_input=pth_input, pth_output=pth_output, xf=xf)
    convert_api(inputs)

if __name__ == "__main__":
    # test_register_api()
    test_convert_api()