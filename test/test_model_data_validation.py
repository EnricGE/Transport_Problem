from pathlib import Path

from pydantic import ValidationError
import pytest

from transport.context import ModelData
from transport.factory import ModelDataFactory


PATH = Path(__file__).parent


class TestValidationClient:

    with pytest.raises(ValidationError) as error:
        model_data: ModelData = ModelDataFactory.from_json(
            PATH / "data" / "test_model_data_validation_client.json"
        )
    
    assert "Missatge" in str(error.value)
        
