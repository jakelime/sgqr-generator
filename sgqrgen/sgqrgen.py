import segno


class SgQRGenerator:
    def __init__(self, initial_sgqr_str: str):
        if not initial_sgqr_str:
            raise ValueError("initial_sgqr_str cannot be empty")
        self._tags = self.parse_sgqr(initial_sgqr_str)
        self.qr = initial_sgqr_str

    @staticmethod
    def crc16(data: bytes) -> int:
        """Computes the CRC-16/CCITT-FALSE checksum for the given data."""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc

    @staticmethod
    def parse_sgqr(sgqr_str: str) -> dict[str, str]:
        """Parses a Tag-Length-Value (TLV) encoded SGQR string into a dictionary."""
        tags = {}
        i = 0
        while i < len(sgqr_str):
            if i + 4 > len(sgqr_str):
                break
            tag = sgqr_str[i : i + 2]
            length_str = sgqr_str[i + 2 : i + 4]
            try:
                length = int(length_str)
            except ValueError:
                break
            val = sgqr_str[i + 4 : i + 4 + length]
            tags[tag] = val
            i += 4 + length
            if tag == "63":
                break
        return tags

    @staticmethod
    def build_sgqr(tags: dict[str, str]) -> str:
        """Builds a TLV-encoded SGQR string from a tags dictionary, recomputing Tag 63 (CRC)."""
        parts = []
        # Build all tags except Tag 63 (CRC)
        for tag in sorted(tags.keys()):
            if tag == "63":
                continue
            val = tags[tag]
            parts.append(f"{tag}{len(val):02d}{val}")

        partial_str = "".join(parts) + "6304"
        crc_val = SgQRGenerator.crc16(partial_str.encode("utf-8"))
        return f"{partial_str}{crc_val:04X}"

    def change_price(self, amount: float) -> "SgQRGenerator":
        """Changes the price (Tag 54) in the SGQR string and returns the generator."""
        self._tags["54"] = f"{amount:.2f}"
        self.qr = self.build_sgqr(self._tags)
        return self

    def change_comment(self, msg: str = "") -> "SgQRGenerator":
        """Changes the payment comment/reference (Tag 62) in the SGQR string and returns the generator."""
        if not msg:
            self._tags.pop("62", None)
        else:
            # Tag 62 is Additional Data Field Template
            # Sub-tag 01 is Bill Number / Reference Number
            sub_tag = "01"
            sub_len = f"{len(msg):02d}"
            tag_62_val = f"{sub_tag}{sub_len}{msg}"
            self._tags["62"] = tag_62_val
        self.qr = self.build_sgqr(self._tags)
        return self

    def output_qrcode(self, outname: str = "output-qrcode.png"):
        qrcode = segno.make(self.qr)
        qrcode.save(outname, scale=20, border=2)
        print(f"generated qr code {outname=}")
