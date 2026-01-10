class SteganographyError(Exception):
    """Błąd ogólny steganografii"""

class InvalidImageFormat(SteganographyError):
    pass

class MessageTooLarge(SteganographyError):
    pass

class MessageTooShort(SteganographyError):
    pass

class NoHiddenMessage(SteganographyError):
    pass

class InvalidPassword(SteganographyError):
    pass

