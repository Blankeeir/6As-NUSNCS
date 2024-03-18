from controller.controller import Controller

class Main:
    def run():
        MainController= Controller()
        MainController.get_static_data()

if __name__ == '__main__':
    Main.run()