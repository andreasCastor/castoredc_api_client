from typing import Union, Any, TYPE_CHECKING, List, Optional

from castoredc_api_client.exceptions import CastorException

if TYPE_CHECKING:
    from castoredc_api_client.castor_objects.castor_data_point import CastorDataPoint
    from castoredc_api_client.castor_objects.castor_form import CastorForm
    from castoredc_api_client.castor_objects.castor_study import CastorStudy


class CastorFormInstance:
    """Object representing a Castor form instance. Examples are survey instance or report instance."""

    def __init__(self, instance_id: str, instance_type: str, name_of_form: str,
                 study: "CastorStudy") -> None:
        """Creates a CastorFormInstance."""
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.name_of_form = name_of_form
        self.record = None

        self.instance_of = self.find_form(study)
        if self.instance_of is None:
            raise CastorException("The form that this is an instance of does not exist in the study!")

        self.data_points = []

    def add_data_point(self, data_point: "CastorDataPoint") -> None:
        """Adds a data point to the form instance."""
        self.data_points.append(data_point)
        data_point.form_instance = self

    def get_all_data_points(self) -> List["CastorDataPoint"]:
        """Returns all data_points of the form instance"""
        return self.data_points

    def get_single_data_point(self, field_id: str) -> Optional["CastorDataPoint"]:
        """Returns a single data_point based on id."""
        return next((data_point for data_point in self.data_points if data_point.field_id == field_id), None)

    # Helpers
    def find_form(self, study: "CastorStudy") -> Union["CastorForm", CastorException]:
        """Find which form is the originator of this instance."""
        if self.instance_type == "Survey":
            # Surveys can be found on name_of_form
            return study.instance_of_form(self.name_of_form, self.instance_type)
        else:
            # Reports can be found on instance_id
            return study.instance_of_form(self.instance_id, self.instance_type)

    # Standard Operators
    def __eq__(self, other: Any) -> Union[bool, type(NotImplemented)]:
        if not isinstance(other, CastorFormInstance):
            return NotImplemented
        else:
            return self.instance_id == other.instance_id

    def __repr__(self) -> str:
        return self.instance_id
