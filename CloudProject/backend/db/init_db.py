from backend.db.session import engine, Base
import backend.models.migration  # noqa: F401 — ensure models are registered
import backend.models.job         # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
