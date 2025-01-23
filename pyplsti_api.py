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
    def __init__(self, **data):
        super().__init__(**data)
        dir_temp_data = Path(__file__).parent.joinpath("temp_data")
        self.global_params["fixed"] = dir_temp_data.joinpath(self.global_params.get("fixed"))
        self.global_params["moving"] = dir_temp_data.joinpath(self.global_params.get("moving"))
        self.global_params["image_out"] = dir_temp_data.joinpath(self.global_params.get("image_out"))

app = FastAPI()

@app.post("/plastimatch_register")
def register_api(
    all_inputs: Inputs_register
    ) -> None:
    r"""
    Purpose:
        - To run image registration using pyplastimatch.
    """
    print(f"static image: {all_inputs.global_params['fixed']}")
    print(f"moving image: {all_inputs.global_params['moving']}")
    print(f"output image: {all_inputs.global_params['image_out']}")
    register(all_inputs.global_params, all_inputs.stage_params_list)


def test_register_api():
    pth_static = "static.nrrd"
    pth_moving = "moving.nrrd"
    pth_output = "registered.nrrd"

    global_params = {
        "fixed" : f"{pth_static}",
        "moving" : f"{pth_moving}",
        "image_out" : f"{pth_output}",
    }
    
    stage_params_list = [
        {
            "xform": "bspline"
        }
    ]
    inputs = Inputs_register(global_params=global_params, stage_params_list=stage_params_list)
    register_api(inputs)

if __name__ == "__main__":
    test_register_api()