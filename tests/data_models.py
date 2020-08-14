# -*- coding: [stf-8 -*-
"""
Contains the definition of all data models according to the Castor EDC API.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

country_model_1 = {
    "id": [str, ],
    "country_id": [str, ],
    "country_name": [str, ],
    "country_tld": [str, ],
    "country_cca2": [str, ],
    "country_cca3": [str, ],
    "_links": [dict, ],
}

country_model_2 = {
    "id": [str, ],
    "country_id": [str, ],
    "country_name": [str, ],
    "country_tld": [str, ],
    "country_cca2": [str, ],
    "country_cca3": [str, ],
}

study_data_point_model = {
    "field_id": [str, ],
    "field_value": [str, ],
    "record_id": [str, ],
    "updated_on": [str, ],
}

study_data_point_extended_model = {
    "record_id": [str, ],
    "field_variable_name": [str, ],
    "field_id": [str, ],
    "value": [str, ],
    "updated_on": [str, ],
    "_embedded": [dict, ],
    "_links": [dict, ],
}

study_step_model = {
    "id": [str, ],
    "step_id": [str, ],
    "step_description": [str, ],
    "step_name": [str, ],
    "step_order": [int, ],
    "_embedded": [dict, ],
    "_links": [dict, ],
}

user_model = {
    "id": [str, ],
    "user_id": [str, ],
    "entity_id": [str, ],
    "full_name": [str, ],
    "name_first": [str, ],
    "name_middle": [str, type(None)],
    "name_last": [str, ],
    "email_address": [str, ],
    "institute": [str, type(None)],
    "department": [str, type(None)],
    "last_login": [str, ],
    "_links": [dict, ],
}

study_model = {
    "crf_id": [str, ],
    "study_id": [str, ],
    "name": [str, ],
    "created_by": [str, ],
    "created_on": [str, ],
    "live": [bool, ],
    "randomization_enabled": [bool, ],
    "gcp_enabled": [bool, ],
    "surveys_enabled": [bool, ],
    "premium_support_enabled": [bool, ],
    "main_contact": [str, ],
    "expected_centers": [int, type(None)],
    "duration": [int, type(None)],
    "expected_records": [int, type(None)],
    "slug": [str, ],
    "version": [str, ],
    "domain": [str, ],
    "_links": [dict, ],
}

report_model = {
    "id": [str, ],
    "report_id": [str, ],
    "description": [str, ],
    "name": [str, ],
    "type": [str, ],
    "_links": [dict, ],
}

report_instance_model = {
    "id": [str, ],
    "name": [str, ],
    "status": [str, ],
    "parent_id": [str, ],
    "parent_type": [str, ],
    "record_id": [str, ],
    "report_name": [str, ],
    "created_on": [str, ],
    "created_by": [str, ],
    "_embedded": [dict, ],
    "_links": [dict, ],
}

report_data_point_model = {
    "field_id": [str, ],
    "report_instance_id": [str, ],
    "report_instance_name": [str, ],
    "field_value": [str, ],
    "record_id": [str, ],
    "updated_on": [str, ],
}

report_data_point_extended_model = {
    "record_id": [str, ],
    "field_variable_name": [str, ],
    "field_id": [str, ],
    "value": [str, ],
    "updated_on": [str, ],
    "report_instance_id": [str, ],
    "_embedded": [dict, ],
    "_links": [dict, ],
}

report_step_model = {
    "id": [str, ],
    "report_step_id": [str, ],
    "report_step_name": [str, ],
    "report_step_description": [str, ],
    "report_step_number": [int, ],
    "_links": [dict, ],
    "_embedded": [dict, ],
}

survey_data_point_model = {
    "field_id": [str, ],
    "survey_instance_id": [str, ],
    "survey_name": [str, ],
    "field_value": [str, ],
    "record_id": [str, ],
    "updated_on": [str, ],
}

survey_data_point_extended_model = {
    "record_id": [str, ],
    "field_variable_name": [str, ],
    "field_id": [str, ],
    "value": [str, ],
    "updated_on": [str, ],
    "survey_instance_id": [str, ],
    "_embedded": [dict, ],
    "_links": [dict, ],
}

field_dep_model = {
    "id": [str, ],
    "operator": [str, ],
    "value": [str, ],
    "parent_id": [str, ],
    "child_id": [str, ],
    "_links": [dict, ],
}

field_model = {
    "id": [str, ],
    "parent_id": [str, ],
    "field_id": [str, ],
    "field_number": [int, ],
    "field_label": [str, ],
    "field_is_alias": [bool, ],
    "field_variable_name": [str, type(None)],
    "field_type": [str, ],
    "field_required": [int, ],
    "field_hidden": [int, ],
    "field_info": [str, ],
    "field_units": [str, ],
    "field_min": [int, float, type(None), ],
    "field_min_label": [str, type(None), ],
    "field_max": [int, float, type(None), ],
    "field_max_label": [str, type(None), ],
    "field_summary_template": [str, type(None), ],
    "field_slider_step": [int, type(None), ],
    "report_id": [str, ],
    "field_length": [int, type(None), ],
    "additional_config": [str, ],
    "exclude_on_data_export": [bool, ],
    "option_group": [dict, type(None), ],
    "metadata_points": [list, ],
    "validations": [list, ],
    "dependency_parents": [list, ],
    "dependency_children": [list, ],
    "_links": [dict, ],
}

field_opt_model = {
    "id": [str, ],
    "name": [str, ],
    "description": [str, ],
    "layout": [bool, ],
    "options": [list, ],
    "_links": [dict, ],
}

field_val_model = {
    "id": [int, ],
    "type": [str, ],
    "value": [str, ],
    "operator": [str, ],
    "text": [str, ],
    "field_id": [str, ],
    "_links": [dict, ],
}

institute_model = {
    "id": [str, ],
    "institute_id": [str, ],
    "name": [str, ],
    "abbreviation": [str, ],
    "code": [str, type(None)],
    "order": [int, ],
    "country_id": [int, ],
    "deleted": [bool, ],
    "_links": [dict, ],
}

metadata_model = {
    "id": [str, ],
    "metadata_type": [dict, ],
    "parent_id": [str, type(None)],
    "value": [str, ],
    "description": [str, type(None)],
    "element_type": [str, ],
    "element_id": [str],
    "_links": [dict, ],
}

metadata_type_model = {
    "id": [int, ],
    "name": [str, ],
    "description": [str, ],
    "_links": [dict, ],
}

phase_model = {
    "id": [str, ],
    "phase_id": [str, ],
    "phase_description": [str, type(None)],
    "phase_name": [str, ],
    "phase_duration": [int, type(None)],
    "phase_order": [int, ],
    "_links": [dict, ],
}

query_model = {
    "id":  [str, ],
    "record_id":  [str, ],
    "field_id":  [str, ],
    "status":  [str, ],
    "first_query_remark":  [str, ],
    "created_by":  [str, ],
    "created_on":  [dict, ],
    "updated_by":  [str, ],
    "updated_on":  [dict, ],
    "_embedded":  [dict, ],
    "_links":  [dict, ],
}

record_model = {
    "id": [str, ],
    "record_id": [str, ],
    "_embedded": [dict, ],
    "ccr_patient_id": [str, ],
    "randomized_id": [str, type(None)],
    "randomization_group": [int, type(None)],
    "randomization_group_name": [str, type(None)],
    "last_opened_step": [str, type(None)],
    "progress": [int, ],
    "status": [str, ],
    "archived": [bool, ],
    "archived_reason": [str, type(None)],
    "created_by": [str, ],
    "created_on": [dict, ],
    "updated_by": [str, ],
    "updated_on": [dict, ],
    "_links": [dict, ],
}

record_progress_model = {
    "record_id": [str, ],
    "steps": [list, ],
    "_links": [dict, ],
}

steps_model = {
    "step_id": [str, ],
    "complete": [int, ],
    "sdv": [bool, ],
    "locked": [bool, ],
    "signed": [bool, ],
}

statistics_model = {
    "study_id": [str, ],
    "records": [dict, ],
    "_links": [dict, ],
}

stats_records_model = {
    "total_count": [int, ],
    "institutes": [list, ],
}

stats_institutes_model = {
    "institute_id": [str, ],
    "institute_name": [str, ],
    "record_count": [int, ],
}
data_options = {
    "numeric": "1",
    "date": "11-11-2017",
    "string": "testing",
    "dropdown": "1",
    "radio": "1",
    "textarea": "testing",
    "slider": "5",
    "checkbox": "1",
    "calculation": "5",
    "year": "2005",
}