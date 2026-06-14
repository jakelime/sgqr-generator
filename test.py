from sgqrgen import SgQRGenerator


def main():
    sgqr_test_str = "00020101021125280009SG.PAYNOW010100211+659876543203011530370254040.005802SG5913TAN AH GAO 63042968"
    qr_gen = SgQRGenerator(sgqr_test_str)
    qr_gen.change_price(8.00).change_comment("membership")
    qr_gen.output_qrcode("output-qrcode.png")


if __name__ == "__main__":
    main()
