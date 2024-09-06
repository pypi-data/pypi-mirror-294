import json
import os
from copy import deepcopy


def process_files(input_file, output_file, overwrite):
    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"File '{input_file}' does not exist.")
        return
    if os.path.isfile(output_file) and not overwrite:
        print(f"File '{output_file}' already exists.")
        return
    with open(input_file, 'r') as f:
        data = json.load(f)
    with open("temp.txt", 'w') as f:
        # Write terraform_version
        terraform_version = data['terraform_version']
        f.write(f'terraform_version = "{terraform_version}"\n\n')
          
        
        # Write variables
        try:
            variables = deepcopy(data['variables'])
            f.write('variables = ')
            for key in variables.keys():
                variables[key]["name"] = key
            f.write(json.dumps(variables, indent=4))
            f.write('#\n\n')
        except KeyError:
            pass
        
        
        
        # Write planned_values
        f.write('planned_values = ')
        planned_values = data['planned_values']
        
        try:
            outputs = planned_values["outputs"]
            for key in outputs.keys():
                outputs[key]["name"] = key
                del outputs[key]["type"]
            filtered_planned_values["outputs"] = outputs
        except KeyError:
            pass
        
        dict_ressources = dict()
        try:
            resources: list = deepcopy(planned_values["root_module"]["resources"])
            for resource in resources:
                dict_ressources[resource["address"]] = resource
        except KeyError:
            pass
        filtered_planned_values = dict()
        filtered_planned_values["resources"] = dict_ressources
        
        f.write(json.dumps(filtered_planned_values, indent=4))
        f.write('#\n\n')
        
        
        try:
            # Write resource_changes
            resource_changes = dict()
            for resource in  data['resource_changes']:
                resource_changes[resource["address"]] = resource
            f.write('resource_changes = ')
            f.write(json.dumps(resource_changes, indent=4))
            f.write('#\n\n')
        except KeyError:
            pass
        
        
        
        try:
            # Write resource_drift
            resource_drift = dict()
            for resource in  data['resource_drift']:
                resource_drift[resource["address"]] = resource
            f.write('resource_drift = ')
            f.write(json.dumps(resource_drift, indent=4))
            f.write('#\n\n')
        except KeyError:
            pass
        
        
        try:
            # Write output_changes      
            output_changes = deepcopy(data["output_changes"])
            for key in output_changes:
                output_changes[key] = {
                    "name": key,
                    "change": {
                        "actions" : output_changes[key]["actions"],
                        "after": output_changes[key]["after"],
                        "after_unknown": output_changes[key]["after_unknown"],
                        "before": output_changes[key]["before"],
                    }
                }
            f.write('output_changes = ')
            f.write(json.dumps(output_changes, indent=4))
            f.write('#\n\n')
        except KeyError:
            pass
        
        
        # Write the raw JSON data
        f.write('raw = ')
        f.write(json.dumps(data, indent=4))
        f.write('#\n')
    with open("temp.txt", 'r') as f:
        temp_data = f.readlines()
    with open(output_file, 'w') as f:
        new_lines = [temp_data[0]]
        for i in range(1, len(temp_data)):
            line = temp_data[i]
            if len(line) > 1 and line[-2] not in ("{", "[", ",", "#"):
                line = line[:-1] + ",\n"
            new_lines.append(line)
        f.writelines(new_lines)
    os.remove("temp.txt")
    print(f"Data processed and written to '{output_file}'.")
# Example usage
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process input and output files.')
    parser.add_argument('--infile', default='plan.json', help='Input file name (default: plan.json)')
    parser.add_argument('--outfile', default='mock-tfplan-v2.sentinel', help='Output file name (default: mock-tfplan-v2.sentinel)')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting the output file if it exists')
    args = parser.parse_args()
    process_files(args.infile, args.outfile, args.overwrite)

