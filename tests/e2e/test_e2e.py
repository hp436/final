# tests/e2e/test_e2e.py

import pytest  


@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    page.goto('http://localhost:8000')
    

    assert page.inner_text('h1') == 'Hello World'
    

