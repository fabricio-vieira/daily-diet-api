from flask import Flask, request, jsonify
from database import db
from models.meal import Meal
from models.user import User


app = Flask(__name__)

app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/daily-diet'

db.init_app(app)

#Rota de Refeições

# registrar refeições
@app.route('/meal', methods=['POST'])
def register_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    in_diet = data.get("in_diet")
    user_id = data.get("user_id")

    if name and description and user_id:
        new_meal = Meal(name=name, description=description, in_diet=in_diet, user_id=user_id)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Refeição registrada com sucesso"})
                    
    return jsonify({"message": "Dádos incompletos"}), 400

# editar refeições
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
        
# visualizar todas as refeições
@app.route('/meal', methods=['GET'])
def get_meals():
    meals = Meal.query.all()
    meal_list = [{"id": meal.id, "descrição": meal.description,"na_dieta": meal.in_diet, "horario": meal.registered_at, "user_id": meal.user_id} for meal in meals]
    return jsonify(meal_list)

# visualizar uma única refeição por id
@app.route('/meal/<int:id_meal>', methods=['GET'])
def get_meal_by_id(id_meal):
    meal = Meal.query.get(id_meal)
    if not meal:
        return jsonify({"message": "Refeição não encontrada"})
    else:
        return {"nome": meal.name, "descrição": meal.description, "na_dieta": meal.in_diet, "horario": meal.registered_at, "user_id": meal.user_id}

# listar todas as refeições de um usuário pelo id do usuário 
@app.route('/meal/user/<int:id_user>', methods=['GET'])
def meal_by_user(id_user):
    meals_by_user = Meal.query.filter_by(user_id=id_user).all()

    if not meals_by_user:
        return jsonify({"message": "Não há refeições registradas"})
    else:
        meal_list = [{"id": meal.id, "descrição": meal.description,"na_dieta": meal.in_diet, "horario": meal.registered_at} for meal in meals_by_user]
        return jsonify(meal_list)
    
# apagar refeições
@app.route('/meal/<int:id_meal>', methods=['DELETE'])
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)
    if not meal:
         return jsonify({"message": "Refeição não encontrada"})
    else:
        db.session.delete(meal)
        db.session.commit()
        return jsonify({"message": "Refeição removida!"})

#Rotas de Usuários
    
# Criação de Usuários    
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")

    if username and email:
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"message":"Usuário já cadastrado"})
        else:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
        return jsonify({"message": "Cadastro realizado com sucesso"})
                    
    return jsonify({"message": "Credenciais Inválidas"}), 400

# Rota Leitura de todos os usuários
@app.route('/user', methods=['GET'])
def read_users():
    users = User.query.all()
    user_list = [{"id": user.id, "nome": user.username, "email": user.email} for user in users]
    return jsonify(user_list)


if __name__ == '__main__':
    app.run(debug=True)