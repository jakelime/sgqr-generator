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
