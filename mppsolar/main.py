from mppsolar import main


if __name__ == "__main__":
    main():
        daemon = setup_daemon_mode(args)
        log.info(daemon)
