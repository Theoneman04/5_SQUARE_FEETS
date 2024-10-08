from fivesquarefeets import create_app

app = create_app()  # Create the app instance

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode
