from PyPlastimatch import register

def test_register():
    pth_static = ""
    pth_moving = ""
    pth_output = ""
    
    global_params = {
        "fixed" : f"{pth_static}",
        "moving" : f"{pth_moving}",
        "img_out" : f"{pth_output}",
    }
