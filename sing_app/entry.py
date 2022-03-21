
from sing_app import app
#from sing_app.config_default import ProductionConfig, DevelopmentConfig, TestingConfig

#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

    

app.debug = True
#app.config.config['TEMPLATES_AUTO_RELOAD'] = True


#----------------------------------------------------------------------------#
# Run instance of server
# app.run(host='0.0.0.0') - note: host='0.0.0.0' allows your local machine to access the container in docker from localhost
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run('0.0.0.0', port=5000)
    #app.run()
