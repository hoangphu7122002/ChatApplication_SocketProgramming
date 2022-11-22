HEADER_LENGTH = 10
QUEUE_CLIENT = 5

user1 = { "user_name": "HP7122002",
          "password": "071202"}

user2 = { "user_name": "GP2002",
          "password": "wtf" }
        
user3 = { "user_name": "dakLoc",
          "password": "123456"}

list_user = [user1,user2,user3]

auth_success = {
    "user_name" : "SERVER",
    "type" : "login",
    "message" : "login success"
}

auth_fail = {
    "user_name" : "SERVER",
    "type" : "login",
    "message" : "login fail"
}

auth_already = {
    "user_name" : "SERVER",
    "type" : "login",
    "message" : "login already exists"
}