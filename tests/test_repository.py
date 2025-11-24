import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.adapters.db import models
from app.adapters.repo.event import EventRepository
from app.domain.dtos import CreateEventDTO


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def event_repository(db_session):
    return EventRepository(db_session)


@pytest.fixture
def sample_event_dto():
    return CreateEventDTO(
        title="Test",
        description="Test description",
        datetime=datetime(2025, 11, 24, 18, 0),
        max_seats=50,
        owner_id=1
    )


class TestEventRepository:
    def test_create_event_success(
        self, 
        event_repository: EventRepository,
        sample_event_dto: CreateEventDTO
    ):
        """Тест успешного создания события"""
        # Выполнение
        result = event_repository.create(sample_event_dto)
        
        # Проверка
        assert result.id is not None
        assert result.title == sample_event_dto.title
        assert result.description == sample_event_dto.description
        assert result.datetime == sample_event_dto.datetime
        assert result.max_seats == sample_event_dto.max_seats
        assert result.owner_id == sample_event_dto.owner_id
    
    
    def test_create_event_persists_to_db(
        self, 
        event_repository: EventRepository, 
        sample_event_dto: CreateEventDTO, 
        db_session: Session
    ):
        """Тест сохранения события в БД"""
        # Выполнение
        created_event = event_repository.create(sample_event_dto)
        
        # Проверка
        db_event = db_session.query(models.Event).filter_by(id=created_event.id).first()
        assert db_event is not None
        assert db_event.title == sample_event_dto.title
        assert db_event.max_seats == sample_event_dto.max_seats
    
    
    def test_map_to_domain(
        self, 
        event_repository: EventRepository
        ):
        """Тест маппинга из DB модели в доменную модель"""
        # Подготовка
        db_event = models.Event(
            id=1,
            title="Концерт",
            description="концерт",
            datetime=datetime(2025, 11, 30, 20, 0),
            max_seats=100,
            owner_id=5
        )
        
        # Выполнение
        domain_event = event_repository._map_to_domain(db_event)
        
        # Проверка
        assert domain_event.id == db_event.id
        assert domain_event.title == db_event.title
        assert domain_event.description == db_event.description
        assert domain_event.datetime == db_event.datetime
        assert domain_event.max_seats == db_event.max_seats
        assert domain_event.owner_id == db_event.owner_id
