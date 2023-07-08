import asyncio
import datetime

import busy_checker.dotenv_loader
import busy_checker.hkid
from busy_checker.telegram_bot import send_message

TIME_INTERVAL = 5
HEART_BEAT_INTERVAL = 3600


async def check_hkid_availability_loop():
    await send_message("Start a new round.\n")

    time_passed = 0

    while True:
        try:
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            available_slots = busy_checker.hkid.check_availability()

            if available_slots:
                message = "Available slots found:\n"
                for slot in available_slots:
                    message += (
                        f"Date: {slot['date']},"
                        + "Office ID: {slot['officeId']},"
                        + " Regular Quota: {slot['quotaR']},"
                        + " Extension Quota: {slot['quotaK']}\n"
                    )
                message = f"[{time_now}] {message}"
                print(message)
                await send_message(message)
            else:
                print(f"[{time_now}] No available slots at the moment.")

            time_passed += TIME_INTERVAL
            if time_passed >= HEART_BEAT_INTERVAL:
                time_passed -= HEART_BEAT_INTERVAL
                await send_message(f"[{time_now}] Everything is okay.")
            # Delay for x seconds before checking again
            await asyncio.sleep(TIME_INTERVAL)
        except (TypeError, ValueError) as e:
            message = f"[{time_now}] An error occurred: {e}"
            send_message(message)
            print(message)


# Run the event loop
async def run_hkid():
    asyncio.create_task(check_hkid_availability_loop())
    await asyncio.sleep(3600 * 24 * 365)  # Run for 1 year (adjust as needed)


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m busy_checker` and `$ busy_checker `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    asyncio.run(run_hkid())
