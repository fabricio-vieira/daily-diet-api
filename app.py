from flask import Flask, request, jsonify
from database import db
from models.meal import Meal


app = Flask(__name__)

app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'

db.init_app(app)

#Rota de Refeições

#Registro de refeições
@app.route('/meal', methods=['POST'])
def register_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    in_diet = data.get("in_diet")

    if name and description:
        new_meal = Meal(name=name, description=description, in_diet=in_diet)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Refeição registrada com sucesso"})
                    
    return jsonify({"message": "Dádos incompletos"}), 400

#Rota Leitura de todos as refeições
@app.route('/meal', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    meal_list = [{"ID": meal.id, "Descrição": meal.description,"Na Dieta": meal.in_diet, "Horário": meal.created_at} for meal in meals]
    return jsonify(meal_list)


if __name__ == '__main__':
    app.run(debug=True)