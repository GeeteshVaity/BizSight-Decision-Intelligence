# Contributing to BizSight Decision Intelligence System

Thank you for your interest in contributing to BizSight! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/BizSight-Decision-Intelligence.git
   cd BizSight-Decision-Intelligence
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run tests to ensure everything works**:
   ```bash
   python tests/test_bizsight.py
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all classes and methods
- Keep functions focused and concise
- Comment complex logic

### Example of Good Code Style

```python
def calculate_profit_margin(revenue, cost):
    """
    Calculate profit margin percentage
    
    Args:
        revenue (float): Total revenue
        cost (float): Total cost
        
    Returns:
        float: Profit margin as percentage
    """
    if revenue == 0:
        return 0
    
    profit = revenue - cost
    margin = (profit / revenue) * 100
    
    return margin
```

### Code Structure

- Keep modules focused on single responsibility
- Use classes for stateful operations
- Use functions for stateless operations
- Avoid deep nesting (max 3-4 levels)
- Use early returns to reduce complexity

## Adding New Features

### 1. New Analytics Feature

If adding new analytics capabilities:

1. Add methods to `src/analytics.py`
2. Add corresponding tests to `tests/test_bizsight.py`
3. Update `DOCUMENTATION.md` with API details
4. Add usage example to `example_usage.py`

### 2. New Risk Detection Rule

If adding new risk detection:

1. Add detection method to `src/risk_detector.py`
2. Add threshold to default thresholds
3. Call method in `detect_all_risks()`
4. Add test case
5. Document the new rule

### 3. New Visualization

If adding new visualizations:

1. Add plot method to `src/visualizer.py`
2. Follow existing naming convention: `plot_*`
3. Use consistent styling
4. Save with DPI=300
5. Add example to documentation

### 4. New Scenario Type

If adding new simulation scenarios:

1. Add simulation method to `src/scenario_simulator.py`
2. Use `_calculate_scenario_impact()` helper
3. Add to scenarios list
4. Test with unit tests

## Testing

### Writing Tests

All new features must include tests:

```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'revenue': [10000] * 10,
            'cost': [7000] * 10
        })
    
    def test_new_functionality(self):
        """Test description"""
        # Arrange
        expected = 3000
        
        # Act
        result = calculate_profit(self.data)
        
        # Assert
        self.assertEqual(expected, result)
```

### Running Tests

```bash
# Run all tests
python tests/test_bizsight.py

# Run specific test class
python -m unittest tests.test_bizsight.TestDataLoader

# Run specific test
python -m unittest tests.test_bizsight.TestDataLoader.test_load_data_success
```

## Commit Guidelines

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **test**: Adding tests
- **refactor**: Code refactoring
- **style**: Code style changes (formatting)
- **chore**: Maintenance tasks

### Examples

```
feat: Add quarterly aggregation to analytics

Added get_quarterly_aggregates() method to BusinessAnalytics
class to support quarterly reporting.

Closes #123
```

```
fix: Handle division by zero in profit margin calculation

Added check for zero revenue before calculating profit margin
to prevent ZeroDivisionError.
```

## Pull Request Process

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes**:
   ```bash
   python tests/test_bizsight.py
   python main.py
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Your feature description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Submit for review

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for new features
- [ ] Tested manually

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings generated
```

## Documentation

When adding features, update:

1. **README.md**: High-level usage
2. **DOCUMENTATION.md**: Detailed API reference
3. **example_usage.py**: Working examples
4. **Docstrings**: In-code documentation

## Code Review

### What We Look For

- Code quality and readability
- Test coverage
- Documentation completeness
- Performance considerations
- Security implications
- Backward compatibility

### Review Process

1. Automated tests must pass
2. Code review by maintainer
3. Feedback and iteration
4. Approval and merge

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version
- Dependency versions
- Error messages/stack traces

### Feature Requests

Include:
- Problem description
- Proposed solution
- Alternative solutions considered
- Potential impact

## Community Guidelines

### Be Respectful

- Be kind and courteous
- Respect different viewpoints
- Accept constructive criticism
- Focus on what's best for the project

### Be Professional

- Use clear, professional language
- Stay on topic
- Be patient with newcomers
- Help others learn

## Questions?

- Open an issue for questions
- Tag as "question"
- Check existing issues first
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing to BizSight! 🎉
