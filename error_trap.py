import io
from pymongo.errors import DuplicateKeyError, WriteError
def print_exception(thrown_exception: Exception):
    """
    Analyze the supplied selection and return a text string that captures what violations of the
    schema & any uniqueness constraints that caused the input exception.
    :param thrown_exception:    The exception that MongoDB threw.
    :return:                    The formatted text describing the issue(s) in the exception.
    """
    # Use StringIO as a buffer to accumulate the output.
    with io.StringIO() as output:
        output.write('***************** Start of Exception print *****************\n')
        # DuplicateKeyError is a subtype of WriteError.  So I have to check for DuplicateKeyError first, and then
        # NOT check for WriteError to get this to work properly.
        if isinstance(thrown_exception, DuplicateKeyError):
            error_message = thrown_exception.details
            # There may be multiple columns in the uniqueness constraint.
            # I'm not sure what happens if there are multiple uniqueness constraints violated at the same insert.
            fields = []
            output.write("Uniqueness constraint violated on the fields:")
            # Get the list of fields in the uniqueness constraint.
            for field in iter(error_message['keyValue']):
                fields.append(field)
            output.write(f"{', '.join(fields)}' should be unique.")
        elif isinstance(thrown_exception, WriteError):
            error_message = thrown_exception.details["errInfo"]["details"]
            # In case there are multiple criteria violated at the same time.
            for error in error_message["schemaRulesNotSatisfied"]:
                # One field could have multiple constraints violated.
                field_errors = error.get("propertiesNotSatisfied")
                if field_errors:
                    for field_error in field_errors:
                        field = field_error["propertyName"]
                        reasons = field_error.get("details", [])
                        for reason in reasons:
                            operator_name = reason.get("operatorName")
                            if operator_name == "enum":
                                allowed_values = reason["specifiedAs"]["enum"]
                                output.write(
                                    f"Error: Invalid value for field '{field}'. Allowed values are: {allowed_values}\n")
                            elif operator_name in ["maxLength", "minLength"]:
                                specified_length = reason["specifiedAs"][operator_name]
                                output.write(
                                    f"Error: Invalid length for field '{field}'. The length should be {operator_name} "
                                    f"{specified_length}.\n")
                            elif operator_name == "unique":
                                output.write(
                                    f"Error: field '{field}' already exists. Please choose a different value.\n")
                            elif operator_name == "combineUnique":
                                fields = reason["specifiedAs"]["fields"]
                                output.write(f"Error: Combination of fields '{', '.join(fields)}' should be unique.\n")
                            else:
                                output.write(
                                    f"Error: '{reason['reason']}' for field '{field}'. Please correct the input.\n")
        results = output.getvalue().rstrip()
    return results
