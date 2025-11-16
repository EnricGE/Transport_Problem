from pathlib import Path

from pydantic import ValidationError
import pytest

from transport.context import ModelData
from transport.factory import ModelDataFactory


PATH = Path(__file__).parent


class TestValidationClient:
    """Test client validation errors"""
    
    def test_client_negative_demand_raises_error(self):
        """Test that negative demand values raise ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            model_data: ModelData = ModelDataFactory.from_json(
                PATH / "data" / "test_model_data_validation" / "test_model_data_validation_client.json"
            )
        
        error_message = str(exc_info.value)
        assert "Value" in error_message or "demand" in error_message.lower()


class TestValidationWorkshop:
    """Test workshop validation errors"""
    
    def test_workshop_validation(self):
        """Test workshop validation - add specific test case"""
        # This would need actual invalid workshop data to test
        pass


class TestValidationRoute:
    """Test route validation errors"""
    
    def test_route_validation(self):
        """Test route validation - add specific test case"""
        # This would need actual invalid route data to test
        pass
