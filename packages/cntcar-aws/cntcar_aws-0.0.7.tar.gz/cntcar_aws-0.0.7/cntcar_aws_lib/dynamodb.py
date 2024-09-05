import boto3
import datetime as dt
from .utils import handle_error

def get_params(key:dict, table_name:str, params:list):
    '''This function retrieves specific parameters from a DynamoDB table item.
    
    Parameters:
        key : dict
            A dictionary where each key-value pair represents an attribute name and its value that will be used to identify the item in the DynamoDB table.
        table_name : str
            The name of the DynamoDB table where the item is stored.
        params : list
            A list of strings representing the names of the attributes that will be retrieved from the DynamoDB item.

    Return:
        dict
    '''
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        item = response['Item']
        return {param: item[param] for param in params}
    except Exception as e:
        detail = f'Error getting params from DynamoDB: {str(e)}'
        handle_error(e,detail)


def update_item(key:dict, table_name:str, update_dict:dict):
    """This function update data from an specific item on a DynamoDB table.
    
    Parameters:
        key : dict
            A dictionary where each key-value pair represents an attribute name and its value that will be used to identify the item in the DynamoDB table.
        table_name : str
            The name of the DynamoDB table where the item is stored.
        update_dict : dict
            A dictionary where each key-value pair represents an attribute name and its new value that will be updated in the DynamoDB item.
        
    Return:
        None
    """
    dynamodb = boto3.resource('dynamodb')
    dynamodb = dynamodb.Table(table_name)

    for param, value in update_dict.items():
        dynamodb.update_item(
            Key=key,
            UpdateExpression=f'SET {param} = :val',
            ExpressionAttributeValues={':val': value}
        )

    print(f'DynamoDB updated successfully - {dt.datetime.now()}')