import pytest
from pages.home_page import ExploraHomePage
from pytest_cases import case

def launch(browser):
    homepage = ExploraHomePage(browser)
    homepage.load()
    return homepage

@pytest.mark.NRT
@pytest.mark.case_tag("SCRUM-3")
def test_page_title(browser):
    homepage = launch(browser)
    assert(homepage.title()) == 'Luxury Cruises | Explora Journeys'

@pytest.mark.SANITY
@pytest.mark.case_tag("SCRUM-5")
def test_destination_list(browser):
    homepage = launch(browser)
    homepage.click_on_destination_field()
    assert(len(homepage.get_destination_list())) == 5
    
