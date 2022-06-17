from flask import request, jsonify
from flask_restful import Resource
from bs4 import BeautifulSoup
from flask_cors import cross_origin

# class GetReviewApi(Resource):
    
#     def get(self,professorName, className):
#         reviews = Reviews.objects.filter(className__in= [className], professor__in = [professorName])
#         data = []
#         for i in range(len(reviews)):
#             data.append({
#                 'className': reviews[i].className,
#                 'professor': reviews[i]. professor,
#                 'review': reviews[i].review,
#                 'date': reviews[i].date,
#                 'likes': reviews[i].likes,
#                 'dislikes': reviews[i].dislikes
#             })
#         return jsonify(data)

# class PostReviewApi(Resource):
#     def post(self):
#         body = request.get_json()
#         review = Reviews(**body).save()
#         return {'Response:':'Review added successfully'},200


class Process(Resource):
    pass
    # def post(self):
    #     body = request.get_data(); 
    #     # soup = BeautifulSoup(body, 'html.parser')
    #     # print(body)
    #     response = jsonify(message="OK!")
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     return response