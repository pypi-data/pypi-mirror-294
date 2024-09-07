from typing import Optional

from app.errors.errors import ModelNotFoundException, NotAuthorizedError
from app.models import db
from app.models.database import Database
from app.schemas import (
    CreateDatabaseInputSchema,
    DatabaseSchema,
    QueryDatabaseInputSchema,
    UpdateDatabaseInputSchema,
)
from app.settings import settings
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity

bp = Blueprint("databases", __name__)


@bp.route("/")
def get_databases():
    databases = Database.find_by_owner(id=get_jwt_identity())
    return [
        DatabaseSchema.model_validate(database).model_dump() for database in databases
    ]


@bp.route("/", methods=["POST"])
def create_database():
    schema: CreateDatabaseInputSchema = CreateDatabaseInputSchema.model_validate(
        request.json
    )
    database = Database(
        name=schema.name, description=schema.description, owner_id=get_jwt_identity()
    )
    try:
        return DatabaseSchema.model_validate(database.create()).model_dump()
    except Exception as e:
        return make_response(f"Error creating database {str(e)}"), 500


@bp.route("/<int:id>", methods=["DELETE"])
def delete_database(id: int):
    try:
        Database.delete_by_id(id, owner_id=get_jwt_identity())
    except ModelNotFoundException:
        return make_response(f"Database with id {id} not found"), 403
    except NotAuthorizedError as e:
        return make_response(str(e)), 403

    return jsonify({"message": "Database deleted successfully"}), 200


@bp.route("/<int:id>")
def get_database(id: int):
    database = Database.find_by_id(id)
    if not database:
        return make_response(f"Database with id {id} not found"), 403

    return DatabaseSchema.model_validate(database).model_dump_json()


@bp.route("/<int:id>", methods=["PUT"])
def update_database(id: int):
    if database := Database.find_by_id(id):
        schema = UpdateDatabaseInputSchema.model_validate(request.json)
        database.update(schema)
        db.session.commit()
        return DatabaseSchema.model_validate(database).model_dump_json()
    else:
        return make_response("Database not found"), 404


@bp.route("/run", methods=["POST"])
@bp.route("/<int:id>/run", methods=["POST"])
def run(id: Optional[int] = None):
    schema = QueryDatabaseInputSchema.model_validate(request.json)

    start_row = request.args.get("start_row", default=0, type=int)
    end_row = request.args.get(
        "end_row",
        default=settings.DEFAULT_SELECT_PAGE_SIZE or settings.result_set_hard_limit,
        type=int,
    )
    with_total_count = request.args.get(
        "with_total_count",
        default=True,
        type=bool,
    )

    owner_id = get_jwt_identity()
    try:
        result = Database.run(
            id=id,
            owner_id=owner_id,
            query=schema.query,
            start_row=start_row,
            end_row=end_row,
            with_total_count=with_total_count,
        )
        return result.model_dump(), 200
    except ModelNotFoundException:
        make_response("Database not found"), 404
    except NotAuthorizedError:
        return (
            make_response("Not authorized to execute the query on this database"),
            403,
        )
    except Exception as e:
        return make_response(str(e)), 500
