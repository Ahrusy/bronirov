import pytest
from event_importer.models import EventSource, ImportLog
from datetime import datetime


@pytest.mark.django_db
def test_event_source_and_log():
    source = EventSource.objects.create(
        name='RSS Parser',
        source_type='rss',
        url='https://example.com/events.xml'
    )

    log = ImportLog.objects.create(
        source=source,
        raw_data='<xml>sample</xml>',
        status='success'
    )

    assert log.source.name == 'RSS Parser'
    assert log.status == 'success'
