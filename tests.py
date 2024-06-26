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
def sample_document2():
    source_code = """
my_list = list(1, 2, 3, 'a')
my_dict = dict(key='value', my='val', num=42)
my_set = set(1, 2, 3)
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


def test_dict_pop2(sample_document2):
    my_dict = sample_document2.find_dict('my_dict')
    assert my_dict.pop('key').value == 'value'
    assert 'key' not in str(sample_document2)


def test_dict_update_with_dict(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.update({'new_key': 123})
    assert "'new_key': 123" in str(sample_document)


def test_dict_update_with_dict2(sample_document2):
    my_dict = sample_document2.find_dict('my_dict')
    my_dict.update({'new_key': 123})
    assert "new_key=123" in str(sample_document2)


def test_dict_update_with_kwargs(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.update(new_key2=456)
    assert "'new_key2': 456" in str(sample_document)


def test_dict_update_with_kwargs2(sample_document2):
    my_dict = sample_document2.find_dict('my_dict')
    my_dict.update(new_key2=456)
    assert "new_key2=456" in str(sample_document2)


def test_dict_update_with_kwargs_existing(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.update(new_key2=456, num=43)
    assert "'new_key2': 456" in str(sample_document)
    assert "'num': 43" in str(sample_document)


def test_dict_update_with_kwargs_existing2(sample_document2):
    my_dict = sample_document2.find_dict('my_dict')
    my_dict.update(new_key2=456, num=43)
    assert "new_key2=456" in str(sample_document2)
    assert "num=43" in str(sample_document2)


def test_dict_clear(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    my_dict.clear()
    assert "{}" in str(sample_document)


def test_dict_clear2(sample_document2):
    my_dict = sample_document2.find_dict('my_dict')
    my_dict.clear()
    assert "my_dict = dict()" in str(sample_document2)


@pytest.mark.parametrize("sample_document", ["sample_document1", "sample_document2"], indirect=True)
def test_dict_get_existing_key(sample_document):
    assert sample_document.find_dict('my_dict').get('key') == 'value'


@pytest.mark.parametrize("sample_document", ["sample_document1", "sample_document2"], indirect=True)
def test_dict_get_non_existing_key(sample_document):
    my_dict = sample_document.find_dict('my_dict')
    assert my_dict.get('nonexistent', default='default') == 'default'


def test_list_pop(sample_document):
    my_list = sample_document.find_list('my_list')
    assert my_list.pop(0).value == 1
    assert "[2, 3, 'a']" in str(sample_document)


def test_list_pop2(sample_document2):
    my_list = sample_document2.find_list('my_list')
    assert my_list.pop(0).value == 1
    assert "list(2, 3, 'a')" in str(sample_document2)


@pytest.mark.parametrize("sample_document", ["sample_document1", "sample_document2"], indirect=True)
def test_list_append(sample_document):
    sample_document.find_list('my_list').append('b')
    assert "'b'" in str(sample_document)


def test_list_remove(sample_document):
    sample_document.find_list('my_list').remove(2)
    assert "[1, 3, 'a']" in str(sample_document)


def test_list_remove2(sample_document2):
    sample_document2.find_list('my_list').remove(2)
    assert "list(1, 3, 'a')" in str(sample_document2)


@pytest.mark.parametrize("sample_document", ["sample_document1", "sample_document2"], indirect=True)
def test_list_remove_non_existing_element(sample_document):
    my_list = sample_document.find_list('my_list')
    with pytest.raises(ValueError):
        my_list.remove(4)


def test_list_clear(sample_document):
    sample_document.find_list('my_list').clear()
    assert "my_list = []" in str(sample_document)


def test_list_clear2(sample_document2):
    sample_document2.find_list('my_list').clear()
    assert "my_list = list()" in str(sample_document2)


def test_list_reverse(sample_document):
    sample_document.find_list('my_list').reverse()
    assert "my_list = ['a', 3, 2, 1]" in str(sample_document)


def test_list_reverse2(sample_document2):
    sample_document2.find_list('my_list').reverse()
    assert "my_list = list('a', 3, 2, 1)" in str(sample_document2)


def test_list_extend(sample_document):
    sample_document.find_list('my_list').extend(['b', 'c'])
    assert "my_list = [1, 2, 3, 'a', 'b', 'c']" in str(sample_document)


def test_list_extend2(sample_document2):
    sample_document2.find_list('my_list').extend(['b', 'c'])
    assert "my_list = list(1, 2, 3, 'a', 'b', 'c')" in str(sample_document2)


def test_list_insert(sample_document):
    sample_document.find_list('my_list').insert(1, 'b')
    assert "my_list = [1, 'b', 2, 3, 'a']" in str(sample_document)


def test_list_insert2(sample_document2):
    sample_document2.find_list('my_list').insert(1, 'b')
    assert "my_list = list(1, 'b', 2, 3, 'a')" in str(sample_document2)


def test_set_add(sample_document):
    sample_document.find_set('my_set').add(4)
    assert "my_set = {1, 2, 3, 4}" in str(sample_document)


def test_set_add2(sample_document2):
    sample_document2.find_set('my_set').add(4)
    assert "my_set = set(1, 2, 3, 4)" in str(sample_document2)


def test_set_add_copy(sample_document):
    sample_document.find_set('my_set').add(3)
    assert "my_set = {1, 2, 3}" in str(sample_document)


def test_set_add_copy2(sample_document2):
    sample_document2.find_set('my_set').add(3)
    assert "my_set = set(1, 2, 3)" in str(sample_document2)


def test_set_remove_existing_element(sample_document):
    sample_document.find_set('my_set').remove(3)
    assert "my_set = {1, 2}" in str(sample_document)


def test_set_remove_existing_element2(sample_document2):
    sample_document2.find_set('my_set').remove(3)
    assert "my_set = set(1, 2)" in str(sample_document2)


@pytest.mark.parametrize("sample_document", ["sample_document1", "sample_document2"], indirect=True)
def test_set_remove_non_existing_element(sample_document):
    my_set = sample_document.find_set('my_set')
    with pytest.raises(KeyError):
        my_set.remove(10)


def test_set_discard_existing_element(sample_document):
    sample_document.find_set('my_set').discard(3)
    assert "my_set = {1, 2}" in str(sample_document)


def test_set_discard_existing_element2(sample_document2):
    sample_document2.find_set('my_set').discard(3)
    assert "my_set = set(1, 2)" in str(sample_document2)


def test_set_discard_non_existing_element(sample_document):
    my_set = sample_document.find_set('my_set').discard(10)
    assert "my_set = {1, 2, 3}" in str(sample_document)


def test_set_discard_non_existing_element2(sample_document2):
    my_set = sample_document2.find_set('my_set').discard(10)
    assert "my_set = set(1, 2, 3)" in str(sample_document2)


def test_set_update(sample_document):
    sample_document.find_set('my_set').update([4, 5])
    assert "my_set = {1, 2, 3, 4, 5}" in str(sample_document)


def test_set_update2(sample_document2):
    sample_document2.find_set('my_set').update([4, 5])
    assert "my_set = set(1, 2, 3, 4, 5)" in str(sample_document2)


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


