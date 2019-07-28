import json


class UtilityMethods:
    SUCCESS_KEY = 'success'
    MESSAGE_KEY = 'message'
    ERROR_KEY = 'error'
    REQUIRED_FIELDS_FOR_GRID = ['start', 'limit', 'sorters', 'filters']

    @staticmethod
    def get_required_data(required_fields, data):
        received_data = {}
        for element in required_fields:
            value = data.get(element, None)
            if value is None:
                raise DataValidationError(element, element + ' is required')
            received_data[element] = value
        return received_data

    @staticmethod
    def get_allowed_data(allowed_fields, data):
        received_data = {}
        for element in allowed_fields:
            value = data.get(element, None)
            if value is not None:
                received_data[element] = value
        return received_data

    @staticmethod
    def get_default_response():
        status = 200
        response_data = {
            UtilityMethods.SUCCESS_KEY: False,
            UtilityMethods.MESSAGE_KEY: {
                UtilityMethods.ERROR_KEY: 'Server Error - Request not handled'
            }
        }
        return status, response_data

    @staticmethod
    def save_object_values(_object, allowed_fields, received_data):
        for key, value in UtilityMethods.get_allowed_data(allowed_fields, received_data).items():
            if hasattr(_object, key):
                setattr(_object, key, value)
        _object.save()

    @staticmethod
    def get_formatted_data_remove_nesting(parent_key, _data, result_dict):
        for key, value in _data.items():
            if parent_key is None:
                result_key = key
            else:
                result_key = parent_key + '__' + key
            if type(value) == dict:
                result_dict = UtilityMethods.get_formatted_data_remove_nesting(result_key, value, result_dict)
            else:
                result_dict[result_key] = value
        return result_dict

    @staticmethod
    def get_filtered_and_sorted_data(initial_query_set, model_serializer, start, limit, sorters, filters):
        query_set = initial_query_set.all()
        query_set = UtilityMethods.apply_sorter_on_query_set(query_set, sorters)
        query_set = UtilityMethods.apply_filter_on_query_set(query_set, filters)
        if start is None or start < 1:
            start = 1
        serializer_instance = model_serializer(query_set[start - 1: limit], many=True)
        data = []
        data_in_dict = json.loads(json.dumps(serializer_instance.data))
        for element in data_in_dict:
            formatted_element = UtilityMethods.get_formatted_data_remove_nesting(None, element, {})
            data.append(formatted_element)
        return query_set.count(), data

    @staticmethod
    def apply_sorter_on_query_set(query_set, sorters):
        for element in sorters:
            if element['order'] == 'ASC':
                field_name = element['mapping']
            else:
                field_name = '-' + element['mapping']
            query_set = query_set.order_by(field_name)
        return query_set

    @staticmethod
    def apply_filter_on_query_set(query_set, filters):
        for element in filters:
            filter_type = element['type']
            column_name = element['mapping']
            arguments = {}
            if filter_type == 'number':
                # query_set = User.objects.filter(**{element.mapping:})
                if element.get('lessThan', None) is not None:
                    arguments[column_name + "__lte"] = element['lessThan']
                if element.get('greaterThan', None) is not None:
                    arguments[column_name + "__gte"] = element['greaterThan']
                if element.get('equalTo', None) is not None:
                    arguments.clear()
                    arguments[column_name] = element['equalTo']

            if filter_type == 'string':
                arguments = {
                    column_name + "__contains": element['stringValue']
                }

            if filter_type == 'date':
                if element.get("beforeDate", None) is not None:
                    arguments[column_name + "__lte"] = element['beforeDate'].split('T')[0]
                if element.get("afterDate", None) is not None:
                    arguments[column_name + "__gte"] = element['afterDate'].split('T')[0]
                if element.get("onDate", None) is not None:
                    arguments.clear()
                    arguments[column_name] = element['onDate'].split('T')[0]

            if filter_type == 'list':
                arguments = {
                    column_name + '__in': element['listValues']
                }

            if filter_type == 'bool':
                arguments = {
                    column_name: element['boolValue']
                }
            query_set = query_set.filter(**arguments)
        return query_set

    @staticmethod
    def get_list_data_for_request(received_data, initial_query_set, model_serializer):
        status, response_data = UtilityMethods.get_default_response()
        try:
            total_count, records_data = UtilityMethods.get_filtered_and_sorted_data(initial_query_set,
                                                                                    model_serializer,
                                                                                    received_data['start'],
                                                                                    received_data['limit'],
                                                                                    received_data['sorters'],
                                                                                    received_data['filters'])
            response_data[UtilityMethods.SUCCESS_KEY] = True
            response_data[UtilityMethods.MESSAGE_KEY] = {
                'total_records': total_count,
                'data': records_data
            }
        except DataValidationError as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                e.args[0]: e.args[1]
            }
        except Exception as e:
            response_data[UtilityMethods.MESSAGE_KEY] = {
                UtilityMethods.ERROR_KEY: str(e)
            }
        return status, response_data


class DataValidationError(Exception):
    pass
