from typing import List

from fastapi import FastAPI

from players.player_category_leader import PlayerCategoryLeader

app = FastAPI()


@app.get("/", response_model=List[PlayerCategoryLeader])
async def get_category_leaders():
    # This function requests the top n players of a specific category
    return {"message": "The server works"}
