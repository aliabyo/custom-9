import random
import time
import requests
from highrise import BaseBot, Highrise, Position, AnchorPosition, Reaction
from highrise import __main__
from asyncio import run as arun
from emotes import Dance_Floor
import asyncio
from random import choice
import json
from typing import List
from datetime import datetime, timedelta
from highrise.models import SessionMetadata
import re
from highrise.models import SessionMetadata,  GetMessagesRequest, User ,Item, Position, CurrencyItem, Reaction
from typing import Any, Dict, Union
from highrise.__main__ import *
import asyncio, random




class BotDefinition:
    
      
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token
        self.following_username = None

class Counter:
    bot_id = ""
    static_ctr = 0
    usernames = ['Alionardo_','Babygirl_Cin']

class Bot(BaseBot):
  
    continuous_emote_task = None
    cooldowns = {}  # Class-level variable to store cooldown timestamps
    emote_looping = False

    def __init__(self):
        super().__init__()
        self.load_membership()
        self.load_moderators()
        self.load_temporary_vips()
        self.following_username = None
        self.maze_players = {}
        self.user_points = {}  # Dictionary to store user points

        #conversation id var
        self.convo_id_registry = []

      
    def load_temporary_vips(self):
        try:
            with open("temporary.json", "r") as file:
                self.temporary_vips = json.load(file)
        except FileNotFoundError:
            self.temporary_vips = {}
   
    def save_temporary_vips(self):
      with open("temporary.json", "w") as file:
          json.dump(self.temporary_vips, file)
    def load_moderators(self):
        try:
            with open("moderators.json", "r") as file:
                self.moderators = json.load(file)
        except FileNotFoundError:
            self.moderators = []

        # Add default moderators here
        default_moderators = ['Alionardo_','Babygirl_Cin']
        for mod in default_moderators:
            if mod.lower() not in self.moderators:
                self.moderators.append(mod.lower())
       
    def load_membership(self):
     try:
        with open("membership.json", "r") as file:
            self.membership = json.load(file)
     except FileNotFoundError:
        self.membership = []
    def save_membership(self):
     with open("membership.json", "w") as file:
        json.dump(self.membership, file)

  
    def save_moderators(self):

      with open("moderators.json", "w") as file:
            json.dump(self.moderators, file)

  
    async def announce(self,user_input,message: str):
      while True:  
              await asyncio.sleep(6)
              await self.highrise.chat(user_input)
              await asyncio.sleep(60)
              await self.highrise.send_emote('emote-hello')
    async def on_start(self, session_metadata: SessionMetadata) -> None:
      try:
       
        Counter.bot_id = session_metadata.user_id
        print("Ali is booting ...")
   

        self.highrise.tg.create_task(self.highrise.walk_to(Position(2.5, 0.25, 4.5, facing='FrontRight')))
        self.load_temporary_vips()

        await self.highrise.chat(f"hi guys im here ")
      except Exception as e:
          print(f"An exception occured: {e}")  
    async def on_emote(self, user: User ,emote_id : str , receiver: User | None )-> None:
      print (f"{user.username} , {emote_id}")

    async def on_user_join(self, user: User) -> None:

     try:

        await self.highrise.send_whisper(user.id,f"\n ____________________________\nHello {user.username}\nWelcome to what gonna be your lovely place\n        💜Tip a Cutie💜\n• !list or -list \nto veiw the functions \nfor bots dm @Alionardo_ .\n ____________________________\n")
        await self.highrise.send_emote('emote-salute')
     
     except Exception as e:
            print(f"An error on user_on_join: {e}") 


    async def on_user_leave(self, user: User) ->None:
      try:
        print(f"{user.username} has left the room")
        await self.highrise.chat(f"  {user.username} left the room")
      
      except Exception as e:
         print(f"An error on user_on_join: {e}") 
      
    
    async def teleport_user_next_to(self, target_username: str, requester_user: User):
      room_users = await self.highrise.get_room_users()
      requester_position = None

      for user, position in room_users.content:
        if user.id == requester_user.id:
            requester_position = position
            break
      for user, position in room_users.content:
        if user.username.lower() == target_username.lower(): 
          z = requester_position.z 
          new_z = z + 1 

          user_dict = {
            "id": user.id,
            "position": Position(requester_position.x, requester_position.y, new_z, requester_position.facing)
          }
          await self.highrise.teleport(user_dict["id"], user_dict["position"])

   

   

    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions) 
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
     try:
      if user.username == "Babygirl_Cin" :
        if reaction == "heart":
          await self.highrise.chat(f"{receiver.username} is now a Permanent VIP, given by {user.username}")

          receiver_username = receiver.username.lower()
          if receiver_username not in self.moderators:
                self.moderators.append(receiver_username)
                self.save_moderators()


        if user.username == "Babygirl_Cin"  :
          if reaction == "wink":
              await self.highrise.chat(f"{receiver.username} is now a Temporary VIP, given by {user.username}")

              receiver_username = receiver.username.lower()
              if receiver_username not in self.temporary_vips:
                    self.temporary_vips[receiver_username] = int(time.time()) + 24 * 60 * 60  # VIP for 24 hours
                    self.save_temporary_vips()


      if user.username in ["Babygirl_Cin"] and reaction == "clap":
            await self.highrise.chat(f"{receiver.username} is remove from the commands by {user.username}")

            receiver_username = receiver.username.lower()

            # Remove user from moderators list
            if receiver_username in self.moderators:
                self.moderators.remove(receiver_username)
                self.save_moderators()

            # Add user to temporary VIPs list
            if receiver_username not in self.temporary_vips:
                self.temporary_vips[receiver_username] = int(time.time()) + 24 * 60 * 60  # VIP for 24 hours
                self.save_temporary_vips()

      if user.username in ["Babygirl_Cin"] and reaction == "wave":
            await self.highrise.moderate_room(receiver.id, "kick")
            await self.highrise.chat(f"{receiver.username} is Kicked by {user.username}")

      if reaction =="thumbs" and user.username.lower() in self.moderators:
         target_username = receiver.username
         if target_username not in ["Babygirl_Cin"]:
            await self.teleport_user_next_to(target_username, user)



     except Exception as e:
            print(f"An exception occured: {e}")

      

    def remaining_time(self, username):
        if username in self.temporary_vips:
            remaining_seconds = self.temporary_vips[username] - int(time.time())
            if remaining_seconds > 0:
                return str(timedelta(seconds=remaining_seconds))
        return "Not a temporary VIP."


    async def on_chat(self, user: User, message: str) -> None:
      try:
         user_input = None
         print(f"{user.username} said: {message}")     
         if message.lower().startswith("-announce "):
           if user.username.lower() in self.moderators:
             parts = message.split()
             if len(parts) >= 3:
                user_input =  message[len("-announce "):]
                await self.highrise.chat( "Alright i will loop with with intervals of 60 seconds")
                await self.announce(user_input,message)
                
         if message.startswith("❤️ all"):
           if user.username.lower() in self.moderators:
             roomUsers = (await self.highrise.get_room_users()).content
             for roomUser, _ in roomUsers:
                await self.highrise.react("heart", roomUser.id)
         if message.startswith("!kick"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !kick @username")
                    return

                mention = parts[1]
                username_to_kick = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_kick.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_kick.lower())
                    user_id_to_kick = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_kick, "kick")
                    await self.highrise.chat( f"Kicked {mention}.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!mute"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !mute @username")
                    return

                mention = parts[1]
                username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_mute.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                    user_id_to_mute = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_mute, "mute",3600)  # Mute for 1 hour
                    await self.highrise.chat(f"Muted {mention} for 1 hour.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!unmute"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !mute @username")
                    return

                mention = parts[1]
                username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_mute.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                    user_id_to_mute = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_mute, "mute",1)  # Mute for 1 hour
                    await self.highrise.chat(f"{mention} Unmuted.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!ban"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !ban @username")
                    return

                mention = parts[1]
                username_to_ban = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_ban.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_ban.lower())
                    user_id_to_ban = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_ban, "ban", 3600)  # Ban for 1 hour
                    await self.highrise.chat(f"Banned {mention} for 1 hour.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

        
        
         if message == "!tip5":
              if user.username == "Babygirl_Cin" :
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                  await self.highrise.tip_user(roomUser.id, "gold_bar_5")
              else: 
                await  self.highrise.send_whisper(user.id, f"Only @Babygirl_Cin can use tip!")

         if message == "!tip1":
              if user.username == "Babygirl_Cin":
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                  await self.highrise.tip_user(roomUser.id, "gold_bar_1")
              else: 
                await  self.highrise.send_whisper(user.id, f"Only the @Babygirl_Cin can use tip!")

                

         if message.lower().lstrip().startswith(("-list", "!list")):
                await self.highrise.chat("\\commands you can use:\n• !feedback or -feedback \n• !teleport or -teleport \n• -buy or !buy for \n 🎫VIP Tickets🎫 ")
                await self.highrise.chat(f"\n ____________________________\n• !mod or -mod ( only for mods )")
        
         if message.lower().lstrip().startswith(("-buy" , "!buy")):
             await self.highrise.chat(f"\n  vip = 50 🎫 \nTip 50 to bot you will be aceessed to use tele command ")
        
     
         if message.lower().lstrip().startswith(("-teleport", "!teleport")):
                    await self.highrise.chat(f"\n • Teleports\n ____________________________\nGround floor : -0  \nvip : (vip only), make sure you have 🎫VIP Tickets 🎫 \n• type -buy or !buy for details \ndj :( Mods only )")
         if message.lower().lstrip().startswith(("!rules", "-rules")):
           await self.highrise.chat(f"\n\n        RULES\n ____________________________\n 1. NO UNDERAGE \n 2. No advertising\n 3. No hate speech \n 4. No begging (those trash will be immediately banned 🚫) \n 5. No spamming ")
         if message.lower().lstrip().startswith(("-feedback", "!feedback")):
                    await self.highrise.send_whisper(user.id, "• [ Submit Feedback ]\\Thank you for joining our room! \n We value your feedback,")
                    await self.highrise.send_whisper(user.id,"Please share your feedback/suggestions with @Alionardo_ to improve our environment. Your contributions are valuable and will help us improve.")  

         if user.username.lower() in self.moderators:
            if message.lower().lstrip().startswith(("-mod","!mod")):
               await self.highrise.send_whisper(user.id,"\n  \n•Moderating :\n ____________________________\n !kick @ \n !ban @ \n !mute @ \n !unmute @ ")
               await self.highrise.send_whisper(user.id,"\n  \n•Teleporting :\n ____________________________\n!vip1 @\n!vip2 @\n!host @\n!dj @\n!g @\nReact : thumb to summon.")
            
             
         if message.lstrip().startswith(("!vip1","!dj","!host","!g",'!vip2' )):
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]
            usernames = [user.username.lower() for user in users]
            parts = message[1:].split()
            args = parts[1:]

            if len(args) < 1:
                await self.highrise.send_whisper(user.id, f"Kullanım: !{parçalar[0]} <@Alionardo_>")
                return
            elif args[0][0] != "@":
                await self.highrise.send_whisper(user.id, "Invalid user format. Please use '@username'.")
                return
            elif args[0][1:].lower() not in usernames:
                await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                return

            user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
            user_name = next((u.username.lower() for u in users if u.username.lower() == args[0][1:].lower()), None)
            if not user_id:
                await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
                return                     
            try:
                if message.startswith("!vip1"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(3.5, 4.25,4.5))
                if message.startswith("!vip2"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(4.5, 8.5,3.5))

                if message.startswith("!dj"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(12,14,6))
                if message.startswith("!host"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(11,19.5,4.5))
                if message.startswith("!g"):   
                  if user.username.lower() in self.moderators:
                     await self.highrise.teleport(user_id, Position(12.5,0.25,13.5))
               
              
            except Exception as e:
             print(f"An exception occurred[Due To {parts[0][1:]}]: {e}")

          
         if message.startswith("!time"):
            parts = message.split()
            if len(parts) == 2:
                target_mention = parts[1]

                # Remove the "@" symbol if present
                target_user = target_mention.lstrip('@')

                # Check if the target user has temporary VIP status
                remaining_time = self.remaining_time(target_user.lower())
                await self.highrise.send_whisper(user.id, f"Remaining time for {target_mention}'s temporary VIP status: {remaining_time}")
            else:
                await self.highrise.send_whisper(user.id, "Usage: !time @username")


       
         if message.lower().startswith('vip1') :
            if user.username.lower() in self.moderators or user.username.lower() in self.membership :    
              await self.highrise.teleport(f"{user.id}", Position(3.5, 4.25,4.5))
            else:
             await self.highrise.send_whisper((user.id)," this is a privet place for VIPs , uou can use it by purchaseing VIP Ticket type -buy")
         if message.lower().startswith('vip2') :
           if user.username.lower() in self.moderators or user.username.lower() in self.membership  :    
             await self.highrise.teleport(f"{user.id}", Position(4.5, 8.5,3.5))
           else:
            await self.highrise.send_whisper((user.id)," this is a privet place for VIPs , uou can use it by purchaseing VIP Ticket  type -buy")
         if message.lower().startswith('dj') :
              if user.username.lower() in self.moderators:    
                await self.highrise.teleport(f"{user.id}", Position(12,14,6))
         if message.lower().startswith('host') :
            if user.username.lower() in self.moderators:    
              await self.highrise.teleport(f"{user.id}", Position(11,19.5,4.5))
        
         if message.startswith('-g'):
             await self.highrise.teleport(f"{user.id}", Position(12.5,0.25,13.5))
           
        
         if message.startswith("/e1"):
                 await self.highrise.set_outfit(outfit=[
          Item(type='clothing', 
                    amount=1, 
                    id='body-flesh',
                    account_bound=False,
                    active_palette=12),
          Item(type='clothing',
                    amount=1,
                    id='shirt-n_starteritems2019raglanwhite',
                   account_bound=False,
                    active_palette=-1),
          Item(type='clothing', 
               amount=1, 
               id='pants-n_room12019blackacidwashjeans',
               account_bound=False,
               active_palette=-1),
          Item(type='clothing', 
               amount=1, 
               id='nose-n_01_b',
               account_bound=False,
               active_palette=-1),
         Item(type='clothing',
              amount=1, 
              id='watch-n_room32019blackwatch', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing', 
              amount=1, 
              id='watch-n_room32019blackwatch', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing', 
              amount=1, id='shoes-n_room22019tallsocks', 
              account_bound=False,
              active_palette=-1), 
         Item(type='clothing',
              amount=1, 
              id='shoes-n_converse_black',
              account_bound=False,
              active_palette=-1),       
         Item(type='clothing',
              amount=1, 
              id='freckle-n_basic2018freckle22', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing',
              amount=1,
              id='mouth-basic2018smirk',
              account_bound=False,
              active_palette=3),
         Item(type='clothing',
              amount=1,
              id= 'hair_back-n_malenew01',
              account_bound=False, active_palette=70),
        Item(type='clothing',
              amount=1,
              id= 'hair_front-n_malenew01',
              account_bound=False, active_palette=70),  
         Item(type='clothing', 
              amount=1, 
              id='eye-n_basic2018malediamondsleepy',
              account_bound=False,
              active_palette=2),
        Item(type='clothing', 
             amount=1,
             id='eyebrow-n_06', 
             account_bound=False,
             active_palette=-1)
      ])

         if  message.lower().startswith("wallet"):
            if user.username.lower() in self.moderators :

                  wallet = (await self.highrise.get_wallet()).content
                  await self.highrise.send_whisper(user.id, f"The bot wallet contains {wallet[0].amount} {wallet[0].type}")

            else: 
                await  self.highrise.send_whisper(user.id, f"Only Moderators Can View the Wallet")

    
          
      except Exception as e:
        print(f"An exception occured: {e}")  


    async def follow_user(self, target_username: str):
      while self.following_username == target_username:

          response = await self.highrise.get_room_users()
          target_user_position = None
          for user_info in response.content:
              if user_info[0].username.lower() == target_username.lower():
                  target_user_position = user_info[1]
                  break

          if target_user_position:
              nearby_position = Position(target_user_position.x + 1.0, target_user_position.y, target_user_position.z)
              await self.highrise.walk_to(nearby_position)

              await asyncio.sleep(2)
            
    async def on_whisper(self, user: User, message: str ) -> None:

        if message == "here":
            if user.username.lower() in self.moderators:
                response = await self.highrise.get_room_users()
                users = [content for content in response.content]
                for u in users:
                    if u[0].id == user.id:
                        try:
                            await self.highrise.teleport(Counter.bot_id,Position((u[1].x),(u[1].y),(u[1].z),"FrontRight"))


                            break
                        except:

                            pass
       
        if message.startswith("/say"):
            if user.username.lower() in self.moderators:
                text = message.replace("/say", "").strip()
                await self.highrise.chat(text)

   
         

        elif message.startswith("/come"):
            if user.username.lower() in self.moderators:
                response = await self.highrise.get_room_users()
                your_pos = None
                for content in response.content:
                    if content[0].id == user.id:
                        if isinstance(content[1], Position):
                            your_pos = content[1]
                            break
                if not your_pos:
                    await self.highrise.send_whisper(user.id, "Invalid coordinates!")
                    return
                await self.highrise.chat(f"@{user.username} I'm coming ..")
                await self.highrise.walk_to(your_pos)

        elif message.lower().startswith("/follow"):
         
            target_username = message.split("@")[1].strip()

            if target_username.lower() == self.following_username:
                await self.highrise.send_whisper(user.id,"I am already following.")
            elif message.startswith("/say"):
              if user.username.lower() in self.moderators:
                  text = message.replace("/say", "").strip()
                  await self.highrise.chat(text)
            else:
                self.following_username = target_username
                await self.highrise.chat(f"hey {target_username}.")
            
                await self.follow_user(target_username)
        elif message.lower() == "stop following":
            self.following_username = None
          
            await self.highrise.walk_to(Position(2.5,0.25,4.5,"FrontRight"))

  
  
              
    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem) -> None:
        try:
            print(f"{sender.username} tipped {receiver.username} an amount of {tip.amount}")
            await self.highrise.chat(f"𝓣𝓱𝓮 𝓐𝓶𝓪𝔃𝓲𝓷𝓰 {sender.username} 𝓽𝓲𝓹𝓹𝓮𝓭 {receiver.username} 𝓪𝓷 𝓪𝓶𝓸𝓾𝓷𝓽 𝓸𝓯  {tip.amount}𝐆𝐎𝐋𝐃")

            
       
            if tip.amount == 50:
              if receiver.username  == "Babygirl_Cin_Bot":    
                 sender_username = sender.username.lower()
                 if sender_username not in self.membership:
                   self.membership[sender_username] = int(time.time()) + 24 * 60 * 60  
                   self.save_membership()
                   await self.highrise.chat(f"Thank you {sender_username} for purchasing TRMPORARY vip ticket , now u can use the command vip to teleport to the vip now \nvip1: first floor. \nvip2:second floor 🎫") 

                 
        except Exception as e:
             print(f"An exception occured: {e}")

 

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:


        print(f"{user.username}: {pos}")

   
          
  
    

   




    
