import boto3
import datetime as dt
from utils import handle_error

def get_params_from_dynamodb(key, table, params):
    '''This function retrieves specific parameters from a DynamoDB table item.
    
    Parameters:
        key : dict
            A dictionary where each key-value pair represents an attribute name and its value that will be used to identify the item in the DynamoDB table.
        table : str
            The name of the DynamoDB table where the item is stored.
        params : list
            A list of strings representing the names of the attributes that will be retrieved from the DynamoDB item.

    Return:
        dict
    '''
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table)
        response = table.get_item(Key=key)
        item = response['Item']
        return {param: item[param] for param in params}
    except Exception as e:
        detail = f'Error getting params from DynamoDB: {str(e)}'
        handle_error(e,detail)


def update_item(key:str, table_name:str, update_dict:dict):
    """This function update data from an specific item on a DynamoDB table.
    
    Parameters:
        proccess_name : str
            This is used as the key to identify the item in the DynamoDB table that needs to be updated.
        table_name : str
            The name of the DynamoDB table where the item is stored.
        update_dict : dict
            A dictionary where each key-value pair represents an attribute name and its new value that will be updated in the DynamoDB item.
        
    Return:
        None
    """
    job_config = boto3.resource('dynamodb')
    job_config = job_config.Table(table_name)

    for param, value in update_dict.items():
        job_config.update_item(
            Key={'key': key},
            UpdateExpression=f'SET {param} = :val',
            ExpressionAttributeValues={':val': value}
        )

    print(f'DynamoDB updated successfully - {dt.datetime.now()}')