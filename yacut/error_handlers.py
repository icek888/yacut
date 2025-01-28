from http import HTTPStatus

from flask import jsonify, render_template

from . import app


class APIError(Exception):
    """Исключение для ошибок в API."""
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


@app.errorhandler(APIError)
def handle_api_error(error):
    """
    Обработчик кастомных исключений APIError.
    Возвращает JSON с полем 'message' и соответствующим статус-кодом.
    """
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(404)
def page_not_found(e):
    """
    Кастомная страница ошибки 404 (Not Found),
    показываем HTML-шаблон 404.html.
    """
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(e):
    """
    Обработчик внутренней ошибки сервера (500).
    Возвращаем JSON с 'error', но можно отдать и шаблон, если нужно.
    """
    return jsonify(
        {'error': 'Internal Server Error'}
        ), HTTPStatus.INTERNAL_SERVER_ERROR
