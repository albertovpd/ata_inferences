from flask import Flask, jsonify, request
import json
from ata_fir import ata_fir_function


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    '''
    - It uses an input json through GET. It must contain certain parameters. Check the Readme.
    - It Delivers ATA in json format.
    Adapted from https://www.youtube.com/watch?v=s_ht4AKnWZg&lc=z220gpfjoxnlurv4304t1aokg42ehhj3eurkyxdt4iyebk0h00410
    '''
    input_data= request.get_json()

    return jsonify({"Inferred ATA":ata_fir_function(input_data)})
    

if __name__ == "__main__":
    app.run(debug=True)