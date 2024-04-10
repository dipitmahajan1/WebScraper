import json
# [‘ObjectTypes’][‘value’][‘originalValue’].lower()
def vaildate(slots):
    if slots['ObjectTypes']:
        if slots[‘ObjectTypes’][‘value’][‘originalValue’].lower() == ‘power’:
            print(‘Validating Power Object Type’)
            return {
                ‘isValid’: True,
                ‘invalidSlot’: ‘ObjectTypePower’,
                ‘message’: ‘Here is the Power information.....’
            }
        if slots[‘ObjectTypes’][‘value’][‘originalValue’].lower() == ‘banks’:
            print(‘Validating Banks Object Type’)
            return {
                ‘isValid’: True,
                ‘invalidSlot’: ‘ObjectTypeBanks’,
                ‘message’: ‘Here is the Banks information.....’
            }
        if slots[‘ObjectTypes’][‘value’][‘originalValue’].lower() == ‘rail’:
            print(‘Validating Rail Object Type’)
            return {
                ‘isValid’: True,
                ‘invalidSlot’: ‘ObjectTypeRail’,
                ‘message’: ‘Here is the Rail information.....’
            }
        if slots[‘ObjectTypes’][‘value’][‘originalValue’].lower() == ‘hospital’:
            print(‘Validating Hospital Object Type’)
            return {
                ‘isValid’: True,
                ‘invalidSlot’: ‘ObjectTypeHospital’,
                ‘message’: ‘Here is the Hospital information.....’
            }
        # else:
        #     print(‘Validating None type Object Type’)
        #     return {
        #         ‘isValid’: False,
        #         ‘invalidSlot’: ‘ObjectTypes’,
        #         ‘message’: ‘Here is the None information.....’
        #     }
    return {
        ‘isValid’: False,
        ‘invalidSlot’: ‘ObjectTypes’,
        ‘message’: ‘The Validation failed.....’
    }
def lambda_handler(event, context):
    print(event)
    slots = event[‘sessionState’][‘intent’][‘slots’]
    intent = event[‘sessionState’][‘intent’][‘name’]
    print(slots)
    print(intent)
    validation_result = vaildate(slots)
    print(“CHECK HERE”)
    print(validation_result)
    if event[‘invocationSource’] == ‘DialogCodeHook’:
        if not validation_result[‘isValid’]:
            print(“CHECK HERE 2")
            print(validation_result)
            response = {
                ‘sessionState’: {
                        ‘dialogAction’: {
                            ‘slotToElicit’: validation_result[‘invalidSlot’],
                            ‘type’: ‘ElicitSlot’
                        },
                        ‘intent’: {
                            ‘name’: intent,
                            ‘slots’: slots
                        }
                    },
                    ‘messages’: [
                        {
                        ‘contentType’: ‘PlainText’,
                        ‘content’: validation_result[‘message’]
                        }
                    ]
            }
        else:
            response = {
                ‘sessionState’: {
                    ‘dialogAction’: {
                        ‘type’: ‘Delegate’
                    },
                    ‘intent’: {
                        ‘name’: intent,
                        ‘slots’: slots
                    }
                }
            #     “messages”: [
            #         {
            #             ‘contentType’: ‘PlainText’,
            #             ‘content’: validation_result[‘message’]
            #         }
            #     ]
            }
    # else:
    #     response = {
    #         ‘sessionState’: {
    #             ‘dialogAction’: {
    #                 ‘type’: ‘Delegate’
    #             },
    #             ‘intent’: {
    #                 ‘name’: intent,
    #                 ‘slots’: slots
    #             }
    #         }
    #     }
    # if event[‘invocationSource’] == ‘FulfillmentCodeHook’:
    print(response)
    return response






