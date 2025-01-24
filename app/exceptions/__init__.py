class UserError(Exception):
    pass


class ApplicationError(Exception):
    pass


class IncorrectValueError(UserError):
    pass


class NotFoundError(UserError):
    pass


class EmptyDataError(UserError):
    pass


class DatabaseError(ApplicationError):
    pass
