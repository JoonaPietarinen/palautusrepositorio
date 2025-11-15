*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  Kalle666
    Set Password  Kalle123
    Set PasswordConfirmation  Kalle123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  Ka
    Set Password  Kalle123
    Set PasswordConfirmation  Kalle123
    Click Button  Register
    Register Should Fail With Message  Username must be atleast 3 characters long

Register With Valid Username And Too Short Password
    Set Username  Kalle666
    Set Password  Kal1
    Set PasswordConfirmation  Kal1
    Click Button  Register
    Register Should Fail With Message  Password must be atleast 8 characters long

Register With Valid Username And Invalid Password
    Set Username  Kalle666
    Set Password  KalleKalle
    Set PasswordConfirmation  KalleKalle
    Click Button  Register
    Register Should Fail With Message  Password must contain special characters or letters

Register With Nonmatching Password And Password Confirmation
    Set Username  Kalle666
    Set Password  Kalle123
    Set PasswordConfirmation  Kalle321
    Click Button  Register
    Register Should Fail With Message  Password confirmation does not match password

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  Kalle123
    Set PasswordConfirmation  Kalle123
    Click Button  Register
    Register Should Fail With Message  User with username kalle already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}
    
Set PasswordConfirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}
    
    
*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
