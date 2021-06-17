*** Settings ***
Documentation     A test suite with tests to validate registration
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
Valid Registration
    Navigate to Register page
    Input Username    12358
    Input Password    abcde
    Input Firstname   XYZ1
    Input lastname    ZYX2
    Input phonenumber  987654
    Submit Credentials on register page
    login page should be open
    [Teardown]    Close Browser

Register an existing user
    Navigate to Register page
    Input Username    12358
    Input Password    abcde
    Input Firstname   XYZ1
    Input lastname    ZYX2
    Input phonenumber  987654
    Submit Credentials on register page
    register page should be open
    Element Should contain    //div[@class='flash']    is already registered.
    [Teardown]    Close Browser

Valid Login
    Navigate to Login page
    Input Username    12358
    Input Password    abcde
    Submit Credentials on login page
    User Page Should Be Open
    [Teardown]    Close Browser