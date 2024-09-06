import sweatstack as ss
from jupyterlab.labapp import LabApp


def start_jupyterlab_with_oauth():
    ss.login()
    return LabApp.launch_instance()