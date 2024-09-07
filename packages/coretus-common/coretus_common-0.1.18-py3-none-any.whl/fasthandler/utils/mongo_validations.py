from pymongo.errors import WriteError, DuplicateKeyError, BulkWriteError


class MongoValidationUtils:
    """
    Utility class for handling MongoDB validation errors.

    Provides methods to extract and format error messages from MongoDB write
    and duplicate key errors.
    """

    @staticmethod
    def get_write_validation(error: WriteError | BulkWriteError) -> list[str]:
        """
        Extracts and formats validation error messages from a MongoDB write error.

        Traverses the error details to identify validation issues, such as missing
        required fields, and returns them as a list of human-readable messages.

        Args:
            error (WriteError | BulkWriteError): The MongoDB write error to process.

        Returns:
            list[str]: A list of formatted validation error messages.
        """
        reasons = []

        def traverse_schema_rules_iterative(rules, pp=""):
            stack = [(rules, pp)]  # Initialize stack with the root rules and path

            while stack:
                current_rules, current_pp = stack.pop()

                for rule in current_rules:
                    if rule.get('operatorName') == 'required' and 'missingProperties' in rule:
                        for prop in rule['missingProperties']:
                            reasons.append(f"{current_pp + ('.' if current_pp else '')}{prop}:  This field is required")

                    if 'propertiesNotSatisfied' in rule:
                        for prop in rule['propertiesNotSatisfied']:
                            new_pp = f"{current_pp + ('.' if current_pp else '')}{prop['propertyName']}"
                            stack.append((prop['details'], new_pp))  # Push to stack

                    if 'details' in rule:
                        item_index = rule.get('itemIndex', -1)
                        new_pp = f"{current_pp + (f'.{item_index}' if item_index > -1 else '')}"
                        stack.append((rule['details'], new_pp))  # Push to stack

                    if 'reason' in rule:
                        reasons.append(f"{current_pp}:  {rule['reason']}")

        # Extract relevant information from the error object
        error_dict = error.details if isinstance(error, WriteError) else error.details.get('writeErrors')[0]
        err_info = error_dict.get('errInfo', {})
        details = err_info.get('details', {})
        schema_rules = details.get('schemaRulesNotSatisfied', [])

        # Use the iterative traversal method
        traverse_schema_rules_iterative(schema_rules)

        return reasons

    @staticmethod
    def get_duplicate_validation(error: DuplicateKeyError) -> str:
        """
        Extracts and formats a validation error message from a MongoDB duplicate key error.

        Identifies the field that caused the duplicate key error and returns a
        human-readable message indicating the issue.

        Args:
            error (DuplicateKeyError): The MongoDB duplicate key error to process.

        Returns:
            str: A formatted error message indicating the duplicate key issue.
        """
        error_dict = error.details
        err_info = error_dict.get('keyValue')
        key = list(err_info.keys())[0]
        return f"This {key} is already used, please try another."
