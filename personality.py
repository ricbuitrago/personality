import pandas as pd
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from os.path import join, dirname
import json

authenticator = IAMAuthenticator('yc0-_NsnTAezJFQGCw-RyvOX2yKTb6-CFAFbLB0o2VQN')
personality_insights = PersonalityInsightsV3(
    version='2019-07-25',
    authenticator=authenticator
)
personality_insights.set_service_url('https://gateway.watsonplatform.net/personality-insights/api')

def PersonalityProduct(personality_text):

    profile = personality_insights.profile(
            personality_text,
            'application/json',
            content_type='text/plain',
            consumption_preferences=False,
            content_language='es',
            accept_language='eS',
            raw_scores=False,
            csv_headers=True,
            ).get_result()
    Personality=profile['personality']
    GlobalResult=pd.DataFrame.from_dict(Personality)
    GlobalResult=GlobalResult.drop(['category','significant','trait_id','children'],axis=1)
    Resultado = []
    for p in range(0, 5):
        Data=pd.DataFrame.from_dict(Personality[p])
        Data[['trait_id2', 'child_name','category2','percentile2','significant2']] = Data.children.apply(pd.Series)
        Data= Data.drop(['trait_id','category','significant','children','trait_id2','category2','significant2'],axis=1)
        Resultado.append(Data)

    Resultado = pd.concat(Resultado)
    TextoFinal=Resultado.to_json(orient='records')   
    return TextoFinal
