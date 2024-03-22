import pytest
from code_crafter import Code, File


@pytest.fixture
def sample_document():
    source_code = """
my_list = [1, 2, 3, 'a']
my_dict = {'key': 'value', 'my': 'val', 'num': 42}
my_set = {1, 2, 3}
"""
    return Code(source_code)


@pytest.fixture
def temp_python_file(tmp_path):
    # Create a temporary Python file for testing
    temp_file = tmp_path / "test_file.py"
    temp_file.write_text("""
my_list = [1, 2, 3]
my_dict = {'key': 'value'}
""")
    return str(temp_file)


def test_dict_pop(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    assert my_dict.pop('key').value == 'value'
    assert 'key' not in str(sample_document)


def test_dict_update_with_dict(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.update({'new_key': 123})
    assert "'new_key': 123" in str(sample_document)


def test_dict_update_with_kwargs(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.update(new_key2=456)
    assert "'new_key2': 456" in str(sample_document)


def test_dict_clear(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.clear()
    assert "{}" in str(sample_document)


def test_dict_get_existing_key(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    assert my_dict.get('key').value == 'value'


def test_dict_get_non_existing_key(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    assert my_dict.get('nonexistent', default='default') == 'default'


def test_list_pop(sample_document):
    my_list = sample_document.find_list('my_list')
    assert my_list.pop(0).value == 1
    assert "[2, 3, 'a']" in str(sample_document)


def test_list_append(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.append('b')
    assert "'b'" in str(sample_document)


def test_list_remove(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.remove(2)
    assert "[1, 3, 'a']" in str(sample_document)


def test_list_clear(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.clear()
    assert "[]" in str(sample_document)


def test_list_reverse(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.reverse()
    expected_output = """
my_list = ['a', 3, 2, 1]
my_dict = {'key': 'value', 'my': 'val', 'num': 42}
my_set = {1, 2, 3}
"""
    assert str(sample_document).strip() == expected_output.strip()



def test_list_extend(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.extend(['b', 'c'])
    expected_output = """
my_list = [1, 2, 3, 'a', 'b', 'c']
my_dict = {'key': 'value', 'my': 'val', 'num': 42}
my_set = {1, 2, 3}
"""
    assert str(sample_document).strip() == expected_output.strip()


def test_list_insert(sample_document):
    my_list = sample_document.find_list('my_list')
    my_list.insert(1, 'b')
    expected_output = """
my_list = [1, 'b', 2, 3, 'a']
my_dict = {'key': 'value', 'my': 'val', 'num': 42}
my_set = {1, 2, 3}
"""
    assert str(sample_document).strip() == expected_output.strip()


def test_set_add(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.add(4)
    expected_output_contains = "my_set = {1, 2, 3, 4}"
    assert expected_output_contains in str(sample_document)


def test_set_add_copy(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.add(3)
    expected_output_contains = "my_set = {1, 2, 3}"
    assert expected_output_contains in str(sample_document)


def test_set_remove_existing_element(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.remove(3)
    expected_output_contains = "my_set = {1, 2}"
    assert expected_output_contains in str(sample_document)


def test_set_discard_existing_element(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.discard(3)
    expected_output_contains = "my_set = {1, 2}"
    assert expected_output_contains in str(sample_document)


def test_set_discard_non_existing_element(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.discard(10)  # Should not modify the set
    expected_output_contains = "my_set = {1, 2, 3}"
    assert expected_output_contains in str(sample_document)


def test_set_update(sample_document):
    my_set = sample_document.find_set('my_set')
    my_set.update([4, 5])
    expected_output_contains = "my_set = {1, 2, 3, 4, 5}"
    assert expected_output_contains in str(sample_document)


def test_file_context_manager_modifies_file(temp_python_file):
    # Use the context manager to modify the file
    with File(temp_python_file) as file:
        file.find_list("my_list").append(4)
        file.find_dict("my_dict").update({"new_key": "new_value"})

    # Read the file back to check if changes were applied
    with open(temp_python_file, "r") as f:
        content = f.read()

    # Assert that the list and dictionary have been modified as expected
    assert "my_list = [1, 2, 3, 4]" in content
    assert 'my_dict = {"key": "value", "new_key": "new_value"}' in content


