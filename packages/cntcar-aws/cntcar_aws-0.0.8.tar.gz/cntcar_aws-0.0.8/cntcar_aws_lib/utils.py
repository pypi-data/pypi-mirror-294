import croniter as cron
from datetime import datetime as dt

def handle_error(e, detail=""):
    """Generic error handler function.
    
    Parameters:
        e : Exception
            The exception object.
        detail : str
            Additional detail or message to include in the error log.
    
    Returns:
        None
    """
    print(f'Error: {str(e)}')
    if detail: print(f'detail: {detail}')


def get_next_cron(cron_expression:str, start_time:dt):
    """This function calculates the next time a cron expression will run.
    
    Parameters:
        cron_expression : str
            The cron expression that defines the schedule.
        start_time : datetime
            The time from which the cron expression will be calculated.
    
    Returns:
        datetime
    """
    cron_iter = cron.croniter(cron_expression, start_time)
    return cron_iter.get_next(dt)