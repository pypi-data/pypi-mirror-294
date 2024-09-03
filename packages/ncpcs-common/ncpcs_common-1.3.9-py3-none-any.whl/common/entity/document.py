from dataclasses import dataclass
from common.entity.timeline import Timeline


DEFAULT_DOCUMENT_AVG_LEN = 256


@dataclass
class Document:
    uuid: str
    medical_institution_code: str
    medical_record_no: str
    discharge_time: str
    table_name: str
    column_name: str
    table_uuid: str
    page: int
    page_uuid: str
    start_index: int
    end_index: int
    content: str
    md5_sum: str
    timeline: Timeline = None