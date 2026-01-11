from pathlib import Path

from transport.engine.engine import Engine
from transport.factory.model_data_factory import ModelDataFactory


def main() -> None:

    root = Path(__file__).resolve().parents[2]

    data_path = root / "test/data/test_model_data/test_data_and_data_factory.json"

    data = ModelDataFactory.from_json(str(data_path))
    engine = Engine(model_data=data, engine_type="cbc")

    result = engine.run()

    print("Status:", result.status)

    if result.transport_quantity == {}:
        print("No solution extracted (model infeasible or not solved).")
        return

    print("Objective:", result.objective)
    for route_id, qty in result.transport_quantity.items():
        print(route_id, qty)


if __name__ == "__main__":
    main()
