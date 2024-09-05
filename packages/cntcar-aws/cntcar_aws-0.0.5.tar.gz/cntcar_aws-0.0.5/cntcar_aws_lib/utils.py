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