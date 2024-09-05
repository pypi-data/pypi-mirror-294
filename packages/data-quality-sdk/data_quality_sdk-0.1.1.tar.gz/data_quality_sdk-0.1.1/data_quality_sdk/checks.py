# checks.py

from datetime import datetime

class NullCheck:
    def has_issues(self, record, column):
        """Check for null values in the specified column of a record."""
        null_count = 1 if record.get(column) is None else 0
        null_percentage = (null_count / 1) * 100 if null_count > 0 else 0
        return {
            "is_null": null_count > 0,  # Check if there is a null value
            "metrics": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "column": column,
                "issue": "Null value found",
                "category": "Null Percentage",
                "total_rows": 1,
                "null_count": null_count,
                "null_percentage": null_percentage,
            }
        }

class CompletenessCheck:
    def check(self, record, column):
        """Check the completeness of the specified column in a record."""
        total_rows = 1  # We're checking a single record
        null_count = 1 if record.get(column) is None else 0
        completeness_percentage = ((total_rows - null_count) / total_rows) * 100
        return {
            "is_complete": completeness_percentage == 100,  # Check if the data is complete
            "metrics": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "column": column,
                "issue": "Incomplete data",
                "category": "Completeness",
                "total_rows": total_rows,
                "null_count": null_count,
                "completeness_percentage": completeness_percentage,
            }
        }



class TypeCheck:
    def __init__(self, schema):
        self.schema = schema

    def has_issues(self, value, column):
        """Check the data type of the value against the expected type."""
        expected_type = self.schema[column]
        actual_type = type(value).__name__  # Get the actual type of the value
        is_correct_type = (expected_type == "int" and actual_type in ["int", "int64"]) or \
                          (expected_type == "string" and actual_type == "str")
        return {
            "is_correct_type": is_correct_type,
            "metrics": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "column": column,
                "issue": "Data type mismatch",
                "category": "Data Type",
                "expected_type": expected_type,
                "actual_type": actual_type,
            }
        }


class DataQualityCheck:
    def __init__(self, checks):
        self.checks = checks

    def perform_checks(self, record, expected_types):
        issues = []
        for check in self.checks:
            if isinstance(check, NullCheck):
                for column in expected_types.keys():
                    result = check.has_issues(record, column)
                    if result["is_null"]:
                        issues.append(result["metrics"])

            elif isinstance(check, CompletenessCheck):
                for column in expected_types.keys():
                    result = check.check(record, column)
                    if not result["is_complete"]:
                        issues.append(result["metrics"])

            elif isinstance(check, TypeCheck):
                for column in expected_types.keys():
                    if column in record:
                        result = check.has_issues(record[column], column)
                        if not result["is_correct_type"]:
                            issues.append(result["metrics"])
        
        return issues

