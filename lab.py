# from dotenv import load_dotenv
# load_dotenv()
from app.telegrambot.base import BOT

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

resp2 = """
The Bhagavad Gita indicates that the ultimate goal of life is liberation from the material struggle for existence. This involves self-realization and understanding our relationship with the Supreme Lord, Krishna.

Here's how the Gita touches upon this:

*   **Attaining Transcendental Position:** The purpose of life is indicated to be renunciation and attainment of the transcendental position above the three material modes of nature.(18:1)

*   **Self-Realization:** We should make proper use of resources to keep ourselves fit and healthy for the purpose of self-realization, leading to liberation.(3:12)

*   **Returning to the Spiritual Energy:** The Supreme Lord, as the Supersoul, stays with the living entity to get him to return to the spiritual energy.(13:23)

*   **Devotional Service:** After material cessation, there is the manifestation of spiritual activities, or devotional service to the Lord, known as Krishna consciousness, which is the real life of the living entity.(6:20-23)

Ultimately, the Gita suggests that by understanding our true nature and engaging in activities that connect us with the Divine, we can achieve lasting happiness and freedom from the cycle of birth and death.
"""


BOT.send_message(7964021486, "Hello")

# from src.agents.responder import multi_query_fusion
# from app.webapp.dataclass import model_query
# from src.agents.search import search_for


# query = "What is the goal of life?"
# agent = multi_query_fusion(query=model_query(model='deep_1',
#                                            question=query))

# print(agent.cleaned())
