from pydantic import BaseModel, Field


class model_query(BaseModel):
    model : str = Field('naive',description= "The name of the model")
    query : str = Field('Give a summary of Gita',description="The query of the user")
    past_discussions : str = Field(description="Summary of past discussions or compilation of all questions")
    reply_to : str = Field(description="The previous message, on which the user is asking")
    


    