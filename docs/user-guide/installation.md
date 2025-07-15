# Installation

Learn how to install JsonPort and set up your development environment.

## Requirements

- **Python**: 3.7 or higher
- **pip**: Latest version recommended

## Installation Methods

### Using pip (Recommended)

```bash
pip install jsonport
```

### From Source

```bash
git clone https://github.com/Luan1Schons/JsonPort.git
cd JsonPort
pip install -e .
```

### Development Installation

For development and contributing:

```bash
git clone https://github.com/Luan1Schons/JsonPort.git
cd JsonPort
pip install -e ".[dev,test,docs]"
```

## Verify Installation

```python
import jsonport
print(jsonport.__version__)
```

## Optional Dependencies

### For Testing
```bash
pip install -e ".[test]"
```

### For Development
```bash
pip install -e ".[dev]"
```

### For Documentation
```bash
pip install -e ".[docs]"
```

## Python Version Support

| Version | Status | Notes |
|---------|--------|-------|
| Python 3.7 | ✅ Supported | EOL - End of Life |
| Python 3.8 | ✅ Supported | Recommended minimum |
| Python 3.9 | ✅ Supported | Full features |
| Python 3.10 | ✅ Supported | Full features |
| Python 3.11 | ✅ Supported | Full features |
| Python 3.12 | ✅ Supported | Full features |
| Python 3.13 | ✅ Supported | Full features |

## Troubleshooting

### Common Issues

**Import Error**: Make sure you're using Python 3.7+
```bash
python --version
```

**Permission Error**: Use virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

**Build Error**: Update pip and setuptools
```bash
pip install --upgrade pip setuptools wheel
```

## Next Steps

- [Quick Start](quick-start.md) - Get started with JsonPort
- [Examples](examples/) - See practical examples
- [API Reference](api/) - Complete API documentation 