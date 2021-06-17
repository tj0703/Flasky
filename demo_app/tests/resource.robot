*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${SERVER}         0.0.0.0:8080
${BROWSER}        Chrome
${DELAY}          0
${VALID USER}     1234
${VALID PASSWORD}    a
${EMPTY}
${LOGIN URL}         http://${SERVER}/login
${REGISTER URL}      http://${SERVER}/register
${USER URL}          http://${SERVER}/user
${ERROR URL}         http://${SERVER}/error
${INDEX URL}          http://${SERVER}/

*** Keywords ***
Open Browser To Index Page
    Open Browser    ${INDEX URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Index Page Should Be Open

Login Page Should Be Open
    Title Should Be    Log In - Demo App

Register Page Should Be Open
    Title Should Be    Register - Demo App

Go To Login Page
    Click link    Log In
    Login Page Should Be Open

Go To Register Page
    Click link   Register
    Register Page Should Be Open

Input Username
    [Arguments]    ${username}
    Input Text    username   ${username}

Input Password
    [Arguments]    ${password_field}
    Input Text    password   ${password_field}

Input Firstname
    [Arguments]    ${firstname}
    Input Text    firstname    ${firstname}

Input lastname
    [Arguments]    ${lastname}
    Input Text    lastname    ${lastname}

Input phonenumber
    [Arguments]    ${phone}
    Input Text    phone    ${phone}

Register with Credentials
    Click Button    Register

Press the link to register
    Click link      Register

Press the link to login
    Click link      Log In

Submit Credentials on register page
    Click Button    Register

Submit Credentials on login page
    Click Button    Log In

User Page Should Be Open
    Location Should Be    ${USER URL}
    Title Should Be    User Information - Demo App

Index Page Should Be Open
    Location Should Be    ${INDEX URL}
    Title Should Be    index page - Demo App

Navigate to Register page
    Open Browser To Index Page
    Index page should be open
    Press the link to register
    Register Page Should Be Open

Navigate to Login page
    Open Browser To Index Page
    Index page should be open
    Press the link to login
    Login Page Should Be Open
