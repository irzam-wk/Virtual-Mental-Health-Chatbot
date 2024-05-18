from flask import Flask, render_template, jsonify, request
from engine import chat_engine

# input = "I am feeling left out."
# print(input)
# result = chat_engine.chat(input)
# print("Response : ")
# print(result)

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    data = request.json  # Access JSON data
    if not data or "msg" not in data:
        return jsonify({"error": "No text found, please include 'msg' field in the JSON data"}), 400

    input = data["msg"]
    # input = msg
    # print(type(input))
    print(input)
    result = chat_engine.chat(input)
    print()
    print(result.source_nodes)
    print()
    print("Response : ")
    print(result)
    return str(result), 200


# import asyncio

# async def chat_engine_async(input):
#     # Asynchronous implementation of chat_engine.chat
#     # (replace with your actual logic)
#     await asyncio.sleep(1)  # Simulate processing time
#     return "Processed response"

# @app.route("/get", methods=["GET", "POST"])
# async def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)

#     loop = asyncio.get_event_loop()
#     result = await loop.run_in_executor(None, chat_engine_async, input)  # Run chat_engine asynchronously

#     print("Response : ")
#     print(result)
#     return str(result)




if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0", port= 8080, debug= True)


