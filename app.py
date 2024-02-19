import v3_Reddit_lead_finder
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from v3_Reddit_lead_finder import v3_reddit_lead_finder

app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=['POST', 'GET'],
        allow_headers=["*"],
)


# This takes in the passed product/probelm description from the user  (need to figure this out) and then returns the JSON of the leads that passed the K result request and eval stages.
@app.get("/reddit_leads_finder") 
async def reddit_lead_finder(product_description : str) : 
    leads = await v3_reddit_lead_finder(product_description=product_description, user_id_index_name="test-index")
    return JSONResponse(status_code=200, content=leads)