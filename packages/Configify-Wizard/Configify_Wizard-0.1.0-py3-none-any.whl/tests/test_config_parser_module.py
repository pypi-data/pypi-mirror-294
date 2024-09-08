import os
import pytest
import json
import yaml
from config_parser_module.config_reader import ConfigParserModule

@pytest.fixture
def config_parser():
    return ConfigParserModule()

def test_flatten_dict(config_parser):
    input_dict = {
        'section1': {'key1': 'value1', 'key2': 'value2'},
        'section2': {'key3': 'value3'}
    }
    expected_output = {
        'section1.key1': 'value1',
        'section1.key2': 'value2',
        'section2.key3': 'value3'
    }
    assert config_parser.flatten_dict(input_dict) == expected_output

def test_read_yaml(config_parser, tmp_path):
    yaml_data = {'section': {'key1': 'value1', 'key2': 'value2'}}
    yaml_file = tmp_path / "test.yaml"
    
    with open(yaml_file, 'w') as f:
        yaml.dump(yaml_data, f)
    
    result = config_parser.read_yaml(str(yaml_file))
    expected = {'section.key1': 'value1', 'section.key2': 'value2'}
    assert result == expected

def test_read_cfg(config_parser, tmp_path):
    cfg_data = "[section]\nkey1=value1\nkey2=value2"
    cfg_file = tmp_path / "test.cfg"
    
    with open(cfg_file, 'w') as f:
        f.write(cfg_data)

    result = config_parser.read_cfg(str(cfg_file))
    expected = {'section.key1': 'value1', 'section.key2': 'value2'}
    assert result == expected

def test_write_json(config_parser, tmp_path):
    config_parser.config_dict = {'key1': 'value1', 'key2': 'value2'}
    json_file = tmp_path / "test.json"
    
    config_parser.write_json(str(json_file))
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    assert data == config_parser.config_dict

def test_write_env(config_parser, tmp_path):
    config_parser.config_dict = {'key1': 'value1', 'key2': 'value2'}
    env_file = tmp_path / ".env"
    
    config_parser.write_env(str(env_file))
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    assert "key1='value1'" in content
    assert "key2='value2'" in content

def test_set_os_env(config_parser):
    config_parser.config_dict = {'key1': 'value1', 'key2': 'value2'}
    
    config_parser.set_os_env()
    
    assert os.environ['key1'] == 'value1'
    assert os.environ['key2'] == 'value2'
