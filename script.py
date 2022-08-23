import os
import questionary
from templateframework.metadata import Metadata

def run(metadata: Metadata = None):

    def find_jar():
        import glob
        home = os.path.expanduser('~')

        for file in glob.glob(home + "/.stk/stacks/*/plugin-asniffer/asniffer.jar"):
            return os.path.abspath(file)

    def run_cmd(command):
        import subprocess
        result = subprocess.run(command,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True)
        return result

    def run_inside_a_stack():
        dir_jar = find_jar()
        target_project = str(metadata.target_path)
        return ["java", "-jar", dir_jar, "-p", target_project]

    def run_outsite_a_stack():
        dir_jar = os.path.join(str(metadata.target_path), str(metadata.component_path), "asniffer.jar")
        
        target_project = questionary.path("What's the path to the project you want to analyze?").ask()

        return ["java", "-jar", dir_jar, "-p", target_project]

    questionary.print("Searching for annotations usage..")

    command = None
    command = run_outsite_a_stack()

    result = run_cmd(command)

    if result.returncode == 0:
        questionary.print("Output written at plataforma-treino-lms.json")
    else:
        for item in result.stderr.split("\n"):
           questionary.print(item)
            
    return metadata