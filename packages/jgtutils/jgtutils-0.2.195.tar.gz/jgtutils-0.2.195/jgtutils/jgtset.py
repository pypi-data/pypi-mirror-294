import os
import sys
import json
import ruamel.yaml;yaml:ruamel.yaml.YAML = ruamel.yaml.YAML()
from io import StringIO
import tempfile

import dotenv


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from jgtcliconstants import JGTSET_CLI_DESCRIPTION, JGTSET_CLI_EPILOG, JGTSET_CLI_PROG_NAME,_JGTSET_EXCLUDED_ENV_EXPORT_KEYS
from jgtenv import get_dotenv_jgtset_export_path, is_dotjgt_env_sh_exists, load_dotjgt_env_sh
from jgterrorcodes import JGTFILES_EXIT_ERROR_CODE, JGTSETTING_EXIT_ERROR_CODE

import jgtcommon

def parse_args():

    parser = jgtcommon.new_parser(JGTSET_CLI_DESCRIPTION, JGTSET_CLI_EPILOG,prog=JGTSET_CLI_PROG_NAME, enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    parser.add_argument('-E','-env','--export-env', action='store_true', help='Export settings as environment variables')
    #env keys to export
    parser.add_argument('-K','-keys','--keys', nargs='+', help='Export only the specified keys as environment variables')
    
    parser.add_argument('-J','-json','--json', action='store_true', help='Print as JSON')
    
    parser.add_argument('-Y','--yml','--yaml', action='store_true', help='Print as YAML')
    
    parser.add_argument('-S','--silent', action='store_true', help='silent output')
    
    #view list
    parser.add_argument('-V','--view', action='store_true', help='View settings list')
    
    #add -O --output to specify the env file to export to instead of the default
    parser.add_argument('-O','--output', help='Specify the output env file to export to')
    
    #-U --update-config _config.yml jgt:

    parser.add_argument('-U', '--update', nargs='*', help='Update the specified yaml file with the jgt settings', metavar=('target_yaml_file', 'target_key'),required=False)
    
    #-R --reset-config _config.yml jgt:
    parser.add_argument('-R', '--reset-jgt-config', action='store_true', help='Reset the specified yaml file with the jgt settings', required=False)

    
    args = jgtcommon.parse_args(parser)
    return args


def _init_dotenv_jgt_export_file(env_file=None):
    
    try:
        jgt_batch_path = get_dotenv_jgtset_export_path() if not env_file else env_file
        with open(jgt_batch_path,"w") as f:
            #f.write("#!/bin/bash\n")
            f.write("# This file is generated by JGTSettingsCLI (jgtset)\n")
            f.write("# It should not be edited manually\n" if not env_file else f"# It normally should not be edited manually but it is a custom file, therefore you might if you know what you are doing\n")
            #f.write("# This file is used to fix the list export issue in the environment variables\n")
            #f.write("# Load this file first and then load the .env or other environment variable files to ovveride.  This fixes the list export issue\n")
            
    except:
        exit(JGTFILES_EXIT_ERROR_CODE)



def _add_value_to_jgt_export_file(key,value,quiet=True,env_file=None):
    try:
        enquote = False
        var_type = type(value).__name__
        #print("key is of type:",var_type)
        fixed_value = value 
        if var_type == "bool":
            fixed_value = str(value).lower()
        else:
            if var_type == "list" or var_type == 'CommentedSeq':
                fixed_value = __format_list_to_string(value)
                enquote = True
                
        jgt_batch_path = get_dotenv_jgtset_export_path() if not env_file else env_file
        with open(jgt_batch_path,"a") as f:
            if enquote:
                append_line = f"{key}=\"{fixed_value}\"\n"
            else:
                append_line = f"{key}={fixed_value}\n"
            if not quiet:print(f"export {key}={fixed_value}")
            f.write(append_line.replace('""','"'))
    except:
        exit(JGTFILES_EXIT_ERROR_CODE)        

def export_keys_to_environ(_settings=None,keys=None,quiet=True,env_file=None,custom_path=None):
    _init_dotenv_jgt_export_file(env_file=env_file)
    _what_to_export = _get_data_filtered_by_exportable_keys(_settings, keys,custom_path)
    for key, value in _what_to_export.items():
        if key not in _JGTSET_EXCLUDED_ENV_EXPORT_KEYS:
            if keys is None:
                if value is not None:
                    _export_key(key, value,quiet,env_file=env_file)
            else:
                if key in keys:
                    _export_key(key, value,quiet,env_file=env_file)
    #run the batch file to fix the list export issue
    #os.system(f"source {_get_jgt_batch_filepath()}")
    #load using dotenv
    # for key in os.environ : 
    #     if key in settings:
    #         print(f"export {key}={os.getenv(key)}")
    # print("-------------------")
    #dotenv.load_dotenv(dotenv_path=get_jgt_env_export_path())
    # test_passed=True
    # for key in settings.keys():
    #     if not key in os.environ:
    #         test_passed=False
   
    # for key in os.environ : 
    #     if key in settings:
    #         value = os.getenv(key)
    #         os.environ[key] =value
    #         print(f"export {key}={value}")
    #         os.system(f"export {key}={value}")
    #print("Test passed:" if test_passed else "Test failed:")
    #print(os.getenv("columns_to_remove"))

def _export_key(key, value,quiet=True,is_subkey=False,env_file=None):
    if isinstance(value, dict): 
        #export key of the value as a string coma separated
        subkey_str_val='"' if not is_subkey else ""
        c=0
        for subkey, subvalue in value.items():
            delimiter = "," if c < len(value)-1 else ""
            subkey_var_name = f"{key}_{subkey}"
            subkey_str_val+=subkey+delimiter
            if isinstance(subvalue, dict):                
                _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
            else:
                os.environ[subkey_var_name] = str(subvalue)
                _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
                #if not quiet:print(f"export {key}_{subkey}={subvalue}")
            c+=1
        #os.environ[key] = subkey_str_val
        subkey_str_val+='"' if not is_subkey else ""
        if  not is_subkey and subkey_str_val != "":
            #if not quiet:print(f"export {key}={subkey_str_val}")
            _add_value_to_jgt_export_file(key,subkey_str_val,quiet,env_file=env_file)
    else:
        if isinstance(value, list):
            #if list contains dict, dont export
            if len(value) > 0 and isinstance(value[0], dict):
                for i in range(len(value)):
                    for subkey, subvalue in value[i].items():
                        subkey_var_name = f"{key}_{i}_{subkey}"
                        os.environ[subkey_var_name] = str(subvalue)
                        _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
                        #if not quiet:print(f"export {key}_{i}_{subkey}={subvalue}")
                return
            list_fixed = __format_list_to_string(value)
            os.environ[key] = list_fixed
            _add_value_to_jgt_export_file(key,value,quiet,env_file=env_file)
            #if not quiet:print(f"export {key}={list_fixed}")
        else:
            os.environ[key] = str(value)
            _add_value_to_jgt_export_file(key,value,quiet,env_file=env_file)
            #if not quiet:print(f"export {key}={value}")

def __format_list_to_string(value,enquote=True,single_quote=False):
    list_fixed='"' if not single_quote else "'"
    if not enquote:
        list_fixed=""
    c=0
    for v in value:
        delimiter = ","
        if c == len(value)-1:
            delimiter = ""
        list_fixed+=str(v)+delimiter
        c+=1
    list_fixed+='"' if not single_quote and enquote  else "'" if single_quote and enquote else ""
    
    return list_fixed


def dump_as_json_output(_settings=None,keys=None,custom_path=None):
    _what_to_export = _get_data_filtered_by_exportable_keys(_settings, keys,custom_path)
    return json.dumps(_what_to_export, indent=2)

def dump_as_yaml_output(_settings=None,keys=None,custom_path=None):
    _what_to_export = _get_data_filtered_by_exportable_keys(_settings, keys,custom_path)
    #output to temp file then read it back, fuckin issue
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w+') as temp_file:
        try:
            yaml.dump(_what_to_export, temp_file)
            temp_file.seek(0)
            stream_data = temp_file.read()
        except yaml.YAMLError as exc:
            print(exc)
    
    return stream_data

    # temp_file = tempfile.NamedTemporaryFile(delete=False)
    # temp_path = temp_file.name
    # with open(temp_path,'w') as stream:
    #     try:
    #         yaml.dump(_what_to_export,stream)
    #     except yaml.YAMLError as exc:
    #         print(exc)
    # with open(temp_path, 'r') as stream:
    #     try:
    #         stream_data = yaml.load(stream)
    #     except yaml.YAMLError as exc:
    #         print(exc)
    # print(type(stream_data))
    # return yaml.dump(stream_data)

def update_jgt_on_existing_yaml_file(target_filepath,_settings=None,keys=None,custom_path=None,target_key='jgt',add_on_only=True):
    jgtset_excluded=_JGTSET_EXCLUDED_ENV_EXPORT_KEYS
    if 'jgtset_excluded' in _settings:
        jgtset_excluded_=_settings['jgtset_excluded'].split(",")
        jgtset_excluded =jgtset_excluded+jgtset_excluded_
    
    jgt_yaml_content=dump_as_yaml_output(_settings,keys,custom_path)

    yaml_data_unfiltered=yaml.load(jgt_yaml_content)
    yaml_data=_get_data_filtered_by_exportable_keys(yaml_data_unfiltered, keys,custom_path)
    
    cfg={}
    with open(target_filepath, 'r') as stream:
        try:
            cfg = yaml.load(stream)
            #print(cfg)
        except yaml.YAMLError as exc:
            print(exc)
    
    
    if not add_on_only:
        cfg[target_key] = yaml_data
    else:
        if target_key in cfg:
            for key in yaml_data.keys():
                if key not in cfg[target_key]:
                    cfg[target_key][key] = yaml_data[key]
            #cfg[target_key].update(yaml_data)
        else:
            cfg[target_key] = yaml_data

    #clean up the excluded keys
    for key in jgtset_excluded:
        if key in cfg[target_key]:
            cfg[target_key].pop(key)
    
    os.rename(target_filepath, target_filepath+".bak")

    with open(target_filepath,'w') as temp_file:
        try:
            yaml.dump(cfg, temp_file)
            temp_file.seek(0)

        except yaml.YAMLError as exc:
            print(exc)

    with open(target_filepath, 'r') as stream:
        try:
            cfg = yaml.load(stream)
            #print(cfg)
        except yaml.YAMLError as exc:
            print(exc)
    return cfg
    
    

def _get_data_filtered_by_exportable_keys(data=None, keys=None,custom_path=None):
    if data is None:
        data = _load_settings(custom_path)
    _what_to_export = {}
    try:#jgtset_included
        if 'jgtset_included' in data and keys is None:
            keys=data['jgtset_included'].split(",")
    except:
        pass    
    try:#jgtset_included
        if 'JGTSET_INCLUDED' in os.environ and keys is None:
            keys=os.environ['JGTSET_INCLUDED'].split(",")
    except:
        pass
    if keys is not None:
        for key in keys:
            if key in data:
                _what_to_export[key] = data[key]
        for key in keys:
            if key not in _what_to_export and key in os.environ:
                _what_to_export[key] = os.environ[key]
        for key in keys:
            if key not in _what_to_export and is_dotjgt_env_sh_exists():
                load_dotjgt_env_sh()
                if key in os.environ:
                    _what_to_export[key] = os.environ[key]
    else:
        _what_to_export =data
    #remove keys that should not be exported using _JGTSET_EXCLUDED_ENV_EXPORT_KEYS
    for key in _JGTSET_EXCLUDED_ENV_EXPORT_KEYS:
        if key in _what_to_export:
            _what_to_export.pop(key)
    
    try:
        if os.environ['JGTSET_EXCLUDED']:
            for key in os.environ['JGTSET_EXCLUDED_ENV_EXPORT_KEYS'].split(","):
                if key in _what_to_export:
                    _what_to_export.pop(key)
    except:
        pass
    
    try:
        if 'jgtset_excluded' in data:
            for key in data['jgtset_excluded'].split(","):
                if key in _what_to_export:
                    _what_to_export.pop(key)
            _what_to_export.pop('jgtset_excluded')
    except:
        pass      
    return _what_to_export




def main():
    args = parse_args()
    env_flag = args.export_env
    json_flag = args.json
    yaml_flag = args.yml
    silent_flag = args.silent
    keys = args.keys
    output_file = args.output
    view_flag = args.view
    reset_jgt_flag = True if args.reset_jgt_config else False
    TARGET_YAML_FILE_DEFAULT = '_config.yml'
    TARGET_KEY_DEFAULT = 'jgt'
    target_yaml_file, target_key =TARGET_YAML_FILE_DEFAULT, TARGET_KEY_DEFAULT
    if hasattr(args,'update') and args.update is not None:
        if args.update == f'{TARGET_YAML_FILE_DEFAULT},{TARGET_KEY_DEFAULT}':
            target_yaml_file, target_key = TARGET_YAML_FILE_DEFAULT, TARGET_KEY_DEFAULT
        else:
            update_length = args.update.__len__()
            if update_length > 1:
                target_yaml_file, target_key = args.update.split(',')
            else:
                if update_length==1:
                    target_yaml_file = args.update[0]
                else:
                    target_yaml_file=TARGET_YAML_FILE_DEFAULT
                target_key = TARGET_KEY_DEFAULT
    else:
        target_yaml_file, target_key = None, None
    
    # if args.update:
    #     if len(args.update) == 0:
    #         target_yaml_file, target_key = '_config.yml', 'jgt'
    #     else:
    #         target_yaml_file, target_key = args.update
    try:
        
        print_output=   process_env(env_flag,keys=keys,json_flag=json_flag,yaml_flag=yaml_flag,silent_flag=silent_flag,output_file=output_file,view_flag=view_flag,target_yaml_file=target_yaml_file,target_key=target_key,reset_jgt_flag=reset_jgt_flag)
        
        print(print_output)
        
    except:
        print("Error loading settings")
        sys.exit(JGTSETTING_EXIT_ERROR_CODE)

def process_env(env_flag,keys=None,json_flag=False,yaml_flag=False,silent_flag=False,output_file=None,view_flag=False,custom_path=None,target_yaml_file=None,target_key=None,reset_jgt_flag=False):
    
    settings = _load_settings(custom_path)
    
    if view_flag:
        for key in settings.keys():
            print(key)
        return ""
    
    if env_flag and not json_flag and not yaml_flag and not target_yaml_file:
        export_keys_to_environ(settings,keys=keys,quiet=False if not silent_flag else True,env_file=output_file)
        return ""

    if target_yaml_file:
        updated_yaml_data = update_jgt_on_existing_yaml_file(target_yaml_file,settings,keys,target_key,add_on_only=not reset_jgt_flag)
        stream = StringIO()
        yaml.dump(updated_yaml_data, stream)
        print_output=stream.getvalue()
        return print_output
        

    print_output=""
    if yaml_flag:
        print_output = dump_as_yaml_output(settings,keys )
    else:
        print_output = dump_as_json_output(settings,keys )
    
    if env_flag: #Quiet export with other outputs
        export_keys_to_environ(settings,keys=keys,quiet=True,env_file=output_file)

    
    return print_output

def _load_settings(custom_path):
    return jgtcommon.get_settings(custom_path=custom_path)

if __name__ == '__main__':
    main()