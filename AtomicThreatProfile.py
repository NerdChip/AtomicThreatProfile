# Author: Gamu Manungo | Nerdchip | @NagaiFudo
# Python3
# description: script that creates custom adversary profiles for use in Caldera using json data from CVC
# Script requires Caldera to be installed on ths system
# version: 1.3

# imported modules
import json
import os
import yaml
import argparse
import inquirer
import uuid
import pyinputplus as pyip


# function that checks if the file passed exists in the current working directory.
def file_check(file):
    directory = os.listdir(os.getcwd())

    if file not in directory:
        print("[!] Could Not Find File In The Current Working Directory: ", file)
        exit()
    elif file in directory:
        print("[>] Located File In Current Working Directory")
    else:
        print("[!] Error Occurred Whilst Trying to Locate File In Current Directory")
        exit()

    return file


# Function that locates Caldera ability yaml files stored in stockpile plugin
def find_all_files(directory):
    all_files = []

    print("[>] Locating Yaml Ability files ")

    for root, dirs, files in os.walk(directory):
        for yaml_file in files:
            filelocal = os.path.join(root, yaml_file)
            if filelocal.endswith(".yml") or filelocal.endswith(".yaml"):
                all_files.append(filelocal)

    if len(all_files) == 0:
        print("[!] No Caldera Yaml Ability Files Detected - Please Verify Caldera Installation")
        exit()
    elif len(all_files) > 0:
        print(f"[>] {len(all_files)} Files Located ")

    return all_files


# Function that looks for Caldera stockpile directory on the system
def find_stockpile_dir():
    path = r"/"
    located = False
    stockpile_root = None

    for root, dirs, files in os.walk(path):
        if root.endswith("stockpile/data/abilities"):
            stockpile_root = root
            print("[>] Located Stockpile Directory:  ", stockpile_root)
            located = True

    if not located or stockpile_root is None:
        print("[!] Unable To Locate Required Stockpile Directory Please Validate Caldera Installation")
        exit()

    return stockpile_root


# Function that gets the techniques referenced within the CVC data
def get_techniques(file):
    techniques = []

    validated_file = file_check(file)

    with open(validated_file, "r") as data:
        try:
            json_data = json.loads(data.read())
            threat_techniques = json_data["techniques"]
            print("[>] File Successfully Loaded, Extracting Adversary Techniques")
        except json.decoder.JSONDecodeError:
            print("[!] Unable to load file please check file format")
            exit()

        for technique in threat_techniques:
            techniques.append(technique["techniqueID"])

    return techniques


# Function created to validate user platform input
def validate_platform(user_input):
    options = ["windows"]
    selection = None

    if user_input in options:
        print("[>] Valid Platform Selected: ", user_input)
        selection = user_input
    elif user_input not in options or user_input is None:
        print("[>] You have selected a platform that is not supported AtomicThreatProfile will default "
              "to \"all\" do you wish to continue?: ")
        user_response = pyip.inputYesNo(prompt="Please input yes/no: ")
        if user_response == "no":
            exit()
        elif user_response == "yes":
            print("[>] Proceeding with default all platform value")
            selection = "all"

    return selection


# Function that generates the custom adversary yaml file to be read by Caldera
def generateadversaryfile(group_name, techniques):
    print("[>] Generating New Adversary Yaml File")

    generated_id = uuid.uuid1()

    located = False

    adversary_stockpile = None

    generated_identifier = f"{generated_id}-{str(group_name).upper()}"

    new_yaml = {'id': generated_identifier,
                'name': group_name,
                'description': "Custom adversary threat profile created using AtomticThreatProfile",
                'atomic_ordering': techniques}

    file = open(f"{generated_identifier}.yml", "w")
    yaml.dump(new_yaml, file, sort_keys=False, default_flow_style=False, explicit_start=True)
    file.close()
    print("[>] Adversary Yaml File Created Successfully")

    print("[>] Locating Stockpile Adversary Directory")

    for root, dirs, files in os.walk("/"):
        if root.endswith("stockpile/data/adversaries"):
            located = True
            adversary_stockpile = root
            print("[>] Stockpile Directory Located")

    if located:
        print("[>] Moving File To Stockpile Adversaries Directory")
        os.rename(f"{generated_identifier}.yml", f"{adversary_stockpile}/{generated_identifier}.yml")
        print("[>] File Successfully Moved To Stockpile Adversaries Directory")
    elif not located or adversary_stockpile is None:
        print("[!] Unable To Locate Required Stockpile Directory Please Validated Caldera installation")
        print(f"[!] Created Yaml file Has Not Been Moved, File Can Be Found In Following Directory: {os.getcwd()}")
        exit()

    return


def main():
    parser = argparse.ArgumentParser(
        description="Python Script that creates custom adversary profiles for use in caldera")
    parser.add_argument("-f", "--file", help="Name of the saved json file for chosen threat group",
                        required=True)
    parser.add_argument("-t", "--threatgroup",
                        help="Name of the threat group, this is the name that will appear in caldera", required=True)
    parser.add_argument("-p", "--platform",
                        help="Specifies a platform related to techniques i.e windows, default is all platforms",
                        dest='platform')
    args = parser.parse_args()

    filename = args.file
    threat_group_name = args.threatgroup
    platform = args.platform

    print(r"""

          _                  _   _______ _                    _   _____            __ _ _      
     /\  | |                (_) |__   __| |                  | | |  __ \          / _(_) |     
    /  \ | |_ ___  _ __ ___  _  ___| |  | |__  _ __ ___  __ _| |_| |__) | __ ___ | |_ _| | ___ 
   / /\ \| __/ _ \| '_ ` _ \| |/ __| |  | '_ \| '__/ _ \/ _` | __|  ___/ '__/ _ \|  _| | |/ _ \
  / ____ \ || (_) | | | | | | | (__| |  | | | | | |  __/ (_| | |_| |   | | | (_) | | | | |  __/
 /_/    \_\__\___/|_| |_| |_|_|\___|_|  |_| |_|_|  \___|\__,_|\__|_|   |_|  \___/|_| |_|_|\___|



  Gamu Manungo 
  twitter: @NagaiFudo

    """)

    print("[>] Executing Program")

    adversary_techniques = get_techniques(filename)  # List of techniques contained in CVC data.
    stockpile_directory = find_stockpile_dir()  # Locate Stockpile directory, Caldera abilities location.
    find_yaml_files = find_all_files(stockpile_directory)  # passing the stockpile directory, find abilities available.
    platform_selection = validate_platform(str(platform).lower())  # user input validation
    technique_id_match = []
    non_match = []
    no_technique_id = []
    adversary = {}
    technique_match_attributes = []
    all_t = []
    all_techniques = []

    print("[>] Filtering Information Contained in Yaml Files")
    # open each Caldera yaml file and read the contents.
    for yaml_file in find_yaml_files:
        try:
            with open(yaml_file, "r", encoding='utf-8') as stream:
                yamlload = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(f"[!] Unable To Load The Following Yaml File: {yaml_file} | {error}")
            pass
        # obtain required data from yaml files, data structure is different for some files, strangely.
        for yaml_object in yamlload:
            try:
                ability_platform = yaml_object["platforms"]
                i_d = yaml_object["id"]
                nma = yaml_object["name"]
                atomic_technique = yaml_object["technique"]["attack_id"]
                name = yaml_object["technique"]["name"]
            except KeyError:
                i_d = yaml_object["id"]
                atomic_technique = yaml_object["technique_id"]
                name = yaml_object["technique_name"]
                ability_platform = yaml_object["executors"][0]["platform"]
                nma = yaml_object["name"]

            if platform_selection == "windows":
                if "windows" in ability_platform:
                    if atomic_technique in adversary_techniques:
                        technique_id_match.append(atomic_technique)
                        adversary[f"{atomic_technique} {name}"] = []
                        technique_match_attributes.append([f"{atomic_technique} {name}", nma, i_d])
                    elif atomic_technique not in adversary_techniques:
                        non_match.append(atomic_technique)

            elif platform_selection == "all":
                if atomic_technique in adversary_techniques:
                    technique_id_match.append(atomic_technique)
                    adversary[f"{atomic_technique} {name}"] = []
                    technique_match_attributes.append([f"{atomic_technique} {name}", nma, i_d])
                elif atomic_technique not in adversary_techniques:
                    non_match.append(atomic_technique)
            else:
                print("[!] Unable to process selected platform ERROR - please check input data provided")

    for non_tech in adversary_techniques:
        if non_tech in non_match:
            no_technique_id.append(non_tech)

    print("[>] Calculating Techniques Available In Caldera For Threat Profile Generation...")
    print(f"[>] {len(adversary_techniques)} Techniques Identified Within Threat Group File")
    print(f"[>] {len(technique_id_match)} Techniques Found In Caldera Based On Technique ID")
    print(f"[>] {len(no_technique_id)} Techniques Not In Caldera Based On Technique ID")

    if len(technique_id_match) == 0:
        print("[!] No Techniques Are Present In Caldera, Program Will Now Exit")
        exit()

    for technique in technique_match_attributes:
        if technique[0] in adversary.keys():
            adversary[technique[0]].append([technique[1], technique[2]])

    for key, value in adversary.items():
        technique_name = key
        technique_values = value

        questions = [
            inquirer.Checkbox('Technique Choice',
                              message=f"Please select Technique For {technique_name}:",
                              choices=technique_values,
                              ),
        ]

        answer = inquirer.prompt(questions)
        print(f"[>]User Selected:  {answer['Technique Choice']}")

        # don`t think this is required next version will work to remove this

        all_techniques.append(answer['Technique Choice'])

        print("[>] Technique Selection Complete")

    for list_tech in all_techniques:
        techs = list_tech
        for tech in techs:
            all_t.append(tech[1])

    generateadversaryfile(threat_group_name, all_t)


if __name__ == "__main__":
    main()
