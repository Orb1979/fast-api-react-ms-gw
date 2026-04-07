import logging
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .database import engine

logger = logging.getLogger(__name__)


def warn_if_db_behind_migrations() -> None:
    """Log warnings when DB schema is behind Alembic revisions."""
    try:
        project_root = Path(__file__).resolve().parents[1]
        alembic_ini = project_root / "alembic.ini"
        config = Config(str(alembic_ini))
        script = ScriptDirectory.from_config(config)
        head_revision = script.get_current_head()

        with engine.connect() as connection:
            row = connection.execute(
                text("SELECT version_num FROM alembic_version LIMIT 1")
            ).fetchone()
            current_revision = row[0] if row else None

        if current_revision is None:
            logger.warning(
                "Database is not stamped with Alembic revision. "
                "Expected head revision: %s. "
                "Run 'alembic stamp head' (existing DB) or 'alembic upgrade head' (fresh DB).",
                head_revision,
            )
            return

        if current_revision != head_revision:
            logger.warning(
                "Database migration is behind. Current revision=%s, head revision=%s. "
                "Run 'alembic upgrade head'.",
                current_revision,
                head_revision,
            )
    except SQLAlchemyError as exc:
        logger.warning("Migration check skipped (database unavailable): %s", exc)
    except Exception as exc:
        logger.warning("Migration check skipped due to unexpected error: %s", exc)
