```
    _/_/_/            _/        _/  _/                  _/_/_/  _/        _/_/_/   
  _/        _/  _/_/        _/_/_/  _/  _/    _/      _/        _/          _/      
 _/  _/_/  _/_/      _/  _/    _/  _/  _/    _/      _/        _/          _/       
_/    _/  _/        _/  _/    _/  _/  _/    _/      _/        _/          _/        
 _/_/_/  _/        _/    _/_/_/  _/    _/_/_/        _/_/_/  _/_/_/_/  _/_/_/
                                          _/
                                     _/_/            for i18n JSON
```
# Usage
You can download the complete source code and build executable on your own, or if you use **Microsoft Windows** as operating system, you can download the executable file from the **Executables** folder. This **CLI** try parse and import all json files from the root path, and set the **Path** in **Gridly**
```
usage: gridlyi18njson.exe [-h] [-c] [-s SOURCELANGUAGE] [-v] method rootPath viewId apiKey

Import / Export i18n JSON files

positional arguments:
  method                Method can be 'import' or 'export' depends on what you would like to do
  rootPath              The root path where you have the JSON files, it get all JSON files and
                        try to import them, on export it saves the files to the given path with
                        the same structure
  viewId                ID of the view where you want to import/export the file
  apiKey                API key you obtained in Gridly

options:
  -h, --help            show this help message and exit
  -c, --generatecolumns
                        If you use this switch, it will generate language columns if they do
                        not exist for the language you have in the json
  -s SOURCELANGUAGE, --sourcelanguage SOURCELANGUAGE
                        You can define the source language, if you set, the CLI will try to tie
                        dependencies to this language
  -v, --verbose         Increase output verbosity
```
You can get the help anytime by call the executable with --help flag

## Example command for import
```
.\gridlyi18njson.exe import . 9982tis71srvj kv5gmct471sk6i -c -s "en"

```
- **.\gridlyi18njson.exe** is the name of the executable file
- **import** is the command to call the import of the files into the **View**
- **.** is the root directory, when you use the dot, it will use the executable file path as rootpath to import the files from this folder into **View**
- **9982tis71srvj** is the **View ID**
- **kv5gmct471sk6i** is the **Api Key**
- **-c** if you set this flag, the **CLI** will create the language columns automatically in your **View**
- **-s "en"** if you set this, it will make this language as source language in your **View** and set the dependencies \
### Response of import
```
{
    "status": "importResponse",
    "totalNumberOfFiles": 18,
    "results": [
        {
            "succeed": {
                "numberOfFiles": 18,
                "files": [
                    {
                        "fileName": "D:\\Gridly\\i18njson\\test.json",
                        "numberOfRecords": 12
                    },
                    {
                        "fileName": "D:\\Gridly\\i18njson\\Executables\\test.json",
                        "numberOfRecords": 12
                    }
                ]
            },
            "failed": {
                "numberOfFiles": 0,
                "files": []
            }
        }
    ]
}
```



## Example command for export
```
.\gridlyi18njson.exe export . 9982tis71srvj kv5gmct471sk6i

```
- **.\gridlyi18njson.exe** is the name of the executable file
- **export** is the command to call the export of the files from the **View**
- **.** is the root directory, when you use the dot, it will use the executable file path as rootpath to export the files from the **View**
- **9982tis71srvj** is the **View ID**
- **kv5gmct471sk6i** is the **Api Key** \
### Response of export

```
{
    "status": "exportResponse",
    "totalNumberOfFiles": 9,
    "results": [
        {
            "succeed": {
                "numberOfFiles": 9,
                "files": [
                    {
                        "fileName": "D:\\Gridly\\i18njson\\Executables/test.json",
                        "numberOfRecords": 12
                    },
                    {
                        "fileName": "D:\\Gridly\\i18njson\\export/test.json",
                        "numberOfRecords": 11
                    }
                ]
            },
            "failed": {
                "numberOfFiles": 0,
                "files": []
            }
        }
    ]
}
```