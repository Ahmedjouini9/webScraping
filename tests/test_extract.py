import pytest
from unittest.mock import Mock
from MyProject.src.modules.diploma.data_extractor import DiplomaDataExtractor


def test_extract_data():
    diploma_data_extractor = DiplomaDataExtractor()

    mock_row = Mock()
    mock_columns = [Mock(text=f"Value{i}") for i in range(8)]
    mock_row.find_elements.return_value = mock_columns

    result = diploma_data_extractor.extract_data(mock_row)

    expected_result = (
        "Value1",
        "Value2",
        "Value3",
        "Value4",
        "Value5",
        "Value6",
        "Value7",
    )
    assert result == expected_result


def test_extract_data_with_empty_text():
    diploma_data_extractor = DiplomaDataExtractor()

    mock_row = Mock()
    mock_columns = [Mock(text=f"Value{i}" if i != 2 else "") for i in range(8)]
    mock_row.find_elements.return_value = mock_columns

    result = diploma_data_extractor.extract_data(mock_row)

    expected_result = (
        "Value1",
        "",
        "Value3",
        "Value4",
        "Value5",
        "Value6",
        "Value7",
    )
    assert result == expected_result


def test_extract_cell_table_with_no_columns():
    diploma_data_extractor = DiplomaDataExtractor()

    mock_row = Mock()
    mock_row.find_elements.return_value = []

    result = diploma_data_extractor.extract_cell_table(mock_row)

    expected_result = []
    assert result == expected_result


if __name__ == "__main__":
    pytest.main()
