import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools/import_legacy_offsets.py"
spec = importlib.util.spec_from_file_location("legacy_import", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

HEADER = "type,loader,field,value_decimal,value_hex,il_offset\n"

class LegacyImportTests(unittest.TestCase):
    def run_csv(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.csv"
            path.write_text(content, encoding="utf-8")
            return module.convert(path)

    def test_signed_negative_offset_and_nonoperational(self):
        result = self.run_csv(HEADER + "Players,loadplayersOffsets_8_0_0,Field,-92,0xFFFFFFA4,IL_0001\n")
        self.assertFalse(result["operational"])
        self.assertEqual(result["entries"][0]["valueDecimal"], -92)
        self.assertEqual(result["entries"][0]["status"], "legacy-il-observed")

    def test_rejects_mismatched_hex(self):
        with self.assertRaises(ValueError):
            self.run_csv(HEADER + "Players,loader,Field,4,0x00000005,IL_0001\n")

    def test_rejects_duplicate_fields_per_loader(self):
        with self.assertRaises(ValueError):
            self.run_csv(HEADER + "P,L,F,4,0x4,IL_1\nP,L,F,4,0x4,IL_2\n")

if __name__ == "__main__":
    unittest.main()
