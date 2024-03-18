from controller.controller import Controller
import asyncio

class Main:
    MainController = Controller()

    @staticmethod
    async def run():
        file_paths = [
            "data/static/rainfall/2023/03/15.json",
            "data/static/Traffic Flow.json",
            "data/static/erp_rate/erp_rate.json"
        ]

        tasks = [
            asyncio.create_task(Main.MainController.get_real_time_data()),
            asyncio.create_task(Main.periodic_task(file_paths[0])),
        ]
        await asyncio.gather(*tasks)

    @staticmethod
    async def periodic_task(file_path):
        while True:
            await Main.MainController.get_static_data(file_path)
            await asyncio.sleep(10)


if __name__ == '__main__':
    asyncio.run(Main.run())