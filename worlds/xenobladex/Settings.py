import settings


class XenobladeXSettings(settings.Group):
    class Executable(settings.UserFilePath):
        is_exe = True

    executable: Executable = Executable("Cemu")
