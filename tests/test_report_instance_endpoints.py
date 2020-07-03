# -*- coding: utf-8 -*-
"""
Testing class for report-instance endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-instance

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random


def create_report_instance(client, record_id, fake):
    reports = client.all_reports()
    report_ids = [report["id"] for report in reports]
    random_report = random.choice(report_ids)

    custom_name = str(random.randint(10000000, 99999999))
    if fake:
        random_report += "FAKE"

    return {
        "record_id": record_id,
        "report_id": random_report,
        "report_name_custom": custom_name,
    }


class TestReportInstance:
    report_instance_model = {
        "id": "string",
        "name": "string",
        "status": "string",
        "parent_id": "string",
        "parent_type": "string",
        "record_id": "string",
        "report_name": "string",
        "created_on": "string",
        "created_by": "string",
        "_embedded": "dict",
        "_links": "dict",
    }

    model_keys = report_instance_model.keys()

    @pytest.fixture(scope="class")
    def all_report_instances(self, client):
        all_report_instances = client.all_report_instances()
        return all_report_instances

    def test_all_report_instances(self, all_report_instances, item_totals):
        assert len(all_report_instances) > 0
        assert len(all_report_instances) == item_totals["total_report_instances"]

    def test_all_report_instances_model(self, all_report_instances):
        for i in range(0, 3):
            rand_report_instance = random.choice(all_report_instances)
            api_keys = rand_report_instance.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_report_instance_success(self, client, all_report_instances):
        for i in range(0, 3):
            rand_id = random.choice(all_report_instances)["id"]
            report_instance = client.single_report_instance(rand_id)
            api_keys = report_instance.keys()
            assert len(self.model_keys) == len(api_keys)
            for key in self.model_keys:
                assert key in api_keys

    def test_single_report_instance_failure(self, client, all_report_instances):
        for i in range(0, 3):
            rand_id = random.choice(all_report_instances)["id"] + "FAKE"
            report_instance = client.single_report_instance(rand_id)
            assert report_instance is None

    def test_all_report_instances_record_success(self, client, records_with_reports):
        # Assumes record endpoints are working
        # Assumes there is at least 1 record with a report
        records = list(records_with_reports.keys())
        for i in range(0, 3):
            rand_rec = random.choice(records)
            reports = client.all_report_instances_record(rand_rec)
            for report in reports:
                report_keys = report.keys()
                assert len(self.model_keys) == len(report_keys)
                for key in self.model_keys:
                    assert key in report_keys

    def test_all_report_instances_record_fail(self, client):
        # Assumes record endpoints are working
        records = client.all_records(archived=0)
        record_ids = [record["id"] + "FAKE" for record in records]
        for i in range(0, 3):
            rand_record = random.choice(record_ids)
            reports = client.all_report_instances_record(rand_record)
            assert reports is None

    def test_single_report_instance_record_success(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        for i in range(0, 3):
            random_record = random.choice(records)
            random_report = random.choice(records_with_reports[random_record])
            report = client.single_report_instance_record(random_record, random_report)
            assert report is not None
            report_keys = report.keys()
            assert len(self.model_keys) == len(report_keys)
            for key in self.model_keys:
                assert key in report_keys

    def test_single_report_instance_record_fail(self, client, records_with_reports):
        records = list(records_with_reports.keys())
        for i in range(0, 5):
            random_record = random.choice(records)
            reports = records_with_reports[random_record]
            random_report = random.choice(reports) + "FAKE"
            report = client.single_report_instance_record(random_record, random_report)
            assert report is None

    def test_create_report_instance_record_success(self, client):
        # Assumes record endpoints are working
        # Assumes report endpoints are working
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]

        report_instance = create_report_instance(client, random_record, fake=False)

        record_reports = client.all_report_instances_record(random_record)

        if record_reports is None:
            amount_reports = 0
        else:
            amount_reports = len(record_reports)

        created = client.create_report_instance_record(**report_instance)

        assert created is not None
        assert created["name"] == report_instance["report_name_custom"]
        assert created["record_id"] == report_instance["record_id"]

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports + 1 == new_amount

    def test_create_report_instance_record_fail(self, client):
        # Assumes record endpoints are working
        # Assumes report endpoints are working
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]

        report_instance = create_report_instance(client, random_record, fake=True)

        record_reports = client.all_report_instances_record(random_record)

        if record_reports is None:
            amount_reports = 0
        else:
            amount_reports = len(record_reports)

        created = client.create_report_instance_record(**report_instance)

        assert created is None

        record_reports = client.all_report_instances_record(random_record)
        if record_reports is None:
            new_amount = 0
        else:
            new_amount = len(record_reports)

        assert amount_reports == new_amount

    def test_create_multiple_report_instances_record_success(self, client):
        # Assumes record endpoints are working
        # Assumes report endpoints are working
        records = client.all_records(archived=0)
        random_record = random.choice(records)["id"]

        reports = []
        for i in range(0, 5):
            report_instance = create_report_instance(client, random_record, fake=False)
            reports.append(report_instance)

        record_reports = client.all_report_instances_record(random_record)

        if record_reports is None:
            amount_reports = 0
        else:
            amount_reports = len(record_reports)

        created = client.create_multiple_report_instances_record(random_record, reports)

        assert created is not None
        assert created["total_success"] == 5
        assert created["total_failed"] == 0

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports + 5 == new_amount

    def test_create_multiple_report_instances_record_fail(
        self, client, records_with_reports
    ):
        # Assumes record endpoints are working
        # Assumes report endpoints are working
        # Record needs to already have one report
        records = list(records_with_reports.keys())
        random_record = random.choice(records)

        reports = []
        for i in range(0, 5):
            report_instance = create_report_instance(client, random_record, fake=True)
            reports.append(report_instance)

        record_reports = client.all_report_instances_record(random_record)

        if record_reports is None:
            amount_reports = 0
        else:
            amount_reports = len(record_reports)

        created = client.create_multiple_report_instances_record(random_record, reports)

        assert created is not None
        assert created["total_success"] == 0
        assert created["total_failed"] == 5

        record_reports = client.all_report_instances_record(random_record)
        new_amount = len(record_reports)

        assert amount_reports == new_amount
