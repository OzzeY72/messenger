#!/bin/sh

echo "Start migration"
alembic upgrade head

echo "Migration completed"
exec "$@"
