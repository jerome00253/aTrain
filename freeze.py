import multiprocessing

multiprocessing.freeze_support()


if __name__ == "__main__":
    from aTrain import app

    try:
        app.start()
    except KeyboardInterrupt:
        pass
