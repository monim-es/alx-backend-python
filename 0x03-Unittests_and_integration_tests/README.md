# 0x03. Unittests and Integration Tests

This project focuses on the principles and practices of writing **unit tests** and **integration tests** in Python using the `unittest` framework and related tools.

## 📚 Learning Objectives

By the end of this project, you should be able to:

- Understand the difference between **unit tests** and **integration tests**
- Use `unittest`, `parameterized`, and `mock` libraries effectively
- Apply **mocking**, **parameterization**, and **fixtures** in testing
- Write reliable and isolated tests for Python functions and classes

## 🧪 Technologies

- Python 3.7+
- `unittest`
- `parameterized`
- `unittest.mock`

## 📂 Files

- `utils.py`: Utility functions to be tested
- `client.py`: HTTP client class using `requests`
- `fixtures.py`: Test fixtures used by integration tests
- `test_utils.py`: Unit tests for functions in `utils.py`
- `test_client.py`: Unit and integration tests for `client.py`

## ✅ Running Tests

To run all tests:
```bash
python3 -m unittest discover
To run a specific test file:

bash
Copy
Edit
python3 -m unittest test_utils.py
