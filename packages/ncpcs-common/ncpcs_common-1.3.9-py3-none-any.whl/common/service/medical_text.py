import hashlib
import random
import re
import uuid
from collections import Counter
from common.constants.level_dict import COLUMN_DICT
from common.entity.document import Document, DEFAULT_DOCUMENT_AVG_LEN
from common.entity.relation_key import RelationKey
from common.util.string_util import split_text, cut_by_time

ORDER_TABLE_DICT = {
    "nc_admission_record": {
        "pageUuid": "",
        "orderSql": "",
        "tableUuid": "703000000"
    },
    "nc_discharge_record": {
        "pageUuid": "",
        "orderSql": "",
        "tableUuid": "707000000"
    },
    "nc_daily_disease_course": {
        "pageUuid": "706010000",
        "orderSql": " order by nc_disease_course_no ASC,sort_time ASC, nc_record_time, nc_rid",
        "tableUuid": "706000000"
    },
    "nc_pathology_info": {
        "pageUuid": "711010000",
        "orderSql": " order by nc_pathology_no ASC,sort_time ASC",
        "tableUuid": "711000000"
    },
    "nc_imageology_exam": {
        "pageUuid": "713010000",
        "orderSql": " order by nc_exam_order ASC,nc_report_no ASC,sort_time ASC",
        "tableUuid": "713000000"
    },
    "nc_fist_disease_course": {
        "pageUuid": "705010000",
        "orderSql": " order by nc_disease_course_no ASC,sort_time ASC",
        "tableUuid": "705000000"
    },
    "nc_24hours_admission_discharge_info": {
        "pageUuid": "",
        "orderSql": "",
        "tableUuid": "708000000"
    },
    "nc_readmission_record": {
        "pageUuid": "",
        "orderSql": "",
        "tableUuid": "709000000"
    },
    "nc_death_record": {
        "pageUuid": "",
        "orderSql": "",
        "tableUuid": "712000000"
    }
}

GET_TEXT_SQL_FORMAT = "select {} from {} where nc_medical_institution_code = '{}' and nc_medical_record_no = '{}' and "\
                     "nc_discharge_time = '{}' and nc_hedge = 0 and nc_data_status != 99"


def extract_document_by(cursor, medical_institution_code, medical_record_no, discharge_time, admission_time=None,
                        column_dict=COLUMN_DICT, avg_len=DEFAULT_DOCUMENT_AVG_LEN):
    if not admission_time:
        admission_time = discharge_time
    relation_key = RelationKey(medical_institution_code, medical_record_no, discharge_time, admission_time)
    return extract_medical_text(cursor, relation_key, column_dict, avg_len)


def extract_medical_text(cursor, relation_key, column_dict=COLUMN_DICT, avg_len=DEFAULT_DOCUMENT_AVG_LEN):
    document_list = []
    for table_name, column_list in column_dict.items():
        get_text_sql = GET_TEXT_SQL_FORMAT.format(','.join(column_list), table_name, relation_key.medical_institution_code,
                                                  relation_key.medical_record_no, relation_key.discharge_time)
        table_uuid, page_uuid, get_text_sql = generate_order_sql(get_text_sql)
        cursor.execute(get_text_sql)
        page = 1
        for ele in cursor.fetchall():
            for i, val in enumerate(ele):
                if not val:
                    continue
                column_name = column_list[i]
                content_list = cut_by_time(val, admission_time=relation_key.admission_time, avg_len=avg_len)
                for start_index, end_index, timeline in content_list:
                    content = val[start_index:end_index]
                    document = Document(str(uuid.uuid4()), relation_key.medical_institution_code,
                                        relation_key.medical_record_no, relation_key.discharge_time, table_name,
                                        column_name, table_uuid, page, page_uuid, start_index, start_index + len(content),
                                        content, '', timeline)
                    document_list.append(document)

            page += 1
    return document_list


def md5_document_list(document_list):
    # 创建md5对象
    md5_hash = hashlib.md5()
    for document in document_list:
        # 使用正则表达式替换掉所有非中文、非英文、非数字字符
        cleaned_string = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '', document.content)
        if cleaned_string:
            md5_hash.update(cleaned_string.encode('utf-8'))
            document.md5_sum = md5_hash.hexdigest()


def extract_all_relation_key(cursor):
    cursor.execute("select nc_medical_institution_code, nc_medical_record_no, nc_discharge_time, nc_admission_time from nc_medical_record_first_page where nc_hedge = 0 and nc_data_status != 99 and nc_data_report_type = 1 order by nc_rid")
    relation_key_list = []
    for ele in cursor.fetchall():
        relation_key_list.append(RelationKey(ele[0], ele[1], ele[2].strftime('%Y-%m-%d %H:%M:%S'), ele[3].strftime('%Y-%m-%d %H:%M:%S')))

    return relation_key_list


def extract_relation_key_list_by_global_id(cursor, global_id):
    cursor.execute("select nc_medical_institution_code, nc_medical_record_no, nc_discharge_time, nc_admission_time from nc_mpi_relation where nc_global_id = '{}' order by nc_admission_time".format(global_id))
    relation_key_list = []
    for ele in cursor.fetchall():
        relation_key_list.append(RelationKey(ele[0], ele[1], ele[2].strftime('%Y-%m-%d %H:%M:%S'), ele[3].strftime('%Y-%m-%d %H:%M:%S')))
    return relation_key_list


def generate_order_sql(sql):
    for table_name, order_info in ORDER_TABLE_DICT.items():
        if sql.count(table_name):
            return order_info['tableUuid'], order_info['pageUuid'], sql + order_info['orderSql']
    return '', '', sql


def sentence_count(sentence_list):
    count_dict = Counter(sentence_list)
    for sentence, count in sorted(count_dict.items(), key=lambda t: t[1], reverse=True):
        print(sentence, count)


def random_pick_relation_key(relation_key_dict, num_to_pick):
    selected_relation_key_list = []
    avg_to_pick = num_to_pick // len(relation_key_dict.keys())
    left_relation_key_list = []
    for _, relation_key_list in relation_key_dict.items():
        if len(relation_key_list) <= avg_to_pick:
            selected_relation_key_list.extend(relation_key_list)
        else:
            random_list = random.sample(relation_key_list, avg_to_pick)
            random_set = set(random_list)
            selected_relation_key_list.extend(random_list)
            left_relation_key_list.extend([relation_key for relation_key in relation_key_list
                                           if relation_key not in random_set])
    selected_relation_key_list.extend(random.sample(left_relation_key_list, num_to_pick - len(selected_relation_key_list)))
    return selected_relation_key_list