# data_quality_sdk/checks.py
class DataQualityCheck:
    def __init__(self, null_threshold, completeness_threshold):
        self.null_threshold = null_threshold
        self.completeness_threshold = completeness_threshold

    def check_null_values(self, df, column):
        null_count = df[column].isnull().sum()
        null_percentage = (null_count / len(df)) * 100
        total_rows = len(df)
        return {
            "is_null": null_percentage > self.null_threshold,
            "null_count": null_count,
            "null_percentage": null_percentage,
            "total_rows": total_rows
        }
        
    def check_data_completeness(self, df, column):
        total_rows = len(df)
        null_count = df[column].isnull().sum()
        completeness_percentage = ((total_rows - null_count) / total_rows) * 100
        is_complete = completeness_percentage >= self.completeness_threshold
        return {
            "is_complete": is_complete,
            "completeness_percentage": completeness_percentage,
            "null_count": null_count,
            "total_rows": total_rows
        }

    def check_data_type(self, value, expected_type):
        actual_type = type(value).__name__  # Get the actual type of the value
        is_correct_type = (expected_type == "int" and actual_type in ["int", "int64"]) or \
                          (expected_type == "string" and actual_type == "str")
        return {
            "is_correct_type": is_correct_type,
            "actual_type": actual_type,
            "expected_type": expected_type
        }
