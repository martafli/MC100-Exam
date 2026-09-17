import requests
import logging

logging.basicConfig( 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_sql_injection_login():
    target_url = "http://localhost:5000/login"

    payloads = [
        "' OR '1'='1",
        "' OR 1=1 --",
        "admin' --",
        "' UNION SELECT * FROM users --"
    ]

    for payload in payloads:
        response = requests.post(target_url, data={"username": payload,"password": "anything"},
        allow_redirects=False #prevent automatic redirection to capture the response before any redirect occurs
        )

        logger.info(f"Testing payload: {payload}")
        logger.info(f"Response status code: {response.status_code}")

        if response.status_code == 302: #redirect
            location = response.headers.get("Location", "") #get the location header from the response
            logger.info(f"Redirected to: {location}")

            if "upload" in location: 
                logger.info("Potential vulnerability: Login bypass succeeded!")

            else:
                logger.info("Login failed, no vulnerability detected.") #indicates redirected to login page, meaning the login attempt failed
        else:
            logger.info(f"Response status code: {response.status_code}")
            logger.info("Login failed, no vulnerability detected.")

def test_sql_injection_register():
    target_url = "http://localhost:5000/register"
    username = "'; DROP TABLE users; --"

    logger.info(
        f"Testing registration with SQL injection: "f"{username}")
    response = requests.post(target_url, data={"username": username,"password": "anything"},
        allow_redirects=False #prevent automatic redirection to capture the response before any redirect occurs
    )

    logger.info(f"Response status code: {response.status_code}")
    if response.status_code in (200, 302):
        location = response.headers.get("Location", "") #get the location header from the response
        logger.info(f"Redirected to: {location}")
        logger.info("Application handled the request without crashing, no vulnerability detected.")
    else:
        logger.info("Unexpected response, potential vulnerability detected.")


logger.info("Starting SQL injection tests...")
test_sql_injection_login()
test_sql_injection_register()
logger.info("SQL injection tests completed.")
 