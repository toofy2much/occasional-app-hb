# import os
# from twilio.rest import Client #, logging
# from twilio.twiml.messaging_response import Message #, MessagingResponse
#from twilio.base.exceptions import TwilioRestException

#set the environment variables
#send and sms


# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, token_token)

# client.region = 'us1' #edge 
# client.edge = 'philadelphia'#region 
#logging.basicConfig(filename='./log.txt')
#client.http_client.logger.setLevel(logging.INFO)
# hostname should = api.philadelphia.usa1.twilio.com

# message = client.messages.create(to="+12672581229", from_="+12156085643",
#                                  body="Hello World!")

# print(message)                               
# response = MessagingResponse()
# response.message('disco')

# print(response)
# print(client.http_client.last_response.status_code)


# try:
#     # This could potentially throw an exception!
#     message = client.messages.create(
#         to="+15558675309", 
#         from_="+15017250604",
#         body="Hello there!")
# except TwilioRestException as e:
#     # Implement your fallback code
#     print(e)