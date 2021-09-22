from pathlib import Path

OUTPUT_FILE_DIRECTORY = '../_tools/output_files'

def generate_json(input_list):
    sample_structure = '"samples" : [ {0} ]'
    sample_entry = '{{ "language" : "en-US", "taggedText" : "{0}" }},'
    last_sample_entry = '{{ "language" : "en-US", "taggedText" : "{0}" }}'
    entries = []
    last_entry = len(input_list) - 1
    for i, e in enumerate(input_list):
        if i != last_entry:
            entries.append(sample_entry.format(e.replace('"', '')))
        else:
            entries.append(last_sample_entry.format(e.replace('"', '')))

    entry_string = ' '.join(entries)

    sample_structure = sample_structure.format(entry_string)

    return sample_structure

#codes_list = []
#with open('../_tools/input_files/cpt_codes.txt', 'r') as code_in_file:
#    codes = code_in_file.readlines()
#    for code in codes:
#        codes_list.append(code.strip())

#cpt_code_sample_json = generate_json(codes_list)
#with open(Path(OUTPUT_FILE_DIRECTORY, 'cpt_code_sample_json'), "w+") as code_out_file:
#    code_out_file.write(cpt_code_sample_json)

description_list = []
with open('../_tools/input_files/cpt_descriptions.txt', 'r') as description_in_file:
    codes = description_in_file.readlines()
    for code in codes:
        description_list.append(code.strip())

cpt_description_sample_json = generate_json(description_list)
with open(Path(OUTPUT_FILE_DIRECTORY, 'cpt_description_sample_json'), "w+") as description_out_file:
    description_out_file.write(cpt_description_sample_json)


