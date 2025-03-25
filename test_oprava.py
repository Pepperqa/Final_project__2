import pytest

from playwright.sync_api import sync_playwright



def test_title(page):
    page.goto("https://engeto.cz/")
    title = page.locator("h2").get_by_text("Intenzivní kurzy")
    assert title.inner_text() == "Intenzivní kurzy"


def test_load_courses(page):
    page.goto("https://engeto.cz/")

    btn_reject = page.locator("#cookiescript_reject")
    btn_reject.click()

    btn_course = page.locator("a[href='/prehled-kurzu/']").filter(has_text="Přehled IT kurzů")
    btn_course.wait_for(state="visible", timeout=12000)
    btn_course.click()

    page.wait_for_selector(".card",timeout=12000)
    
    courses=page.locator(".card")

    assert courses.count() >=3
    
   
def test_course_details_display(page):
    page.goto("https://engeto.cz/")

   
    btn_reject = page.locator("#cookiescript_reject")
    btn_reject.click()

    page.wait_for_load_state("networkidle", timeout=30000)

    btn_course = page.locator("a[href='/prehled-kurzu/']").filter(has_text="Přehled IT kurzů")
    btn_course.wait_for(state="visible", timeout=12000)
    btn_course.click()

    course_link = page.locator("a[href='https://engeto.cz/datovy-analytik-s-pythonem/']").locator("h3.title").filter(has_text="Datový analytik s Pythonem")
    course_link.click()

    page.wait_for_load_state("load", timeout=30000)

    course_title = page.locator("h2.title.has-display-lg-bold-font-size")
    course_description = page.locator("div.description p").filter(has_text="Nauč se klíčové dovednosti v oblasti datové analýzy").first
    #course_description = course_title.locator(".. >> xpath=following-sibling::div[contains(@class, 'description')]//p")
   

    assert course_title.is_visible(), "Course title is not visible."
    assert course_description.is_visible(), "Course description is not visible."
    course_description.screenshot(path="course_description.png")
    


@pytest.mark.parametrize(
"email,password,expected_message",
[
     ("alice@gmail.com","heslo","Nesprávný e-mail nebo heslo"),
     ("neviem123@centrum.sk", "Engeto1123","Nesprávný e-mail nebo heslo" )
]
)

def test_login(page, email, password,expected_message):
    page.goto("https://portal.engeto.com/lobby/sign-in")
  
    login_button=page.locator("a", has_text="Přihlásit se pomoci e-mailu a hesla")
    login_button.click()

    email_input=page.locator("input[name='username']")  
    password_input=page.locator("input[name='password']")
    submit_button=page.locator("button[type='submit']")

    email_input.fill(email)
    password_input.fill(password)
    submit_button.click()
    submit_button.wait_for(state="visible", timeout=5000)

    
    alert_message = page.locator("#error-element-password")  
    assert alert_message.inner_text() == expected_message

    page.screenshot(path="po_logine.png")