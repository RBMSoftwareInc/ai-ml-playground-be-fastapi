# Python 3.12 Compatibility Fixes

## Overview

This document outlines the compatibility fixes applied for Python 3.12 support in the AI/ML Playground Backend.

## Issues Encountered

### 1. Missing `distutils` Module

**Error:**
```
ModuleNotFoundError: No module named 'distutils'
```

**Cause:** Python 3.12 removed `distutils` from the standard library.

**Solution:**
- Added `setuptools>=65.0.0` to `requirements.txt`
- `setuptools` provides `distutils` compatibility for Python 3.12+

### 2. NumPy Build Failure

**Error:**
```
AttributeError: module 'pkgutil' has no attribute 'ImpImporter'
```

**Cause:** 
- NumPy 1.24.4 (and older) doesn't have pre-built wheels for Python 3.12
- Build process fails due to `pkg_resources` incompatibility with Python 3.12

**Solution:**
- Updated NumPy version constraint: `numpy>=1.26.0,<2.0.0`
- NumPy 1.26+ has pre-built wheels for Python 3.12
- Maintains API compatibility with existing codebase

## Changes Made

### requirements.txt Updates

1. **Build Tools:**
   ```txt
   setuptools>=65.0.0
   wheel>=0.40.0
   ```

2. **AI/ML Core Libraries:**
   ```txt
   # Updated for Python 3.12 compatibility
   numpy>=1.26.0,<2.0.0
   pandas>=2.0.0,<3.0.0
   scikit-learn>=1.3.0,<2.0.0
   scipy>=1.11.0,<2.0.0
   ```

## Installation Steps

1. **Upgrade build tools:**
   ```bash
   source venv/bin/activate
   pip install --upgrade pip setuptools wheel
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Verification

Verify the installation works:

```bash
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
python -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
```

## Notes

- **NumPy 2.x:** We're using NumPy 1.26.x instead of 2.x to maintain API compatibility with existing code and dependencies
- **Pre-built wheels:** All updated packages have pre-built wheels for Python 3.12, avoiding build issues
- **Backward compatibility:** These changes maintain compatibility with existing code while supporting Python 3.12

## Package Version Updates for Python 3.12

### Deep Learning
- **TensorFlow:** Updated from `>=2.8.0,<=2.13.0` to `>=2.16.0` (TensorFlow 2.16+ required for Python 3.12)
- **tf-keras:** Added `>=2.20.0` (Required for Transformers compatibility with Keras 3. TensorFlow 2.20+ includes Keras 3, but Transformers needs the backwards-compatible tf-keras package)
- **PyTorch:** Updated from `>=1.12.0,<2.0.0` to `>=2.0.0`
- **Transformers:** Updated from `>=4.20.0,<4.38.0` to `>=4.38.0`
- **sentence-transformers:** Updated from `>=2.2.0,<2.3.0` to `>=2.3.0`

### Computer Vision
- **opencv-python:** Updated from `>=4.5.0,<4.10.0` to `>=4.10.0`
- **Pillow:** Updated from `>=9.0.0,<11.0.0` to `>=10.0.0`
- **imageio:** Updated from `>=2.20.0,<2.34.0` to `>=2.34.0`

### NLP
- **spacy:** Updated from `>=3.4.0,<3.8.0` to `>=3.8.0`
- **nltk:** Updated from `>=3.7.0,<3.9.0` to `>=3.9.0`
- **textblob:** Updated from `>=0.17.0,<0.18.0` to `>=0.18.0`

### Time Series & Forecasting
- **statsmodels:** Updated from `>=0.13.0,<0.15.0` to `>=0.14.0` (0.14.6 is latest available, 0.15.0 doesn't exist yet)
- **prophet:** Updated from `>=1.1.0,<1.2.0` to `>=1.2.0`
- **pmdarima:** Updated from `>=2.0.0,<2.1.0` to `>=2.1.0`

### Model Training & Evaluation
- **xgboost:** Updated from `>=1.6.0,<2.0.0` to `>=2.0.0`
- **lightgbm:** Updated from `>=3.3.0,<4.0.0` to `>=4.0.0`
- **catboost:** Updated from `>=1.1.0,<1.3.0` to `>=1.3.0`
- **imbalanced-learn:** Updated from `>=0.10.0,<0.11.0` to `>=0.11.0`

### Other Packages
- **Recommendation Systems:** Updated implicit and scikit-surprise
- **Feature Engineering:** Updated category-encoders and feature-engine
- **Vector Databases:** Updated faiss-cpu and chromadb

## Additional Fixes

### Keras 3 / TensorFlow Compatibility

**Issue:** TensorFlow 2.20+ includes Keras 3, but Transformers library expects the older `tf-keras` package.

**Error:**
```
ValueError: Your currently installed version of Keras is Keras 3, but this is not yet supported in Transformers. Please install the backwards-compatible tf-keras package with `pip install tf-keras`.
```

**Solution:** Added `tf-keras>=2.20.0` to requirements.txt. This provides backwards compatibility for libraries that haven't yet migrated to Keras 3.

## Known Limitations

Some packages may still have Python 3.12 compatibility issues. If you encounter issues with other packages, check their Python 3.12 support status and update version constraints accordingly.

## References

- [Python 3.12 Release Notes](https://docs.python.org/3.12/whatsnew/3.12.html)
- [NumPy 1.26 Release Notes](https://numpy.org/doc/stable/release/1.26.0-notes.html)
- [setuptools distutils compatibility](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

