import unittest

from processor import process_records


class ProcessRecordsTests(unittest.TestCase):
    def test_processes_valid_records(self) -> None:
        result = process_records(
            [
                {
                    "date": "2026-08-14",
                    "product": "Laptop 14",
                    "quantity": 2,
                    "unit_price": 95000,
                    "cost": 73500,
                    "discount_pct": 10,
                }
            ]
        )

        self.assertEqual(result["received"], 1)
        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["rejected"], 0)
        self.assertEqual(result["revenue"], 171000.0)
        self.assertEqual(result["gross_profit"], 24000.0)

    def test_rejects_invalid_quantity(self) -> None:
        result = process_records(
            [
                {
                    "date": "2026-08-14",
                    "product": "Mouse USB",
                    "quantity": 0,
                    "unit_price": 1250,
                    "cost": 585,
                    "discount_pct": 0,
                }
            ]
        )

        self.assertEqual(result["accepted"], 0)
        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["reason"], "invalid_quantity")

    def test_rejects_invalid_discount(self) -> None:
        result = process_records(
            [
                {
                    "date": "2026-08-14",
                    "product": "Monitor 24",
                    "quantity": 1,
                    "unit_price": 18500,
                    "cost": 11200,
                    "discount_pct": 120,
                }
            ]
        )

        self.assertEqual(result["rejected"], 1)
        self.assertEqual(result["rejected_rows"][0]["reason"], "invalid_discount")

    def test_accepts_cleaning_of_strings(self) -> None:
        result = process_records(
            [
                {
                    "date": "2026/08/14",
                    "product": "  Webcam HD  ",
                    "quantity": "2",
                    "unit_price": "4600",
                    "cost": "2750",
                    "discount_pct": "5",
                }
            ]
        )

        self.assertEqual(result["accepted"], 1)
        self.assertEqual(result["accepted_rows"][0]["product"], "Webcam HD")
        self.assertEqual(result["accepted_rows"][0]["quantity"], 2)


if __name__ == "__main__":
    unittest.main()
