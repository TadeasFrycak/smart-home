# from gevent import monkey
# monkey.patch_all()

# from start import app as application

# if __name__ == "__main__":
#     application.run()

from start import app, socketio

def run_server():    
    
    socketio.run(app, debug = True)




run_server()

    
    
