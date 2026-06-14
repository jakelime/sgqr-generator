# SGQR Generator: Singapore Bank Friendly

A Python package for parsing, modifying, and generating SGQR (Singapore Quick Response) codes.

SGQR is a unified payment QR code standard used in Singapore. It wraps various payment schemes (e.g. PayNow, NETS, GrabPay) using a Tag-Length-Value (TLV) encoding format. This library allows you to easily load an SGQR payload, update its fields (like transaction amount or payment reference), and generate a new, valid SGQR payload with a recomputed CRC16 checksum.

## Installation

Install the package via `pip` or your favorite package manager:

```bash
pip install sgqrgen
```

Or with `uv`:

```bash
uv add sgqrgen
```

## Quick Start

1. Using a Singapore Bank App (e.g. UOB TMRW), generate a MyQR code for payment
   1. For example, using UOB TMRW on the iPhone (updated as of 2026-06-15).
   1. Open and login to UOB TMRW app.
   1. Tap `Scan to pay`.
   1. On top top menu bar, choose `MR QR`.
   1. Scan the QR code generated using any QR Reader.
   1. Get the string `sgqr_str = "00020101021125280009SG.PAYNOW010100211+659876543203011530370254040.005802SG5913TAN AH GAO 63042968"`

1. Create an instance of the `SgQRGenerator` class with the `initial_string`.

1. Here is a simple example of how to parse an existing SGQR code, modify the price and comment, and output the updated QR code image:

   ```python
   from decimal import Decimal
   from sgqrgen import SgQRGenerator

   # Initial SGQR string (e.g. PayNow merchant QR code)
   sgqr_str = "00020101021125280009SG.PAYNOW010100211+659876543203011530370254040.005802SG5913TAN AH GAO 63042968"

   # Initialize generator
   qr_gen = SgQRGenerator(sgqr_str)

   # Modify amount to $8.00 and set comment/reference to "membership"
   qr_gen.change_price(Decimal("8.00")).change_comment("membership")

   # Export updated QR code image
   qr_gen.output_qrcode("output-qrcode.png")

   # Get updated raw SGQR string payload
   print("Updated payload:", qr_gen.qr)
   ```

## Features

- **TLV Parsing**: Easily decodes standard Tag-Length-Value SGQR payloads.
- **Price Modification**: Update the transaction amount dynamically (Tag 54) with automatic formatting.
- **Comment/Reference Update**: Add or update payment reference notes (Tag 62 / Sub-tag 01).
- **CRC16 Verification**: Automatic recomputation of the CRC16 checksum (Tag 63) when the payload is built/modified.
- **High-Quality QR Image Generation**: Utilizes `segno` to export QR codes in high-resolution scales.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
