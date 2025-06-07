from dotenv import load_dotenv
load_dotenv()
from app.telegrambot.endpoint import BOT
# print(search_for(query))

resp = """Chapter 4:1 verse 1 [link](https://vedabase.io/en/library/bg/4/1) 
 **The Personality of Godhead, Lord Sri Krishna, said: I instructed this imperishable science of yoga to the sun-god, Vivasvan, and Vivasvan instructed it to Manu, the father of mankind, and Manu in turn instructed it to Ikshvaku.** 
 "Let me worship," Lord Brahma said, "the Supreme Personality of Godhead, Govinda [Krishna], who is the original person and under whose order the sun, which is the king of all planets, is assuming immense power and heat. The sun represents the eye of the Lord and traverses its orbit in obedience to His order."
Chapter 11:40 verse 40 [link](https://vedabase.io/en/library/bg/11/40) 
 **Obeisances to You from the front, from behind and from all sides! O unbounded power, You are the master of limitless might! You are all-pervading, and thus You are everything!** 
 "Whoever comes before You, be he a demigod, is created by You, O Supreme Personality of Godhead."
Chapter 4:5 verse 5 [link](https://vedabase.io/en/library/bg/4/5) 
 **The Personality of Godhead said: Many, many births both you and I have passed. I can remember all of them, but you cannot, O subduer of the enemy!** 
 "I worsh"""

BOT.send_message(7964021486, resp)