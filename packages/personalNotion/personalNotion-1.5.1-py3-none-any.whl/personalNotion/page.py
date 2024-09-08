# from dotenv import load_dotenv
# load_dotenv()
from . import headers,get_logger
import requests
from custom_development_standardisation import generate_outcome_message


import re



pattern = r'^[0-9a-zA-Z\s\.,;:!@#$%^&*()_+\-=\[\]{}|\\\'\"<>/?`~]*$'
# print(api_key)


children = []

# Define the data payload with the children list
data = {
    'children': children
}

def create_page_in_page(page_id,page_name=""):
    # Place this snippet inside the function, and let it be the first that to execute within the function
    try:
        get_logger().store_log()
    except Exception as e:
        None
    
    outcome = get_page(page_id=page_id)
    if outcome["outcome"] == "error":
        return generate_outcome_message("error",outcome["output"],the_type="custom")
    custom_data = {
        "parent": {
            "page_id": page_id
        },
        "properties": {
            "title": [
				{
					"text": {
						"content": page_name
					}
				}
			]
        }
    }
    response = requests.post(f'https://api.notion.com/v1/pages?', headers=headers, json=custom_data)
    if response.status_code == 200:
        data = response.json()
        return generate_outcome_message('success',data)
    else:
        return generate_outcome_message("error",response.text,the_type="others")


    
# https://www.notion.so/Distribution-management-system-51cf3a7b431940cbae992abcea4eca77?pvs=4

def get_page(page_id):
    try:
        get_logger().store_log()
    except Exception as e:
        None
    
    response = requests.get(f'https://api.notion.com/v1/pages/{page_id}?', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return generate_outcome_message('success',data)
    else:
        return generate_outcome_message("error",response.text,the_type="others")
    
# Append text to existing block
def append_text_to_text_block(block_id,str_to_append):
    # LOGGER
    try:
        get_logger().store_log()
    except Exception as e:
        None

    if re.match(pattern, str_to_append) == False:
            return generate_outcome_message("error", "str_to_append parameter is not a primal value...",the_type="custom")
    
    # Get original data
    response = requests.get(f"https://api.notion.com/v1/blocks/{block_id}",headers=headers)
    if response.status_code == 200:
        # Extract data
        data = response.json()
        
        typer = data["type"]
        if typer != "paragraph":
            return generate_outcome_message("error",f"expect block to be of type paragraph. Got {typer} type instead...",the_type="custom")
        original = data[typer]["rich_text"][0]['text']["content"]
        # Append the data
        original += str_to_append
        # update the block
        json = {
            "paragraph": {
                "rich_text": [{ 
                    "text": { "content": original } 
                }],
            }
        }
        response = requests.patch(f"https://api.notion.com/v1/blocks/{block_id}",headers=headers,json=json)
        if response.status_code == 200:
            return generate_outcome_message('success',response.json())
        else:
            return generate_outcome_message("error",response.text,the_type="others")    
    else:
        return generate_outcome_message("error",response.text,the_type="others")



# Each item is contained in a block
def add_text_blocks(page_id,arr):
    # LOGGER
    try:
        get_logger().store_log()
    except Exception as e:
        None

    if isinstance(arr,list) == False:
        return generate_outcome_message("error","arr parameter is not of type list...",the_type="custom")
    json = []
    for i in arr:
        if re.match(pattern, i) == False:
            return generate_outcome_message("error", "there is a value in the list that is not a primal value...",the_type="custom")
        json.append({
			"object": "block",
			"type": "paragraph",
			"paragraph": {
				"rich_text": [
					{
						"type": "text",
						"text": {
							"content": i,
						}
					}
				]
			}
		})
    response = requests.patch(f'https://api.notion.com/v1/blocks/{page_id}/children',headers=headers,json={"children":json})
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return generate_outcome_message('success',data)
    else:
        return generate_outcome_message("error",response.text,the_type="others")
    

def extract_all_blocks_from_page(page_id):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None

    response = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children?', headers=headers)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return generate_outcome_message('success',data)
    else:
        return generate_outcome_message("error",response.text,the_type="others")

def extract_core_data_from_all_blocks(results):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    core_data = []
    for i in results:
        entering_stack = i[i["type"]]["rich_text"]
        if len(entering_stack) >= 1:
            
            data = entering_stack[0]["plain_text"]
            core_data.append(data)
    return generate_outcome_message('success',core_data)

def extract_data(page_id,data_type):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    outcome = extract_all_direct_core_data_encapsulation(page_id=page_id)
    if outcome["outcome"] == "error":
        return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
    outcome = extract_data_from_encapsulations(outcome["output"],data_type=data_type)
    if outcome["outcome"] == "error":
        return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
    return generate_outcome_message("success",outcome["output"])

# Try to get as deep as possible using a single rule
def extract_all_direct_core_data_encapsulation(page_id):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    outcome = extract_all_blocks_from_page(page_id)
    if outcome["outcome"] == "error":
        return generate_outcome_message("error",outcome["output"],the_type="custom")
    final = []
    for i in outcome["output"]["results"]:
        typer = i["type"]
        ider = i["id"]
        encapsulation = i[typer]
        encapsulation["type"] = typer
        encapsulation["id"] = ider
        final.append(encapsulation)
    return generate_outcome_message("success",final)

def extract_data_from_encapsulations(encapsulation_list,data_type="text"):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    func = None
    if data_type != "text" and data_type != "page" and data_type != "id":
        return generate_outcome_message("error",f"data type extract of {data_type} does not exist...",the_type="custom")
    if data_type == "text":
        func = extract_text
    elif data_type == "page":
        func = extract_pages
    elif data_type == "id":
        func = extract_id
    extract = []
    for i in encapsulation_list:
        outcome = func(i)
        if outcome["outcome"] == "error":
            return generate_outcome_message("error",outcome["output"],the_type=outcome["the_type"])
        if outcome["output"] == False:
            continue
        extract.append(outcome["output"])
    return generate_outcome_message("success",extract)

def extract_text(data):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    if data["type"] != "paragraph" and data["type"] != "child_page" and data["type"] != "code" and data["type"] != "heading_3" and data["type"] != "heading_2" and data["type"] != "heading_1":
        return generate_outcome_message("error",f"data of type {data['type']} is not within consideration...",the_type="custom")
    text = None
    if data["type"] == "paragraph" or data["type"] == "code" or data["type"] == "heading_1" or data["type"] == "heading_2" or data["type"] == "heading_3":
        current = data["rich_text"]
        if len(current) == 0:
            text = ""
        else:
            text = current[0]["text"]["content"] 
    if data["type"] == "child_page":
        text = data["title"]
    return generate_outcome_message("success",text)

def extract_pages(data):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    if data["type"] != "child_page":
        return generate_outcome_message("success",False)
    return generate_outcome_message("success",data["id"])


def extract_id(data):
    # LOGGER 
    try:
        get_logger().store_log()
    except Exception as e:
        None
        
    if not isinstance(data, dict):
        return generate_outcome_message("error", "Input data is not a dictionary", the_type="custom")
    
    try:
        id = data["id"]
    except KeyError:
        return generate_outcome_message("error", "ID field is missing", the_type="custom")
    except Exception as e:
        return generate_outcome_message("error", f"An unexpected error occurred: {str(e)}", the_type="custom")
    
    return generate_outcome_message("success", id)


# outcome = get_page("b74cbfbe7cc2490e9dc3210f06eb3c8e")
# print(outcome)


# print(extract_id_from_database_page_url("https://www.notion.so/usefulness-of-function-utility-e3be345283334d7da007b677502eccad?pvs=4"))

# print(get_page("51cf3a7b431940cbae992abcea4eca77"))
# print(extract_all_blocks_from_page("51cf3a7b431940cbae992abcea4eca77"))
# def extract_block_data(page_id):
#     if page_id === 


# https://www.notion.so/Distribution-management-system-51cf3a7b431940cbae992abcea4eca77?pvs=4