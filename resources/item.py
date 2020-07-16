from flask_restx import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):

    # initializes a new object that is used to pass the request
    parser = reqparse.RequestParser()

    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs a store_id!"
    )

    # get all items
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message' : 'Item does not exist!'}, 404
     
    # post items
    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):

            return{'message' : 'Item Already Exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        # Put it inside a try catch block so as to handle errors resulting from data not being 
        # inserted into the db
        try:
            item.save_to_db()
        except:
            return {'message' : "An error occurred while trying to insert the data"}, 500 #internal server error

        return item.json(), 201 #created


    # DELETE AN ITEM
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item :
            item.delete_from_db()

        return {"message": "Item deleted Successfully"}, 200

    # UPDATE AN ITEM
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        # find if the item exists
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)

        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):

    # get all items
    @jwt_required()
    def get(self):

       return {'items' : [item.json() for item in ItemModel.query.all()]}

       