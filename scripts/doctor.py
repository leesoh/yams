"""
This script parses the docs.json file from all YAMS modules and then creates a
single Markdown file. Each module is categorized using PTES phases.
"""

import json
import os
import sys

root_dir = sys.path[0]
doc_filename = 'docs.json'
module_doc = 'module_docs.md'
doc_dic = {
    'intelligence-gathering': [],
    'vulnerability-analysis': [],
    'post-exploitation': [],
    'exploitation': [],
    'reporting': []
}


def json_to_dict(json_file):
    """
    Takes JSON file and returns a dict
    """
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
            return data
        except Exception as err:
            print('[-] Failed to load JSON: {0}'.format(err))


def generate_doc(doc_dic):
    """
    Takes in the dict containing all docs, parses it, then generates beautiful
    Markdowny documentation
    """
    module_string = ''
    for category in doc_dic:
        print('[*] Now processing {0}'.format(category))
        nice_title = category.replace('-', ' ').title()
        module_string += '# ' + nice_title + '\n'
        for module in doc_dic[category]:
            print('[*] Now processing {0}'.format(module['module_name']))
            module_string += dict_to_md(module)
    print('[*] Writing results to {0}'.format(module_doc))
    with open(module_doc, 'a') as f:
        f.write(module_string)
        f.write('\n')


def dict_to_md(dict):
    """
    Parses a dict into Markdown
    """
    print('[*] Parsing documentation for {0}'.format(dict['module_name']))
    module_md = '## ' + dict['module_name'] + '\n'
    module_md += '**Module Author:** ' + dict['module author'] + '\n\n'
    module_md += '**Last Updated:** ' + dict['updated'] + '\n\n'
    module_md += '**Original URL:** ' + dict['url'] + '\n\n'
    module_md += dict['description'] + '\n'
    module_md += '\n'
    return module_md


def main():
    try:
        os.remove(module_doc)
        print('[*] Overwriting old module documentation')
    except Exception:
        print('[-] Old documentation not found')
        pass

    print('[*] Herding documentation')
    for root, directories, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == doc_filename:
                filepath = os.path.join(root, filename)
                print('[+] Found docs: {0}'.format(filepath))
                dict = json_to_dict(filepath)
                if dict['category'] == 'intelligence-gathering':
                    doc_dic['intelligence-gathering'].append(dict)
                elif dict['category'] == 'vulnerability-analysis':
                    doc_dic['vulnerability-analysis'].append(dict)
                elif dict['category'] == 'exploitation':
                    doc_dic['exploitation'].append(dict)
                elif dict['category'] == 'post-exploitation':
                    doc_dic['post-exploitation'].append(dict)
                elif dict['category'] == 'reporting':
                    doc_dic['reporting'].append(dict)
    generate_doc(doc_dic)


if __name__ == '__main__':
    main()
