# Contributing to STT

Thank you for your interest in contributing to the Ultra-Powerful Speech-to-Text System!

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features! Please open an issue describing:
- The enhancement you'd like to see
- Why it would be useful
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/hleong75/STT.git
cd STT

# Install dependencies
pip install -r requirements.txt

# Run examples to test
python examples/api_usage.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Testing

Before submitting a PR:
- Test with different audio files
- Test with different languages
- Test with both noisy and clean audio
- Verify all example scripts work

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
