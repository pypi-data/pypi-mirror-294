
# Usage in your application
from . import headers
from custom_development_standardisation import generate_outcome_message
import requests



x = "8a862259e3a14dc58e00ebb034267bea"
baseURL = "https://api.notion.com/v1/databases/"


data = {
    "filter": {},
    "sorts": []
}

# LOGGER
logger=None
# variable injection function
def insert_logger(logging_class_instance):
    global logger
    name_of_class = logging_class_instance.__class__.__name__
    if name_of_class != "custom_logger":
        return False
    logger = logging_class_instance
    return True


def get_database(id):
    # LOGGER 
    try:
        logger.store_log()
    except Exception as e:
        None
        
    response = requests.post(f'https://api.notion.com/v1/databases/{id}/query',headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return generate_outcome_message('success',data)
    else:
        return generate_outcome_message("error",response.text,the_type="others")

def extract_data_from_properties(property_object):
    # LOGGER 
    try:
        logger.store_log()
    except Exception as e:
        None
        
    extract = {}
    for column_name,obj in property_object.items():
        if obj["type"] == "rich_text":
            if len(obj['rich_text']) >= 1:
                extract[column_name] = obj["rich_text"][0]['plain_text']
        if obj["type"] == "title":
            if len(obj["title"]) >= 1:
                extract[column_name] = obj["title"][0]['plain_text']
        if obj["type"] == "number":
            extract[column_name] = obj["number"]
    return generate_outcome_message('success',extract)


def extract_core_row_data_from_table(results):
    # LOGGER 
    try:
        logger.store_log()
    except Exception as e:
        None
        
    table_data = []
    for row in results:
        outcome = extract_data_from_properties(row["properties"])["output"]
        outcome["url"] = row["url"]
        table_data.append(outcome)
    return generate_outcome_message('success',table_data)

def extract_specific_row(core_rows,column_name,value):
    # LOGGER 
    try:
        logger.store_log()
    except Exception as e:
        None
        
    for i in core_rows:
        # print(i)
        if i[column_name] == value:
            return i
    return False



# outcome = get_database(x,baseURL)
# # print(outcome)
# final = extract_row_data_from_table(results=outcome["results"])
# for i in final:
#     print("------")
#     for key,value in i.items():
#         print(key, ":", value)
# https://api.notion.com/v1/databases/[database_id]/query?filter_properties=[property_id_1]

