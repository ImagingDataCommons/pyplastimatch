from pyplastimatch import register

def test_register():
    pth_static = "../data_test/registration-tutorial/t5.mha"
    pth_moving = "../data_test/registration-tutorial/t0.mha"
    pth_output = "../data_test/test_output/registered.nrrd"

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
    register(global_params, stage_params_list)

if __name__ == "__main__":
    test_register()