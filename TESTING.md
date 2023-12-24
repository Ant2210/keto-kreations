<h1 align="center" id="title"><img src="media/logo.webp" height="125" alt="Title - Keto Kreations Logo"></h1>

<h2 align="center">Testing</h2>

<img src="./documentation/features/responsivescreenshot.webp" alt="Image of Budgify website on different devices">

[View the live project here.](https://budgify-app-a7b562a0c28c.herokuapp.com/)


Extensive testing was carried out throughout the life cycle of this project. As well as all of the documented testing below I asked friends and family to use the site and tell me what was and wasn't working. I worked through the website clicking and checking each feature and function one by one and looked for anything that wasn't working or that was logging an error in the console. 

Had I given myself more time I would have liked to have implemented some automated testing using Jest and is certainly something I will look to implement in future projects. 

In practice and for production code a combination of both manual and automated testing is important. Automated testing can provide fast results especially across large applications whilst manual testing adds the human element and is more adept at spotting things like intuitiveness of the design. Utilising both can ensure high levels of quality and reliability of web applications.


## AUTOMATED TESTING

#### HTML Validator - [W3C](https://validator.w3.org/)

| Page | Errors/Warnings | Solution | Image |
| --- | --- | --- | --- |
| Welcome Page | Warning: Section lacks h2-h6 heading. | There is little use for a h2 element on this page, however a section element is still more semantically correct so ignored this warning. | <img src="./documentation/validators/html/welcome.webp" alt="HTML validator results for welcome page"> |
| Login Page | Warning: Section lacks h2-h6 heading. | Due to the design structure of this page again a h2 header isn't warranted however it is still more semantically correct to keep the section element instead of a DIV. | <img src="./documentation/validators/html/login.webp" alt="HTML validator results for login page"> |
| Register Page | Warning: Section lacks h2-h6 heading. | Due to the design structure of this page again a h2 header isn't warranted however it is still more semantically correct to keep the section element instead of a DIV. | <img src="./documentation/validators/html/register.webp" alt="HTML validator results for register page"> |
| Budget Page | N/A | N/A | <img src="./documentation/validators/html/budget.webp" alt="HTML validator results for budget page"> |
| Budgets Page | Warning: Section lacks h2-h6 heading. | Due to the design structure of this page h2 header falls outside of the section element on this page. It would still be semantically correct to keep the section element instead of a DIV. | <img src="./documentation/validators/html/budgets.webp" alt="HTML validator results for budgets page"> |
| Profile Page | N/A | N/A | <img src="./documentation/validators/html/profile.webp" alt="HTML validator results for profile page"> |
| 404 Page | N/A | N/A | <img src="./documentation/validators/html/404page.webp" alt="HTML validator results for 404 page"> |


#### CSS Validator - [W3C](https://jigsaw.w3.org/css-validator/)

| File | Errors/Warnings | Solution | Image |
| --- | --- | --- | --- |
| styles.css | N/A | N/A | <img src="./documentation/validators/css/styles.webp" alt="CSS validator results for styles.css"> |

### JavaScript Validator

#### JSHint Validator - [JSHint](https://jshint.com/)

| File | Errors/Warnings | Solution | Image |
| --- | --- | --- | --- |
| 404.js | N/A | N/A | <img src="./documentation/validators/js/404.webp" alt="JS validator results for 404.js"> |
| add-budget.js | N/A | N/A | <img src="./documentation/validators/js/add-budget.webp" alt="JS validator results for add-budget.js"> |
| budget.js | 1. Do no user 'new' for side effects. 2. Undefined variable - Chart | Both errors are side effects of using the ChartJS library and how they are implemented and not something I can change, so ignored. | <img src="./documentation/validators/js/budget.webp" alt="JS validator results for budget.js"> |
| confirmpwd.js | N/A | N/A | <img src="./documentation/validators/js/confirmpwd.webp" alt="JS validator results for confirmpwd.js"> |
| support.js | Undefined variables - emailjs & sendMail| Both errors are side effects of using the EmailJS service and how they are implemented and not something I can change, so ignored. | <img src="./documentation/validators/js/support.webp" alt="JS validator results for support.js"> |

### Python Validator - [Code Institute Python Linter](https://pep8ci.herokuapp.com/) 

#### Python Validator?? - [#](#)

| File | Errors/Warnings | Solution | Image |
| --- | --- | --- | --- |
| __ init __.py| Module level import not at top of file. | The reason this is being imported last, is because the 'routes' file will rely on using the 'app' and 'db' variables defined above. If we try to import routes before 'app' and 'db' are defined, then we'll get circular-import errors. So I have ignored this error| <img src="./documentation/validators/python/init.webp" alt="Python validator results for __init__.py"> |
| models.py | N/A | N/A | <img src="./documentation/validators/python/models.webp" alt="Python validator results for models.py"> |
| routes.py | N/A | N/A | <img src="./documentation/validators/python/routes.webp" alt="Python validator results for routes.py"> |
| run.py | N/A | N/A | <img src="./documentation/validators/python/run.webp" alt="Python validator results for run.py"> |

### Lighthouse

I used Lighthouse within the Chrome Developer Tools to test the performance, accessibility, best practices and SEO of the website. 

| Page | Results |
| --- | --- |
| Welcome Page | <img src="./documentation/lighthouse/welcome.webp" alt="Light house results for welcome page"> |
| Log In Page | <img src="./documentation/lighthouse/login.webp" alt="Light house results for log in page"> |
| Register Page | <img src="./documentation/lighthouse/register.webp" alt="Light house results for register page"> |
| Budgets Page | <img src="./documentation/lighthouse/budgets.webp" alt="Light house results for budgets page"> |
| Budget Page | <img src="./documentation/lighthouse/budget.webp" alt="Light house results for budget page"> |
| Profile Page | <img src="./documentation/lighthouse/profile.webp" alt="Light house results for profile page"> |

## MANUAL TESTING

### Testing User Stories

#### First Time Visitor
| Goals | How are they achieved? | Image |
| --- | --- | --- |
| As a first time visitor, I want to easily understand the purpose and features of the Budgify app without any prior knowledge. | This is achieved through clear introductory text and an illustrative image on the welcome screen. | <img src="./documentation/features/welcomescreen.webp" alt="Image of the welcome screen"> |
| As a first time visitor, I want to quickly create a new budget and explore the app's functionalities. | Once a user has registered or logged in they can instantly create a new budget from their main screen which is the budgets screen. | <img src="./documentation/features/budgetsscreen.webp" alt="Image of the budgets screen"> |
| As a first time visitor, I don't want to be overwhelmed with complex instructions or processes to start using the app. | This is achieved with a minimalist style design and clear calls to action on the buttons for the next steps, e.g. login, add budget, add transaction. | <img src="./documentation/features/welcomescreen.webp" alt="Image of the welcome screen"> <img src="./documentation/features/login.webp" alt="Image of the login screen"> <img src="./documentation/features/budgetsscreen.webp" alt="Image of the budgets screen"> <img src="./documentation/features/budgetmanagement.webp" alt="Image of the budget screen"> |
| As a first time visitor, I want to be able to contact budgify easily with any issues or questions I have about the app. | Whether logged in or not the user can contact support either via an online form by clicking the email icon in the footer or any of the social media links in the footer. Once logged in there is also a support button prominently displayed in the navbar which links to the same contact form. | <img src="./documentation/features/footer.webp" alt="Image of the footer"> <img src="./documentation/features/navbar.webp" alt="Image of the navbar"> <img src="./documentation/features/sidenav.webp" alt="Image of the sidenav">|
| As a first time visitor I want to be able to register easily and use the app straight away. | The user is able to click the register button straight from the welcome screen, and once registered is immediately logged in | <img src="./documentation/features/welcomescreen.webp" alt="Image of the welcome screen"> <img src="./documentation/features/register.webp" alt="Image of the registration screen"> |

#### Returning Visitor
| Goals | How are they achieved? | Image |
| --- | --- | --- |
| As a returning visitor, I want to easily log in to my existing account and access my saved budgets. | The welcome screen displays a prominent login button and once a user is logged in the first page they are taken too is their budgets page where all budgets are listed. | <img src="./documentation/features/welcomescreen.webp" alt="Image of the welcome screen"> <img src="./documentation/features/budgetsscreen.webp" alt="Image of the budgets screen"> |
| As a returning visitor, I want to be able to modify or delete existing budgets and view insights on my spending habits. | The user can modify and delete existing budgets from the budget page itself and also view insights at the bottom of each budget. | <img src="./documentation/features/budgetmanagement.webp" alt="Image of the budget management section"> <img src="./documentation/features/insights1.webp" alt="Image of the insights section"> <img src="./documentation/features/insights2.webp" alt="Image of the insights section"> |
| As a returning visitor, I want to be able to modify or delete existing transactions within my budgets. | The user can modify or delete any transaction by simply clicking on it, this is also explained right at the top of the budget page in the budget management section. | <img src="./documentation/features/budgetmanagement.webp" alt="Image of the budget management section"> <img src="./documentation/features/edittransactionmodal.webp" alt="Image of the edit transaction modal">|

#### Frequent Users
As per the [README.md](./README.md) frequent users would have similar needs to returning visitors due to the app's straightforward nature.

### Devices Used For Testing

The site has altogether in one way or another been used and tested on the following devices...

-   Google Pixel 7 - Chrome
-   HP Elitebook (Windows) - Chrome, Edge and Firefox
-   Iphone SE - Safari and Chrome
-   Ipad - Safari and Chrome
-   Macbook Pro - Safari and Chrome
-   Samsung Galaxy Tab S7 - Chrome and Samsung Browser
-   Samsung S23 Ultra - Edge, Chrome, Firefox and Samsung Browser

### Full Manual Testing

#### Welcome Page

| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Log in button | When clicked the user is redirected to the log in page | Clicked log in button | Redirected to the log in page | Pass |
| Register button | When clicked the user is redirected to the registration page | Clicked the register button | Redirected to the register page | Pass  |

#### Log In Page
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Log in with incorrect details | The user stays on the login page but a message is displayed showing incorrect username and/or password | Tried to log in with incorrect details | Remained on login page with a message showing incorrect username and/or password| Pass |
| Log in with correct details | The user is logged in and redirected to the budgets page displaying the message "Welcome, (User)!" | Log in with correct details | Logged in and redirected to the budgets page displaying the message "Welcome, (User)!". | Pass |
| Register Here Link | When clicked the user is redirected to the registration page. | Clicked Register Here link | Redirected to the the registration page | Pass |

#### Registration Page
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Register with incorrect username format | A validation message asking them to match the required format. | Tried to log in with usernames too short, too long and with invalid characters | Validation message is displayed | Pass |
| Register with incorrect password format | A validation message asking them to match the required format | Tried to register with a password that was too long, too short, used only lowercase letters, used only uppercase characters, used only numbers, used only lowercase characters with numbers, used only uppercase characters with numbers, used only special characters. | Validation message is displayed | Pass |
| Register with the correct format but the password and confirm password don't match | A validation message is displayed advising the passwords don't match. | Tried to register with the correct password format but the password and confirm password don't match. | A validation message is displayed advising the passwords don't match. | Pass |
| Register with correct username and password details. | User is registered, logged in and redirected to the budgets page and displayed the message "Registration successful, let's create your first budget!". | Registered with correct details. | Registered, logged in and redirected to the budgets page with a message displaying "Registration successful, let's create your first budget!".| Pass |
| Log In Here Link | When clicked the user is redirected to the log in page. | Clicked Log In Here link | Redirected to the the log in page | Pass |

#### Logged Out Navbar
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Budgify Logo | When clicked the user is redirected to the welcome page | Clicked logo | Redirected to the welcome page | Pass |

#### Footer
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Footer email icon/link | When clicked the support modal is visible | Clicked the email icon/link in footer | The support modal is visible | Pass |
| Footer social icon/link | When clicked the user is redirected to a new tab displaying the appropriate page | Clicked each social icon/link | each link takes you to the appropriate social media page | Pass |

#### Logged In Navbar
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Budgify Logo | When clicked the user is redirected to the budgets page | Clicked logo | Redirected to the budgets page | Pass |
| My Budgets Link | When clicked the user is redirected to the budgets page | Clicked My Budgets link | Redirected to the budgets page | Pass |
| Profile Link | When clicked the user is redirected to the profile page | Clicked Profile link | Redirected to the profile page | Pass |
| Support Link | When clicked the support modal is visible | Clicked Support link | The support modal is visible | Pass |
| Log Out Link | When clicked the log out modal is visible | Clicked log out link | The log out modal is visible | Pass |

#### Logged In Sidenav
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Hamburger icon | When clicked the sidenav is toggled open | Clicked hamburger icon | Sidenav is opened | Pass |
| X icon (when sidenav is visible) | When clicked the sidenav is toggled closed | Clicked X icon | Sidenav is closed | Pass |
| Budgify Logo | When clicked the user is redirected to the budgets page | Clicked logo | Redirected to the budgets page | Pass |
| Click page outside sidenav | Sidenav is toggled close | Clicked page outside of sidenav | Page toggled closed| Pass |
| My Budgets Link | When clicked the user is redirected to the budgets page | Clicked My Budgets link | Redirected to the budgets page | Pass |
| Profile Link | When clicked the user is redirected to the profile page | Clicked Profile link | Redirected to the profile page | Pass |
| Support Link | When clicked the support modal is visible | Clicked Support link | The support modal is visible | Pass |
| Log Out Link | When clicked the log out modal is visible | Clicked log out link | The log out modal is visible | Pass |

#### Budgets Page
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Budget Card | When a budget card is clicked the user is redirected to that budgets page | Clicked budget card | Redirected to appropriate budgets page | Pass |
| Add Budget Card | When the add budget card is clicked the add budget modal is visible | Clicked add budget card | Ass budget modal is visible | Pass |

#### Budget Page
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Add Transaction Button | When clicked the add transaction modal is visible | Clicked add transaction button | Add transaction modal is visible | Pass |
| Rename Budget Button | When clicked the rename budget modal is visible | Clicked rename budget button | Rename budget modal is visible | Pass |
| Delete Budget Button | When clicked the delete budget modal is visible | Clicked delete budget button | Delete budget modal is visible | Pass |
| Existing transaction | When an existing transaction is clicked the edit transaction modal is visible | Clicked an existing transaction | Edit transaction modal is visible | Pass |
| Table Rows | When a transaction is added or deleted the table rows are updated appropriately | Added and removed transactions | Table rows updated appropriately | Pass |
| Totals Section | When transactions are added and removed the tallies are updated | Added and removed transactions | Tallies updated | Pass |
| Insights Section | Only visible when a transaction exists within the budget | Added a transaction to a fresh budget | Insights section is visible | Pass |
| Pie Chart | When a colour is hovered or clicked the appropriate information is displayed | Hovered & clicked on a pie chart colour | Appropriate transaction information is displayed | Pass |
| Bar Chart | When a colour is hovered or clicked the appropriate information is displayed | Hovered & clicked on a bar chart colour | Appropriate transaction information is displayed | Pass |
| Key Button | When clicked the key for the pie chart and bar chart colours is toggled open and closed | Clicked key button | Key is opened then closed on the next click | Pass |

#### Profile Page 
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Delete Account Button | When clicked the delete account modal is visible | Clicked delete account button | Delete account modal is visible | Pass |
| Change password with incorrect current password | Form is reset and message displayed "Incorrect password, your password has not been updated." | Tried to update password with incorrect current password | Form reset and message displayed "Incorrect password, your password has not been updated." | Pass |
| Change password with incorrect new password format | Tried to change password with incorrect password format | A validation message asking them to match the required format | Tried to register with a password that was too long, too short, used only lowercase letters, used only uppercase characters, used only numbers, used only lowercase characters with numbers, used only uppercase characters with numbers, used only special characters. | Validation message is displayed | Pass |
| Change password with the correct format but the password and confirm password don't match | A validation message is displayed advising the passwords don't match. | Tried to change password with the correct password format but the password and confirm password don't match. | A validation message is displayed advising the passwords don't match. | Pass |
| Change password with correct format and matching password and confirm password | Form is reset and message displayed "Password updated successfully." | Changed password with correct format and matching password and confirm password | Form reset and message displayed "Password updated successfully." | Pass |

#### 404 Page
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Logged in user tries to access a page that does not exist or cannot be found | User is redirected to the 404 page with a message displayed "Sorry that page doesn't exist :( Taking you back to safety in 5...", and the user is redirected back to their my budgets page when the countdown ends. | Tried to type a URL to a page that doesn't exist whilst logged in | Redirected to 404 page with countdown then automatically redirected back to my budgets page | Pass |
| Logged out user tries to access a page that does not exist or cannot be found | User is redirected to the 404 page with a message displayed "Sorry that page doesn't exist :( Taking you back to safety in 5...", and the user is redirected back to the welcome page when the countdown ends. | Tried to type a URL to a page that doesn't exist whilst logged out | Redirected to 404 page with countdown then automatically redirected back to welcome page | Pass |

#### Add Budget Modal 
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Choose budget name with too few characters | Validation message is visible | Tried to choose a budget name with only 2 characters | Validation message is visible | Pass |
| Choose budget name with too many characters | Input field will not allow more than 50 characters | Tried to choose a budget name with more than 50 characters | Input field does not allow more than 50 characters | Pass |
| Choose budget name in the correct format | Budget is created, user is redirected to that budget and message displayed "Budget created successfully, lets add some transactions!" | Created a new budget with correctly formatted name | Budget created, redirected to budget and message displayed "Budget created successfully, lets add some transactions!" | Pass |
| Cancel Button | When clicked add budget modal is closed | Clicked cancel button | Add budget modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |

#### Support Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Choose a name with too few characters | Validation message is visible | Tried to choose a budget name with only 2 characters | Validation message is visible | Pass |
| Choose name with too many characters | Input field will not allow more than 50 characters | Tried to choose a budget name with more than 50 characters | Input field does not allow more than 50 characters | Pass |
| Choose an email with an @ symbol | Validation message is visible | Tried to choose an email without an @ symbol | Validation message is visible | Pass |
| Type a message with too few characters | Validation message is visible | Tried to type a message with only 9 characters | Validation message is visible | Pass |
| Type a message with too many characters | Input field will not allow more than 300 characters | Tried to type a message with more than 300 characters | Input field does not allow more than 300 characters | Pass |
| Send message with correct information (no errors) | Spinning loader appears until the message is sent, loader disappears, message displays "Your message has been successfully sent and we will be in touch soon. This box will automatically close in 5..." and the modal is closed when the countdown from 5 is complete. User then received a confirmation email as well as the support inbox for Budgify | Sent message with correct formatting and information | Loader appears, appropriate message appears, modal closes, confirmation email received and email received into Budgify support inbox | Pass |
| Send message with correct information but error is present | Spinning loader appears until sending fails, message displays "Sorry, something went wrong. Please try again later." | Disconnected from internet then tried to send message | Loader appears very briefly before displaying message "Sorry, something went wrong. Please try again later." | Pass |
| Cancel Button | When clicked support modal is closed | Clicked cancel button | support modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |

#### Log Out Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| No! Take me back! Button | When clicked the modal is closed | Clicked No! Take me back! button | Modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |
| Yes, Log me out button | When clicked the user is logged out, redirected to log in page and message displays "You have been logged out, come back again soon!" | Clicked Yes, Log me out button | Logged out, redirected to log in page, message displays "You have been logged out, come back again soon!" | Pass |

#### Add Transaction Modal 
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Add transaction without selecting a transaction type | Validation message is displayed | Tried to add a transaction without selecting a transaction type | Validation message displayed | Pass |
| Choose a description with too few characters | Validation message is visible | Tried to choose a description with only 2 characters | Validation message is visible | Pass |
| Choose description too many characters | Input field will not allow more than 50 characters | Tried to choose a description with more than 50 characters | Input field does not allow more than 50 characters | Pass |
| Choose a transaction amount less than 0 | Validation message is displayed | Tried to choose a transaction amount less than 0 | Validation message is displayed | Pass |
| Choose a transaction amount above 999,999 | Validation message is displayed | Tried to choose a transaction amount of 1,000,000 | Validation message is displayed | Pass |
| Choose a day of the month not between 1 and 31 | Validation message is displayed | Tried to choose 0 & 32 | Validation message is displayed | Pass |
| Add a transaction with correct form details | Modal closes, transaction is added to the correct section of the table, total section, pie chart and bar chart are all updated accordingly | Added a new transaction with correct form details | Modal closes, transaction is added in the correct place in the table, totals, pie chart and bar chart are all updated | Pass |
| Cancel Button | When clicked modal is closed | Clicked cancel button | Modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |

#### Rename Budget Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Choose budget name with too few characters | Validation message is visible | Tried to choose a budget name with only 2 characters | Validation message is visible | Pass |
| Choose budget name with too many characters | Input field will not allow more than 50 characters | Tried to choose a budget name with more than 50 characters | Input field does not allow more than 50 characters | Pass |
| Choose budget name in the correct format | Budget name is updated, budget page is refreshed and message displayed "Budget renamed successfully." | Renamed budget with correctly formatted name | Budget name updated, budget page refreshed and message displayed "Budget renamed successfully." | Pass |
| Cancel Button | When clicked add budget modal is closed | Clicked cancel button | Add budget modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |

#### Delete Budget Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| No! Take me back! Button | When clicked the modal is closed | Clicked No! Take me back! button | Modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |
| Yes, delete it! button | When clicked the budget is deleted, user is redirected back to budgets page and message displays "Budget deleted successfully." | Clicked Yes, delete it! button | Budget deleted, redirected back to budgets page and message displays "Budget deleted successfully." | Pass |

#### Edit Transaction Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Choose a new description with too few characters | Validation message is visible | Tried to choose a description with only 2 characters | Validation message is visible | Pass |
| Choose new description too many characters | Input field will not allow more than 50 characters | Tried to choose a description with more than 50 characters | Input field does not allow more than 50 characters | Pass |
| Choose a new transaction amount less than 0 | Validation message is displayed | Tried to choose a transaction amount less than 0 | Validation message is displayed | Pass |
| Choose a new transaction amount above 999,999 | Validation message is displayed | Tried to choose a transaction amount of 1,000,000 | Validation message is displayed | Pass |
| Choose a new day of the month not between 1 and 31 | Validation message is displayed | Tried to choose 0 & 32 | Validation message is displayed | Pass |
| Edit a transaction with correct form details | Modal closes,transaction details are updated accordingly, transaction is moved to the correct section of the table (if necessary), total section, pie chart and bar chart are all updated accordingly | Change transaction with correct form details, tried changing the type and not updating any details at all | Modal closes,transaction details are updated accordingly (if necessary), transaction is moved to the correct section of the table (if necessary), total section, pie chart and bar chart are all updated accordingly | Pass |
| Delete transaction button | When clicked, displays the delete transaction modal | Clicked delete transaction button | Delete transaction modal is displayed | Pass |
| Cancel Button | When clicked modal is closed | Clicked cancel button | Modal closed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |

#### Delete Transaction Modal
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| No! Take me back! Button | When clicked modal is closed and edit transaction modal is redisplayed | Clicked No! Take me back! Button | Modal closed and edit transaction modal is redisplayed | Pass |
| Click outside of modal | When clicking elsewhere on the page outside of the modal the modal is closed | Clicked elsewhere on page while modal was open | Modal closed | Pass |
| Yes, delete it! Button | When clicked the modal is closed, user is redirected back to the appropriate budget page where the transaction should be removed and message displayed "Transaction deleted successfully." | Clicked Yes delete it! button | Modal closed and redirected back to the budget page where the transaction have been removed and with message displayed "Transaction deleted successfully." | Pass |

#### Defensive Programming (not elsewhere covered)
| Feature/Action | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Logged out user tries to access a page URL that requires them to be logged in | User is redirected to the log in page with a message displayed "Please log in to view this page." | Typed URL for my budgets page whilst logged out | Redirected to log in page with message displayed "Please log in to view this page." | Pass |
| Logged in user tries to access a page URL the COULD belong to another user e.g. budgets or profile page | User is redirected back to their own budgets page with message displayed "You do not have permission to access this page." | Tried to type in the URL pattern for both a test user accounts budgets and profile page and a made up users budgets and profile page whilst logged in | Redirected back to my own budgets page with message displayed "You do not have permission to access this page." | Pass |



## Bugs

### Solved Bugs

| No. | Bug | How I solved the issue |
| --- | --- | --- |
| 1. | The default labels used by ChartJS for the pie chart and bar chart were being cut on smaller screen sizes. | Removed them and created my own key.  |
| 2. | The pie chart was displaying negative figures and "infinity" percentages. | Set the pie chart to show a message of "No income provided" in place of the percentage if income was 0. The pie chart is also now only visible is there is at least 1 transaction. |
| 3. | Fixed circular import error caught at deploy | When using a linter in VS code the routes import in the __ init __.py was being moved to the top. Moved back tot the bottom manually. |
| 4. | Bug - Auto focus on input element of the add budget modal not working. | I was using the wrong element ID so changed the code to match the correct ID. |
| 5. | When signing up with a capital letter in the user name, user taken to 404 page as the user session was saving the user as example "John" but was then checking the database for user "john" when loading the my budgets page. | Fixed by adding .lower() when storing the user in the session upon registration. |
| 6. | When I changed the background from off-white to white the navbar became transparent. | Set the navbar to white also. |


### Unsolved Bugs

None known at this time.