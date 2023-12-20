import settings
from typing import Union

class XenobladeXSettings(settings.Group):
    class Executable(settings.UserFilePath):
        is_exe = True

    class InteractableServer(settings.Bool):
        """Keep server accessable for custom usage"""

    executable: Executable = Executable("Cemu")
    interactable_server: Union[InteractableServer, bool] = False
