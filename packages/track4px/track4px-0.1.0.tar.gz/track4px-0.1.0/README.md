# 4PX Python Client

This is a Python client for the 4PX parcel tracker. It allows you to track your shipments.

## Installation

```bash
pip install track4px
```

## Usage

```python
from track4px import Track4PX

api = Track4PX()

# Realtime tracking

tracking = api.tracking("YOUR_SHIPMENT_NUMBER")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.