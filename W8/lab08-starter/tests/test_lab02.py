"""Lab 2 contract tests — validates openapi.yaml and checks behavior against Flask."""
from pathlib import Path
import pytest
import yaml
from jsonschema import validate


def get_spec():
    spec_path = Path(__file__).resolve().parent.parent / "openapi.yaml"
    return yaml.safe_load(spec_path.read_text(encoding="utf-8"))


def test_get_books_has_operation_id():
    spec = get_spec()
    get_books = spec["paths"]["/books"]["get"]
    assert "operationId" in get_books
    assert get_books["operationId"] == "listBooks"


def test_delete_book_204_has_no_body():
    spec = get_spec()
    delete_204 = spec["paths"]["/books/{id}"]["delete"]["responses"]["204"]
    assert "content" not in delete_204


def test_book_year_is_integer():
    spec = get_spec()
    year_schema = spec["components"]["schemas"]["Book"]["properties"]["year"]
    assert year_schema["type"] == "integer"


def test_book_response_matches_schema(client, sample_book):
    spec = get_spec()
    schema = spec["components"]["schemas"]["Book"]

    # Chuẩn hoá type hỗ trợ null cho jsonschema nếu có nullable
    for prop in ("year", "isbn"):
        if schema["properties"][prop].get("nullable"):
            current_type = schema["properties"][prop]["type"]
            schema["properties"][prop]["type"] = [current_type, "null"]

    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200
    validate(instance=response.get_json(), schema=schema)


def test_response_200_object_schema_has_properties():
    spec = get_spec()
    for path, path_item in spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            res_200 = operation.get("responses", {}).get("200")
            if not res_200:
                continue
            schema = res_200.get("content", {}).get("application/json", {}).get("schema", {})
            if schema.get("type") == "object":
                assert "properties" in schema, f"{method.upper()} {path} thiếu properties trong schema 200"
                assert len(schema["properties"]) > 0, f"{method.upper()} {path} schema 200 không có trường nào"