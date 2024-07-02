import argparse
import os
import sys
from classes import ErrorResponseGenerator, methodResponse
import gridly_api_calls
import requests
import json
import helpers

#abel to pick a sinlge file or a folder path
#path to path column
#able to change sep char
#add optional for cahr encode


logo = """                                                                                    
     _/_/_/            _/        _/  _/                  _/_/_/  _/        _/_/_/   
  _/        _/  _/_/        _/_/_/  _/  _/    _/      _/        _/          _/      
 _/  _/_/  _/_/      _/  _/    _/  _/  _/    _/      _/        _/          _/       
_/    _/  _/        _/  _/    _/  _/  _/    _/      _/        _/          _/        
 _/_/_/  _/        _/    _/_/_/  _/    _/_/_/        _/_/_/  _/_/_/_/  _/_/_/       
                                          _/                                        
                                     _/_/            for i18n JSON                  
                                                                                        """

class CustomHelpParser(argparse.ArgumentParser):
    def print_help(self):
        super().print_help()  # Call the default help message printing
        self.extra_help_action()  # Perform your custom actions

    def extra_help_action(self):
        print(logo)

def import_i18njson(rootPath, viewId, apiKey, view, verbose=False, generatecolumns=False, sourcelanguage=None):
    response = methodResponse("importResponse")
    #we need to find all json file and send their path to the convert
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                transformResponse = helpers.convert_json_into_records(rootPath, filepath, viewId, apiKey, generatecolumns, view, sourcelanguage)
                if transformResponse['type'] == "OK":
                    gridly_api_calls.upload_records_into_gridly(viewId, apiKey, transformResponse['records'])
                    response.add_successful_file(transformResponse['filePath'], transformResponse['numOfRecords'])
                else:
                    response.add_failed_file(transformResponse['filePath'], transformResponse['message'])

    json_output = response.generate_json()
    print(json_output)


def export_i18njson(rootPath, viewId, apiKey):
    helpers.export_into_i18n_json(rootPath, viewId, apiKey)

def main():
    
    # Create the parser
    
    parser = argparse.ArgumentParser(description='Import / Export i18n JSON files')

    # Add arguments    
    parser.add_argument('method', type=str, help='Method can be import or export depends on what you would like to do')
    parser.add_argument('rootPath', type=str, help='The root path where you have the JSON files, it get all JSON files and try to import them, on export it saves the files to the given path with the same structure') 
    parser.add_argument('viewId', type=str, help='ID of the view where you want to import/export the file')
    parser.add_argument('apiKey', type=str, help='API key you obtained in Gridly')
    parser.add_argument('-c', '--generatecolumns', action='store_true', help='If you use this switch, it will generate language columns if they do not exist for the language you have in the json')
    parser.add_argument('-s', '--sourcelanguage', type=str, default=None, help='You can define the source language, if you set, the CLI will try to tie dependencies to this language')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    

    # Parse arguments
    if len(sys.argv) == 2:
        print(logo)
        parser.print_help()  # Manually call print_help if no arguments are given
        sys.exit()
    else:
        args = parser.parse_args()

    valid_request = True
    if args.method not in ["import", "export"]:
        print("Method argument is invalid, you can only use import or export")
        valid_request = False

    if not os.path.exists(args.rootPath) and args.method != "export":
        error_generator = ErrorResponseGenerator(404, "CLI", "File cannot be found")
        print(error_generator.get_response_json())
        valid_request = False

    # Check if Gridly credentials are fine and the view exists
    view = gridly_api_calls.get_view(args.viewId, args.apiKey)
    if isinstance(view, requests.Response) and view.status_code != 200:
        message = json.loads(view.text)["message"] if view.status_code != 401 else "Access denied"
        error_generator = ErrorResponseGenerator(view.status_code, "API", message)
        print(error_generator.get_response_json())
        valid_request = False

    if valid_request:
        if args.method == "import":
            import_i18njson(args.rootPath, args.viewId, args.apiKey, view, args.verbose, args.generatecolumns, args.sourcelanguage)
        if args.method == "export":
            export_i18njson(args.rootPath, args.viewId, args.apiKey)
    else:
        sys.exit()

if __name__ == '__main__':
    main()
