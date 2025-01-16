from dataclasses import dataclass
from typing import Iterable, List, Tuple
from sqlalchemy.orm import Query


@dataclass
class RequestAndQueryData:
    request_args: List[Tuple[str, str]]
    query: Query


def create_request_and_query_data(
    db_model,
    request_args: Iterable[Tuple[str, str]]
) -> RequestAndQueryData:

    query = db_model.query
    return RequestAndQueryData(request_args=list(request_args), query=query)


def apply_request_args_to_query_filter(
    db_model,
    data: RequestAndQueryData
) -> RequestAndQueryData:

    result = RequestAndQueryData(request_args=[], query=data.query)

    for key, value in data.request_args:
        key_parts = key.split(".")

        if len(key_parts) == 1:
            column = getattr(db_model, key)
            result.query = result.query.filter(column == value)

        elif len(key_parts) == 2 and len(key_parts[0]) > 0:
            column = getattr(db_model, key_parts[0])
            operator = key_parts[1]

            if operator == "like":
                result.query = result.query.filter(column.like(value))
            elif operator == "startswith":
                result.query = result.query.filter(column.startswith(value))
            else:
                result.request_args.append((key, value))

        else:
            result.request_args.append((key, value))

    return result


def apply_request_args_to_query_order_by(
    db_model,
    data: RequestAndQueryData
) -> RequestAndQueryData:

    result = RequestAndQueryData(request_args=[], query=data.query)

    for key, value in data.request_args:
        if key != ".order_by":
            result.request_args.append((key, value))
            continue

        value_parts = value.split(",")
        for value_part in value_parts:
            value_part_parts = value_part.split(" ")

            if len(value_part_parts) == 1:
                column = getattr(db_model, value_part)
                result.query = result.query.order_by(column)

            elif len(value_part_parts) == 2:
                column = getattr(db_model, value_part_parts[0])
                direction = value_part_parts[1].lower()
                if direction == "asc":
                    result.query = result.query.order_by(column.asc())
                elif direction == "desc":
                    result.query = result.query.order_by(column.desc())
                else:
                    result.request_args.append((key, value))

            else:
                result.request_args.append((key, value))

    return result


def apply_request_args_to_query_offset_limit(
    data: RequestAndQueryData
) -> RequestAndQueryData:

    result = RequestAndQueryData(request_args=[], query=data.query)

    for key, value in data.request_args:
        if key == ".offset":
            result.query = result.query.offset(int(value))
        elif key == ".limit":
            result.query = result.query.limit(int(value))
        else:
            result.request_args.append((key, value))

    return result


def ensure_no_request_args_left(data: RequestAndQueryData) -> None:
    if len(data.request_args) > 0:
        raise ValueError(f"Unsupported request args: {data.request_args}")


def create_query_from_request_args(
    db_model,
    request_args: Iterable[Tuple[str, str]]
) -> Query:

    # TODO: Prevent SQL injection.

    data = create_request_and_query_data(db_model, request_args)
    data = apply_request_args_to_query_filter(db_model, data)
    data = apply_request_args_to_query_order_by(db_model, data)
    data = apply_request_args_to_query_offset_limit(data)
    ensure_no_request_args_left(data)

    return data.query
