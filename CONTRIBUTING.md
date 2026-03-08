# Contributing to Cyber Planner

First off, thanks for considering contributing! It's people like you that make Cyber Planner such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain the rationale for this feature**

### Pull Requests

* Fill in the required template
* Follow the PEP 8 Python style guide
* Include appropriate test cases if applicable
* Ensure the code runs without errors
* Document your changes clearly

## Development Setup

1. Fork and clone the repository
   ```bash
   git clone https://github.com/xdrew87/cyber-planner.git
   cd cyber-planner
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. Make your changes and test thoroughly

6. Commit with clear messages
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

7. Push to your fork and submit a pull request

## Style Guide

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep lines under 100 characters where practical

### Commit Messages
- Use the imperative mood ("add feature" not "added feature")
- Limit first line to 50 characters
- Reference issues and pull requests liberally after the first line
- Example:
  ```
  Add Pomodoro timer feature
  
  - Implement 25-minute countdown timer
  - Add timer completion notification
  - Fixes #123
  ```

### Comments
- Use comments to explain WHY, not WHAT
- Keep comments up-to-date with code changes

## Testing

Before submitting a pull request:

1. Run the application and test your changes manually
2. Test with different Python versions if possible
3. Verify that existing features still work
4. Check for any error messages or warnings

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help organize and categorize issues and pull requests.

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

---

Questions? Feel free to open an issue for discussion!

Thank you for contributing to Cyber Planner! 🍅
