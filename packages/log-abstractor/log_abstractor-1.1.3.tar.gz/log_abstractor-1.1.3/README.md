### Build the package with below command
  - `python setup.py sdist bdist_wheel`

### Creating a pypy account
- Before we can share package we should have account in a repository like pypy , so lets create one
  - Log In to PyPI:
    - Go to https://pypi.org and log in to your account.
  - Navigate to Your Account Settings:
    - Once logged in, click on your username in the top right corner, and then click on "Account settings."
  - Create an API Token:
    - In the account settings, scroll down to the section called "API tokens."
    - Click "Add API token."
    - Give your token a meaningful name (e.g., "my_project_upload_token"). 
    - You can choose to restrict the token to a specific project or leave it as "Entire account" to allow uploading to any project. 
    - Once you create the token, it will be shown only once. 
      - Make sure to copy it and store it in a safe place.


### Sharing the package
  1. Upload to PyPI:
     - pip install twine 
     - python -m twine upload dist/*
     - Make sure you have credentials set up if it’s a private repository.
  2. Upload to Artifactory
     - If your organization uses JFrog Artifactory, you’ll have a specific repository URL where you can upload your package.
     - twine upload --repository-url https://your-artifactory-url/artifactory/pypi-repo dist/*
  3. Direct Sharing
     - If you don’t have a package repository, you can still share the .tar.gz or .whl file directly with your colleagues or team members. 
     - They can install it using: `pip install /path/to/your/package/dist/python_logger-0.1.0-py3-none-any.whl`

### Version Control and Updates
- As your logger evolves, you can update the version number in setup.py and publish the new version. 
- Other projects can update to the latest version by running:
    - `pip install --upgrade log-abstractor`