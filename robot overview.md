# <img src="https://images.seeklogo.com/logo-png/46/1/robot-framework-logo-png_seeklogo-462634.png" alt="Robot Logo" width="30" height="30"> **Robot Framework**  
## **High level overview**

### 1. Intro
Robot Framework is a Python-based, extensible keyword-driven automation framework for acceptance testing, acceptance test driven development (ATDD), behavior driven development (BDD) and robotic process automation (RPA). 

Tests are composed of a sequence of high-level keywords that represent actions or operations that the system or application under test should perform. Keywords are typically written in plain English and organized in a tabular format:
```robot
*** Settings ***
Documentation       Simple example

*** Test Cases ***
Open Browser ${BASE_URL}
[Teardown] Close Browser
```

**Dependency injection, scope and state management**


Robot doesn't have built-in dependency injection in the way traditional programming languages do. However, it offers various machanisms to manage dependencies and scope, such as:
- Test Setup & Teardown (scoped dependencies) using suite setup for sharing resources accross all test cases, test setup for per-test initialization.
- Modularization using resource files for dependency management, which promotes reusability and dependency injection at the test level.
- Python classes for global state management to allow stateful behavior across multiple test cases when data persistance and consitency is required.

**Mixing pytest and robot framework tests**
- Robot and Pytest can be combined in a single project.
- Plugin pytest-robotframework allows to execute robot tests via pytest. Robot tests can be run along with pytest tests.
- Powerful pytest fixtures (like database connections, authentication tokens, etc.) can be shared with robot tests.
- Unified reports for robot and pytest can be generated.
  

### 2. Standard Libraries and Extensions

Robot Framework comes with a set of built-in standard libraries, which are sufficient only for very simple scenarious. For complex scenarious it can be extended using custom libraries or custom Python code for specific testing needs. 

**Core Libraries:**
- BuiltIn: A set of common keywords for control flow, variable manipulation, logging. 
- Collections: Handles Python List/Dictonary operations.
- OperatingSystem: Enables various operating system related tasks.
- Screenshot: Provides keywords to capture screenshots of the desktop.
- etc.


**Extensions:**
- SeleniumLibrary: Web browser interactions (WebDriver)
- AppiumLibrary: Android and iOS testing. Uses Appium internally.
- RequestsLibrary: HTTP level testing using Python Requests internally (REST API)
- DatabaseLibrary: Interaction with data base (SQL queries)
- SapGuiLibrary: Testing the SAPGUI client using the internal SAP Scripting Engine.
- Pabot: Parallel execution
- Custom Libraries: own customization for specific needs
- etc. 
  (note: even if the range of libraries suggested by robot as extenstions is huge, some of them are deprecated and not supported)


### 3. Test types:
- Web UI           
- API               
- Mobile Testing    
- E2E               

#### Examples of UI and API tests with custom keywords

1. **UI**
```robot
*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${BROWSER}  chrome
${URL}      https://explorajourneys.com/
${EXPECTED_TITLE}    Luxury Cruises | Explora Journeys
${DESTINATION_FIELD}  css=.quickBooking__destination
${LIST_DESTINATIONS}  css=.quickBooking__place
${EXPECTED_COUNT}  6

*** Test Cases ***
Verify Website Title
    [Tags]  SCRUM-3  SANITY
    Open Browser  ${URL}  ${BROWSER}
    Title Should Be    ${EXPECTED_TITLE}
    Close Browser

Verify Destination List
    [Tags]  SCRUM-5  NRT
    Open Browser   ${URL}  ${BROWSER}
    Wait Until Page Contains Element    ${DESTINATION_FIELD}
    Click Element  ${DESTINATION_FIELD}
    ${item_count}=    Count Items in List
    Verify Item Count  ${item_count}  ${EXPECTED_COUNT}
    Close Browser


*** Keywords ***
Count Items in List
    ${items}=  Get WebElements    ${LIST_DESTINATIONS}    
    ${item_count}=  Get Length   ${items}
    [RETURN]    ${item_count}


Verify Item Count
    [Arguments]  ${actual_count}    ${expected_count}
    Should Be Equal As Numbers    ${actual_count}    ${expected_count}
    Log  Verified that the list contains ${actual_count} items.
```

2. **API**

```robot
*** Settings ***
Library       RequestsLibrary

*** Variables ***
${BASE_URL}  https://reqres.in/api

*** Test Cases ***
Verify Single User Details
    [Tags]    SCRUM-8  API
    Create Session    reqres    ${BASE_URL}
    ${response}    GET On Session    reqres    /users/2
    Log    ${response.json()}

    #Validate response values
    ${user_data}    Set Variable    ${response.json()}[data]
    Should Be Equal As Strings    ${user_data}[id]    2
    Should Be Equal As Strings    ${user_data}[email]    janet.weaver@reqres.in
```


### 4. Reporting and Xray Integration

By default it generates logs and reports based on XML outputs. The generated XML report can be imported into Xray using a dedicated REST API endpoint **POST /api/v2/import/execution/robot**. This integration allows automated test results to be linked directly to Xray Test Executions and Tests. Robot supports tagging for correct mapping with Jira issue keys.

#### Example of execution results of 2 above mentioned UI tests uploaded to Xray as is without customization

![Tagging](tagging.PNG)
![Test details](testdetails.png)

### 5. Considerations and challenges

1. Debbuging:   
   It doesn't support interactive debugging like breakpoints. 
   Hard to inspect variable values during the execution, each time they have to be loged to the console to be able to see intermediate values. It may be difficult to track variable values espessialy in long test cases.
   UI tests may fail without useful error messages, which may be tricky especially by running in headless-mode.
   Execution logs (automatically saved in a separate file in html format) may be large and not detailed enough info without a proper comfiguration.
   In case of API tests robot logs only the status codes but not response bodies, which makes it difficult to debug incorrect headers, payload or authentication failures.


2. Overhead:
   
   Abstraction:  
   While user-friendly, keyword-driven approach can lead to duplication or over-abstraction if not managed carefully. Poorly designed or duplicated keywords might make tests hard to maintain in the long run. 
   
   Performance:  
   Can introduce performance overhead, especially when dealing with large test suites or highly complex test cases, because every single keyword maps internaly to Python functions and a single test step may involve several internal calls before execution.


3. Learning curve for advanced usage:  
   Simple tests are straightforward and easy to understand/create/read. For leveraging advanced features, creating custom libraries a deeper understanding of the framework is required.


4. Customization:  
   Compared to code-centric frameworks it is less flexible. Complex workflows can be handled via customizations, which requires Python (supports also Java) programming skills.
