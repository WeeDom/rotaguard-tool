from flask_restx import Api

api = Api(
    version='1.0',
    title='RotaGuard API',
    description='A comprehensive API for managing employee shifts and ensuring compliance with UK Working Time Regulations.',
    prefix='/api'
)
