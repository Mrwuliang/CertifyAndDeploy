from web import app, socketio
import eventlet

if __name__ == '__main__':
    # 您可以在这里配置 host 和 port
    # 例如: app.run(host='0.0.0.0', port=80, debug=True)
    # app.run(debug=True)
    socketio.run(app, debug=True, port=5555)