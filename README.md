# Bitbucket CLI
This project is for authenticating and using the Bitbucket API as a CLI with Python.

## Description
The application connects to Bitbucket and, through a CLI, allows you to:

- Create projects
- Create repositories
- Add users to a repository
- Remove users from a repository
- Create branch restriction rules

## Project Structure

- **bitbucket_cli.py**: Contains the logic for using the Bitbucket API and makes it available as a CLI using the Python Click library.
- **oauth_authentication**: Contains the logic for automatically obtaining the Bearer Token. It uses Flask to temporarily start a web server and catch the authorization code via the /callback endpoint.
- **payload_examples**: To make the code flexible, the payload for each request is in JSON format. (Each endpoint has multiple optional values that users can configure.) The examples provided allow for quick use of the CLI.

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/edissonb250/bitbucket-cli.git
    cd bitbucket-cli
    ```
2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    ```bash
    CLIENT_KEY=your_bitbucket_client_key
    CLIENT_SECRET=your_bitbucket_client_secret
    ```

    Due to some restrictions on certain Bitbucket APIs (https://jira.atlassian.com/browse/BCLOUD-22896), a client password needs to be created as well:

    ```bash
    BITBUCKET_USERNAME=your_bitbucket_username
    BITBUCKET_PASSWORD=your_bitbucket_password
    ```

4. **Run the application**

   ```bash
   python bitbucket_cli.py
