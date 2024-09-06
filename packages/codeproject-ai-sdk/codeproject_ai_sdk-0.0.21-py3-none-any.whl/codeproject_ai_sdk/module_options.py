# from __future__ import annotations
import os
import sys

from .module_logging import LogVerbosity

def _get_env_var(name: str, default: any = "") -> any:
    value = os.getenv(name, "")
    if value == "" and default != "":
        value = default
    return value

class ModuleOptions:
    """
    Helper methods to access options passed to modules
    """

    # TODO: make these instance, not class variables (ie do all of this inside
    # an __init__ method). This allows us to import this class without this
    # machinery being invoked until the caller needs it

    # You can't call ModuleOptions.getEnvVariable at the root of this class,
    # so the only option is to pull the guts of this method out and hack.
    @staticmethod
    def getEnvVariable(name: str, default: any = "") -> any:
        """ Returns the value of the environment with the given name """
        return _get_env_var(name, default)
    

    # Settings

    # Was this module launched by the server or launched externally (eg by a debugger)
    launched_by_server  = _get_env_var("CPAI_MODULE_SERVER_LAUNCHED", "false")

    # Directory containing the current python interpreter 
    python_dir          = os.path.dirname(sys.executable)

    # Path to the current module
    current_file_path   = os.path.dirname(__file__)
    module_path         = os.path.normpath(_get_env_var("CPAI_MODULE_PATH", os.getcwd()))

    # These can be read from the modulesettings.json file if we're keen
    module_id           = _get_env_var("CPAI_MODULE_ID",          None)
    module_name         = _get_env_var("CPAI_MODULE_NAME",        None)

    # If module ID and name weren't set, get it from the modulesettings file
    if not module_id or not module_name:
        try:
            with open(os.path.join(module_path, "modulesettings.json")) as json_file:
                # data = json.load(json_file)
                file_data = json_file.read()
                import commentjson
                data = commentjson.loads(file_data)

                module_id   = list(data["Modules"].keys())[0]
                module_name = list(data["Modules"].values())[0]["Name"]
        except Exception as ex:
            print(f"Unable to read module info in {module_path}")
            module_id   = os.path.basename(module_path)
            module_name = module_id

    queue_name          = _get_env_var("CPAI_MODULE_QUEUENAME",   module_id.lower() + "_queue")

    # Port the server listens on, both for clients and for backend modules
    port                = _get_env_var("CPAI_PORT",               "32168")

    # The path to the root folder containing the application
    server_root_path    = _get_env_var("CPAI_APPROOTPATH", None)

    # If path root not set, we start taking wild guesses
    if not server_root_path:
        root_path = os.path.normpath(os.path.join(module_path, "../../..")) # root/src/modules/module
        if root_path.lower().endswith("codeproject.ai-server"):
            server_root_path = root_path
        else:
            root_path = os.path.normpath(os.path.join(module_path, "../..")) # root/modules/module
            if root_path.lower().endswith("codeproject.ai-server"):
                server_root_path = root_path
            else:
                root_path = os.path.normpath(os.path.join(module_path, "..")) # CodeProject.AI-Modules/module
                if root_path.lower().endswith("codeproject.ai-modules"):
                    server_root_path = os.path.normpath(os.path.join(module_path, "../../CodeProject.AI-Server"))

    # How many tasks to spin up for a module
    parallelism         = _get_env_var("CPAI_MODULE_PARALLELISM", "0");

    # How much RAM is needed to perform tasks in this module?
    required_MB         = _get_env_var("CPAI_MODULE_REQUIRED_MB", "0");

    # Whether to *allow* support for GPU. Doesn't mean it's possibly it can or will
    # support GPU. More often used to disable GPU when a GPU causes problems
    enable_GPU         = _get_env_var("CPAI_MODULE_ENABLE_GPU",   "True")

    # Implementation specific GPU device name. Depends on hardware and library being
    # used. Generally not specified, so don't use _get_env_var (otherwise needless warnings)
    accel_device_name   = os.getenv("CPAI_ACCEL_DEVICE_NAME",     None) 

    # Whether or not to enable, disable or force half-precision operations. This
    # is module, library and hardware specific, but common for PyTorch
    half_precision      = _get_env_var("CPAI_HALF_PRECISION",     None) # will set to non-None in module_runner

    # Can be Quiet, Info or Loud. Module specific, requires module implementation
    log_verbosity       = _get_env_var("CPAI_LOG_VERBOSITY",      LogVerbosity.Quiet)

    # General purpose flags. These aren't currently supported as common flags
    # use_CUDA          = False
    # use_ROCm          = False
    # use_Coral         = False
    # use_ONNXRuntime   = False
    # use_OpenVINO      = False

    # We're hardcoding localhost because we have no plans to have the 
    # analysis services and the server on separate machines or containers.
    # At no point should any outside app have access to the backend 
    # services. It all must be done through the API.
    base_api_url        = f"http://localhost:{port}/v1/"

    # Normalise input
    launched_by_server  = str(launched_by_server).lower() == "true"
    port                = int(port) if str(port).isnumeric() else 32168
    enable_GPU          = str(enable_GPU).lower() == "true"
    required_MB         = int(required_MB) if str(required_MB).isnumeric() else 0
    parallelism         = int(parallelism) if str(parallelism).isnumeric() else 0

    # If a value was found but it was incorrect, ignore it
    if half_precision and half_precision not in [ "force", "enable", "disable" ]:
        half_precision = None

    if isinstance(log_verbosity, str):
        log_verbosity = LogVerbosity(log_verbosity.lower())
    elif not isinstance(log_verbosity, LogVerbosity):
        log_verbosity = LogVerbosity.Quiet
    if not log_verbosity:
        log_verbosity = LogVerbosity.Quiet

    if parallelism <= 0:
        if (sys.version_info.major >= 3 and sys.version_info.minor >= 13):
            parallelism = os.process_cpu_count() // 2
        else:
            parallelism = os.cpu_count() // 2