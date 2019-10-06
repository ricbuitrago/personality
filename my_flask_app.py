from flask import Flask, Response, jsonify 
from flask_restplus import Api, Resource, fields, reqparse 
from flask_cors import CORS, cross_origin 
import os 
# the app 
app = Flask(__name__) 
CORS(app) 
api = Api(app, version='1.0', title='APIs for Personality', validate=False) 
ns = api.namespace('personality', 'Returns a list of all primes below a given upper bound') 
# load the algo 
from personality import PersonalityProduct as algo 
''' We import our function `PersonalityProduct` from the file personality.py. You create all the classes and functions that you want in that file, and import them into the app. ''' 
# model the input data 
model_input = api.model('Enter the text:', { "PERSONALITY_TEXT": fields.String}) 
# the input data type here is Integer. You can change this to whatever works for your app. 
# On Bluemix, get the port number from the environment variable PORT # When running this app on the local machine, default to 8080 
port = int(os.getenv('PORT', 8080)) 
# The ENDPOINT 
@ns.route('/personality') 
# the endpoint 
class SIEVE(Resource): 
    @api.response(200, "Success", model_input)   
    @api.expect(model_input)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('PERSONALITY_TEXT', type=str)
        args = parser.parse_args()
        inp = str(args["PERSONALITY_TEXT"]) 
        result = algo(inp) 
        return jsonify({"texto": result}) 
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
