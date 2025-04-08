class SuccessResponses:
    @staticmethod
    def success_login(id_courier):
        return {"id": id_courier}

    @staticmethod
    def success_ordered(track):
        return {"track": track}

    SUCCESSFUL_REGISTRATION = {'ok': True}
    SUCCESSFUL_DELETE_USER = {'ok': True}


class ErrorResponses:
    LOGIN_IS_ALREADY_USING = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
    INSUFFICIENT_DATA_FOR_REGISTRATION = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}
    INSUFFICIENT_DATA_FOR_LOGIN = {"code": 400, "message":  "Недостаточно данных для входа"}
    NON_EXISTENT_DATA_FOR_LOGIN = {"code": 404, "message": "Учетная запись не найдена"}
