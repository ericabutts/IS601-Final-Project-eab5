Project Description: Overview of the calculator application and its features.

This project is a command-line Read Evaluate Print Loop (REPL) calculator application.

Installation Instructions: Steps to set up the virtual environment and install dependencies.

    git clone https://github.com/ericabutts/IS601-Midterm-Project-eab5.git
    cd IS601_MIDTERM_MODULE
    pip install -m requirements.txt

Configuration Setup: Instructions on creating and configuring the .env file with necessary environment variables.

    You can create your .env file manually or copy from the example template if provided:

    cp .env.example .env

    Then open .env and configure your environment variables

    These values are automatically loaded at runtime by CalculatorConfig in config.py.
    If a variable is missing from the .env file, the application falls back to a safe default.
    For example:

    - If CALCULATOR_LOG_DIR is not set, logs are stored in <base_dir>/logs.
    - If CALCULATOR_HISTORY_FILE is not set, history is saved to <base_dir>/history/calculator_history.csv.
    - If any configuration is invalid (e.g., negative precision or history size), a ConfigurationError will be raised at startup.

    Logs are automatically created inside the directory specified by CALCULATOR_LOG_DIR or the default logs/ folder.

    Typical logging includes:
    - Application startup and shutdown messages
    - Operation executions and exceptions
    - History file save/load activities
    
    To view logs:

    cat logs/calculator.log

    You can customize the log directory or filename in the .env file using:

    CALCULATOR_LOG_DIR=./custom_logs
    CALCULATOR_LOG_FILE=./custom_logs/my_calculator.log

Usage Guide: Detailed explanation of how to use the command-line interface and its supported commands.

    Once installed and configured, run the calculator from your terminal:

    python -m app.main

The following commands are available:

    exit:
        Quit the program.

    help:
        List all possible commands.

    undo:
        Remove the previous calculation from the history.

    redo:
        Restore the most recently deleted calculation.

    clear:
        Clears all history of calculations from the session.

    save: 
        Save all calculations to a history file.

    load:
        Load a save file of calculation history.

    add:
        Add two numbers together.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    subtract:
        Subtract a number from another number.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    multiply:
        Multiply two numbers.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    divide:
        Divide one number by another.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    power: 
        Raise one number to the power of another.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    root: 
        Calculate the nth root of a number.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    modulus: 
        Compute the remainder of the division of two numbers.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    integerdivide (known as Integer Division): 
        Perform division that results in an integer quotient, discarding any fractional part.

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    percentcalculation (known as Percentage Calculation): 
        Calculate the percentage of one number with respect to another (e.g., Percentage(a, b) computes (a / b) * 100).

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

    absolutedifference: 
        Calculate the absolute difference between two numbers

        First number<Decimal>: the first operand.
        Second number <Decimal>: the second operand.

Testing Instructions: How to run unit tests and check test coverage.

    cd IS601_MIDTERM_MODULE
    # Activate virtual environment in Windows
    venv\Scripts\activate

    # Activate virtual environment in macOS / Linux
    source venv/bin/activate

    # install dependencies
    pip install -r requirements.txt
    
    # Make sure playwright is installed
    playwright install

    # Start the FastAPI server
    uvicorn main:app --reload

    # Run all tests in the tests/ folder with coverage report
    pytest -v --cov=app tests/

    # Test End-to-End (e2e) Tests with Playwright
    # In a new terminal run the following commands
    cd frontend
    python -m http.server 5500 -d frontend/

    # Run FRONTEND REGISTRATION/LOGIN Tests
    npx playwright test




CI/CD Information: Overview of GitHub Actions workflow and its purpose.

    Pushing commits to the repository triggers the GitHub Actions workflow. 
    The unit tests stored in the tests folders will run upon push.
    The tests will fail if the changes result in less than 90% coverage.

    You can view the workflow status in your repository under Actions → Workflows.

    BEFORE RUNNING Frontend Playwright Tests:
    Run the Frontend server
    python -m http.server 5500 -d frontend/




Accessing FastAPI Docs:

    While Docker is running, access http://localhost:8000/docs to view API endpoints.

Accessing pgAdmin:

    While Docker is running, access http://localhost:5050
    Username: admin@admin.com
    Password: admin

    In the left sidebar, click the Query Tool and input the settings.
    Setting	Value:
    Host	    db
    User	    postgres
    Password	postgres
    DB Name	    fastapi_db
    Port        5432

    If the 'user' table is missing from pgAdmin, create it with the SQL command.



CURL Commands for testing the API:
    Open Terminal and run WSL
    Run the following commands:

    Register a new user:
    curl -X POST "http://localhost:8000/register" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'

    Login:
    curl -X POST "http://localhost:8000/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"testpass"}'

    Create a calculation
    curl -X POST "http://localhost:8000/calculations/" \
    -H "Content-Type: application/json" \
    -d '{"a":10,"b":5,"type":"ADD","user_id":1}'

    Get all calculations
    curl -X GET "http://localhost:8000/calculations/"

    Get a single calculation by ID
    curl -X GET "http://localhost:8000/calculations/1"

    Update a calculation
    curl -X PUT "http://localhost:8000/calculations/1" \
    -H "Content-Type: application/json" \
    -d '{"a":20,"b":10,"type":"MULTIPLY"}'

    Delete a calculation
    curl -X DELETE "http://localhost:8000/calculations/1"

    Get calculations for a specific user
    curl -X GET "http://localhost:8000/calculations/user/1"

    Quick API Calculator
    curl -X GET "http://localhost:8000/calculate/ADD?a=10&b=5"