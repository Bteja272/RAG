from app.db.base import Base
from app.db.models import Document, DocumentChunk
from app.db.session import engine


def main():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    main()