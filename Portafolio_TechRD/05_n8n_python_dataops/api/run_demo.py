import json
from pathlib import Path

from processor import process_records


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "data" / "ventas_demo.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    result = process_records(payload["records"])

    print("DataOps demo")
    print(f"Received: {result['received']}")
    print(f"Accepted: {result['accepted']}")
    print(f"Rejected: {result['rejected']}")
    print(f"Revenue: {result['revenue']:.2f}")
    print(f"Gross profit: {result['gross_profit']:.2f}")
    print(f"Gross margin: {result['gross_margin_pct']:.2f}%")

    if result["rejected_rows"]:
        print("\nRejected rows:")
        for item in result["rejected_rows"]:
            print(f"- {item['reason']}: {item['row']}")


if __name__ == "__main__":
    main()
