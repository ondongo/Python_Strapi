from flask import Flask, jsonify,render_template,request
import requests

app = Flask(__name__, template_folder='templates')

# A mettre dans le fichier env
strapi_api_url = "http://localhost:1337"
token="your token"

@app.route('/')
def index():
    x = 2
    return str(x) 


@app.route('/foods', methods=['GET'])
def get_foods():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{strapi_api_url}/api/foods", headers=headers)
    if response.status_code == 200:
        foods = response.json()['data']
        return render_template('table.html', foods=foods)
    else:
        return jsonify({"message": "Erreur lors de la récupération des influenceurs depuis Strapi"}), 500



@app.route('/add-foods', methods=['POST'])
def post_food():
    title = request.form.get("title")
   
    if not title:
        return jsonify({"message": "Données non valides"}), 400

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
      "data": {
      "title": title
      }}
    response = requests.post(f"{strapi_api_url}/api/foods", json=payload, headers=headers)
    if response.status_code in [200, 201]:
        new_food = response.json()
        #return jsonify(new_food)
        return redirect(url_for('get_foods'))
    else:
        return jsonify({"message": "Erreur lors de la création du food dans Strapi"}), 500


@app.route('/create-food', methods=['GET'])
def create_food_form():
    return render_template('food_form.html')

if __name__ == '__main__':
    app.run()
