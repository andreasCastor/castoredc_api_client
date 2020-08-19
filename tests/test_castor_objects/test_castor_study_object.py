# -*- coding: utf-8 -*-
"""
Testing class for the CastorStudy class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from castoredc_api_client.castor_objects import CastorStep, CastorField, CastorForm, CastorStudy


class TestCastorStudy:
    """Testing class for CastorStudy object unit tests."""

    def test_study_create(self):
        """Tests creation of a study."""
        study = CastorStudy("FAKE-ID")
        assert type(study) is CastorStudy
        assert study.study_id == "FAKE-ID"

    def test_study_add_form(self):
        """Tests adding a form to a study."""
        study = CastorStudy("FAKE-ID")
        assert len(study.forms) == 0
        form = CastorForm("Survey", "FAKE-FORM-ID", "Fake Survey")
        study.add_form(form)
        assert len(study.forms) == 1
        assert study.forms[0] == form
        assert form.study == study

    def test_study_get_all_forms(self, study_with_forms):
        """Tests getting all forms from the study."""
        forms = study_with_forms.get_all_forms()
        assert len(forms) == 4
        for form in forms:
            assert type(form) is CastorForm

    def test_study_get_single_form(self, study_with_forms):
        """Tests getting a single form from the study."""
        form = study_with_forms.get_single_form("FAKE-REPORT-ID2")
        assert type(form) is CastorForm
        assert form.form_id == "FAKE-REPORT-ID2"
        assert form.form_type == "Report"
        assert form.form_name == "Fake Report"

    def test_study_get_single_form_fail(self, study_with_forms):
        """Tests failing to get a form from the study."""
        form = study_with_forms.get_single_form("FAKE-REPORT-ID3")
        assert form is None

    def test_study_get_all_steps(self, complete_study):
        """Tests getting all steps from the study."""
        steps = complete_study.get_all_steps()
        assert len(steps) == 9
        for step in steps:
            assert type(step) is CastorStep

    def test_study_get_single_step(self, complete_study):
        """Tests getting a single step from the study."""
        step = complete_study.get_single_step("FAKE-REPORT-STEP-ID2")
        assert type(step) is CastorStep
        assert step.step_id == "FAKE-REPORT-STEP-ID2"
        assert step.step_name == "Report Step 1b"

    def test_study_get_single_step_fail(self, complete_study):
        """Tests failing to get a step from the study."""
        step = complete_study.get_single_step("FAKE-REPORT-STEP-ID5")
        assert step is None

    def test_study_get_all_fields(self, complete_study):
        """Tests getting all fields from the study."""
        fields = complete_study.get_all_fields()
        assert len(fields) == 17
        for field in fields:
            assert type(field) is CastorField

    def test_study_get_single_field(self, complete_study):
        """Tests getting a single field from the study."""
        field = complete_study.get_single_field("FAKE-SURVEY-FIELD-ID3")
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID3"
        assert field.field_name == "Survey Field 1a3"

    def test_study_get_single_field_fail(self, complete_study):
        """Tests failing to get a field from the study."""
        field = complete_study.get_single_field("FAKE-SURVEY-FIELD-ID7")
        assert field is None

    def test_study_get_study_fields(self, complete_study):
        """Tests getting all study fields."""
        fields = complete_study.get_all_study_fields()
        assert len(fields) == 4
        for field in fields:
            assert type(field) is CastorField
            assert field.step.form.form_type == "Study"

    def test_study_get_survey_fields(self, complete_study):
        """Tests getting all survey fields."""
        fields = complete_study.get_all_survey_fields()
        assert len(fields) == 6
        for field in fields:
            assert type(field) is CastorField
            assert field.step.form.form_type == "Survey"

    def test_study_get_report_fields(self, complete_study):
        """Tests getting all report fields."""
        fields = complete_study.get_all_report_fields()
        assert len(fields) == 7
        for field in fields:
            assert type(field) is CastorField
            assert field.step.form.form_type == "Report"