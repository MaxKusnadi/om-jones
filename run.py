from bot import app

context = ('ssl.crt', 'ssl.key')
app.run(debug=True, ssl_context=context)
