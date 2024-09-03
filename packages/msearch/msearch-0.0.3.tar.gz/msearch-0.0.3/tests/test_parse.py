import pytest
from msearch.parse import mparse

# Test data
JSON_STRING = '{"key1": "value1", "key2": 42}'
ROS2_STRING = "key1:=value1 key2:=42"
KEY_VALUE_STRING = "key1=value1 key2=42"
COMMAND_LINE_STRING = "--key1 value1 --key2 42"
YAML_STRING = "key1: value1\nkey2: 42"

@pytest.fixture
def test_files(tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text(JSON_STRING)
    
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(YAML_STRING)
    
    ros_file = tmp_path / "test.ros"
    ros_file.write_text(ROS2_STRING)
    
    return {"json": json_file, "yaml": yaml_file, "ros": ros_file}

def test_parse_json():
    result = mparse(JSON_STRING)
    assert result == {"key1": "value1", "key2": 42}

def test_parse_ros2():
    result = mparse(ROS2_STRING)
    assert result == {"key1": "value1", "key2": "42"}

def test_parse_key_value():
    result = mparse(KEY_VALUE_STRING)
    assert result == {"key1": "value1", "key2": "42"}

def test_parse_command_line():
    result = mparse(COMMAND_LINE_STRING)
    assert result == {"key1": "value1", "key2": "42"}

def test_parse_yaml():
    result = mparse(YAML_STRING)
    assert result == {"key1": "value1", "key2": 42}

def test_parse_json_file(test_files):
    result = mparse(str(test_files["json"]))
    assert result == {"key1": "value1", "key2": 42}

def test_parse_yaml_file(test_files):
    result = mparse(str(test_files["yaml"]))
    assert result == {"key1": "value1", "key2": 42}

def test_parse_ros_file(test_files):
    result = mparse(str(test_files["ros"]))
    assert result == {"key1": "value1", "key2": "42"}

def test_parse_empty_string():
    with pytest.raises(ValueError):
        mparse("")

def test_parse_unsupported_format():
    with pytest.raises(ValueError):
        mparse("This is not a supported format")

@mparse
def decorated_function(**kwargs):
    return kwargs

def test_mparse_as_decorator():
    result = decorated_function("key1:=value1 key2:=42")
    assert result == {"key1": "value1", "key2": "42"}

def test_mparse_as_decorator_with_additional_kwargs():
    result = decorated_function("key1:=value1", key2="42")
    assert result == {"key1": "value1", "key2": "42"}
