# -*- coding: utf-8 -*-
"""
Main CastorClient object for communication with Castor EDC API.
Link: https://data.castoredc.com/api

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

import json
import logging
import requests


from castoredc_api_client.exceptions import castor_exception_handler, CastorException


class CastorClient:
    # INITIALIZATION
    base_url = "https://data.castoredc.com/api"
    auth_url = "https://data.castoredc.com/oauth/token"
    headers = {
        "accept": "application/hal+json",
        "Content-Type": "application/json; charset=utf-8",
    }

    def __init__(self, client_id, client_secret):
        """Create a CastorClient to communicate with a Castor database. Links the CastorClient to an account with
        client_id and client_secret. If test is set to True, suppresses logging to the command line."""
        # Instantiate Requests sessions
        self.s = requests.Session()
        self.s.headers.update(self.headers)

        # Instantiate logging
        self.logger = logging.getLogger(__name__)

        # Grab authentication token for given client
        token = self.request_auth_token(client_id, client_secret)
        self.headers["authorization"] = "Bearer " + token
        self.s.headers.update(self.headers)

        # Instantiate global study variables
        self.study_url = ""
        self.field_references = {}

    def link_study(self, study_id):
        """Link a study to the CastorClient based on the study_id"""
        self.study_url = self.base_url + "/study/" + study_id

    def gather_field_map(self):
        """Queries the study and collects all fields that are used at least once."""
        # TODO: Add type of field to field map
        self.field_references["study"] = self.study_fields()
        self.field_references["reports"] = self.report_fields()
        self.field_references["surveys"] = self.survey_fields()

    # API ENDPOINTS
    # COUNTRY
    def all_countries(self):
        """Returns a list of dicts of all available countries."""
        endpoint = "/country"
        raw_data = self.retrieve_general_data(endpoint=endpoint)
        return raw_data["results"]

    def single_country(self, country_id):
        """Returns a dict with the given country based on country_id.
        Returns None if country not found."""
        endpoint = "/country/{0}".format(country_id)
        return self.retrieve_general_data(endpoint=endpoint)

    # DATA-POINT-COLLECTION GET (STUDY)
    def all_study_data_points(self):
        """Returns a list of dicts of all study data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/study", data_name="items"
        )

    def all_report_data_points(self):
        """Returns a list of dicts all report data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/report-instance", data_name="items"
        )

    def all_survey_data_points(self):
        """Returns a list of dicts all survey data."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/data-point-collection/survey-instance", data_name="items"
        )

    # DATA-POINT-COLLECTION GET (INSTANCE)
    def single_report_instance_data_points(self, report_id):
        """Returns a list of the data for given report_id. 
        Returns None if report not found."""
        url = "/data-point-collection/report-instance/{report_id}".format(
            report_id=report_id
        )
        return self.retrieve_data_points(url)

    def single_survey_instance_data_points(self, survey_instance_id):
        """Returns a list of data from a single survey instance id.
        Returns None if report not found."""
        url = "/data-point-collection/survey-instance/{survey_instance_id}".format(
            survey_instance_id=survey_instance_id
        )
        return self.retrieve_data_points(url)

    def single_survey_package_instance_data_points(self, survey_package_instance_id):
        """Returns a list of data from a single survey package instance. 
        Returns None if package not found."""
        url = "/data-point-collection/survey-package-instance/{survey_package_instance_id}".format(
            survey_package_instance_id=survey_package_instance_id
        )
        return self.retrieve_data_points(url)

    # DATA-POINT-COLLECTION GET (RECORD)
    def all_study_data_points_record(self, record_id):
        """Returns a list of all study data collected for given record. 
        Returns None if record not found."""
        url = "/record/{record_id}/data-point-collection/study".format(
            record_id=record_id
        )
        return self.retrieve_data_points(url)

    def all_report_data_points_record(self, record_id):
        """Returns a list of all report data collected for given record. 
        Returns None if record not found."""
        url = "/record/{record_id}/data-point-collection/report-instance".format(
            record_id=record_id
        )
        return self.retrieve_data_points(url)

    def single_report_data_points_record(self, record_id, report_id):
        """Returns a list of the data for given report_id for given. 
        Returns None if record or report not found."""
        url = "/record/{record_id}/data-point-collection/report-instance/{report_id}".format(
            record_id=record_id, report_id=report_id
        )
        return self.retrieve_data_points(url)

    def all_survey_data_points_record(self, record_id):
        """Returns a list of all survey data collected for given record. 
        Returns None if record not found."""
        url = "/record/{record_id}/data-point-collection/survey-instance".format(
            record_id=record_id
        )
        return self.retrieve_data_points(url)

    def single_survey_data_points_record(self, record_id, survey_instance_id):
        """Returns a list of data from a single survey instance 
        collected for given record record_id. Returns None if record not found."""
        url = "/record/{record_id}/data-point-collection/survey-instance/{survey_instance_id}".format(
            record_id=record_id, survey_instance_id=survey_instance_id
        )
        return self.retrieve_data_points(url)

    def single_survey_package_data_points_record(
        self, record_id, survey_package_instance_id
    ):
        """Returns a list of data from a single survey package instance 
        collected for given record record_id. Returns None if record not found"""
        url = "/record/{record_id}/data-point-collection/survey-package-instance/{survey_package_instance_id}".format(
            record_id=record_id, survey_package_instance_id=survey_package_instance_id
        )
        return self.retrieve_data_points(url)

    # DATA-POINT-COLLECTION POST (RECORD)
    def update_study_data_record(self, record_id, common, body):
        """Creates/updates a collection of field values. 
        Returns None if record not found.
        Post Data Models:
        Common: {
            "change_reason": "string",
            "confirmed_changes": boolean
                }
        Body: [{
            "field_id": "string",
            "field_value": "string",
            "change_reason": "string",
            "confirmed_changes": boolean
                }]
            """
        url = self.study_url + "/record/{record_id}/data-point-collection/study".format(
            record_id=record_id
        )
        post_data = {"common": common, "data": body}
        return self.castor_post(url, post_data)

    def update_report_data_record(self, record_id, report_id, common, body):
        """Creates/updates a report instance. 
        Returns None if record not found.
        Post Data Models:
        Common: {
            "change_reason": "string",
            "confirmed_changes": boolean
                }
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
            "change_reason": "string",
            "confirmed_changes": boolean
                }]
        """
        url = (
            self.study_url
            + "/record/{record_id}/data-point-collection/report-instance/{report_id}".format(
                record_id=record_id, report_id=report_id
            )
        )
        post_data = {"common": common, "data": body}
        return self.castor_post(url, post_data)

    def update_survey_instance_data_record(self, record_id, survey_instance_id, body):
        """Creates/updates a survey instance. 
        Returns None if record not found.
        Post Data Models:
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
                }]
        """
        url = (
            self.study_url
            + "/record/{record_id}/data-point-collection/survey-instance/{survey_instance_id}".format(
                record_id=record_id, survey_instance_id=survey_instance_id
            )
        )
        post_data = {"data": body}
        return self.castor_post(url, post_data)

    def update_survey_package_instance_data_record(
        self, record_id, survey_package_instance_id, body
    ):
        """Creates/updates a survey package instance. 
        Returns None if record not found.
        Post Data Models:
        Body: [{
            "field_id": "string",
            "instance_id": "string",
            "field_value": "string",
                }]
        """
        url = (
            self.study_url
            + "/record/{record_id}/data-point-collection/survey-package-instance/{survey_package_instance_id}".format(
                record_id=record_id,
                survey_package_instance_id=survey_package_instance_id,
            )
        )
        post_data = {"data": body}
        return self.castor_post(url, post_data)

    # FIELDS
    def all_fields(self):
        """Returns a list of dicts of all fields."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field",
            data_name="fields",
            query_string=["include=metadata|validations|optiongroup"],
        )

    def single_field(self, field_id):
        """Returns a dict of a single field.
        Returns None if field_id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field",
            data_id=field_id,
            params={"include": "metadata|validations|optiongroup"},
        )

    # FIELD DEPENDENCY
    def all_field_dependencies(self):
        """Returns a list of dicts of all field depencencies."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-dependency", data_name="fieldDependencies"
        )

    def single_field_dependency(self, field_dependency_id):
        """Returns a single dict of a field dependency.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-dependency", data_id=field_dependency_id
        )

    # FIELD OPTION GROUP
    def all_field_optiongroups(self):
        """Returns a list of dicts of all field option groups."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-optiongroup", data_name="fieldOptionGroups"
        )

    def single_field_optiongroup(self, field_optiongroup_id):
        """Returns a single dict of a field optiongroup.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-optiongroup", data_id=field_optiongroup_id
        )

    # FIELD VALIDATION
    def all_field_validations(self):
        """Returns a list of dicts of all field validations."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/field-validation", data_name="fieldValidations"
        )

    def single_field_validation(self, field_validation_id):
        """Returns a single dict of a field validation.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/field-validation", data_id=field_validation_id
        )

    # INSTITUTES
    def all_institutes(self):
        """Returns a list of dicts of all institutes."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/institute", data_name="institutes"
        )

    def single_institute(self, institute_id):
        """Returns a single dict of an institute.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/institute", data_id=institute_id)

    # METADATA
    def all_metadata(self):
        """Returns a list of dicts of all metadata."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/metadata", data_name="metadatas"
        )

    def single_metadata(self, metadata_id):
        """Returns a single dict of an metadata.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/metadata", data_id=metadata_id)

    # METADATATYPE
    def all_metadatatypes(self):
        """Returns a list of dicts of all metadatatypes."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/metadatatype", data_name="metadatatypes"
        )

    def single_metadatatype(self, metadatatype_id):
        """Returns a single dict of an metadatatype.
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/metadatatype", data_id=metadatatype_id
        )

    # PHASES
    def all_phases(self):
        """Returns a list of dicts of all phases."""
        return self.retrieve_all_data_by_endpoint(endpoint="/phase", data_name="phases")

    def single_phase(self, phase_id):
        """Returns a single dict of an phase.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/phase", data_id=phase_id)

    # QUERIES
    def all_queries(self):
        """Returns a list of dicts of all queries."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/query", data_name="queries"
        )

    def single_query(self, query_id):
        """Returns a single dict of an query.
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/query", data_id=query_id)

    # RECORDS
    def all_records(self, institute_id=None, archived=None):
        """Returns a list of dicts of all records. 
        Archived can be None (all records), 0 (unarchived records) 
        or 1 (archived records)."""
        query_string = []
        if institute_id is not None:
            query_string.append("institute={0}".format(institute_id))
        if archived is not None:
            query_string.append("archived={0}".format(archived))
        return self.retrieve_all_data_by_endpoint(
            endpoint="/record", data_name="records", query_string=query_string
        )

    def single_record(self, record_id):
        """Returns a dict of a record.
        Returns None when record not found."""
        return self.retrieve_data_by_id(endpoint="/record", data_id=record_id)

    def create_record(self, institute_id, email, record_id=None, ccr_patient_id=None):
        """Creates a record. Record_id is only necessary when id generation
        strategy is set to free text. Ccr_patient_id is an optional parameter.
        Returns None when record creation failed."""
        body = {
            "record_id": record_id,
            "ccr_record_id": ccr_patient_id,
            "institute_id": institute_id,
            "email_address": email,
        }
        url = self.study_url + "/record"
        return self.castor_post(url, body)

    # REPORTS
    def all_reports(self):
        """Returns a list of dicts of all reports."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/report", data_name="reports"
        )

    def single_report(self, report_id):
        """Returns a single dict of an report. 
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/report", data_id=report_id)

    # REPORT INSTANCES
    def all_report_instances(self):
        """Returns a list of dicts of all report_instances."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/report-instance", data_name="reportInstances"
        )

    def single_report_instance(self, report_instance_id):
        """Returns a single dict of an report_instance. 
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/report-instance", data_id=report_instance_id
        )

    def all_report_instances_record(self, record_id):
        """Returns a list of dicts of all report_instances for record_id. 
        Returns None if record not found."""
        formatted_endpoint = "/record/{0}/report-instance".format(record_id)
        return self.retrieve_all_data_by_endpoint(
            endpoint=formatted_endpoint, data_name="reportInstances"
        )

    def single_report_instance_record(self, record_id, report_instance_id):
        """Returns a dict containing the given report for record. 
        Returns None if record or report not found."""
        formatted_endpoint = "/record/{0}/report-instance".format(record_id)
        return self.retrieve_data_by_id(
            endpoint=formatted_endpoint, data_id=report_instance_id
        )

    def create_report_instance_record(
        self, record_id, report_id, report_name_custom, parent_id=None
    ):
        """Creates a report instance for a record.
        Returns None if creation failed."""
        url = self.study_url + "/record/{0}/report-instance".format(record_id)
        body = {
            "report_id": report_id,
            "report_name_custom": report_name_custom,
            "parent_id": parent_id,
        }
        return self.castor_post(url, body)

    def create_multiple_report_instances_record(self, record_id, body):
        """Creates multiple report instances for a record.
        Body should be a list of dictionaries formatted according to:
        "report_id": report_id,
        "report_name_custom": report_name_custom,
        "parent_id": parent_id
        """
        data = {"data": body}
        url = self.study_url + "/record/{0}/report-instance-collection".format(
            record_id
        )
        return self.castor_post(url, data)

    # REPORT-DATA-ENTRY
    def single_report_instance_all_fields_record(self, record_id, report_instance_id):
        """Returns a list of all data for a report for a record.
        Returns None if report not found for given id."""
        formatted_url = "/record/{0}/data-point/report/{1}".format(
            record_id, report_instance_id
        )
        return self.retrieve_all_data_by_endpoint(
            endpoint=formatted_url, data_name="ReportDataPoints"
        )

    def single_report_instance_single_field_record(
        self, record_id, report_instance_id, field_id
    ):
        """Returns a data point for a report for a record.
        Returns None if report not found for given record or field not found
        for given report."""
        data_point = "/".join([report_instance_id, field_id])
        formatted_url = "/record/{0}/data-point/report".format(record_id)
        return self.retrieve_data_by_id(endpoint=formatted_url, data_id=data_point)

    def update_report_instance_single_field_record(
        self,
        record_id,
        report_ins_id,
        field_id,
        change_reason,
        field_value=None,
        file=None,
    ):
        """Updates a report field value. Either field_value or file needs to be None.
        Returns None if data creation failed."""
        # TODO: Allow file uploading
        endpoint = "/record/{0}/data-point/report/{1}/{2}".format(
            record_id, report_ins_id, field_id
        )
        url = self.study_url + endpoint

        # TODO: Throw error when both file and field_value are None or not None
        body = {}

        if field_value is not None:
            body = {
                "field_value": str(field_value),
                "change_reason": change_reason,
                "instance_id": report_ins_id,
            }

        elif file is not None:
            body = {
                "change_reason": change_reason,
                "instance_id": report_ins_id,
                "upload_file": file,
            }

        return self.castor_post(url, body)

    # REPORT-STEP
    def single_report_all_steps(self, report_id):
        """Returns a list of dicts of all steps of a single report.
        Returns None if report not found."""
        endpoint = "/report/{0}/report-step".format(report_id)
        return self.retrieve_all_data_by_endpoint(
            endpoint=endpoint, data_name="report_steps"
        )

    def single_report_single_step(self, report_id, report_step_id):
        """Returns a single dict of a step of a report. 
        Returns None if report or step not found."""
        endpoint = "/report/{0}/report-step".format(report_id)
        return self.retrieve_data_by_id(endpoint=endpoint, data_id=report_step_id)

    # STEP
    def all_steps(self):
        """Returns a list of dicts of all study steps."""
        return self.retrieve_all_data_by_endpoint(endpoint="/step", data_name="steps")

    def single_step(self, step_id):
        """Returns a single dict of a step in the study. 
        Returns None if id not found.."""
        return self.retrieve_data_by_id(endpoint="/step", data_id=step_id)

    # STUDY
    def all_studies(self):
        """Returns a list of dicts of studies you have access to."""
        endpoint = "/study"
        all_studies = self.retrieve_general_data(
            endpoint, embedded=True, data_id="study"
        )
        return all_studies

    def single_study(self, study_id):
        """Returns a dict of a single study. 
        Returns None if study not found or not authorized to view study."""
        endpoint = "/study/{0}".format(study_id)
        return self.retrieve_general_data(endpoint)

    def all_users_study(self, study_id):
        """Returns a list of dicts of users that have access to this study.
        Returns None if study not found or not authorized to view study."""
        endpoint = "/study/{0}/user".format(study_id)
        all_users = self.retrieve_general_data(
            endpoint, embedded=True, data_id="studyUsers"
        )
        return all_users

    def single_user_study(self, study_id, user_id):
        """Returns a user for given study.
        Returns None if study/user not found or not authorized to view study.
        """
        endpoint = "/study/{0}/user/{1}".format(study_id, user_id)
        return self.retrieve_general_data(endpoint)

    # STUDY-DATA-ENTRY
    def all_study_fields_record(self, record_id):
        """Returns a list of all study fields of a record.
        Returns None if record not found."""
        endpoint = "/record/{record_id}/data-point/study".format(record_id=record_id)
        return self.retrieve_all_data_by_endpoint(endpoint, data_name="StudyDataPoints")

    def single_study_field_record(self, record_id, field_id):
        """Returns the value for a single field for a record in the study.
        Returns None if record or field not found."""
        endpoint = "/record/{record_id}/data-point/study".format(record_id=record_id)
        return self.retrieve_data_by_id(endpoint, data_id=field_id)

    def update_single_study_field_record(
        self, record_id, field_id, field_value, change_reason
    ):
        """Update a data point for a record.
        Returns None if target not found."""
        # TODO: create file uploading possibility
        url = self.study_url + "/record/{record_id}/data-point/study/{field_id}".format(
            record_id=record_id, field_id=field_id
        )
        body = {
            "field_value": str(field_value),
            "change_reason": change_reason,
            # "upload_file": None,
        }
        return self.castor_post(url, body)

    # STATISTICS
    def statistics(self):
        endpoint = "statistics"
        return self.retrieve_data_by_id("", endpoint)

    # SURVEY
    def all_surveys(self):
        """Returns a list of dicts of all available surveys."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/survey", data_name="surveys"
        )

    def single_survey(self, survey_id):
        """Returns a single dict of a survey in the study. 
        Returns None if id not found."""
        return self.retrieve_data_by_id(endpoint="/survey", data_id=survey_id)

    def all_survey_packages(self):
        """Returns a list of dicts of all available survey packages."""
        return self.retrieve_all_data_by_endpoint(
            endpoint="/surveypackage", data_name="survey_packages"
        )

    def single_survey_package(self, survey_package_id):
        """Returns a single dict of a survey package in the study. 
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/surveypackage", data_id=survey_package_id
        )

    def all_survey_package_instances(self, record=None):
        """Returns a list of dicts of all available survey packages."""
        endpoint = "/surveypackageinstance"
        dataname = "surveypackageinstance"
        if record is None:
            return self.retrieve_all_data_by_endpoint(
                endpoint=endpoint, data_name=dataname
            )
        else:
            query = ["record_id=" + record]
            return self.retrieve_all_data_by_endpoint(
                endpoint=endpoint, data_name=dataname, query_string=query
            )

    def single_survey_package_instance(self, survey_package_instance_id):
        """Returns a single dict of a survey package in the study. 
        Returns None if id not found."""
        return self.retrieve_data_by_id(
            endpoint="/surveypackageinstance", data_id=survey_package_instance_id
        )

    # TODO: refactor this, should be able to be more concise
    def create_survey_package_instance(
        self,
        survey_package_id,
        record_id,
        email_address,
        ccr_patient_id=None,
        package_invitation_subject=None,
        package_invitation=None,
        auto_send=None,
        auto_lock_on_finish=None,
    ):
        """Create a survey package. 
        Arguments marked with None are non-obligatory."""
        url = self.study_url + "/surveypackageinstance"
        temp_body = {
            "survey_package_id": survey_package_id,
            "record_id": record_id,
            "ccr_patient_id": ccr_patient_id,
            "email_address": email_address,
            "package_invitation_subject": package_invitation_subject,
            "package_invitation": package_invitation,
            "auto_send": auto_send,
            "auto_lock_on_finish": auto_lock_on_finish,
        }

        body = {}
        for item in temp_body:
            if temp_body[item] is not None:
                body[item] = temp_body[item]

        return self.castor_post(url, body)

    def patch_survey_package_instance(self, survey_package_instance_id, status):
        """Lock/unlock survey package."""
        url = self.study_url + "/surveypackageinstance/" + survey_package_instance_id
        body = {
            "locked": status,
        }
        return self.castor_patch(url, body)

    # SURVEY-DATA-ENTRY
    def single_survey_instance_all_fields_record(self, record_id, survey_instance_id):
        """Retrieves a list of fields with data for a single survey.
        Returns None if record or survey not found."""
        endpoint = "/record/{record_id}/data-point/survey/{survey_instance_id}".format(
            record_id=record_id, survey_instance_id=survey_instance_id
        )
        return self.retrieve_all_data_by_endpoint(
            endpoint, data_name="SurveyDataPoints"
        )

    def single_survey_instance_single_field_record(
        self, record_id, survey_instance_id, field_id
    ):
        """Retrieves a single field with data for the given survey.
        Returns None if record, survey or field not found."""
        endpoint = "/record/{record_id}/data-point/survey/{survey_instance_id}".format(
            record_id=record_id, survey_instance_id=survey_instance_id
        )
        return self.retrieve_data_by_id(endpoint, data_id=field_id)

    def update_survey_instance_single_field_record(
        self, record_id, survey_instance_id, field_id, field_value, change_reason
    ):
        """Update a field result for a survey (package) instance.
        Returns None if survey not found"""
        url = (
            self.study_url
            + "/record/{record_id}/data-point/survey/{survey_instance_id}/{field_id}".format(
                record_id=record_id,
                survey_instance_id=survey_instance_id,
                field_id=field_id,
            )
        )

        body = {
            "field_value": str(field_value),
            "change_reason": change_reason,
            "instance_id": survey_instance_id,
            # "upload_file": None,
        }
        return self.castor_post(url, body)

    # SURVEY-STEP
    def single_survey_all_steps(self, survey_id):
        """Retrieves a list of dicts of steps for a single survey.
        Returns None if survey not found."""
        endpoint = "/survey/{survey_id}/survey-step".format(survey_id=survey_id)
        return self.retrieve_all_data_by_endpoint(endpoint, data_name="survey_steps")

    def single_survey_single_step(self, survey_id, survey_step_id):
        """Retrieves a dict of a single survey step.
        Returns None if survey or step not found."""
        endpoint = "/survey/{survey_id}/survey-step".format(survey_id=survey_id)
        return self.retrieve_data_by_id(endpoint, data_id=survey_step_id)

    # USER
    def all_users(self):
        """Retrieves list of users that current user is authorized to see."""
        endpoint = "/user"
        return self.retrieve_general_data(endpoint, embedded=True, data_id="user")

    def single_user(self, user_id):
        """Retrieves a single user by ID."""
        endpoint = "/user/{user_id}".format(user_id=user_id)
        return self.retrieve_general_data(endpoint)

    # RECORD PROGRESS
    def record_progress(self):
        # TODO: Only retrieves 1 page (25 records) and does not give page count through the API, so can't use
        # TODO: retrieve multiple pages. Need to work with amount of records in study.
        endpoint = "/record-progress/steps"
        raw_data = self.retrieve_data_by_id(endpoint, data_id="")
        return raw_data["_embedded"]["records"]

    # HELPER FUNCTIONS
    # noinspection PyMethodMayBeStatic
    def castor_get(self, url, params):
        """Query the Castor server with a certain request."""
        try:
            response = self.s.get(url=url, params=params)
            content = json.loads(response.content)
            # Check if the return object is an error
            if "status" in content.keys() and "detail" in content.keys():
                # If Castor server throws an error, raise an error
                raise CastorException(str(content["status"]) + " " + content["detail"])
            else:
                return content
        except requests.exceptions.RequestException as e:
            raise CastorException(e)

    @castor_exception_handler
    def castor_post(self, url, body):
        """Helper function to post body to url."""
        try:
            body = json.dumps(body).encode()
            response = self.s.post(url=url, data=body)
            # Log Auditing Trail for changing data
            content = json.loads(response.content)
            # Check if the return object is an error
            if "status" in content.keys() and "detail" in content.keys():
                # If Castor server throws an error, raise an error
                raise CastorException(str(content["status"]) + " " + content["detail"])
            else:
                return content
        except requests.exceptions.RequestException as e:
            raise CastorException(e)

    @castor_exception_handler
    def castor_patch(self, url, body):
        """Helper function to patch body to url."""
        try:
            body = json.dumps(body).encode()
            response = self.s.patch(url=url, data=body)
            # Log Auditing Trail for changing data
            content = json.loads(response.content)
            if "status" in content.keys():
                # If Castor server throws an error, raise an error
                raise CastorException(str(content["status"]) + " " + content["detail"])
            else:
                return content
        except requests.exceptions.RequestException as e:
            raise CastorException(e)

    @castor_exception_handler
    def request_auth_token(self, client_id, client_secret):
        """Request an authentication token from Castor EDC for given client."""
        auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        }
        response = self.castor_post(url=self.auth_url, body=auth_data)
        token = response["access_token"]
        return token

    @castor_exception_handler
    def retrieve_general_data(self, endpoint, embedded=False, data_id=""):
        url = self.base_url + endpoint
        response = self.castor_get(url=url, params=None)
        if embedded:
            data = response["_embedded"][data_id]
        else:
            data = response

        return data

    @castor_exception_handler
    def retrieve_data_points(self, endpoint):
        """Retrieves data point with data_id.
        Returns None if data_id is not found at given endpoint."""
        url = self.study_url + endpoint
        data = self.castor_get(url=url, params=None)
        return data["_embedded"]["items"]

    @castor_exception_handler
    def retrieve_data_by_id(self, endpoint, data_id, params=None):
        """Retrieves data point with data_id.
        Returns None if data_id is not found at given endpoint."""
        # TODO: Refactor special case that does not have multiple pages
        # but also is not filtered on id (see record-progress)
        if data_id != "":
            url = self.study_url + endpoint + "/{data_id}".format(data_id=data_id)
        # Ugly hack to make this function also work for special cases
        # See also TODO
        else:
            url = self.study_url + endpoint
        return self.castor_get(url=url, params=params)

    def retrieve_all_data_by_endpoint(self, endpoint, data_name, query_string=None):
        """Retrieves all data on endpoint.
        data_name is that which holds data within ['_embedded'] (ex: 'fields')
        query_string is a list of extra information to be sent."""
        formatted_suffix = endpoint
        if query_string is not None:
            formatted_suffix += "?" + "+".join(query_string)
        url = self.study_url + formatted_suffix
        return self.retrieve_multiple_pages(url=url, data_name=data_name)

    @castor_exception_handler
    def retrieve_multiple_pages(self, url, data_name):
        """Helper function to gather all data when there are multiple pages.
        data_name is that which holds data within ['_embedded'] (ex: 'fields')
        """
        variables = []
        response = self.retrieve_single_page(url=url, page="1")
        fields = response["_embedded"][data_name]
        pages = response["page_count"] + 1
        variables.extend(fields)
        for i in range(2, pages):
            response = self.retrieve_single_page(url, i)
            fields = response["_embedded"][data_name]
            variables.extend(fields)
        return variables

    def retrieve_single_page(self, url, page):
        """Helper function to query a single page and return the data from that page."""
        # TODO: Handle this through params in requests
        if "?" in url:
            local_url = url + "&page={0}".format(page)
        else:
            local_url = url + "?page={0}".format(page)
        response = self.castor_get(url=local_url, params=None)
        return response

    @castor_exception_handler
    def request_size(self, endpoint, base=False):
        if not base:
            url = self.study_url + endpoint
        else:
            url = self.base_url + endpoint
        response = self.castor_get(url=url, params=None)
        return response["total_items"]

    # DATA MAPPING FUNCTIONS
    def report_instance_fields(self):
        """Returns a list of field ids for every report in the study.
        Can only gather data on fields that have already been filled in once
        for any subject."""
        # Get all report data fields
        report_data_points = self.all_report_data_points()
        seen = []
        report_instance_fields = []

        for field in report_data_points:
            # If the field is not yet in the collection, add it
            if field["field_id"] not in seen:
                seen.append(field["field_id"])
                _castor_field = CastorField(
                    field["field_id"], field["report_instance_id"], "report_instance"
                )
                report_instance_fields.append(_castor_field)

        return report_instance_fields

    def survey_instance_fields(self):
        """Returns a list of field ids for every survey in the study.
        Can only gather data on fields that have already been filled in once
        for any subject."""
        # Get all survey data fields
        survey_data_points = self.all_survey_data_points()
        seen = []
        survey_instance_fields = []

        for field in survey_data_points:
            # If the field is not yet in the collection, add it
            if field["field_id"] not in seen:
                seen.append(field["field_id"])
                _castor_field = CastorField(
                    field["field_id"],
                    field["survey_instance_id"],
                    "survey_instance",
                    survey_name=field["survey_name"],
                )
                survey_instance_fields.append(_castor_field)

        return survey_instance_fields

    def study_fields(self):
        """Returns a list of field ids for every phase/study-field in the study.
        Can only gather data on fields that have already been filled in once
        for any subject."""
        # Get all study fields and remove duplicates
        study_fields = []
        study_data_points = self.all_study_data_points()
        study_field_ids = [field["field_id"] for field in study_data_points]
        study_field_ids = list(set(study_field_ids))

        # Add all study fields to the collections
        for field in study_field_ids:
            _castor_field = CastorField(field, "STUDY", "study")
            study_fields.append(_castor_field)

        return study_fields

    def report_fields(self):
        """Transforms a list of CastorVariables that are linked to a report
        instance and links them to their report"""
        # Get the list with all report instance fields
        report_instance_fields = self.report_instance_fields()

        # Get all report instances, and link them to a report
        report_instances = self.all_report_instances()
        report_instance_to_report = {}
        for instance in report_instances:
            instance_id = instance["id"]
            report_id = instance["_embedded"]["report"]["id"]
            report_instance_to_report[instance_id] = report_id

        # Link the field to a report through their report instance
        report_fields = []
        for field in report_instance_fields:
            parent_report = report_instance_to_report[field.parent_id]
            field.parent_id = parent_report
            field.parent_type = "report"
            report_fields.append(field)

        return report_fields

    def survey_fields(self):
        """Transforms a list of CastorVariables that are linked to a survey
        instance and links them to their survey"""
        # Get the list with all survey instance fields
        survey_instance_fields = self.survey_instance_fields()

        # Get all surveys, and link them to their name
        surveys = self.all_surveys()
        survey_id_to_name = {}
        for survey in surveys:
            survey_id = survey["id"]
            survey_name = survey["name"]
            survey_id_to_name[survey_name] = survey_id

        # Link the field to a survey through the survey name
        survey_fields = []
        for field in survey_instance_fields:
            parent_survey = survey_id_to_name[field.survey_name]
            field.parent_id = parent_survey
            field.parent_type = "survey"
            survey_fields.append(field)

        return survey_fields


class CastorField:
    """Object containing data to reference and manipulate a Castor field in the database."""

    def __init__(self, field_id, parent_id, parent_type, survey_name=None):
        self.field_id = field_id
        self.parent_id = parent_id
        self.parent_type = parent_type
        if parent_type == "survey_instance":
            self.survey_name = survey_name
        else:
            self.survey_name = None

    def __eq__(self, other):
        if not isinstance(other, CastorField):
            return NotImplemented

        return self.field_id == other.field_id

    def __repr__(self):
        return "id - {field_id}; type - {parent_type}; parent - {parent_id}".format(
            field_id=self.field_id,
            parent_type=self.parent_type,
            parent_id=self.parent_id,
        )
