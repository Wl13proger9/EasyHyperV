import os



DEBUG_MODE   = False
PROJECT_PATH = os.path.abspath( os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") )


path_collection = {
    "dir": {
                "project":     PROJECT_PATH,
                "hypervisor":  os.path.join(PROJECT_PATH, "hv"),
                "build":       os.path.join(PROJECT_PATH, "build"), 
                "cli":         os.path.join(PROJECT_PATH, "cli"), 
        },

    "files": {
                "hypervisor":  os.path.join(PROJECT_PATH,"hv",   "hypervisor.py"),
                "cli":         os.path.join(PROJECT_PATH,"cli",  "cli.py"), 
                "build":       os.path.join(PROJECT_PATH,"build","build.py"),
        }
    }


if __name__ == "__main__":
    print("Hello World!")

