"""
A simple websocket server forwarding chat messages received from a livestream chat

After connection the client needs to register to the livestream via following 
json where URL is the URL of the livestream:
{com:"register",val:"URL"}
Supported are twitch, youtube and reddit livestreams

Licensed under:
The MIT License

Copyright (c) 2022 FDMX2 @ github 
 
"""

import logging
import json
from threading import Thread
from threading import Lock
from websocket_server import WebsocketServer
from chat_downloader import ChatDownloader


ws_port = 13254

logger = logging.getLogger('MsgForwarder')
logger.setLevel(logging.INFO)


thread_lock = Lock()

chat_downloaders = {}



def register_chat(url, client):
  release_chat(client['id'])
  logger.info("Client " + str(client['id']) + " registers chat for '" + url + "'")
  thread = Thread(target = start_receiving_chat, args = (url,client))
  thread.start()  
  
def release_chat(client_id, url = False):
  
  thread_lock.acquire()
  
  if client_id in chat_downloaders and chat_downloaders[client_id]:
    for chat_downloader in chat_downloaders[client_id].copy():
      if url and chat_downloader['url'] != url:
        continue 
      try: 
        chat_downloader['downloader'].close()
        logger.info("Released chat downloader of " + chat_downloader['url'] + " for client " + str(client_id))
      except Exception as e:
        logger.warning("Failed to release chat downloader of " + chat_downloader['url'] + " for client " + str(client_id) + " because: " + str(e))
      chat_downloaders[client_id].remove(chat_downloader)
    if len(chat_downloaders[client_id]) <= 0:
      del chat_downloaders[client_id]
      logger.info("Released all chat downloaders of client " + str(client_id))
  thread_lock.release()

# Starts receiving the chat for given url to forward messages via the client_id
def start_receiving_chat(url, client):
  logger.info("Start chat downloader instance for client " + str(client['id']) + " of url: " + url)

  chatDownloader_instance = ChatDownloader()
    
  try:        
    thread_lock.acquire()
    
    downloaders = []
    if client['id'] in chat_downloaders:
      downloaders = chat_downloaders[client['id']] 
    downloaders.append({
      'downloader' : chatDownloader_instance,
      'url' : url
    })  
    chat_downloaders[client['id']] = downloaders
    
    thread_lock.release()
    
  except Exception as e:
    logger.error("Error while creating chatDownloader instance for " + str(client['id']) + " of url: " + url + ": " + str(e))
    release_chat(client['id'])
    return
  
  try:    
    chat = chatDownloader_instance.get_chat(url)
    for message in chat:
      
      msg_type = message.get("message_type")
      if not msg_type or not (msg_type == "text_message"):
        continue
              
      text = message.get("message")
      if not text:
        continue             
      
      timestamp = message.get("timestamp")
      if not timestamp:
        continue            
      
      author = message.get("author")
      if not author:
        continue
      author_id = author.get("id")
      if not author_id:
        continue       

      #chat.print_formatted(message)
      
      msg = {
        "author_id" : author_id,
        "timestamp" : timestamp,
        "text" : text,
        "msg" : message,
        "url" : url
      }
      
      msg_json = json.dumps(msg, separators=(',', ':'))
        
      server.send_message(client, msg_json)      
  except Exception as e:
    logger.error("Error while receiving chat messages for " + str(client['id']) + " of url: " + url + ":" + str(e))
  
  release_chat(client['id'], url)  

# Called for every client connecting (after handshake)
def new_client(client, server):
  logger.info("New client connected and was given id %d" % client['id'])
  server.send_message(client, '{"info": "welcome"}') 

# Called for every client disconnecting
def client_left(client, server):
  print("Client(%d) disconnected" % client['id'])
  release_chat(client['id'])

# Called when a client sends a message
def message_received(client, server, message):
      
  msgJson = None 
  try:
    msgJson = json.loads(message)    
  except Exception as e:
    logger.warning("Failed to parse invalid message from client " + str(client['id']) + ": " + message + " because: " + str(e))
    return
  
  if not "com" in msgJson:
    logger.warning("Got invalid message from client " + str(client['id']) + " without 'com' field: " + message)
    return
    
  if not "val" in msgJson:
    logger.warning("Got invalid message from client " + str(client['id']) + " without 'val' field: " + message)
    return
       
  parts = message.split("=")
  com = msgJson["com"]
  val = msgJson["val"]
  
  logger.info("Received " + com + " from client " + str(client['id']))
  
  if com == "register":
    register_chat(val, client)
    return
    
  if com == "unregister":    
    release_chat(client['id'])
    return
    
  logger.warning("Got unknown command from client " + str(client['id']) + " without 'val' field: " + message)
  

server = WebsocketServer(host='127.0.0.1', port=ws_port, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
