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

#Atualização de refeições
@app.route('/meal/<int:id_meal>', methods=['PUT'])
def update_meal(id_meal):
    data = request.json
    meal = Meal.query.get(id_meal)

    if not meal:
        return jsonify({"message": "Refeição não encontrada"})
    else: 
        if data.get("name") and data.get("description") and data.get("in_diet"):
            meal.name = data.get("name")
            meal.description = data.get("description")
            meal.in_diet = data.get("in_diet")
            db.session.commit()
            return jsonify({"message": "Dados alterados"})

        return jsonify({"message": "Informações incompletas"})
        
#Leitura de todas as refeições
@app.route('/meal', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    meal_list = [{"ID": meal.id, "Descrição": meal.description,"Na Dieta": meal.in_diet, "Horário": meal.registered_at} for meal in meals]
    return jsonify(meal_list)

#Consulta de refeição por id
@app.route('/meal/<int:id_meal>', methods=['GET'])
def get_meal_by_id(id_meal):
    meal = Meal.query.get(id_meal)
    if not meal:
        return jsonify({"message": "Refeição não encontrada"})
    else:
        return {"Nome": meal.name, "Descrição": meal.description, "Na Dieta": meal.in_diet, "Horário": meal.registered_at}

#Deleção de refeições
@app.route('/meal/<int:id_meal>', methods=['DELETE'])
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)
    if not meal:
         return jsonify({"message": "Refeição não encontrada"})
    else:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição removida!"})


if __name__ == '__main__':
    app.run(debug=True)