HEADER_LENGTH = 10
QUEUE_CLIENT = 5

CHAT_PROTOCOL_HI = 'Chat_Hi'
CHAT_PROTOCOL_HI_ACK = 'Chat_Hi_ACK'
CHAT_PROTOCOL_BYE = 'Chat_Bye'
CHAT_PROTOCOL_BYE_ACK = 'Chat_Bye_Ack'
CHAT_PROTOCOL_UPDATE = 'Chat_Update'
CHAT_PROTOCOL_UPDATE_ACK = 'Chat_Update_Ack'
CHAT_PROTOCOL_CONNECT = 'Chat_Connect'
CHAT_PROTOCOL_CONNECT_ACK = 'Chat_Connect_Ack'
CHAT_PROTOCOL_DIS = 'Chat_Dis'
CHAT_PROTOCOL_DIS_ACK = 'Chat_Dis_Ack'
CHAT_PROTOCOL_MSG = 'Chat_Msg'
CHAT_PROTOCOL_CHAT_GROUP = 'Chat_Group'
CHAT_PROTOCOL_CHAT_GROUP_ACK = 'Chat_Group_Ack'
CHAT_PROTOCOL_TRANSFER_FILE = 'Transfer_File'
CHAT_PROTOCOL_TRANSFER_FILE_ACK = 'Transfer_File_Ack'
CHAT_PROTOCOL_TRANSFER_GROUP = 'Transfer_Group'
CHAT_PROTOCOL_TRANSFER_GROUP_ACK = 'Transfer_Group_Ack'
AUTH_PROTOCOL_SUCCESS = 'Authentication_success'
AUTH_PROTOCOL_FAIL = 'Authentication_fail'
AUTH_PROTOCOL_ALREADY = 'Authentication_already'
AUTHENTICATION = 'Authentication'


ALREADY_CONNECT = 10
FAIL_CONNECT = 10

user1 = { "user_name": "HP7122002",
          "password": "123456"}

user2 = { "user_name": "GP2002",
          "password": "123456" }
        
user3 = { "user_name": "dakLoc",
          "password": "123456"}

user4 = { "user_name": "nguyen",
          "password": "123456"}

list_user = [user1,user2,user3,user4]

auth_success_connect = {
    "user_name" : "SERVER",
    "type" : AUTH_PROTOCOL_SUCCESS
}

auth_fail_connect = {
    "user_name" : "SERVER",
    "type" : AUTH_PROTOCOL_FAIL
}

auth_already_connect = {
    "user_name" : "SERVER",
    "type" : AUTH_PROTOCOL_ALREADY
}