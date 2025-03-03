import pytest
from src.pages.home_page import ExploraHomePage


def launch(browser):
    homepage = ExploraHomePage(browser)
    homepage.load()
    return homepage

@pytest.mark.SANITY
@pytest.mark.xray(test_key="TPT-70")
def test_page_title(browser):
    homepage = launch(browser)
    assert(homepage.title()) == 'Luxury Cruises | Explora Journey'

@pytest.mark.NRT
@pytest.mark.xray(test_key="TPT-71")
def test_destination_list(browser):
    homepage = launch(browser)
    homepage.click_on_destination_field()
    assert(len(homepage.get_destination_list())) == 8
    
