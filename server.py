#!flask/bin/python
from flask import Flask, jsonify, request

from Board import *
from Figure import *
from TDPlayer import *
from Model import *
import tensorflow as tf
import os


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/', methods=['POST'])
def index():
    return "Hello, World!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    content = request.get_json()
    print(content)
    return jsonify({'tasks': tasks})

@app.route('/getMove', methods=['POST'])
def get_move():
    content = request.get_json()
    color = Color.WHITE if content["color"] == "white" else Color.BLACK
    figures = content["figures"]
    move = getMove(color, figures)
    return move

model_path = os.environ.get('MODEL_PATH', 'models/')
summary_path = os.environ.get('SUMMARY_PATH', 'summaries/')
checkpoint_path = os.environ.get('CHECKPOINT_PATH', 'checkpoints/')

if not os.path.exists(model_path):
    os.makedirs(model_path)

if not os.path.exists(checkpoint_path):
    os.makedirs(checkpoint_path)

if not os.path.exists(summary_path):
    os.makedirs(summary_path)

def getMove(color, figures):
    board = Board()
    for figure in figures:
        board.doMoveFromString(figure + " N")
    graph = tf.Graph()
    sess = tf.Session(graph=graph)
    with sess.as_default(), graph.as_default():
        model = Model(sess, model_path, summary_path, checkpoint_path, restore= True)
        player = TDAgent(model)
        player.color = color
        move = player.getMove(board)
        return(move.toString())


if __name__ == '__main__':
    app.run(debug=False)