from flask_restx import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

    # get a single store
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    # add a new store
    @jwt_required()
    def post(self, name):
        
        if StoreModel.find_by_name(name):
            return{'message' : 'Store already Exists!'}, 400
        
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while trying to add a store!'}, 500

        return store.json()


    # delete a store
    @jwt_required()
    def delete(self, name):
        
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message': 'Store Deleted'}



class StoreList(Resource):
    
    # get a list of all stores
    @jwt_required()
    def get(self):
        
        return {'stores' : [store.json() for store in StoreModel.query.all()]}